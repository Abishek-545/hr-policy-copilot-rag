from fastapi import APIRouter

from services.analytics_store import analytics_store
from services.vector_store import chunks_count, documents_metadata

router = APIRouter(tags=["analytics"])


@router.get("/analytics")
def analytics():
    docs = documents_metadata()
    return {
        "documents_count": len(docs),
        "chunks_count": chunks_count(),
        "questions_asked": analytics_store.questions_asked,
        "average_response_time": analytics_store.average_response_time,
        "most_referenced_documents": [
            {"document": name, "count": count}
            for name, count in analytics_store.document_hits.most_common(5)
        ],
        "common_question_categories": [
            {"category": name, "count": count}
            for name, count in analytics_store.category_hits.most_common(5)
        ],
    }
