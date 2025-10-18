# app/models/property.py
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column as SAColumn, text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TEXT, TIMESTAMP, NUMERIC, JSONB
from datetime import datetime
import uuid
from enum import Enum

# Enums (assuming they exist in .enums)
from .enums import PropertyType, ListingStatus

# Forward references - import User and Transaction later
# from .user import User
# from .payment import Transaction

class PropertyListingBase(SQLModel):
    """Base schema for Property Listing."""
    title: str = Field(max_length=200)
    description: Optional[str] = Field(
        default=None, 
        sa_column=SAColumn(TEXT)
    )
    property_type: PropertyType = Field(index=True)
    price: float = Field(gt=0)  # Positive price
    location: str = Field(index=True, max_length=255)
    
    # Geographic coordinates
    latitude: Optional[float] = Field(ge=-90, le=90)
    longitude: Optional[float] = Field(ge=-180, le=180)
    
    # Images as JSON array of URLs
    images: List[str] = Field(default_factory=list, sa_column=SAColumn(JSONB))
    
    # Status
    status: ListingStatus = Field(default=ListingStatus.AVAILABLE)
    
    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=SAColumn(
            TIMESTAMP(timezone=True),
            server_default=text("NOW()"),
            nullable=False
        )
    )

class PropertyListing(PropertyListingBase, table=True):
    """Database table model for Property Listings."""
    __tablename__ = "property_listings"
    
    # Primary key
    id: Optional[uuid.UUID] = Field(
        default=None,  # Let DB generate
        
        sa_column=SAColumn(
            UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
            nullable=False
        )
    )
    
    # Foreign Key to User (owner)
    owner_id: uuid.UUID = Field(
        sa_column=SAColumn(
            UUID(as_uuid=True),
            ForeignKey("users.id", ondelete="CASCADE"),  # Delete listing if owner deleted
            index=True
        )
    )
    
    # Forward relationship to Owner (User)
    owner: Optional["User"] = Relationship(
        back_populates="property_listings",
        sa_relationship_kwargs={
            "lazy": "select"
        }
    )
    
    # Relationship to Transactions (one-to-many - listing can have multiple transactions)
    # transactions: List["Transaction"] = Relationship(
    #     back_populates="property_listing",
    #     sa_relationship_kwargs={
    #         "lazy": "select"
    #     }
    # )  # Comment out until Transaction exists
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_property_listings_owner_id', 'owner_id'),
        Index('ix_property_listings_status', 'status'),
        Index('ix_property_listings_created_at', 'created_at'),
        Index('ix_property_listings_location', 'location'),
        {"extend_existing": True}
    )

# API Schemas
class PropertyListingRead(PropertyListingBase):
    id: uuid.UUID
    owner_id: uuid.UUID

class PropertyListingCreate(PropertyListingBase):
    pass  # owner_id set by service

class PropertyListingUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    status: Optional[ListingStatus] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    images: Optional[List[str]] = None

# Enums (if not in .enums, add here)
class PropertyType(str, Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    CONDO = "condo"
    LAND = "land"
    COMMERCIAL = "commercial"

class ListingStatus(str, Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"
    UNDER_OFFER = "under_offer"