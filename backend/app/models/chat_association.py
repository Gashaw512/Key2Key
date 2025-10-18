from sqlmodel import Field, SQLModel
from typing import Optional
import uuid

# =========================================================
# ASSOCIATION TABLE
# =========================================================

class UserChatLink(SQLModel, table=True):
    """
    Association table for the Many-to-Many relationship between User and ChatThread.
    """
    __tablename__ = "user_chat_links"
    
    # Composite primary keys using the Foreign Keys
    # Note: These must point to the plural table names defined on the primary models.
    user_id: Optional[uuid.UUID] = Field(
        default=None, 
        primary_key=True, 
        foreign_key="users.id"      
    )
    thread_id: Optional[uuid.UUID] = Field(
        default=None, 
        primary_key=True, 
        foreign_key="chat_threads.id" 
    )
