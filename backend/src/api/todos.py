"""Todos API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from datetime import datetime
import uuid

from ..models.todo import Todo, TodoBase
from ..models.user import User
from .deps import get_current_user
from ..core.database import get_async_session
from ..core.exceptions import TodoNotFoundException, PermissionDeniedException
from .responses import format_success_response, format_error_response, format_collection_response

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    project_id: Optional[str] = None,
    tags: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc"
):
    """
    Get all tasks for the specified user with filtering, pagination, sorting, and search.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        current_user: The current authenticated user
        db: Database session
        status: Filter by task status (pending, in_progress, completed)
        priority: Filter by task priority (low, medium, high, urgent)
        project_id: Filter by project ID
        tags: Filter by tags (comma-separated tags to match)
        search: Search term to match in title or description
        limit: Number of tasks to return (default: 50)
        offset: Number of tasks to skip (default: 0)
        sort_by: Field to sort by (created_at, updated_at, priority, due_date) (default: created_at)
        sort_order: Sort order (asc, desc) (default: desc)

    Returns:
        Standardized response with list of tasks for the specified user
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to access tasks for this user"
        )

    # Build query with filters
    statement = select(Todo).where(Todo.user_id == current_user.id)

    # Apply status filter if provided
    if status:
        statement = statement.where(Todo.status == status)

    # Apply priority filter if provided
    if priority:
        statement = statement.where(Todo.priority == priority)

    # Apply project_id filter if provided
    if project_id:
        try:
            project_uuid = uuid.UUID(project_id)
            statement = statement.where(Todo.project_id == project_uuid)
        except ValueError:
            return format_error_response(
                error_code="INVALID_PROJECT_ID",
                message="Invalid project ID format"
            )

    # Apply tags filter if provided
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        for tag in tag_list:
            tag_pattern = f"%{tag}%"
            statement = statement.where(Todo.tags.ilike(tag_pattern))

    # Apply search filter if provided
    if search:
        search_pattern = f"%{search}%"
        statement = statement.where((Todo.title.ilike(search_pattern)) | (Todo.description.ilike(search_pattern)))

    # Apply sorting
    sort_column = getattr(Todo, sort_by, Todo.created_at)
    if sort_order.lower() == "asc":
        statement = statement.order_by(sort_column.asc())
    else:
        statement = statement.order_by(sort_column.desc())

    # Apply pagination
    statement = statement.offset(offset).limit(limit)

    result = await db.execute(statement)
    tasks = result.scalars().all()

    # Get total count for pagination info (without limits)
    count_statement = select(func.count(Todo.id)).where(Todo.user_id == current_user.id)
    if status:
        count_statement = count_statement.where(Todo.status == status)
    if priority:
        count_statement = count_statement.where(Todo.priority == priority)
    if project_id:
        try:
            project_uuid = uuid.UUID(project_id)
            count_statement = count_statement.where(Todo.project_id == project_uuid)
        except ValueError:
            pass  # Already handled above
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        for tag in tag_list:
            tag_pattern = f"%{tag}%"
            count_statement = count_statement.where(Todo.tags.ilike(tag_pattern))
    if search:
        search_pattern = f"%{search}%"
        count_statement = count_statement.where((Todo.title.ilike(search_pattern)) | (Todo.description.ilike(search_pattern)))

    # Execute count query separately
    count_result = await db.execute(count_statement)
    total_count = count_result.scalar_one()

    return format_collection_response(
        data=[task.dict() for task in tasks],
        message=f"Retrieved {len(tasks)} tasks for user {user_id}",
        total=total_count,
        page=(offset // limit) + 1,
        limit=limit
    )


@router.post("/{user_id}/tasks")
async def create_task(
    user_id: str,
    todo_data: TodoBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the specified user.

    Args:
        user_id: The ID of the user for whom to create the task
        todo_data: Task data from request body
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with the created task
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to create tasks for this user"
        )

    # Create new task with the current user's ID
    task_data = todo_data.dict()
    # If task is created with 'completed' status, set completed_at
    if task_data.get('status') == 'completed' and task_data.get('completed_at') is None:
        task_data['completed_at'] = datetime.utcnow()

    task = Todo(**task_data, user_id=current_user.id)

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return format_success_response(
        data=task.dict(),
        message="Task created successfully"
    )


@router.get("/{user_id}/tasks/{task_id}")
async def get_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task by ID for the specified user.

    Args:
        user_id: The ID of the user whose task to retrieve
        task_id: The ID of the task to retrieve
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with the requested task
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to access tasks for this user"
        )

    # Convert task_id string to UUID object
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_TASK_ID",
            message="Invalid task ID format"
        )

    # Get the task by ID
    statement = select(Todo).where(Todo.id == task_uuid)
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        return format_error_response(
            error_code="TASK_NOT_FOUND",
            message="Task not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to access this task"
        )

    return format_success_response(
        data=task.dict(),
        message=f"Retrieved task {task_id}"
    )


@router.put("/{user_id}/tasks/{task_id}")
async def update_task_put(
    user_id: str,
    task_id: str,
    todo_update: TodoBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task by ID for the specified user using PUT method.

    Args:
        user_id: The ID of the user whose task to update
        task_id: The ID of the task to update
        todo_update: Updated task data from request body
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with the updated task
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to update tasks for this user"
        )

    # Convert task_id string to UUID object
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_TASK_ID",
            message="Invalid task ID format"
        )

    # Get the existing task
    statement = select(Todo).where(Todo.id == task_uuid)
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        return format_error_response(
            error_code="TASK_NOT_FOUND",
            message="Task not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to update this task"
        )

    # Update the task with the new data
    for key, value in todo_update.dict().items():  # Use dict() instead of exclude_unset=True for PUT
        if key == "status":
            # Handle status update and synchronize completed_at accordingly
            old_status = task.status
            task.status = value
            if value == "completed":
                if task.completed_at is None:
                    task.completed_at = datetime.utcnow()
            elif old_status == "completed" and value != "completed":
                # Task was completed but is now changing to a different status
                task.completed_at = None
        else:
            setattr(task, key, value)

    task.updated_at = datetime.utcnow()  # Update timestamp

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return format_success_response(
        data=task.dict(),
        message=f"Task {task_id} updated successfully"
    )


@router.patch("/{user_id}/tasks/{task_id}")
async def update_task(
    user_id: str,
    task_id: str,
    todo_update: TodoBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task by ID for the specified user using PATCH method.

    Args:
        user_id: The ID of the user whose task to update
        task_id: The ID of the task to update
        todo_update: Updated task data from request body
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with the updated task
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to update tasks for this user"
        )

    # Convert task_id string to UUID object
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_TASK_ID",
            message="Invalid task ID format"
        )

    # Get the existing task
    statement = select(Todo).where(Todo.id == task_uuid)
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        return format_error_response(
            error_code="TASK_NOT_FOUND",
            message="Task not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to update this task"
        )

    # Update the task with the new data
    for key, value in todo_update.dict(exclude_unset=True).items():
        if key == "status":
            # Handle status update and synchronize completed_at accordingly
            old_status = task.status
            task.status = value
            if value == "completed":
                if task.completed_at is None:
                    task.completed_at = datetime.utcnow()
            elif old_status == "completed" and value != "completed":
                # Task was completed but is now changing to a different status
                task.completed_at = None
        else:
            setattr(task, key, value)

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return format_success_response(
        data=task.dict(),
        message=f"Task {task_id} updated successfully"
    )


@router.patch("/{user_id}/tasks/{task_id}/complete")
async def toggle_task_completion(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific task by ID for the specified user.

    Args:
        user_id: The ID of the user whose task to update
        task_id: The ID of the task to toggle completion status
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with the updated task with toggled completion status
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to update tasks for this user"
        )

    # Convert task_id string to UUID object
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_TASK_ID",
            message="Invalid task ID format"
        )

    # Get the existing task
    statement = select(Todo).where(Todo.id == task_uuid)
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        return format_error_response(
            error_code="TASK_NOT_FOUND",
            message="Task not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to update this task"
        )

    # Toggle the completion status by changing the status field
    if task.status == "completed":
        task.status = "pending"
        task.completed_at = None
    else:
        task.status = "completed"
        task.completed_at = datetime.utcnow()

    task.updated_at = datetime.utcnow()

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return format_success_response(
        data=task.dict(),
        message=f"Task {task_id} completion status updated successfully"
    )


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task by ID for the specified user.

    Args:
        user_id: The ID of the user whose task to delete
        task_id: The ID of the task to delete
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with success message
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to delete tasks for this user"
        )

    # Convert task_id string to UUID object
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_TASK_ID",
            message="Invalid task ID format"
        )

    # Get the existing task
    statement = select(Todo).where(Todo.id == task_uuid)
    result = await db.execute(statement)
    task = result.scalar_one_or_none()

    if not task:
        return format_error_response(
            error_code="TASK_NOT_FOUND",
            message="Task not found"
        )

    # Check if the task belongs to the current user
    if task.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            message="Not authorized to delete this task"
        )

    # Delete the task
    await db.delete(task)
    await db.commit()

    return format_success_response(
        data=None,
        message=f"Task {task_id} deleted successfully"
    )