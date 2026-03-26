from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select
import sys
import os

# Add backend to path for proper imports
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_path)

from database.connection import engine
from models.task_model import Task
# Updated imports to include update_task
from crud.task_crud import create_task, get_tasks, delete_task, update_task

# Import function to complete a task (this may need to be created if it doesn't exist)
def complete_task_in_db(session, task_id: int):
    """Helper function to complete a task in the database."""
    task = session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}

    task.status = "completed"
    session.add(task)
    session.commit()
    session.refresh(task)
    return task 

# MCP Server ka naam
mcp = FastMCP("Todo-Chatbot")

@mcp.tool()
def add_task(user_id: str, title: str, description: str = ""):
    """Add a new task to the todo list for a specific user.

    Args:
        user_id: ID of the user creating the task
        title: Title of the task
        description: Optional description of the task

    Returns:
        Task object with id, status, and title
    """
    with Session(engine) as session:
        new_task = Task(title=title, description=description, user_id=user_id)
        result = create_task(session, new_task)
        return {
            "task_id": result.id,
            "status": "created",
            "title": result.title
        }

# UPDATED TOOL: Added status filter
@mcp.tool()
def list_tasks(user_id: str, status: str = None):
    """Retrieve tasks from the list for a specific user.

    Args:
        user_id: ID of the user whose tasks to retrieve
        status: Optional status filter ("all", "pending", "completed")

    Returns:
        Array of task objects
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)

        # Status filtering as per specification
        if status and status != "all":
            statement = statement.where(Task.status == status)

        results = session.exec(statement).all()
        # Format results as per specification
        formatted_results = []
        for task in results:
            formatted_results.append({
                "id": task.id,
                "title": task.title,
                "completed": task.status == "completed",
                "status": task.status
            })
        return formatted_results

# UPDATED TOOL: Renamed from remove_task to delete_task
@mcp.tool()
def delete_task(user_id: str, task_id: int):
    """Remove a task from the list.

    Args:
        user_id: ID of the user requesting deletion
        task_id: ID of the task to delete

    Returns:
        task_id, status, and title of the deleted task
    """
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            return {"error": "Task not found", "task_id": task_id}

        # Verify ownership
        if task.user_id != user_id:
            return {"error": "Permission denied", "task_id": task_id}

        result = delete_task(session, task_id)
        return {
            "task_id": task_id,
            "status": "deleted",
            "title": result.title if result else "Unknown"
        }

# NEW TOOL: Added update_task tool
@mcp.tool()
def update_task(user_id: str, task_id: int, title: str = None, description: str = None):
    """Modify task title or description.

    Args:
        user_id: ID of the user requesting the update
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        task_id, status, and title of the updated task
    """
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            return {"error": "Task not found", "task_id": task_id}

        # Verify ownership
        if task.user_id != user_id:
            return {"error": "Permission denied", "task_id": task_id}

        result = update_task(session, task_id, title=title, description=description)
        return {
            "task_id": task_id,
            "status": "updated",
            "title": result.title if result else title
        }

# NEW TOOL: Added complete_task tool (missing requirement)
@mcp.tool()
def complete_task(user_id: str, task_id: int):
    """Mark a task as complete.

    Args:
        user_id: ID of the user requesting completion
        task_id: ID of the task to mark as complete

    Returns:
        task_id, status, and title of the completed task
    """
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            return {"error": "Task not found", "task_id": task_id}

        # Verify ownership
        if task.user_id != user_id:
            return {"error": "Permission denied", "task_id": task_id}

        task.status = "completed"
        session.add(task)
        session.commit()
        session.refresh(task)
        return {
            "task_id": task_id,
            "status": "completed",
            "title": task.title
        }