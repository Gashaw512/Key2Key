# app/models/vehicle.py

from typing import Optional, List
from sqlmodel import Field, SQLModel, Column, Relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Integer, TEXT, VARCHAR
from datetime import datetime
import uuid

# --- Local Imports ---
from .enums import ListingStatus # Uses the general ListingStatus enum
from .user import User  # Used for type hinting the 'owner' relationship
from .payment import Transaction # Used for type hinting the 'transactions' relationship


# ----------------------------------------------------------------------
# 1. Vehicle Listing Base Model (For API Schemas)
# ----------------------------------------------------------------------
class VehicleListingBase(SQLModel):
    title: str = Field(sa_column=Column("title", VARCHAR(255)))
    make: str = Field(index=True) # Brand (e.g., Toyota)
    model: str = Field(index=True) # Model name
    year: int = Field(sa_column=Column("year", Integer)) # Manufacture year
    price: float
    
    # Specific vehicle details
    mileage: int = Field(sa_column=Column("mileage", Integer))
    fuel_type: str
    transmission: str # Auto/Manual
    
    # Store images as a JSONB array of URLs
    images: List[str] = Field(default=[], sa_column=Column(JSONB))
    
    # Listing Status (Uses the general ListingStatus enum: available, leased, sold)
    status: ListingStatus = Field(default=ListingStatus.AVAILABLE)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# ----------------------------------------------------------------------
# 2. Vehicle Listing Table Model (ORM Definition)
# ----------------------------------------------------------------------
class VehicleListing(VehicleListingBase, table=True):
    """The ORM model for the Vehicle Listings table."""
    
    # Primary Key (UUID)
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    
    # Foreign Key to User
    owner_id: uuid.UUID = Field(foreign_key="user.id", index=True)

    # --- RELATIONSHIPS ---
    # Many-to-One: The listing belongs to one owner
    owner: User = Relationship(back_populates="vehicle_listings")
    
    # One-to-Many: The listing can be part of many transactions
    transactions: List["Transaction"] = Relationship(back_populates="vehicle_listing")


# ----------------------------------------------------------------------
# 3. Pydantic Schemas (For API I/O)
# ----------------------------------------------------------------------

class VehicleListingRead(VehicleListingBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime

class VehicleListingCreate(VehicleListingBase):
    # Owner_id is typically injected by the service layer from the authenticated user
    pass

class VehicleListingUpdate(SQLModel):
    title: Optional[str] = None
    price: Optional[float] = None
    mileage: Optional[int] = None
    status: Optional[ListingStatus] = None
    # Other fields (make, model, year) are typically not updated often