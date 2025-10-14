# app/models/review.py

from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, Column
from datetime import datetime
from sqlalchemy import TEXT, Integer
import uuid

# Local imports
from .user import User


class ReviewBase(SQLModel):
    # Linkage fields (FKs defined in the User model to prevent circular import errors here)
    reviewer_id: uuid.UUID = Field(foreign_key="user.id", index=True, description="User who gave the review")
    target_user_id: uuid.UUID = Field(foreign_key="user.id", index=True, description="User who is being reviewed")
    
    # Content fields
    rating: int = Field(sa_column=Column("rating", Integer), le=5, ge=1) # Integer column with constraints
    comment: Optional[str] = Field(default=None, sa_column=Column("comment", TEXT))
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Review(ReviewBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )

    # --- RELATIONSHIPS (Requires specific joins/foreign_keys kwargs) ---
    reviewer: User = Relationship(back_populates="reviews_given", 
                                    sa_relationship_kwargs={"foreign_keys": "[Review.reviewer_id]"})
    target_user: User = Relationship(back_populates="reviews_received", 
                                       sa_relationship_kwargs={"foreign_keys": "[Review.target_user_id]"})


# --- PYDANTIC SCHEMAS ---
class ReviewRead(ReviewBase):
    id: uuid.UUID

class ReviewCreate(ReviewBase):
    # The reviewer_id will be automatically injected by the service layer from the authenticated user
    pass