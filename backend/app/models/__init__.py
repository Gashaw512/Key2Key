# app/models/__init__.py

# =========================================================================
# The purpose of this file is to ensure all SQLModel table definitions 
# are correctly imported and registered with SQLModel's metadata before 
# the application starts (critical for Alembic/lifespan table creation).
# =========================================================================

# 1. Core/Shared Definitions
# Import all enums and shared types for global access
from .enums import * # 2. Base Entities
from .user import User, UserBase, UserCreate, UserRead, UserUpdate

# 3. Broker Profile (Associated with User)
# Note: BrokerProfile is the table model
from .broker import BrokerProfile, BrokerProfileBase, BrokerProfileRead

# 4. Marketplace Listings 
# Property
from .property import PropertyListing, PropertyListingBase, PropertyListingRead, PropertyListingCreate, PropertyListingUpdate
# Vehicle
from .vehicle import VehicleListing, VehicleListingBase, VehicleListingRead, VehicleListingCreate, VehicleListingUpdate

# 5. Transactional Entities
# Payment/Transaction
from .payment import Transaction, TransactionBase, TransactionRead, TransactionCreate 
# Review
from .review import Review, ReviewBase, ReviewRead, ReviewCreate

# 6. Operational/Enhancement Modules
# Chat (Assuming ChatMessage and ChatThread are both tables)
from .chat import ChatThread, ChatMessage, ChatThreadBase, ChatMessageBase, ChatThreadRead, ChatMessageRead
# Notification
from .notification import Notification, NotificationBase, NotificationRead, NotificationCreate 
# Verification
from .verification import Verification, VerificationBase, VerificationRead, VerificationCreate 
# Analytics
from .analytics import AnalyticsEvent, AnalyticsEventBase, AnalyticsEventRead
# Audit Log
from .audit_log import AuditLog, AuditLogBase, AuditLogRead

# Note on Robustness:
# While some Schemas (e.g., *Read, *Create) are not strictly needed by Alembic, 
# explicitly listing the *Base and *Table classes ensures SQLModel's metadata 
# is fully populated, and future model discovery tools have clear targets.