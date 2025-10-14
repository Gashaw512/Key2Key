# app/models/audit_log.py
from sqlmodel import Field, SQLModel
from datetime import datetime
import uuid

class AuditLogBase(SQLModel):
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    action: str = Field(index=True)
    resource_type: str
    resource_id: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    details: dict = Field(default={}) # Store extra details as JSON

class AuditLog(AuditLogBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    # Relationship to User is optional (for system actions)