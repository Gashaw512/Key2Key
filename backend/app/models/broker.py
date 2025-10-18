# app/models/broker.py
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column as SAColumn, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TEXT, TIMESTAMP
from datetime import datetime
import uuid

# Forward reference - import User later
# from .user import User  # Don't import here yet!

class BrokerProfileBase(SQLModel):
    """Base schema for BrokerProfile."""
    license_number: str = Field(
        sa_column=SAColumn(VARCHAR(50), unique=True, index=True)
    )
    bio: Optional[str] = Field(default=None, sa_column=SAColumn(TEXT))
    years_experience: int = Field(default=0, ge=0)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=SAColumn(
            TIMESTAMP(timezone=True),
            server_default=text("NOW()"),
            nullable=False
        )
    )

class BrokerProfile(BrokerProfileBase, table=True):
    """Database table model."""
    __tablename__ = "broker_profiles"
    
    id: Optional[uuid.UUID] = Field(
        default=None,  # Let DB generate
        sa_column=SAColumn(
            UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
            nullable=False
        )
    )
    
    # Foreign Key - UNIQUE for one-to-one
    user_id: uuid.UUID = Field(
        sa_column=SAColumn(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),
            unique=True,  # One-to-one constraint
            index=True
        )
    )
    
    # Back reference to User (string ref)
    user: "User" = Relationship(back_populates="broker_profile")

# Pydantic schemas
class BrokerProfileCreate(BrokerProfileBase):
    pass

class BrokerProfileRead(BrokerProfileBase):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None

class BrokerProfileUpdate(SQLModel):
    license_number: Optional[str] = None
    bio: Optional[str] = None
    years_experience: Optional[int] = None
    is_verified: Optional[bool] = None