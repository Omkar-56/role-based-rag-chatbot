from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService


router = APIRouter(prefix="/chat", tags=["chat"])

retriever = RetrievalService()
llm_service = LLMService()

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        retrieved_chunks = retriever.retrieve(
            query=request.query,
            user_role=request.role,
        )

        # Temporary mock answer (LLM will replace this later)
        answer = llm_service.generate_answer(
            query=request.query,
            chunks=retrieved_chunks,
        )

        return {
            "answer": answer,
            "sources": retrieved_chunks,
        }

    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
