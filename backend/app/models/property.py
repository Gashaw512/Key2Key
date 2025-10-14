# app/models/property.py

from typing import Optional, List
from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy.dialects.postgresql import JSONB, TEXT
from datetime import datetime
import uuid

# --- Local Imports ---
from .enums import PropertyType, ListingStatus
from .user import User  # Used for type hinting the 'owner' relationship
from .payment import Transaction # Used for type hinting the 'transactions' relationship


# ----------------------------------------------------------------------
# 1. Property Listing Base Model (For API Schemas)
# ----------------------------------------------------------------------
class PropertyListingBase(SQLModel):
    title: str
    description: Optional[str] = Field(default=None, sa_column=Column("description", TEXT))
    property_type: PropertyType = Field(index=True)
    price: float
    location: str = Field(index=True)
    
    # Geographic coordinates (optional, but highly recommended)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    # Store images as a JSONB array of URLs
    images: List[str] = Field(default=[], sa_column=Column(JSONB))
    
    # Listing Status
    status: ListingStatus = Field(default=ListingStatus.AVAILABLE)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# ----------------------------------------------------------------------
# 2. Property Listing Table Model (ORM Definition)
# ----------------------------------------------------------------------
class PropertyListing(PropertyListingBase, table=True):
    """The ORM model for the Property Listings table."""
    
    # Primary Key (UUID)
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    
    # Foreign Key to User
    owner_id: uuid.UUID = Field(foreign_key="user.id", index=True)

    # --- RELATIONSHIPS ---
    # Many-to-One: The listing belongs to one owner
    owner: User = Relationship(back_populates="property_listings")
    
    # One-to-Many: The listing can be part of many transactions
    transactions: List["Transaction"] = Relationship(back_populates="property_listing")


# ----------------------------------------------------------------------
# 3. Pydantic Schemas (For API I/O)
# ----------------------------------------------------------------------

class PropertyListingRead(PropertyListingBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime

class PropertyListingCreate(PropertyListingBase):
    # Owner_id is typically injected by the service layer from the authenticated user
    pass

class PropertyListingUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    status: Optional[ListingStatus] = None

# Note: Updates to images, latitude, longitude, etc., would also be optional here.