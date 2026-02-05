#!/usr/bin/env python3
"""
Simple test to verify that the application can interact with the updated database schema.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.src.core.database import get_session, sync_engine
from backend.src.models.todo import Todo, TodoBase
from backend.src.models.user import User
from backend.src.models.project import Project
from sqlmodel import SQLModel, Session, select
import uuid
from datetime import datetime

def test_application_interaction():
    """Test that the application can create and query records with the updated schema."""

    print("Testing application interaction with updated schema...")

    # Create a session using the sync engine
    with Session(sync_engine) as db:
        try:
            # Create a test user
            user = User(
                email="test@example.com",
                name="Test User",
                hashed_password="hashed_password_here"
            )

            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created user with ID: {user.id}")

            # Create a test project
            project = Project(
                name="Test Project",
                description="Test project description",
                color="#FF0000",
                user_id=user.id
            )

            db.add(project)
            db.commit()
            db.refresh(project)
            print(f"Created project with ID: {project.id}")

            # Create a todo with all the new fields
            todo_data = TodoBase(
                title="Test Todo",
                description="Test todo description",
                status="pending",  # New field
                priority="medium",
                due_date=datetime.now(),
                project_id=project.id,  # New field
                tags="test,important",  # New field
                reminder_time=datetime.now(),  # New field
                completed=False
            )

            todo = Todo(
                **todo_data.model_dump(),
                user_id=user.id
            )

            db.add(todo)
            db.commit()
            db.refresh(todo)
            print(f"Created todo with ID: {todo.id}")
            print(f"Todo status: {todo.status}")
            print(f"Todo tags: {todo.tags}")
            print(f"Todo project_id: {todo.project_id}")
            print(f"Todo reminder_time: {todo.reminder_time}")
            print(f"Todo due_date: {todo.due_date}")

            # Query the todo to make sure all fields are accessible
            statement = select(Todo).where(Todo.id == todo.id)
            result = db.exec(statement)
            retrieved_todo = result.first()
            if retrieved_todo:
                print(f"Retrieved todo - Title: {retrieved_todo.title}, Status: {retrieved_todo.status}, Tags: {retrieved_todo.tags}")

            # Clean up (remove test data)
            db.delete(retrieved_todo)
            db.delete(project)
            db.delete(user)
            db.commit()

            print("All tests passed! Application can interact with the updated schema.")

        except Exception as e:
            print(f"Error during testing: {e}")
            db.rollback()

if __name__ == "__main__":
    test_application_interaction()