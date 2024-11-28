from fastapi import FastAPI
from app.routers import document, chat

app = FastAPI(title="RAG System API")

app.include_router(document.router, prefix="/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to RAG System API"} 