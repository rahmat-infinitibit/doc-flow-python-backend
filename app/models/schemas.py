from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None
    title: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    references: List[str]
    chat_id: Optional[str] = None

class ChatMessageResponse(BaseModel):
    role: str
    content: str
    timestamp: datetime

class ChatHistoryResponse(BaseModel):
    chat_id: str
    title: Optional[str]
    last_message: str
    timestamp: datetime

class DocumentResponse(BaseModel):
    message: str
    document_id: str