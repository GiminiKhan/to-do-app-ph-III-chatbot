import asyncio
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
import uuid
from ..models.todo import Todo, TodoBase
from ..core.database import get_async_session
from sqlmodel import select
logger = logging.getLogger(__name__)
# Initialize FastAPI for MCP HTTP Bridge
mcp_app = FastAPI(title="Taskify MCP HTTP Bridge")
class TaskParams(BaseModel):
    title: str
    description: str = ""
    priority: str = "medium"
    due_date: Optional[str] = None
@mcp_app.post("/tools/add_task")
async def add_task_tool(request: Request):
    data = await request.json()
    params = data.get("params", {})
    user_id = data.get("context", {}).get("user_id", "test-user")
    async for session in get_async_session():
        new_task = Todo(
            title=params.get("title"),
            description=params.get("description", ""),
            priority=params.get("priority", "medium"),
            user_id=uuid.UUID(user_id) if len(user_id) == 36 else uuid.uuid4()
        )
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return {"id": str(new_task.id), "status": "success", "title": new_task.title}
@mcp_app.post("/tools/list_tasks")
async def list_tasks_tool(request: Request):
    data = await request.json()
    # In real scenario, filter by user_id from context
    async for session in get_async_session():
        query = select(Todo)
        result = await session.execute(query)
        tasks = result.scalars().all()
        return {"tasks": [{"id": str(t.id), "title": t.title, "status": t.status} for t in tasks]}
@mcp_app.post("/tools/complete_task")
async def complete_task_tool(request: Request):
    data = await request.json()
    task_id = data.get("params", {}).get("task_id")
    async for session in get_async_session():
        query = select(Todo).where(Todo.id == uuid.UUID(task_id))
        result = await session.execute(query)
        task = result.scalar_one_or_none()
        if task:
            task.status = "completed"
            await session.commit()
            return {"status": "updated", "id": task_id}
        return {"error": "Task not found"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(mcp_app, host="127.0.0.1", port=3000)
