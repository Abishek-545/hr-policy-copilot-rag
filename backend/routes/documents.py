from fastapi import APIRouter

from services.vector_store import documents_metadata

router = APIRouter(tags=["documents"])


@router.get("/documents")
def documents():
    return {"documents": documents_metadata()}
