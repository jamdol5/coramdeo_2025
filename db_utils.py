import sqlite3
from datetime import datetime
import os
from pytz import timezone

DB_PATH = 'attendance.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    return conn

def init_db(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY,
            date TEXT,
            grade TEXT,
            student_name TEXT,
            attended INTEGER,
            contacted INTEGER DEFAULT 0,
            contact_date TEXT,
            update_count INTEGER DEFAULT 0,
            UNIQUE(date, grade, student_name)
        )
    ''')
    # Add missing columns if they don't exist
    try:
        c.execute('ALTER TABLE attendance ADD COLUMN contact_date TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        c.execute('ALTER TABLE attendance ADD COLUMN update_count INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists

    conn.commit()

def save_attendance_to_db(conn, attendance, date):
    c = conn.cursor()
    for grade, students in attendance.items():
        for student, attended in students.items():
            # Check if the record already exists for the given date, grade, and student_name
            c.execute('''
                SELECT id, update_count FROM attendance
                WHERE date = ? AND grade = ? AND student_name = ?
            ''', (date, grade, student))
            record = c.fetchone()

            if record:
                # If record exists, update it with the new attendance value and increment the update count
                new_update_count = record[1] + 1
                c.execute('''
                    UPDATE attendance
                    SET attended = ?, update_count = ?
                    WHERE date = ? AND grade = ? AND student_name = ?
                ''', (int(attended), new_update_count, date, grade, student))
            else:
                # If record does not exist, insert a new record with update_count set to 0
                c.execute('''
                    INSERT INTO attendance (date, grade, student_name, attended, update_count) VALUES (?, ?, ?, ?, 0)
                ''', (date, grade, student, int(attended)))
    conn.commit()

def get_attendance_summary(conn, date):
    c = conn.cursor()
    c.execute('''
        SELECT grade, COUNT(student_name) as total, SUM(attended) as attended
        FROM attendance
        WHERE date = ?
        GROUP BY grade
    ''', (date,))
    summary = c.fetchall()
    return summary

def get_non_attendees(conn, date):
    c = conn.cursor()
    c.execute('''
        SELECT grade, student_name
        FROM attendance
        WHERE date = ? AND attended = 0
    ''', (date,))
    non_attendees = c.fetchall()
    return non_attendees

def remove_duplicates(conn):
    c = conn.cursor()
    c.execute('''
        DELETE FROM attendance
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM attendance
            GROUP BY date, grade, student_name
        )
    ''')
    conn.commit()

def update_contact_status(conn, student_name, contacted):
    contact_date = datetime.now().strftime('%Y-%m-%d') if contacted == 1 else None
    c = conn.cursor()
    c.execute('''
        UPDATE attendance
        SET contacted = ?, contact_date = ?
        WHERE student_name = ?
    ''', (contacted, contact_date, student_name))
    conn.commit()

def get_contacted_students(conn):
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT student_name, contact_date
        FROM attendance
        WHERE contacted = 1
    ''')
    contacted_students = c.fetchall()
    return contacted_students

def update_contact_status(conn, student_name, contacted, contact_datetime):
    contact_date = contact_datetime.strftime('%Y-%m-%d %H:%M:%S') if contacted == 1 else None
    c = conn.cursor()
    c.execute('''
        UPDATE attendance
        SET contacted = ?, contact_date = ?
        WHERE student_name = ?
    ''', (contacted, contact_date, student_name))
    conn.commit()

def get_contacted_students(conn):
    c = conn.cursor()
    c.execute('''
        SELECT DISTINCT student_name, MAX(contact_date)
        FROM attendance
        WHERE contacted = 1
        GROUP BY student_name
    ''')
    contacted_students = c.fetchall()
    return contacted_students
