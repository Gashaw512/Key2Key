# app/models/audit_log.py (COMPLETE AND PROFESSIONAL)

from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel, Relationship, Column
from sqlalchemy.dialects.postgresql import UUID, JSONB, TEXT
from datetime import datetime
import uuid

# --- Local Imports ---
from .user import User # Used for the optional Relationship

# ----------------------------------------------------------------------
# 1. Audit Log Base Model (For API Schemas)
# ----------------------------------------------------------------------
class AuditLogBase(SQLModel):
    """Base schema for the Audit Log records."""
    
    # Linkage to the user who performed the action (optional for system/anonymous actions)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id", index=True)
    
    # Action details
    action: str = Field(index=True, sa_column=Column("action", TEXT)) # e.g., 'USER_CREATED', 'LISTING_UPDATED'
    resource_type: str = Field(description="The model/table being affected, e.g., 'User', 'PropertyListing'")
    resource_id: Optional[str] = Field(default=None, index=True, description="The UUID of the affected resource (stored as string)")
    
    # Operational/System details
    ip_address: Optional[str] = Field(default=None, index=True)
    
    # Use Dict[str, Any] for flexibility, mapped to PostgreSQL's JSONB
    details: Dict[str, Any] = Field(
        default={}, 
        sa_column=Column(JSONB), 
        description="Structured details of the change or request payload."
    )
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)


# ----------------------------------------------------------------------
# 2. Audit Log Table Model (ORM Definition)
# ----------------------------------------------------------------------
class AuditLog(AuditLogBase, table=True):
    """The ORM model for the Audit Log table."""
    
    # Primary Key (UUID)
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        primary_key=True, 
        index=True, 
        nullable=False
    )
    
    # Relationship to User (optional, and usually not back-populated to User for performance)
    user: Optional["User"] = Relationship(back_populates="audit_logs")


# ----------------------------------------------------------------------
# 3. Pydantic Schemas (For API I/O)
# ----------------------------------------------------------------------
class AuditLogRead(AuditLogBase):
    """Schema for returning an Audit Log record."""
    id: uuid.UUID
    timestamp: datetime
    # Note: No AuditLogCreate is usually needed, as creation is done by the service layer.