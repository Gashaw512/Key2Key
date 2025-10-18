# app/models/analytics.py

from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, Column, JSON
from datetime import datetime
from enum import Enum
import uuid

# Local imports
from .user import User

# --- Event Type Enum ---
class AnalyticEventType(str, Enum):
    LISTING_VIEW = "listing_view"
    SEARCH_PERFORMED = "search_performed"
    PROFILE_VIEW = "profile_view"
    TRANSACTION_CLICK = "transaction_click"


class AnalyticsEventBase(SQLModel):
    # Linkage
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", index=True, description="Null for unauthenticated users")
    session_id: Optional[uuid.UUID] = Field(default=None, index=True, description="For tracking anonymous users")
    
    # Content
    type: AnalyticEventType
    resource_id: Optional[uuid.UUID] = Field(default=None, index=True, description="ID of the listing/user being viewed")
    # Use JSONB to store flexible, semi-structured data (search terms, filters, device info)
    details: dict = Field(default={}, sa_column=Column(JSON))
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)


class AnalyticsEvent(AnalyticsEventBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    
    # --- RELATIONSHIP ---
    # user: Optional[User] = Relationship(back_populates="analytics_events") # Assuming you add this to User model

# --- PYDANTIC SCHEMAS ---
class AnalyticsEventRead(AnalyticsEventBase):
    id: uuid.UUID