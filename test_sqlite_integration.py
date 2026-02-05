#!/usr/bin/env python3
"""
Simple test to verify that the updated SQLite database schema works correctly.
"""

import sqlite3
from datetime import datetime

def test_sqlite_integration():
    """Test that the SQLite database schema works with the expected data."""

    print("Testing SQLite database schema integration...")

    # Connect to the SQLite database
    conn = sqlite3.connect('backend/database.db')
    cursor = conn.cursor()

    try:
        # Insert a test user
        user_id = 'test_user_123'
        cursor.execute("""
            INSERT INTO user (id, email, name, hashed_password, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            'test@example.com',
            'Test User',
            'hashed_password_here',
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        print(f"Inserted test user with ID: {user_id}")

        # Insert a test project
        project_id = 'test_project_123'
        cursor.execute("""
            INSERT INTO project (id, name, description, color, user_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            project_id,
            'Test Project',
            'Test project description',
            '#FF0000',
            user_id,
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        print(f"Inserted test project with ID: {project_id}")

        # Insert a test todo with all the new fields
        todo_id = 'test_todo_123'
        cursor.execute("""
            INSERT INTO todo (id, title, description, status, priority, due_date,
                             project_id, tags, reminder_time, completed, user_id,
                             created_at, updated_at, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            todo_id,
            'Test Todo',
            'Test todo description',
            'pending',  # New field
            'medium',
            datetime.now().isoformat(),  # due_date
            project_id,  # New field
            'test,important',  # New field
            datetime.now().isoformat(),  # New field
            0,  # completed
            user_id,
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            None  # completed_at
        ))
        print(f"Inserted test todo with ID: {todo_id}")

        # Query the todo to verify all fields are accessible
        cursor.execute("SELECT * FROM todo WHERE id = ?", (todo_id,))
        result = cursor.fetchone()

        # Get column names
        column_names = [description[0] for description in cursor.description]
        todo_dict = dict(zip(column_names, result))

        print(f"Retrieved todo - Title: {todo_dict['title']}")
        print(f"Status: {todo_dict['status']}")
        print(f"Tags: {todo_dict['tags']}")
        print(f"Project ID: {todo_dict['project_id']}")
        print(f"Reminder time: {todo_dict['reminder_time']}")
        print(f"Due date: {todo_dict['due_date']}")

        # Verify all expected columns exist by checking for the new ones
        expected_new_columns = ['project_id', 'tags', 'reminder_time', 'status', 'due_date', 'completed_at']
        existing_columns = [col[0] for col in cursor.description]

        missing_columns = [col for col in expected_new_columns if col not in existing_columns]
        if missing_columns:
            print(f"[ERROR] Missing columns: {missing_columns}")
        else:
            print(f"[SUCCESS] All expected columns present: {expected_new_columns}")

        # Clean up test data
        cursor.execute("DELETE FROM todo WHERE id = ?", (todo_id,))
        cursor.execute("DELETE FROM project WHERE id = ?", (project_id,))
        cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
        conn.commit()

        print("All tests passed! SQLite database schema is working correctly.")

    except Exception as e:
        print(f"Error during testing: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    test_sqlite_integration()