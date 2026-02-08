# Quickstart: MCP Server and AI Agent Integration for Taskify Phase III

## Overview
This quickstart guide provides a rapid introduction to setting up and running the MCP server and AI agent integration for Taskify Phase III. It covers the essential steps to get the system operational.

## Version Information
- **Quickstart Version**: 1.0.0
- **Constitution Compliance**: v3.0.0 (AI-Native Evolution)
- **Date Created**: 2026-02-07
- **Author**: Spec-Kit Plus

## Prerequisites

### System Requirements
- Python 3.13+ installed
- Node.js 18+ for frontend (if developing frontend)
- Access to Neon PostgreSQL database
- OpenAI API key
- MCP SDK compatible environment

### Environment Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd to-do-app-chatbot
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Update the following values in `.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=your_neon_postgres_connection_string
   MCP_SERVER_PORT=8001
   ```

## Installation Steps

### Step 1: Install MCP SDK
```bash
pip install mcp-sdk  # Or whatever the official MCP SDK package is called
```

### Step 2: Set up Database Models
```bash
# Run database migrations to create required tables
python -m backend.database.migrate
```

### Step 3: Initialize MCP Server
```bash
# Start the MCP server
python -m backend.mcp_server.server
```

### Step 4: Configure OpenAI Assistant
```bash
# Register tools with OpenAI Assistant
python -m backend.ai.assistant_config
```

## Running the System

### Starting Services
1. Start the MCP server:
   ```bash
   python -m backend.mcp_server.server
   ```

2. Start the main application:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

3. If developing frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Verifying Installation
1. Check MCP server health:
   ```bash
   curl http://localhost:8001/health
   ```

2. Verify database connectivity:
   ```bash
   python -c "from backend.database.connection import get_db; print('DB connected')"
   ```

3. Test tool availability:
   ```bash
   # This should list all registered MCP tools
   curl http://localhost:8001/tools
   ```

## Basic Usage

### Interacting with the AI Agent
1. Access the frontend chat interface (usually at http://localhost:3000)
2. Authenticate using your account
3. Start a conversation with the AI assistant
4. Request task operations like:
   - "Add a task to buy groceries"
   - "Show me my pending tasks"
   - "Complete the task with ID 123"

### Using MCP Tools Directly
The MCP server exposes tools that can be called directly:

```bash
# Example curl command to call add_task tool
curl -X POST http://localhost:8001/tools/add_task \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test task",
    "description": "This is a test task",
    "priority": "medium"
  }'
```

## Sample API Calls

### Adding a Task
```python
import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create a thread
thread = client.beta.threads.create()

# Add a message to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Please create a task titled 'Sample Task' with high priority."
)

# Run the assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id="your-assistant-id",
)

# Wait for completion and get response
while run.status in ['queued', 'in_progress']:
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    time.sleep(1)

messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

### Listing Tasks
```bash
# This would be processed through the AI agent
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Show me all my pending tasks"
  }'
```

## Troubleshooting

### Common Issues

#### MCP Server Won't Start
- Verify MCP SDK is properly installed
- Check that required ports are available
- Ensure all configuration variables are set

#### AI Agent Not Responding
- Confirm OpenAI API key is valid and has sufficient quota
- Check that assistant is properly configured with tools
- Verify database connectivity

#### Database Connection Issues
- Confirm DATABASE_URL is properly formatted
- Check that Neon PostgreSQL is accessible
- Verify required tables exist

### Debugging Commands
```bash
# Check environment variables
python -c "import os; print(os.getenv('DATABASE_URL'))"

# Verify OpenAI connection
python -c "import openai; openai.api_key = os.getenv('OPENAI_API_KEY'); print(openai.Model.list())"

# Check database connection
python -c "from backend.database.connection import engine; engine.connect(); print('Connected')"
```

## Next Steps

1. **Customize the AI Assistant**: Modify the assistant instructions in `backend/ai/assistant_config.py` to match your specific use case

2. **Extend Tool Functionality**: Add additional tools by creating new files in `backend/mcp_server/tools/`

3. **Enhance Frontend**: Customize the OpenAI ChatKit integration in the frontend components

4. **Add Authentication**: Implement proper user authentication and authorization

5. **Configure Production Settings**: Update configuration for production deployment

## Development Workflow

### Making Changes to MCP Tools
1. Modify the tool implementation in `backend/mcp_server/tools/`
2. Update the tool schema if parameters change
3. Restart the MCP server to reload tools
4. Reconfigure the OpenAI Assistant if schema changed

### Testing Changes
```bash
# Run unit tests for MCP tools
pytest tests/unit/test_mcp_tools.py

# Run integration tests for AI interactions
pytest tests/integration/test_ai_integration.py

# Run end-to-end tests
pytest tests/e2e/test_mcp_ai_integration.py
```

## Cleanup and Legacy Files

### Identifying Phase I Files (Console App)
Look for files related to console application:
- `console_app.py` or similar entry points
- Terminal-based UI modules
- In-memory storage implementations

### Identifying Phase II Files (Basic Web App)
Look for files related to basic web implementation:
- Traditional REST API endpoints for tasks
- Stateful session management
- Non-AI-based task management UI

These files should be evaluated for removal or deprecation as they contradict the new AI-native architecture.