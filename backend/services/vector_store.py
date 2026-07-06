from datetime import datetime, timezone
from hashlib import blake2b
import json
from math import sqrt
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

from services.pdf_loader import get_document_metadata, load_policy_pages
from services.settings import POLICY_DIR, VECTOR_INDEX_PATH


NO_DOCUMENTS_MESSAGE = "No HR policy documents are available."

index_state = {
    "indexed": False,
    "last_indexed": "",
    "chunks_count": 0,
    "chunk_counts": {},
    "chunks": [],
}


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z0-9'-]{2,}", text.lower())


def _embed(text: str, dimensions: int = 384) -> list[float]:
    vector = [0.0] * dimensions
    for token in _tokens(text):
        digest = blake2b(token.encode("utf-8"), digest_size=8).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign
    norm = sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def _cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def _preferred_category(question: str) -> str:
    lowered = question.lower()
    if any(term in lowered for term in ["remote", "hybrid", "work from home"]):
        return "Remote Work"
    if any(term in lowered for term in ["leave", "vacation", "sick", "holiday", "pto"]):
        return "Leave and Time Off"
    if any(term in lowered for term in ["travel", "expense", "reimburse", "receipt"]):
        return "Travel and Expense"
    if any(term in lowered for term in ["conduct", "harassment", "concern", "ethics", "report"]):
        return "Code of Conduct"
    if any(term in lowered for term in ["password", "security", "device", "vpn", "data", "phishing"]):
        return "IT Security"
    return ""


def _load_persisted_index() -> None:
    if not VECTOR_INDEX_PATH.exists():
        return
    payload = json.loads(VECTOR_INDEX_PATH.read_text(encoding="utf-8"))
    index_state.update(payload)


def _save_index() -> None:
    VECTOR_INDEX_PATH.write_text(json.dumps(index_state, indent=2), encoding="utf-8")


def index_policy_documents() -> None:
    POLICY_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = list(POLICY_DIR.glob("*.pdf"))

    if not pdfs:
        index_state.update({"indexed": True, "last_indexed": "", "chunks_count": 0, "chunk_counts": {}, "chunks": []})
        _save_index()
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=560,
        chunk_overlap=90,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    pages = load_policy_pages(POLICY_DIR)
    chunk_counts: dict[str, int] = {}
    chunks: list[dict] = []

    for page in pages:
        page_chunks = splitter.split_text(page.text)
        for chunk_index, text in enumerate(page_chunks, start=1):
            chunks.append(
                {
                    "id": f"{page.document}:p{page.page}:c{chunk_index}",
                    "text": text,
                    "document": page.document,
                    "page": page.page,
                    "category": page.category,
                    "chunk": chunk_index,
                    "embedding": _embed(text),
                }
            )
            chunk_counts[page.document] = chunk_counts.get(page.document, 0) + 1

    indexed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    index_state.update(
        {
            "indexed": True,
            "last_indexed": indexed_at,
            "chunks_count": len(chunks),
            "chunk_counts": chunk_counts,
            "chunks": chunks,
        }
    )
    _save_index()


def search_policy_chunks(question: str, top_k: int = 5) -> list[dict]:
    if not index_state["chunks"]:
        _load_persisted_index()
    if not index_state["chunks"]:
        return []

    query = _embed(question)
    query_terms = set(_tokens(question))
    preferred_category = _preferred_category(question)

    def score_chunk(chunk: dict) -> float:
        overlap = len(query_terms.intersection(set(_tokens(chunk["text"])))) / max(1, len(query_terms))
        semantic = max(0.0, _cosine(query, chunk["embedding"]))
        category_boost = 0.18 if preferred_category and chunk.get("category") == preferred_category else 0.0
        category_penalty = -0.12 if preferred_category and chunk.get("category") != preferred_category else 0.0
        return round(min(0.95, max(0.0, (semantic * 0.7) + (overlap * 0.55) + category_boost + category_penalty)), 3)

    ranked = sorted(
        (
            {
                "text": chunk["text"],
                "document": chunk["document"],
                "page": chunk["page"],
                "category": chunk.get("category", "General HR Policy"),
                "score": score_chunk(chunk),
            }
            for chunk in index_state["chunks"]
        ),
        key=lambda item: item["score"],
        reverse=True,
    )
    return ranked[:top_k]


def documents_metadata() -> list[dict]:
    docs = get_document_metadata(POLICY_DIR, index_state["chunk_counts"])
    for doc in docs:
        doc["last_indexed"] = index_state["last_indexed"]
    return docs


def chunks_count() -> int:
    return index_state["chunks_count"]
