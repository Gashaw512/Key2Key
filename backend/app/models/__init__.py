# # app/models/__init__.py
# from __future__ import annotations
# from typing import List
# from sqlmodel import SQLModel
# import sqlalchemy
# from sqlalchemy.orm import configure_mappers

# # Prevent recursive imports and early mapper configuration
# _CONFIGURED = False

# # Import models in dependency order (parents before children)
# # User must be imported FIRST as it's referenced by Notification
# try:
#     from .user import User, UserBase, UserCreate, UserRead, UserUpdate
#     from .notification import Notification, NotificationBase, NotificationRead, NotificationCreate
#     from .broker import BrokerProfile, BrokerProfileBase, BrokerProfileRead
#     from .property import PropertyListing, PropertyListingBase, PropertyListingRead, PropertyListingCreate, PropertyListingUpdate
#     from .vehicle import VehicleListing, VehicleListingBase, VehicleListingRead, VehicleListingCreate, VehicleListingUpdate
#     from .payment import Transaction, TransactionBase, TransactionRead, TransactionCreate
#     from .review import Review, ReviewBase, ReviewRead, ReviewCreate
#     from .chat import ChatThread, ChatMessage, ChatThreadBase, ChatMessageBase, ChatThreadRead, ChatMessageRead
#     from .verification import Verification, VerificationBase, VerificationRead, VerificationCreate
#     from .analytics import AnalyticsEvent, AnalyticsEventBase, AnalyticsEventRead
#     from .audit_log import AuditLog, AuditLogBase, AuditLogRead
#     from .enums import *
    
#     # ✅ All models imported successfully
#     MODELS_IMPORTED = True
    
# except ImportError as e:
#     print(f"⚠️ Model import error: {e}")
#     MODELS_IMPORTED = False

# def configure_models() -> bool:
#     """Configure SQLAlchemy mappers ONLY when all models are ready."""
#     global _CONFIGURED
    
#     if _CONFIGURED:
#         return True
    
#     if not MODELS_IMPORTED:
#         print("⚠️ Cannot configure models - imports incomplete")
#         return False
    
#     try:
#         # ✅ Configure mappers after ALL imports complete
#         configure_mappers()
#         _CONFIGURED = True
#         print("✅ SQLAlchemy mappers configured successfully!")
#         return True
        
#     except Exception as e:
#         print(f"❌ Mapper configuration failed: {e}")
#         return False

# # Export models
# __all__ = [
#     "User", "Notification", "BrokerProfile", "PropertyListing", "VehicleListing",
#     "Transaction", "Review", "ChatThread", "ChatMessage", "Verification",
#     "AnalyticsEvent", "AuditLog", "configure_models", "UserBase", "NotificationBase"
# ]

# def create_db_and_tables(engine):
#     """Create tables after ensuring models are configured."""
#     if configure_models():  # Configure first
#         SQLModel.metadata.create_all(engine)
#         print("✅ Database tables created!")
#     else:
#         raise RuntimeError("Cannot create tables - model configuration failed")

# # Defer configuration until explicitly called
# metadata = SQLModel.metadata

# app/models/__init__.py
# Just re-export models - no configuration here
from .user import User, UserCreate, UserRead, UserUpdate
from .notification import Notification, NotificationCreate, NotificationRead
from .broker import BrokerProfile, BrokerProfileCreate, BrokerProfileRead

from .property import (
    PropertyListing, 
    PropertyListingCreate, 
    PropertyListingRead,
    PropertyListingUpdate,
    PropertyType,  
    ListingStatus       
)
# from .chat import ChatThread, ChatThreadCreate, ChatThreadRead, ChatThreadUpdate, UserChatLink
# from .review import Review, ReviewCreate, ReviewRead, ReviewUpdate


__all__ = [
    # User Models
    "User", "UserCreate", "UserRead", "UserUpdate",
    
    # Notification Models
    "Notification", "NotificationCreate", "NotificationRead",

    # Broker Models
    "BrokerProfile", "BrokerProfileCreate", "BrokerProfileRead"

    # Property Models
    "PropertyListing", "PropertyListingCreate", "PropertyListingRead", "PropertyListingUpdate", "PropertyType", "ListingStatus",
    
    # Chat Models
    # "ChatThread", "ChatThreadCreate", "ChatThreadRead", "ChatThreadUpdate", "UserChatLink",
    
    # Review Models
    # "Review", "ReviewCreate", "ReviewRead", "ReviewUpdate"
    # Review Models
]


# Configure mappers AFTER all imports
try:
    from sqlalchemy.orm import configure_mappers
    configure_mappers()
    print("✅ Mappers configured in __init__.py")
except Exception as e:
    print(f"⚠️ Mapper config warning: {e}")





