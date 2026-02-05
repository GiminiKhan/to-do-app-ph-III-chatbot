"""Projects API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid

from ..models.project import Project, ProjectBase
from ..models.user import User
from .deps import get_current_user
from ..core.database import get_async_session
from .responses import format_success_response, format_error_response, format_collection_response

router = APIRouter(prefix="/api", tags=["projects"])


@router.get("/{user_id}/projects")
async def get_projects(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Get all projects for the specified user.

    Args:
        user_id: The ID of the user whose projects to retrieve
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with list of projects for the specified user
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to access projects for this user"
        )

    # Query projects for the current user only
    statement = select(Project).where(Project.user_id == current_user.id)
    result = await db.execute(statement)
    projects = result.all()

    return format_collection_response(
        data=[project.dict() for project in projects],
        message=f"Retrieved {len(projects)} projects for user {user_id}",
        total=len(projects)
    )


@router.post("/{user_id}/projects")
async def create_project(
    user_id: str,
    project_data: ProjectBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Create a new project for the specified user.

    Args:
        user_id: The ID of the user for whom to create the project
        project_data: Project data from request body
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with the created project
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to create projects for this user"
        )

    # Create new project with the current user's ID
    project = Project(**project_data.dict(), user_id=current_user.id)

    db.add(project)
    await db.commit()
    await db.refresh(project)

    return format_success_response(
        data=project.dict(),
        message="Project created successfully"
    )


@router.get("/{user_id}/projects/{project_id}")
async def get_project(
    user_id: str,
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific project by ID for the specified user.

    Args:
        user_id: The ID of the user whose project to retrieve
        project_id: The ID of the project to retrieve
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with the requested project
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to access projects for this user"
        )

    # Convert project_id string to UUID object
    try:
        project_uuid = uuid.UUID(project_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_PROJECT_ID",
            error_message="Invalid project ID format"
        )

    # Get the project by ID
    statement = select(Project).where(Project.id == project_uuid)
    result = await db.execute(statement)
    project = result.first()

    if not project:
        return format_error_response(
            error_code="PROJECT_NOT_FOUND",
            error_message="Project not found"
        )

    # Check if the project belongs to the current user
    if project.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to access this project"
        )

    return format_success_response(
        data=project.dict(),
        message=f"Retrieved project {project_id}"
    )


@router.put("/{user_id}/projects/{project_id}")
async def update_project_put(
    user_id: str,
    project_id: str,
    project_update: ProjectBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific project by ID for the specified user using PUT method.

    Args:
        user_id: The ID of the user whose project to update
        project_id: The ID of the project to update
        project_update: Updated project data from request body
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with the updated project
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to update projects for this user"
        )

    # Convert project_id string to UUID object
    try:
        project_uuid = uuid.UUID(project_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_PROJECT_ID",
            error_message="Invalid project ID format"
        )

    # Get the existing project
    statement = select(Project).where(Project.id == project_uuid)
    result = await db.execute(statement)
    project = result.first()

    if not project:
        return format_error_response(
            error_code="PROJECT_NOT_FOUND",
            error_message="Project not found"
        )

    # Check if the project belongs to the current user
    if project.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to update this project"
        )

    # Update the project with the new data
    for key, value in project_update.dict().items():  # Use dict() instead of exclude_unset=True for PUT
        setattr(project, key, value)
    project.updated_at = datetime.utcnow()  # Update timestamp

    db.add(project)
    await db.commit()
    await db.refresh(project)

    return format_success_response(
        data=project.dict(),
        message=f"Project {project_id} updated successfully"
    )


@router.patch("/{user_id}/projects/{project_id}")
async def update_project(
    user_id: str,
    project_id: str,
    project_update: ProjectBase,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific project by ID for the specified user using PATCH method.

    Args:
        user_id: The ID of the user whose project to update
        project_id: The ID of the project to update
        project_update: Updated project data from request body
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with the updated project
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to update projects for this user"
        )

    # Convert project_id string to UUID object
    try:
        project_uuid = uuid.UUID(project_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_PROJECT_ID",
            error_message="Invalid project ID format"
        )

    # Get the existing project
    statement = select(Project).where(Project.id == project_uuid)
    result = await db.execute(statement)
    project = result.first()

    if not project:
        return format_error_response(
            error_code="PROJECT_NOT_FOUND",
            error_message="Project not found"
        )

    # Check if the project belongs to the current user
    if project.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to update this project"
        )

    # Update the project with the new data
    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(project, key, value)

    db.add(project)
    await db.commit()
    await db.refresh(project)

    return format_success_response(
        data=project.dict(),
        message=f"Project {project_id} updated successfully"
    )


@router.delete("/{user_id}/projects/{project_id}")
async def delete_project(
    user_id: str,
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific project by ID for the specified user.

    Args:
        user_id: The ID of the user whose project to delete
        project_id: The ID of the project to delete
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with success message
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to delete projects for this user"
        )

    # Convert project_id string to UUID object
    try:
        project_uuid = uuid.UUID(project_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_PROJECT_ID",
            error_message="Invalid project ID format"
        )

    # Get the existing project
    statement = select(Project).where(Project.id == project_uuid)
    result = await db.execute(statement)
    project = result.first()

    if not project:
        return format_error_response(
            error_code="PROJECT_NOT_FOUND",
            error_message="Project not found"
        )

    # Check if the project belongs to the current user
    if project.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to delete this project"
        )

    # Delete the project
    await db.delete(project)
    await db.commit()

    return format_success_response(
        data=None,
        message=f"Project {project_id} deleted successfully"
    )


@router.get("/{user_id}/projects/{project_id}/tasks")
async def get_tasks_by_project(
    user_id: str,
    project_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for a specific project.

    Args:
        user_id: The ID of the user whose project tasks to retrieve
        project_id: The ID of the project whose tasks to retrieve
        current_user: The current authenticated user
        db: Database session

    Returns:
        Standardized response with list of tasks for the specified project
    """
    # Validate that the requested user_id matches the authenticated user's ID
    if user_id != str(current_user.id):
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to access tasks for this user"
        )

    # Convert project_id string to UUID object
    try:
        project_uuid = uuid.UUID(project_id)
    except ValueError:
        return format_error_response(
            error_code="INVALID_PROJECT_ID",
            error_message="Invalid project ID format"
        )

    # Get the project by ID to verify it exists and belongs to the user
    statement = select(Project).where(Project.id == project_uuid)
    result = await db.execute(statement)
    project = result.first()

    if not project:
        return format_error_response(
            error_code="PROJECT_NOT_FOUND",
            error_message="Project not found"
        )

    # Check if the project belongs to the current user
    if project.user_id != current_user.id:
        return format_error_response(
            error_code="PERMISSION_DENIED",
            error_message="Not authorized to access this project"
        )

    # Get tasks for the specified project
    from ..models.todo import Todo
    statement = select(Todo).where(Todo.project_id == project_uuid)
    result = await db.execute(statement)
    tasks = result.all()

    return format_collection_response(
        data=[task.dict() for task in tasks],
        message=f"Retrieved {len(tasks)} tasks for project {project_id}",
        total=len(tasks)
    )