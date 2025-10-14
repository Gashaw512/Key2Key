# app/models/user.py (FINAL)

from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Column
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID, TEXT, VARCHAR
from datetime import datetime
import uuid

# --- LOCAL IMPORTS for Model Definitions ---
from .enums import UserRole
# These imports are ONLY for type hinting the relationships
from .broker import BrokerProfile 
from .property import PropertyListing 
from .vehicle import VehicleListing 
from .payment import Transaction
from .review import Review
from .chat import ChatThread
from .audit_log import AuditLog

# --- USER MODELS (Simplified for clarity) ---

class UserBase(SQLModel):
    full_name: str
    email: str = Field(index=True, unique=True, sa_column=Column("email", VARCHAR(255)))
    phone: Optional[str] = Field(default=None, index=True)
    password_hash: str = Field(exclude=True, sa_column=Column("password_hash", TEXT))
    role: UserRole = Field(default=UserRole.BUYER)
    verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, index=True, server_default=text("uuid_generate_v4()"))
    )

    # --- RELATIONSHIPS (The core update for professionalism) ---
    
    # One-to-One: Broker Profile (Optional)
    broker_profile: Optional[BrokerProfile] = Relationship(back_populates="user")
    
    # One-to-Many: Listings owned by the User
    property_listings: List["PropertyListing"] = Relationship(back_populates="owner")
    vehicle_listings: List["VehicleListing"] = Relationship(back_populates="owner")
    
    # One-to-Many: Transactions initiated by the User
    transactions: List["Transaction"] = Relationship(back_populates="buyer")
    
    # One-to-Many: Reviews given and received
    reviews_given: List["Review"] = Relationship(back_populates="reviewer", 
                                                sa_relationship_kwargs={"primaryjoin": "User.id == Review.reviewer_id"})
    reviews_received: List["Review"] = Relationship(back_populates="target_user", 
                                                   sa_relationship_kwargs={"primaryjoin": "User.id == Review.target_user_id"})
    
    # One-to-Many: Chat threads created/participated in
    chat_threads: List["ChatThread"] = Relationship(back_populates="participants") # Assuming many-to-many through another table

    audit_logs: List["AuditLog"] = Relationship(back_populates="user")


# --- PYDANTIC SCHEMAS (UserCreate, UserRead, UserUpdate remain as defined) ---
# ... (UserCreate, UserRead, UserUpdate logic here) ...

# --- PYDANTIC SCHEMAS ---
class UserRead(UserBase):
    id: uuid.UUID


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
