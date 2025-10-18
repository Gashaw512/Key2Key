from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import text, Column as SAColumn, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TEXT
from datetime import datetime
import uuid

# --- REVIEW BASE ---
class ReviewBase(SQLModel):
    # The user giving the review (the 'reviewer')
    reviewer_id: uuid.UUID = Field(
        sa_column=SAColumn(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            index=True
        )
    )
    # The user receiving the review (the 'target_user')
    target_user_id: uuid.UUID = Field(
        sa_column=SAColumn(
            UUID(as_uuid=True),
            # Note: We must specify primaryjoin explicitly on the User model,
            # but the FK is still necessary here.
            ForeignKey("users.id", ondelete="CASCADE"),
            index=True
        )
    )
    rating: int = Field(ge=1, le=5) # Assuming a 1-5 rating
    comment: Optional[str] = Field(default=None, sa_column=SAColumn(TEXT))
    created_at: datetime = Field(default_factory=datetime.utcnow)

# --- REVIEW MODEL ---
class Review(ReviewBase, table=True):
    __tablename__ = "reviews"

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=SAColumn(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()")
        )
    )
    
    # Relationships back to User
    reviewer: "User" = Relationship(
        back_populates="reviews_given",
        sa_relationship_kwargs={"foreign_keys": "[Review.reviewer_id]"}
    )
    target_user: "User" = Relationship(
        back_populates="reviews_received",
        sa_relationship_kwargs={"foreign_keys": "[Review.target_user_id]"}
    )


# --- PYDANTIC SCHEMAS ---
class ReviewRead(ReviewBase):
    id: uuid.UUID
    
class ReviewCreate(ReviewBase):
    # Exclude IDs for creation, as they are often supplied via API context
    reviewer_id: Optional[uuid.UUID] = None
    target_user_id: uuid.UUID # Target must always be provided
    
class ReviewUpdate(SQLModel):
    rating: Optional[int] = None
    comment: Optional[str] = None
