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