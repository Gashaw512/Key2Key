# app/models/notification.py

from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from sqlalchemy import TEXT, Enum
import uuid

# Local imports
from .user import User

# --- Notification Type Enum (Professional Enhancement) ---
class NotificationType(str, Enum):
    TRANSACTION_SUCCESS = "transaction_success"
    NEW_MESSAGE = "new_message"
    LISTING_UPDATE = "listing_update"
    ACCOUNT_ALERT = "account_alert"


class NotificationBase(SQLModel):
    # Linkage
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True, description="The user receiving the notification")
    
    # Content
    type: NotificationType
    title: str
    message: str = Field(sa_column=Column("message", TEXT))
    link: Optional[str] = None # Deep link to the relevant page in the app
    
    # Status
    is_read: bool = Field(default=False, index=True)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Notification(NotificationBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    
    # --- RELATIONSHIP ---
    user: User = Relationship(back_populates="notifications") # Assuming you add this to User model


# --- PYDANTIC SCHEMAS ---
class NotificationRead(NotificationBase):
    id: uuid.UUID
    
class NotificationCreate(NotificationBase):
    # user_id will be provided by the service/event system
    pass