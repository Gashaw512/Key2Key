# # app/models/notification.py


# from __future__ import annotations
# from typing import Optional
# from datetime import datetime
# from sqlmodel import SQLModel, Field, Column, Relationship
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import Mapped
# from sqlalchemy import TEXT
# import uuid
# from enum import Enum
# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from app.models.user import User

# class NotificationType(str, Enum):
#     TRANSACTION_SUCCESS = "transaction_success"
#     NEW_MESSAGE = "new_message"
#     LISTING_UPDATE = "listing_update"
#     ACCOUNT_ALERT = "account_alert"

# class NotificationBase(SQLModel):
#     # ✅ Use table name in foreign_key, not class name
#     user_id: uuid.UUID = Field(
#         foreign_key="users.id",  # ✅ Reference TABLE name
#         index=True
#     )
    
#     type: NotificationType
#     title: str
#     message: str = Field(sa_column=Column("message", TEXT))
#     link: Optional[str] = None
#     is_read: bool = Field(default=False, index=True)
#     created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# class Notification(NotificationBase, table=True):
#     __tablename__ = "notifications"

#     id: Optional[uuid.UUID] = Field(  # Make Optional for SQLModel compatibility
#         default_factory=uuid.uuid4,
#         primary_key=True,
#      )

#     # ✅ Use string-based relationship with proper configuration
#     # ✅ String reference - resolved by configure_mappers()
#     user: Optional["User"] = Relationship(
#         back_populates="notifications",
#         sa_relationship_kwargs={"lazy": "select"}
#     )


# class NotificationRead(NotificationBase):
#     id: uuid.UUID

# class NotificationCreate(NotificationBase):
#     pass



# app/models/notification.py
# app/models/notification.py
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import TEXT, Column as SAColumn, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from enum import Enum

class NotificationType(str, Enum):
    TRANSACTION_SUCCESS = "transaction_success"
    NEW_MESSAGE = "new_message"
    LISTING_UPDATE = "listing_update"
    ACCOUNT_ALERT = "account_alert"

class NotificationBase(SQLModel):
    user_id: uuid.UUID = Field(
        sa_column=SAColumn(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            index=True
        )
    )
    type: NotificationType
    title: str
    message: str = Field(sa_column=SAColumn(TEXT))
    link: Optional[str] = None
    is_read: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Notification(NotificationBase, table=True):
    __tablename__ = "notifications"
    
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=SAColumn(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()")
        )
    )
    
    # ✅ SQLModel Relationship
    user: Optional["User"] = Relationship(
        back_populates="notifications",
        sa_relationship_kwargs={"lazy": "select"}
    )

class NotificationRead(NotificationBase):
    id: uuid.UUID

class NotificationCreate(NotificationBase):
    pass