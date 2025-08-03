from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from zoneinfo import ZoneInfo
import holidays

from database import create_tables, get_db_connection
from models import get_classes, book_class, get_bookings_by_email
from schemas import BookingRequest, BookingResponse, ClassInfo

app = FastAPI(title="Omnify Fitness API", version="1.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure tables are created
create_tables()

# Indian Holidays
indian_holidays = holidays.country_holidays('IN', years=datetime.now().year)

@app.get("/classes", response_model=list[ClassInfo])
def list_classes(timezone: str = "Asia/Kolkata"):
    tz = ZoneInfo(timezone)
    conn = get_db_connection()
    classes = get_classes(conn)

    for cls in classes:
        cls["datetime"] = cls["datetime"].astimezone(tz)
        cls["is_holiday"] = cls["datetime"].date() in indian_holidays

    return classes

@app.post("/book", response_model=BookingResponse)
def make_booking(data: BookingRequest):
    conn = get_db_connection()
    return book_class(conn, data)

@app.get("/bookings", response_model=list[BookingResponse])
def list_bookings(email: str = Query(..., description="Client email")):
    conn = get_db_connection()
    return get_bookings_by_email(conn, email)
