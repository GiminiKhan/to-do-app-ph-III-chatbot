#!/usr/bin/env python3
"""
Script to fix the SQLite database schema mismatch for the todo table.
This script adds missing columns to the todo table and creates missing tables.
"""

import sqlite3
from pathlib import Path

def fix_sqlite_database():
    """Fix the SQLite database schema."""
    db_path = Path("backend/database.db")

    if not db_path.exists():
        print(f"Database file {db_path} does not exist.")
        return

    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Check current todo table structure
    cursor.execute("PRAGMA table_info(todo)")
    current_columns = [col[1] for col in cursor.fetchall()]
    print(f"Current todo table columns: {current_columns}")

    # Add missing columns to todo table
    missing_columns = []

    # Check for each expected column
    expected_columns = [
        ('project_id', 'TEXT'),
        ('tags', 'VARCHAR(500)'),
        ('reminder_time', 'DATETIME'),
        ('status', 'VARCHAR(20)'),
        ('due_date', 'DATETIME'),
        ('completed_at', 'DATETIME')
    ]

    for col_name, col_type in expected_columns:
        if col_name not in current_columns:
            missing_columns.append((col_name, col_type))

    if missing_columns:
        print(f"Adding missing columns: {missing_columns}")
        for col_name, col_type in missing_columns:
            try:
                cursor.execute(f"ALTER TABLE todo ADD COLUMN {col_name} {col_type}")
                print(f"Added column {col_name} of type {col_type}")
            except sqlite3.OperationalError as e:
                print(f"Could not add column {col_name}: {e}")
    else:
        print("No missing columns to add to todo table")

    # Check if project table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='project'")
    project_table_exists = cursor.fetchone() is not None

    if not project_table_exists:
        print("Creating missing project table...")
        cursor.execute("""
            CREATE TABLE project (
                id TEXT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                color VARCHAR(7) DEFAULT '#000000',
                user_id TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Project table created successfully")
    else:
        print("Project table already exists")

    # Check if status column has values, if not populate based on completed column
    cursor.execute("SELECT COUNT(*) FROM todo WHERE status IS NULL OR status = ''")
    null_status_count = cursor.fetchone()[0]

    if null_status_count > 0:
        print(f"Updating {null_status_count} todos with missing status based on completed field...")
        cursor.execute("""
            UPDATE todo
            SET status = CASE
                WHEN completed = 1 THEN 'completed'
                ELSE 'pending'
            END
            WHERE status IS NULL OR status = ''
        """)
        print("Status column updated successfully")

    # Commit changes
    conn.commit()

    # Verify changes
    cursor.execute("PRAGMA table_info(todo)")
    updated_columns = [col[1] for col in cursor.fetchall()]
    print(f"\nUpdated todo table columns: {updated_columns}")

    # Check project table structure
    cursor.execute("PRAGMA table_info(project)")
    project_columns = [col[1] for col in cursor.fetchall()]
    print(f"Project table columns: {project_columns}")

    conn.close()
    print("\nSQLite database schema updated successfully!")


if __name__ == "__main__":
    fix_sqlite_database()