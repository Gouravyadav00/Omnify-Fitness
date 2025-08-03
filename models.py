# models.py

from datetime import datetime
from sqlite3 import Connection
from schemas import BookingRequest
from fastapi import HTTPException

def get_classes(conn: Connection):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.id, c.name, c.datetime, i.name as instructor, i.activity, i.type,
           c.max_slots, c.price,
           (c.max_slots - COUNT(b.id)) as available_slots
    FROM classes c
    JOIN instructors i ON c.instructor_id = i.id
    LEFT JOIN bookings b ON b.class_id = c.id
    WHERE c.datetime >= CURRENT_TIMESTAMP
    GROUP BY c.id
    ORDER BY c.datetime ASC
    """)
    return [dict(row) for row in cursor.fetchall()]

def book_class(conn: Connection, data: BookingRequest):
    cursor = conn.cursor()

    # Check if class exists and fetch availability
    cursor.execute("""
    SELECT c.id, c.max_slots, COUNT(b.id) as booked
    FROM classes c
    LEFT JOIN bookings b ON b.class_id = c.id
    WHERE c.id = ?
    GROUP BY c.id
    """, (data.class_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Class not found")

    if row["booked"] >= row["max_slots"]:
        raise HTTPException(status_code=400, detail="Class is fully booked")

    cursor.execute("""
    INSERT INTO bookings (class_id, client_name, client_email)
    VALUES (?, ?, ?)
    """, (data.class_id, data.client_name, data.client_email))
    conn.commit()

    booking_id = cursor.lastrowid
    cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
    return dict(cursor.fetchone())

def get_bookings_by_email(conn: Connection, email: str):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM bookings WHERE client_email = ?
    ORDER BY booking_time DESC
    """, (email,))
    return [dict(row) for row in cursor.fetchall()]
