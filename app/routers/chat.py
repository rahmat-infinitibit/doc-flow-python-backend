from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4

from app.services.chat_service import ChatService
from app.models.schemas import ChatRequest, ChatResponse
from app.database.database import get_db
from app.models.chat import ChatHistory

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    chat_service = ChatService()
    response, references = await chat_service.get_response(request.message)
    
    # Save user message
    chat_id = request.chat_id or str(uuid4())
    db.add(ChatHistory(
        chat_id=chat_id,
        role="user",
        content=request.message,
        title=request.title if hasattr(request, 'title') else None
    ))
    
    # Save assistant response
    db.add(ChatHistory(
        chat_id=chat_id,
        role="assistant",
        content=response,
        title=request.title if hasattr(request, 'title') else None
    ))
    
    db.commit()
    
    return ChatResponse(
        response=response,
        references=references,
        chat_id=chat_id
    )

@router.get("/chat/history", response_model=List[dict])
async def get_chat_history(db: Session = Depends(get_db)):
    # Get unique chat sessions with their latest messages
    chats = db.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).all()
    
    # Group by chat_id
    chat_sessions = {}
    for chat in chats:
        if chat.chat_id not in chat_sessions:
            chat_sessions[chat.chat_id] = {
                "chat_id": chat.chat_id,
                "title": chat.title,
                "last_message": chat.content,
                "timestamp": chat.timestamp
            }
    
    return list(chat_sessions.values())

@router.get("/chat/{chat_id}/messages")
async def get_chat_messages(chat_id: str, db: Session = Depends(get_db)):
    messages = db.query(ChatHistory).filter(
        ChatHistory.chat_id == chat_id
    ).order_by(ChatHistory.timestamp).all()
    
    return [
        {
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]