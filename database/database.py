import sqlite3
import sys
from pathlib import Path

from PySide6.QtCore import QStandardPaths

DATABASE_NAME = "campusmate.db"


def get_database_path():
    """Use a writable per-user location for installed app builds."""
    if getattr(sys, "frozen", False):
        data_directory = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        database_path = Path(data_directory) / DATABASE_NAME
    else:
        database_path = Path(__file__).resolve().parent.parent / DATABASE_NAME

    database_path.parent.mkdir(parents=True, exist_ok=True)
    return str(database_path)


def get_connection():
    return sqlite3.connect(get_database_path())


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # -------------------------
    # Classes table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            teacher TEXT,
            day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            room TEXT
        )
    """)

    # -------------------------
    # Tasks table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT,
            due_date TEXT,
            priority TEXT,
            completed INTEGER DEFAULT 0
        )
    """)
        # -------------------------
    # Attendance table
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            attended INTEGER NOT NULL,
            total INTEGER NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            goal_hours REAL DEFAULT 10,
            completed_hours REAL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)


    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("CampusMate database is ready!")
