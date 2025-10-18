from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import text, Column as SAColumn, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

# =========================================================
# ASSOCIATION MODEL (UserChatLink)
# Used for the Many-to-Many link between User and ChatThread
# =========================================================
class UserChatLink(SQLModel, table=True):
    """
    Association table linking users to chat threads.
    Composite primary key prevents duplicate entries.
    """
    __tablename__ = "user_chat_link"
    
    # Foreign Key to User
    user_id: uuid.UUID = Field(
        sa_column=SAColumn(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
            index=True
        )
    )
    
    # Foreign Key to ChatThread
    chat_thread_id: uuid.UUID = Field(
        sa_column=SAColumn(
            UUID(as_uuid=True),
            ForeignKey("chat_threads.id", ondelete="CASCADE"),
            primary_key=True,
            index=True
        )
    )

# =========================================================
# CHAT THREAD MODEL
# =========================================================
class ChatThreadBase(SQLModel):
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class ChatThread(ChatThreadBase, table=True):
    """Database table for a chat conversation thread."""
    __tablename__ = "chat_threads"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=SAColumn(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()")
        )
    )

    # Many-to-Many Relationship to User
    participants: List["User"] = Relationship(
        back_populates="chat_threads",
        link_model=UserChatLink, # Pass the class object
        sa_relationship_kwargs={"lazy": "select"}
    )
    
    # One-to-Many Relationship to Messages (assuming a Message model exists elsewhere)
    # messages: List["Message"] = Relationship(back_populates="thread")


class ChatThreadRead(ChatThreadBase):
    id: uuid.UUID
    
class ChatThreadCreate(SQLModel):
    # When creating a thread, we usually need the IDs of the initial users
    user_ids: List[uuid.UUID]
    
class ChatThreadUpdate(SQLModel):
    is_active: Optional[bool] = None
