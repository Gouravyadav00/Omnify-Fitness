# schemas.py

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class BookingRequest(BaseModel):
    class_id: int
    client_name: str = Field(..., min_length=1)
    client_email: str

class BookingResponse(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: str
    booking_time: datetime

class ClassInfo(BaseModel):
    id: int
    name: str
    datetime: datetime
    instructor: str
    activity: str
    type: str
    available_slots: int
    max_slots: int
    price: int
    is_holiday: bool = False
