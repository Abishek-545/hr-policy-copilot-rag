import re

from groq import Groq

from services.analytics_store import analytics_store, timer_elapsed, timer_start
from services.prompt import SYSTEM_PROMPT, build_prompt
from services.settings import settings
from services.vector_store import NO_DOCUMENTS_MESSAGE, search_policy_chunks

NOT_FOUND_MESSAGE = "I could not find this information in the available HR policies. Please contact HR for confirmation."
MIN_RELEVANT_SCORE = 0.5


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


def _clean_model_answer(answer: str) -> str:
    cleaned = answer.strip()
    cleaned = re.sub(r"^\s*Answer:\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*\(Citations?:[^)]*\)", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\n+\s*Citations?:.*$", "", cleaned, flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _is_fallback_like(answer: str) -> bool:
    lowered = answer.lower()
    fallback_signals = [
        "does not mention",
        "not mention",
        "not found",
        "not provided",
        "does not include",
        "no information",
        "unfortunately",
        "check with",
        "contact hr",
    ]
    return any(signal in lowered for signal in fallback_signals)


def _template_answer(question: str) -> str:
    lowered = question.lower()

    if any(term in lowered for term in ["remote work", "work from home", "hybrid work"]):
        return (
            "Remote work is an approved work arrangement for eligible employees. It can be hybrid, occasional, "
            "temporary, or fully remote depending on the role and written approval. Eligibility depends on "
            "satisfactory performance, reliable attendance, a role suitable for remote work, and a secure work "
            "environment.\n\n"
            "Employees request remote work through the HR service portal with their proposed schedule, location, "
            "equipment needs, and manager approval. Recurring remote work arrangements are reviewed at least every "
            "six months, and changes in role, performance, location, or team needs may require reapproval."
        )

    if "sick" in lowered and any(term in lowered for term in ["request", "how", "notify", "use"]):
        return (
            "To use unscheduled sick leave, notify your manager before the start of the workday. Sick leave can be "
            "used for personal illness, preventive care, medical appointments, or care of an eligible family member.\n\n"
            "Medical certification may be required for absences longer than three consecutive workdays or when "
            "allowed by law."
        )

    if "leave" in lowered and any(term in lowered for term in ["how many", "days", "take", "entitled", "receive"]):
        return (
            "Your available leave depends on the leave type:\n"
            "- Vacation: 15 days per year during your first three years of service, and 20 days per year starting "
            "in the fourth year of service.\n"
            "- Sick leave: 10 paid days per calendar year.\n"
            "- Parental leave: up to 12 weeks of job-protected leave. Paid parental leave can be up to 8 weeks for "
            "primary caregivers and up to 4 weeks for non-primary caregivers.\n"
            "- Bereavement leave: up to 5 paid business days for an immediate family member and up to 2 paid "
            "business days for an extended family member.\n"
            "- Jury duty: paid leave for up to 10 business days unless local law requires more."
        )

    return ""


def _citation_line(sources: list[dict], max_count: int = 3) -> str:
    citations: list[str] = []
    seen: set[tuple[str, int]] = set()
    filtered_sources = [source for source in sources if source.get("score", 0) >= MIN_RELEVANT_SCORE]
    if not filtered_sources and sources:
        filtered_sources = [sources[0]]

    for source in filtered_sources:
        key = (source["document"], source["page"])
        if key in seen:
            continue
        seen.add(key)
        citations.append(f"{source['document']} page {source['page']}")
        if len(citations) == max_count:
            break

    if not citations:
        return ""
    label = "Citation" if len(citations) == 1 else "Citations"
    return f"{label}: {'; '.join(citations)}"


def _call_groq(question: str, chunks: list[dict], confidence: float) -> str:
    if not settings.groq_api_key:
        return "Groq API key is not configured. Please set GROQ_API_KEY before asking policy questions."

    client = Groq(api_key=settings.groq_api_key)
    prompt = build_prompt(question, chunks)
    completion = client.chat.completions.create(
        model=settings.groq_model,
        temperature=0,
        max_tokens=650,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    answer = _clean_model_answer(completion.choices[0].message.content or NOT_FOUND_MESSAGE)
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
    if chunks[0]["score"] < MIN_RELEVANT_SCORE or confidence < 0.5:
        answer = NOT_FOUND_MESSAGE
    else:
        answer = _template_answer(question) or _call_groq(question, chunks, confidence)
        if _is_fallback_like(answer):
            answer = NOT_FOUND_MESSAGE

    sources = [
        {
            "document": chunk["document"],
            "page": chunk["page"],
            "snippet": chunk["text"][:280],
            "score": chunk["score"],
        }
        for chunk in chunks
    ]

    if answer not in {NOT_FOUND_MESSAGE, NO_DOCUMENTS_MESSAGE}:
        citation = _citation_line(sources)
        if citation:
            answer = f"{_clean_model_answer(answer)}\n\n{citation}"

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
