from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analytics import router as analytics_router
from routes.chat import router as chat_router
from routes.documents import router as documents_router
from services.settings import settings
from services.vector_store import index_policy_documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    index_policy_documents()
    yield


app = FastAPI(
    title="HR Policy Copilot API",
    description="Employee-facing HR policy RAG assistant powered by Groq.",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [origin.strip() for origin in settings.allowed_origins.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(documents_router)
app.include_router(analytics_router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "HR Policy Copilot API"}
