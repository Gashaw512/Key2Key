# app/models/payment.py

from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Column
from datetime import datetime
from sqlalchemy import TEXT
import uuid

# Local imports
from .enums import ListingType, PaymentGateway, PaymentStatus
from .user import User
from .property import PropertyListing
from .vehicle import VehicleListing


class TransactionBase(SQLModel):
    # Linkage fields
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True, description="The ID of the buyer (User)")
    listing_id: Optional[uuid.UUID] = Field(index=True, description="Property or Vehicle ID")
    listing_type: ListingType
    
    # Financial fields
    amount: float
    payment_gateway: PaymentGateway
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING, index=True)
    reference: str = Field(unique=True, description="Payment gateway reference code")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Transaction(TransactionBase, table=True):
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    
    # --- RELATIONSHIPS ---
    buyer: User = Relationship(back_populates="transactions")
    
    # Conditional Relationships (requires manual join handling for conditional linkage)
    # The actual joins are defined in the User/Listing models using sa_relationship_kwargs.
    # We keep the back_populates here for integrity.
    property_listing: Optional[PropertyListing] = Relationship(back_populates="transactions")
    vehicle_listing: Optional[VehicleListing] = Relationship(back_populates="transactions")


# --- PYDANTIC SCHEMAS ---
class TransactionRead(TransactionBase):
    id: uuid.UUID
    
class TransactionCreate(TransactionBase):
    pass
    # No ID or created_at needed here