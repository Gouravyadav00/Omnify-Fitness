# database.py

import sqlite3

def get_db_connection():
    conn = sqlite3.connect("fitness.db", detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS instructors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        activity TEXT NOT NULL,
        type TEXT CHECK(type IN ('solo', 'group')) NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        datetime TIMESTAMP NOT NULL,
        instructor_id INTEGER NOT NULL,
        max_slots INTEGER NOT NULL,
        price INTEGER NOT NULL,
        FOREIGN KEY(instructor_id) REFERENCES instructors(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        client_name TEXT NOT NULL,
        client_email TEXT NOT NULL,
        booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(class_id) REFERENCES classes(id)
    )
    """)

    conn.commit()
    conn.close()
