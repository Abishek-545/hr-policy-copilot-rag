# HR Policy Copilot

Employee-facing RAG assistant for HR policy questions.

## Overview

HR Policy Copilot is a professional internal HR assistant where employees ask questions about company policies. Employees cannot upload, delete, or manage documents. The backend indexes a controlled set of preloaded policy PDFs from `backend/data/policies/` and answers only from retrieved policy context with citations.

The included policy library is a fictional enterprise policy set so it is safe to host publicly and does not expose confidential or copyrighted company policies.

## Tech Stack

- Frontend: React, TypeScript, TailwindCSS, Axios, React Router
- Backend: FastAPI, Python
- AI: Groq Chat Completions API
- RAG: LangChain text splitting, persisted local vector index, deterministic hashing embeddings
- PDF Processing: PyMuPDF

## Business Value

- Gives employees fast self-service answers to common HR policy questions
- Reduces repetitive HR helpdesk traffic
- Keeps responses grounded in approved policy documents
- Shows citations, source documents, page numbers, and retrieved context
- Avoids employee-side uploads for tighter governance

## Architecture

```text
frontend/ React UI
    |
    | Axios
    v
backend/ FastAPI
    |
    | startup indexing
    v
backend/data/policies/*.pdf -> PyMuPDF -> chunks -> embeddings -> local vector index
    |
    | top-k retrieval
    v
Groq LLM grounded answer with citations
```

## RAG Workflow

1. Backend starts and reads all PDFs in `backend/data/policies/`.
2. Each document is extracted page by page.
3. Text is split into overlapping chunks.
4. Chunks are embedded and stored in a persisted local vector index.
5. `/chat` retrieves the top matching chunks for a question.
6. Groq receives only the retrieved context and must answer from that context.
7. The API returns an answer, confidence score, sources, and expandable retrieved context.

## Policy Documents

The app includes six industry-style policy PDFs:

- Employee Handbook
- Remote Work Policy
- Leave Policy
- Travel & Expense Policy
- Code of Conduct
- IT Security Policy

These are synthetic enterprise documents for a fictional company, written to be clear, detailed, and citation-friendly.

## Local Setup

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --port 8000
```

Set your Groq API key in `backend/.env`:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000` by default. For deployment, set:

```env
VITE_API_BASE_URL=https://your-backend.onrender.com
```

## API

### GET `/documents`

Returns metadata about indexed policy documents.

### POST `/chat`

```json
{
  "question": "What is the remote work policy?"
}
```

### GET `/analytics`

Returns simple usage and indexing analytics.

## Example Questions

- How many vacation days do employees receive?
- What is the remote work policy?
- How do I request sick leave?
- What expenses are reimbursable?
- What is the probation period?
- How do I report workplace concerns?

## Free Hosting

Recommended Render setup:

- Frontend: Static Site from `frontend`, build command `npm install && npm run build`, publish directory `dist`
- Backend: Web Service from `backend`, build command `pip install -r requirements.txt`, start command `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Environment variable: `GROQ_API_KEY`
- Frontend environment variable: `VITE_API_BASE_URL=https://your-backend-service.onrender.com`

The Hobby plan can host the application at no monthly platform cost. Free services can sleep and have resource limits. Vite environment variables are injected at build time, so redeploy the frontend after setting `VITE_API_BASE_URL`.

## Limitations

- Policy documents are synthetic and should be replaced with approved company policies before internal production use.
- The app does not provide legal advice.
- No authentication or employee identity integration is included.
- The vector index is local to the backend instance.
- Render free instances may sleep and rebuild indexes on restart.

## Future Improvements

- HR admin document management
- Leave request automation
- Employee onboarding assistant
- Interview assistant
- HR ticket classification
- Feedback-based answer improvement
- Authentication and role-based access control
- PostgreSQL persistence
- Docker deployment
- CI/CD pipeline
