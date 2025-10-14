# app/models/chat.py
from sqlmodel import Field, SQLModel, Column, Relationship
from datetime import datetime
import uuid
from .user import User # Import User

class ChatThread(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    # user_ids: List[uuid.UUID] # In a many-to-many, this requires an association table, keeping it simple here
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    messages: List["ChatMessage"] = Relationship(back_populates="thread")
    # participants: List[User] = Relationship(back_populates="chat_threads", link_model=UserThreadLink) # More complex setup

class ChatMessage(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    thread_id: uuid.UUID = Field(foreign_key="chatthread.id")
    sender_id: uuid.UUID = Field(foreign_key="user.id")
    content: str = Field(sa_column=Column("content", TEXT))
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    thread: ChatThread = Relationship(back_populates="messages")
    sender: User = Relationship()
