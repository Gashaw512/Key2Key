# app/models/broker.py (FINAL)

from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
import uuid
# Import User for the relationship definition
from .user import User 

class BrokerProfileBase(SQLModel):
    license_number: str = Field(unique=True, index=True)
    agency_name: str = Field(index=True)
    rating: float = Field(default=0.0)

class BrokerProfile(BrokerProfileBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    
    # Foreign Key: Links directly to the User table
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True)

    # Relationship back to User
    user: User = Relationship(back_populates="broker_profile")

# ... (BrokerProfileRead schema here) ...