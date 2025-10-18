# app/models/enums.py (REVISED)

from enum import Enum

# --- User & Marketplace Enums ---
class UserRole(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"
    BROKER = "broker"
    ADMIN = "admin"

class PropertyType(str, Enum):
    HOUSE = "house"
    APARTMENT = "apartment"
    LAND = "land"
    OFFICE = "office"

class ListingStatus(str, Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    SOLD = "sold"
    LEASED = "leased" # For Vehicles

# --- Transaction Enums ---
class ListingType(str, Enum):
    PROPERTY = "property"
    VEHICLE = "vehicle"

class PaymentGateway(str, Enum):
    CHAPA = "chapa"
    TELEBIRR = "telebirr"
    STRIPE = "stripe"
    # Add other local/international gateways

class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"



# app/models/enums.py
# from enum import Enum
# from typing import Optional

# class UserRole(str, Enum):
#     BUYER = "buyer"
#     SELLER = "seller"
#     BROKER = "broker"
#     ADMIN = "admin"

# class PropertyType(str, Enum):
#     APARTMENT = "apartment"
#     HOUSE = "house"
#     CONDO = "condo"
#     LAND = "land"
#     COMMERCIAL = "commercial"
#     OFFICE = "office"

# class ListingStatus(str, Enum):
#     AVAILABLE = "available"
#     PENDING = "pending"
#     SOLD = "sold"
#     UNDER_OFFER = "under_offer"
#     WITHDRAWN = "withdrawn"

# class NotificationType(str, Enum):
#     TRANSACTION_SUCCESS = "transaction_success"
#     NEW_MESSAGE = "new_message"
#     LISTING_UPDATE = "listing_update"
#     ACCOUNT_ALERT = "account_alert"

# # Export all enums
# __all__ = [
#     "UserRole", "PropertyType", "ListingStatus", 
#     "NotificationType"
# ]