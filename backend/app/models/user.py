# # app/models/user.py

# from typing import Optional, List, TYPE_CHECKING
# from sqlmodel import Field, SQLModel, Relationship, Column
# # from sqlalchemy.orm import Mapped, relationship
# from sqlalchemy import text
# from sqlalchemy.dialects.postgresql import UUID, TEXT, VARCHAR
# from datetime import datetime
# import uuid

# from .enums import UserRole

# # if TYPE_CHECKING:
# #     from app.models.notification import Notification
# #     from app.models.property import PropertyListing
# #     from app.models.vehicle import VehicleListing
# #     from app.models.payment import Transaction
# #     from app.models.broker import BrokerProfile

# class UserBase(SQLModel):
#     full_name: str
#     email: str = Field(sa_column=Column("email", VARCHAR(255), index=True, unique=True))
#     phone: Optional[str] = Field(default=None, index=True)
#     password_hash: str = Field(exclude=True, sa_column=Column("password_hash", TEXT))
#     role: UserRole = Field(default=UserRole.BUYER)
#     verified: bool = Field(default=False)
#     created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# class User(UserBase, table=True):
#     __tablename__ = "users"
    
#     id: Optional[uuid.UUID] = Field(
#         default_factory=uuid.uuid4, 
#         sa_column=Column(
#             UUID(as_uuid=True), 
#             primary_key=True, 
#             index=True, 
#             nullable=False, 
#             # server_default=text("uuid_generate_v4()")
#             server_default=text("gen_random_uuid()")  # Use gen_random_uuid() for PostgreSQL 13+
#         )
#     )

#     # ✅ Use string-based relationship for notifications
#     # ✅ String references - resolved by configure_mappers()
#     notifications: List["Notification"] = Relationship(
#         back_populates="user",
#         sa_relationship_kwargs={
#             "cascade": "all, delete-orphan",
#             "lazy": "select"
#         }
#     )
#     broker_profile: Optional["BrokerProfile"] = Relationship(back_populates="user")
#     property_listings: List["PropertyListing"] = Relationship(back_populates="owner")
#     vehicle_listings: List["VehicleListing"] = Relationship(back_populates="owner")
#     transactions: List["Transaction"] = Relationship(back_populates="buyer")

# class UserRead(UserBase):
#     id: uuid.UUID

# class UserCreate(UserBase):
#     password: str

# class UserUpdate(SQLModel):
#     full_name: Optional[str] = None
#     email: Optional[str] = None
#     phone: Optional[str] = None
#     role: Optional[UserRole] = None
#     verified: Optional[bool] = None
#     password: Optional[str] = None


# app/models/user.py

from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, DateTime
from sqlalchemy import text, Column as SAColumn, Index
from sqlalchemy.dialects.postgresql import UUID, TEXT, VARCHAR
from datetime import datetime, timezone

import uuid

from .enums import UserRole

class UserBase(SQLModel):
    full_name: str
    email: str = Field(sa_column=SAColumn(VARCHAR(255), index=True, unique=True))
    phone: Optional[str] = Field(default=None, index=True)
    password_hash: str = Field(exclude=True, sa_column=SAColumn(TEXT))
    role: UserRole = Field(default=UserRole.BUYER)
    verified: bool = Field(default=False)
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=SAColumn(DateTime(timezone=True), nullable=False),
    )

class User(UserBase, table=True):
    __tablename__ = "users"
    
    # Primary key with PostgreSQL UUID generation
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4,
        sa_column=SAColumn(
            UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()")  # PostgreSQL 13+
        )
    )
    
    # Relationships - String references for forward refs
    notifications: List["Notification"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "select"
        }
    )
    
    # One-to-one relationship
    # broker_profile: Optional["BrokerProfile"] = Relationship(
    #     back_populates="user",
    #     sa_relationship_kwargs={
    #         "uselist": False,  # One-to-one
    #         "lazy": "select"
    #     }
    # )

    broker_profile: Optional["BrokerProfile"] = Relationship(
    back_populates="user",
    sa_relationship_kwargs={
        "cascade": "all, delete-orphan",
        "uselist": False,
    }
   )
    
    property_listings: List["PropertyListing"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={
            "cascade": "save-update, merge",  # Save listings when user saved
            "lazy": "select"
        }
    )
    
    # vehicle_listings: List["VehicleListing"] = Relationship(
    #     back_populates="owner",
    #     sa_relationship_kwargs={
    #         "cascade": "save-update, merge",
    #         "lazy": "select"
    #     }
    # )
    
    # transactions: List["Transaction"] = Relationship(
    #     back_populates="buyer",
    #     sa_relationship_kwargs={
    #         "lazy": "select"
    #     }
    # )
    
    # Performance indexes
    __table_args__ = (
        Index('ix_users_email', 'email'),
        Index('ix_users_role', 'role'),
        Index('ix_users_created_at', 'created_at'),
    )

# API Response Models
class UserRead(UserBase):
    id: uuid.UUID

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    verified: Optional[bool] = None
    password: Optional[str] = None

# Fix forward references (add at bottom of file)
def setup_relationships():
    """Configure forward references for relationships."""
    from sqlalchemy.orm import configure_mappers
    configure_mappers()

# Export models
__all__ = [
    "User", "UserBase", "UserRead", "UserCreate", "UserUpdate",
    "UserRole"
]
