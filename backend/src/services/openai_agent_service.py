import os
import sys
import asyncio
import json
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

import sys
import os

# Path manipulation to access backend root level packages from src
backend_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Try importing from legacy crud directory first, fallback to src models
try:
    from crud.conversation_crud import get_conversation as get_conversation_legacy, create_conversation as create_conversation_legacy
except ImportError:
    # Fallback implementation if legacy files are not available
    def get_conversation_legacy(session, thread_id):
        return None

    def create_conversation_legacy(session, conversation):
        return conversation
from ..core.config import settings
from ..models.conversation import Conversation  # Use src model instead

# We'll need to convert the async session for the legacy sync CRUD functions
from sqlmodel import Session
from ..core.database import sync_engine  # Fixed import name

class OpenAIAgentService:
    def __init__(self):
        self.api_key = getattr(settings, "GROQ_API_KEY", None) or getattr(settings, "OPENAI_API_KEY", None)
        self.base_url = "https://api.groq.com/openai/v1" if getattr(settings, "GROQ_API_KEY", None) else None
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = None
        self.assistant = None
        self.mcp_base_url = "http://127.0.0.1:3000"

    async def initialize_assistant(self):
        if not self.client:
            return
        if not self.assistant:
            self.assistant = "Initialized"
            print("Assistant initialized successfully.")

    async def _call_mcp_tool(self, method: str, params: Dict, user_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                headers = {"Authorization": f"Bearer {user_id}", "user_id": str(user_id)}
                response = await client.post(
                    f"{self.mcp_base_url}/tools/{method}", 
                    json={"params": params, "context": headers},
                    timeout=30.0
                )
                return response.json()
            except Exception as e:
                return {"error": f"MCP Connection Failed: {str(e)}"}

    async def process_message(self, message: str, user_id: str, conversation_id: str, db_session: AsyncSession) -> str:
        if not self.client:
            return "AI service not configured."
        
        try:
            # 1. Load History - For now we'll skip loading full history and just start with system prompt
            # In a complete implementation, we'd fetch conversation history from Message model
            messages = []

            # Phase III: Improved NLU System Prompt
            messages.append({
                "role": "system",
                "content": "You are a helpful Task Manager Assistant. You can add, list, delete, and update tasks for the user. When a user gives a command like 'delete task 5', use the 'delete_task' tool with the correct task ID. Use the 'user_id' provided for all task operations."
            })

            # For now, we'll skip loading historical messages since the src models don't have the same structure as legacy ones
            # Eventually, we should fetch from Message model based on conversation_id
            # Skip loading historical messages for now since src models don't have this structure
            # if history and history.messages:
            #     messages.extend(json.loads(history.messages))
            
            messages.append({"role": "user", "content": message})
            
            # 2. Define Tools (Function Calling)
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "add_task",
                        "description": "Add a new task",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "description": {"type": "string"},
                                "user_id": {"type": "string"}
                            },
                            "required": ["title", "user_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "list_tasks",
                        "description": "List tasks for the user",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string"},
                                "status": {"type": "string", "description": "pending or completed"}
                            },
                            "required": ["user_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "delete_task",
                        "description": "Delete a task by ID",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "integer"}
                            },
                            "required": ["task_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_task",
                        "description": "Update task details",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "integer"},
                                "title": {"type": "string"},
                                "description": {"type": "string"}
                            },
                            "required": ["task_id"]
                        }
                    }
                }
            ]
            
            model_name = "llama3-70b-8192" if self.base_url else "gpt-4-turbo"
            
            # 3. Request AI response with tool calling
            response = await self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            messages.append(response_message)
            
            # 4. Handle Tool Calls
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    if function_name == "add_task":
                        function_response = await self._add_task(function_args, user_id, db_session)
                    elif function_name == "list_tasks":
                        function_response = await self._list_tasks(function_args, user_id, db_session)
                    elif function_name == "delete_task":
                        function_response = await self._delete_task(function_args, user_id, db_session)
                    elif function_name == "update_task":
                        function_response = await self._update_task(function_args, user_id, db_session)
                    else:
                        function_response = "Error: Tool not found."
                        
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })
                
                # Second call for natural language summary
                second_response = await self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                )
                ai_response = second_response.choices[0].message.content
                messages.append({"role": "assistant", "content": ai_response})
            else:
                ai_response = response_message.content
                messages.append({"role": "assistant", "content": ai_response})
            
            # 5. Persist Conversation History - Since we're using src models now, we need a different approach
            # The src.models.conversation doesn't have a messages field, so we'll store messages separately in Message model
            # For now, let's create a simple conversation if it doesn't exist
            # In a proper implementation, we'd want to store the full conversation history
            pass  # The messages are already stored individually in the chat API, so we don't need to duplicate here

            await db_session.commit()
            return ai_response

        except Exception as e:
            return f"Error: {str(e)}"

    async def _add_task(self, args: Dict, user_id: str, db_session: AsyncSession) -> str:
        result = await self._call_mcp_tool("add_task", args, user_id)
        return f"MCP Action: Task created with ID {result.get('id')}" if "id" in result else str(result)

    async def _list_tasks(self, args: Dict, user_id: str, db_session: AsyncSession) -> str:
        result = await self._call_mcp_tool("list_tasks", args, user_id)
        if "tasks" in result:
            tasks = [f"- {t['title']} (ID: {t['id']}, Status: {t['status']})" for t in result["tasks"]]
            return "Your tasks:\n" + "\n".join(tasks)
        return "No tasks found."

    async def _update_task(self, args: Dict, user_id: str, db_session: AsyncSession) -> str:
        result = await self._call_mcp_tool("update_task", args, user_id)
        return f"MCP Action: Task {args.get('task_id')} updated."

    async def _delete_task(self, args: Dict, user_id: str, db_session: AsyncSession) -> str:
        result = await self._call_mcp_tool("delete_task", args, user_id)
        return f"MCP Action: {result.get('message', 'Task deleted')}"

openai_agent_service = OpenAIAgentService()