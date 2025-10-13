# app/db/base_class.py (REVISED for SQLModel)

# Import the main SQLModel class
from sqlmodel import SQLModel

# Re-export SQLModel to be the "Base" for all your models.
# This ensures a cleaner import path (e.g., from app.db.base_class import Base)
Base = SQLModel