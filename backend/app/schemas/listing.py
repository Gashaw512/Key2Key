from pydantic import BaseModel
from typing import Optional

class ListingBase(BaseModel):
    title: str
    description: str
    price: float
    category: str

class ListingCreate(ListingBase):
    pass

class ListingRead(ListingBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True
