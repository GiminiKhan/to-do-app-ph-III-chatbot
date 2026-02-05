#!/usr/bin/env python3
"""
Test script to verify that the database schema matches the model definitions.
"""

import sys
import os
from pathlib import Path

# Add the backend to the path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from sqlalchemy import create_engine, inspect
from src.models.todo import Todo
from src.models.project import Project
from src.models.user import User
from sqlmodel import SQLModel

def test_database_schema():
    """Test that the database schema matches the model definitions."""

    print("Testing database schema against model definitions...")

    # Use the local SQLite database for testing
    sqlite_db_url = "sqlite:///backend/database.db"
    engine = create_engine(sqlite_db_url)

    # Get database inspector
    inspector = inspect(engine)

    # Get table names
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")

    # Check todo table
    if 'todo' in tables:
        todo_columns = inspector.get_columns('todo')
        print(f"\nTodo table columns: {[col['name'] for col in todo_columns]}")

        # Expected columns from the model
        expected_todo_cols = {
            'id', 'title', 'description', 'status', 'priority',
            'due_date', 'project_id', 'tags', 'reminder_time',
            'completed', 'user_id', 'created_at', 'updated_at',
            'completed_at'  # Added by our migration
        }

        actual_todo_cols = {col['name'] for col in todo_columns}

        missing_cols = expected_todo_cols - actual_todo_cols
        extra_cols = actual_todo_cols - expected_todo_cols

        if missing_cols:
            print(f"[ERROR] Missing columns in todo table: {missing_cols}")
        else:
            print("[SUCCESS] All expected columns present in todo table")

        if extra_cols:
            print(f"[INFO] Extra columns in todo table: {extra_cols}")

    # Check project table
    if 'project' in tables:
        project_columns = inspector.get_columns('project')
        print(f"\nProject table columns: {[col['name'] for col in project_columns]}")

        # Expected columns from the model
        expected_project_cols = {
            'id', 'name', 'description', 'color', 'user_id', 'created_at', 'updated_at'
        }

        actual_project_cols = {col['name'] for col in project_columns}

        missing_cols = expected_project_cols - actual_project_cols
        extra_cols = actual_project_cols - expected_project_cols

        if missing_cols:
            print(f"[ERROR] Missing columns in project table: {missing_cols}")
        else:
            print("[SUCCESS] All expected columns present in project table")

        if extra_cols:
            print(f"[INFO] Extra columns in project table: {extra_cols}")

    # Check user table
    if 'user' in tables:
        user_columns = inspector.get_columns('user')
        print(f"\nUser table columns: {[col['name'] for col in user_columns]}")

        # Expected columns from the User model
        expected_user_cols = {
            'id', 'email', 'name', 'created_at', 'updated_at', 'hashed_password'
        }

        actual_user_cols = {col['name'] for col in user_columns}

        missing_cols = expected_user_cols - actual_user_cols
        extra_cols = actual_user_cols - expected_user_cols

        if missing_cols:
            print(f"[ERROR] Missing columns in user table: {missing_cols}")
        else:
            print("[SUCCESS] All expected columns present in user table")

    print("\nSchema verification completed!")

if __name__ == "__main__":
    test_database_schema()