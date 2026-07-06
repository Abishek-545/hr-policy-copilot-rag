import json

from groq import Groq

from services.analytics_store import analytics_store, timer_elapsed, timer_start
from services.prompt import SYSTEM_PROMPT, build_prompt
from services.settings import settings
from services.vector_store import NO_DOCUMENTS_MESSAGE, search_policy_chunks

NOT_FOUND_MESSAGE = "I could not find this information in the available HR policies. Please contact HR for confirmation."


def _estimate_confidence(chunks: list[dict]) -> float:
    if not chunks:
        return 0.0
    top_score = chunks[0]["score"]
    supporting = sum(1 for chunk in chunks if chunk["score"] >= 0.2)
    confidence = min(0.95, (top_score * 0.78) + (supporting * 0.04))
    return round(confidence, 2)


def _category_from_question(question: str) -> str:
    lowered = question.lower()
    if any(term in lowered for term in ["remote", "hybrid", "work from home"]):
        return "Remote Work"
    if any(term in lowered for term in ["leave", "vacation", "sick", "holiday", "pto"]):
        return "Leave and Time Off"
    if any(term in lowered for term in ["travel", "expense", "reimburse", "receipt"]):
        return "Travel and Expense"
    if any(term in lowered for term in ["conduct", "harassment", "concern", "ethics", "report"]):
        return "Code of Conduct"
    if any(term in lowered for term in ["password", "security", "device", "vpn", "data"]):
        return "IT Security"
    return "General HR Policy"


def _call_groq(question: str, chunks: list[dict], confidence: float) -> str:
    if not settings.groq_api_key:
        return "Groq API key is not configured. Please set GROQ_API_KEY before asking policy questions."

    client = Groq(api_key=settings.groq_api_key)
    prompt = build_prompt(question, chunks)
    completion = client.chat.completions.create(
        model=settings.groq_model,
        temperature=0.1,
        max_tokens=650,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    answer = completion.choices[0].message.content or NOT_FOUND_MESSAGE
    if confidence < 0.45 and "Low confidence" not in answer:
        answer = f"{answer}\n\nLow confidence. Please verify with HR."
    return answer


def answer_question(question: str) -> dict:
    started = timer_start()
    chunks = search_policy_chunks(question, top_k=5)

    if not chunks:
        return {
            "answer": NO_DOCUMENTS_MESSAGE,
            "confidence": 0.0,
            "sources": [],
            "retrieved_context": [],
        }

    confidence = _estimate_confidence(chunks)
    if confidence < 0.18:
        answer = NOT_FOUND_MESSAGE
    else:
        answer = _call_groq(question, chunks, confidence)

    sources = [
        {
            "document": chunk["document"],
            "page": chunk["page"],
            "snippet": chunk["text"][:280],
            "score": chunk["score"],
        }
        for chunk in chunks
    ]
    elapsed = timer_elapsed(started)
    referenced_docs = sorted({source["document"] for source in sources})
    analytics_store.record_question(elapsed, referenced_docs, _category_from_question(question))

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": sources,
        "retrieved_context": chunks,
        "response_time": round(elapsed, 2),
    }
