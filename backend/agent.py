import os
from openai import OpenAI # Groq is compatible with OpenAI SDK
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq Client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

async def run_todo_agent(user_input: str, user_id: str):
    """
    Groq Agent that uses MCP Server tools to manage tasks.
    """
    print(f"🤖 Agent is thinking... User: {user_id}, Message: {user_input}")

    # 1. Define the system prompt and tools for the AI
    messages = [
        {"role": "system", "content": "You are a helpful Task Manager Assistant. You can add, list, delete, and update tasks for the user. Use the provided tools to interact with the database."},
        {"role": "user", "content": user_input}
    ]

    # 2. Define the tools that the agent can use (Function calling)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task to the todo list for a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The title of the task"},
                        "description": {"type": "string", "description": "Optional description of the task"},
                        "user_id": {"type": "string", "description": "The ID of the user"}
                    },
                    "required": ["title", "user_id"]
                }
            }
        },
        # UPDATED TOOL: Added status parameter
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List tasks for a specific user, optionally filtered by status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user"},
                        "status": {"type": "string", "description": "Filter by status: 'pending' or 'completed'"}
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task by its ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task's title or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "New title of the task"},
                        "description": {"type": "string", "description": "New description of the task"}
                    },
                    "required": ["task_id"]
                }
            }
        }
    ]

    # 3. Call the Groq API with tools
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    return response.choices[0].message.content