from datetime import datetime, timedelta, time
from database import get_db_connection, create_tables

# Activities and assigned tutors
activities = ["Yoga", "Zumba", "HIIT"]
tutors = {
    "Yoga": {"solo": "Anjali", "group": "Ravi"},
    "Zumba": {"solo": "Sakshi", "group": "Rahul"},
    "HIIT": {"solo": "Meera", "group": "Ajay"}
}

def create_instructors(conn):
    cursor = conn.cursor()
    for activity, types in tutors.items():
        for session_type, name in types.items():
            cursor.execute("""
            INSERT INTO instructors (name, activity, type)
            VALUES (?, ?, ?)
            """, (name, activity, session_type))
    conn.commit()

def get_instructor_id(conn, activity, session_type):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id FROM instructors WHERE activity = ? AND type = ?
    """, (activity, session_type))
    return cursor.fetchone()["id"]

def create_classes(conn):
    cursor = conn.cursor()
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    for i in range(7):  # For the next 7 days
        class_day = now + timedelta(days=i)
        
        for activity in activities:
            # Group class (9 AM)
            group_time = datetime.combine(class_day.date(), time(9, 0))
            group_instructor = get_instructor_id(conn, activity, "group")
            cursor.execute("""
            INSERT INTO classes (name, datetime, instructor_id, max_slots, price)
            VALUES (?, ?, ?, ?, ?)
            """, (f"{activity} - Group", group_time, group_instructor, 30, 500))

            # Solo class (2 PM)
            solo_time = datetime.combine(class_day.date(), time(14, 0))
            solo_instructor = get_instructor_id(conn, activity, "solo")
            cursor.execute("""
            INSERT INTO classes (name, datetime, instructor_id, max_slots, price)
            VALUES (?, ?, ?, ?, ?)
            """, (f"{activity} - Solo", solo_time, solo_instructor, 1, 2000))

    conn.commit()

def seed():
    create_tables()
    conn = get_db_connection()
    create_instructors(conn)
    create_classes(conn)
    conn.close()

if __name__ == "__main__":
    seed()
