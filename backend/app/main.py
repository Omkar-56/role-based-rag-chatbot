from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI(title="Role-Based RAG Chatbot API")

@app.get("/")
def root():
    return {"message": "API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Register routers
app.include_router(chat_router)