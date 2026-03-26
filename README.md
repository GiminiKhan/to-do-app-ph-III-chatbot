# Taskify Phase III - AI-Powered Task Management

Welcome to Taskify Phase III! This is an AI-native task management application that integrates OpenAI Agents with MCP (Model Context Protocol) for intelligent task management through natural language. Features secure authentication, CRUD operations, real-time search, priority filtering, and AI-powered task management.

## 🚀 Features

- **AI-Powered Task Management**: Use natural language to create, update, complete, and delete tasks
- **MCP Server Integration**: Official MCP SDK implementation for tool exposure
- **OpenAI Agents**: Uses OpenAI's latest assistant capabilities
- **Real-time Chat Interface**: Conversational UI for task management
- **Authentication System**: Secure user registration and login with JWT tokens
- **CRUD Operations**: Create, Read, Update, and Delete tasks with full functionality
- **Real-time Search**: Instant search functionality to filter tasks by title
- **Priority Filtering**: Filter tasks by priority level (High, Medium, Low, or All)
- **Responsive UI**: Modern, clean interface built with Tailwind CSS
- **Task Management**: Complete task lifecycle with completion toggling
- **Edit Functionality**: Update task details without leaving the dashboard

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (via Neon)
- **Authentication**: JWT-based authentication
- **ORM**: SQLModel for database modeling
- **AI Integration**: OpenAI Agents SDK, MCP Server
- **Dependencies**: Managed with `uv` and `pyproject.toml`

### Frontend
- **Framework**: Next.js 15+ with TypeScript
- **Styling**: Tailwind CSS with Indigo & Slate theme
- **Icons**: Lucide React
- **AI UI**: OpenAI ChatKit integration
- **Architecture**: Client-side rendering with React hooks

### AI & Tools
- **OpenAI Agents**: For natural language task management
- **MCP SDK**: Model Context Protocol server for tool exposure
- **State Management**: Conversation history with message persistence

## 📁 Project Structure

```
├── backend/                 # FastAPI backend
│   ├── api/                # API routes and endpoints
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── todos.py        # Task management endpoints
│   │   ├── chat.py         # Chat endpoints (NEW - Phase III)
│   │   └── mcp_server.py   # MCP server implementation (NEW - Phase III)
│   ├── models/             # Database models (SQLModel)
│   │   ├── user.py         # User model
│   │   ├── todo.py         # Task model
│   │   └── message.py      # Message model for chat history (NEW - Phase III)
│   ├── services/           # Business logic
│   │   ├── auth_service.py # Authentication service
│   │   └── openai_agent_service.py # OpenAI agent service (NEW - Phase III)
│   ├── database/           # Database connection and configuration
│   ├── core/               # Core utilities and security
│   └── main.py             # Application entry point
├── frontend/              # Next.js frontend
│   ├── app/               # Next.js 13+ app router
│   │   ├── chat/          # AI assistant chat page (NEW - Phase III)
│   │   ├── dashboard/     # Dashboard page with task management
│   │   ├── login/         # Login page
│   │   ├── register/      # Registration page
│   │   ├── globals.css    # Global styles
│   │   └── layout.tsx     # Root layout
│   ├── components/        # Reusable UI components
│   │   └── layouts/
│   │       └── sidebar.tsx # Updated with AI Assistant link (Phase III)
│   ├── services/          # API clients and utilities
│   └── public/            # Static assets
├── specs/                 # Specification files
├── history/               # Prompt history records
├── start_backend.py       # Backend startup script (NEW - Phase III)
├── start_mcp_server.py    # MCP server startup script (NEW - Phase III)
├── requirements.txt       # Updated with MCP SDK and OpenAI (Phase III)
├── CLAUDE.md             # Claude Code configuration
└── README.md             # This file
```

## 🏗️ Setup Instructions

### Prerequisites
- Node.js (v18 or higher)
- Python 3.11+
- PostgreSQL database (or Neon account)
- OpenAI API key
- `uv` package manager (recommended) or `pip`

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials and secret keys
```

4. Run database migrations:
```bash
# If using alembic for migrations
alembic upgrade head
```

5. Start the backend server:
```bash
uv run main.py
# Or
python main.py
```

The backend will start on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your backend API URL
```

4. Start the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

The frontend will start on `http://localhost:3000`

## 🚀 Running the Application

### Development
1. Start the backend server in the root directory:
```bash
python start_backend.py
```

2. In a separate terminal, start the MCP server:
```bash
python start_mcp_server.py
```

3. In another terminal, start the frontend in the `frontend/` directory:
```bash
cd frontend && npm run dev
```

4. Open your browser to `http://localhost:3000`

### Phase III AI Features
The application includes several AI-powered features from Phase III:
- **AI Assistant**: Navigate to the "AI Assistant" tab in the sidebar to chat with the AI
- **Natural Language Processing**: Create tasks using natural language like "Create a task to buy groceries"
- **MCP Integration**: The system uses Model Context Protocol for tool exposure
- **Conversation History**: Chat history is preserved and accessible

## 🤖 Using the AI Assistant

Once the application is running:

1. Register and login to the application
2. Navigate to the "AI Assistant" tab in the sidebar
3. Start chatting with the AI assistant using natural language:
   - "Create a task to buy groceries"
   - "Show me my high priority tasks"
   - "Complete the task with ID 123"
   - "Update my task 'Learn Python' to high priority"

### Production
1. Build the frontend:
```bash
cd frontend && npm run build
```

2. Serve the backend with a production ASGI server like Uvicorn:
```bash
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🌐 API Endpoints

The backend provides the following REST API endpoints:

### Task Management
- `GET /api/{user_id}/tasks` - Get all user tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### AI Chat & MCP
- `POST /api/{user_id}/chat` - Chat with AI assistant (Phase III)
- `GET /api/{user_id}/chat/{conversation_id}/history` - Get conversation history (Phase III)

### MCP Server
- MCP server runs on port 3000 and integrates with OpenAI Agents

## 🔐 Authentication

The application uses JWT-based authentication:
- Users must register and login to access the dashboard
- Authentication tokens are stored in localStorage
- Protected routes are guarded by authentication middleware

## 💡 Key Features Explained

### Phase III AI Features

#### AI-Powered Task Management
- Use natural language to create, update, complete, and delete tasks
- OpenAI Agents interpret user requests and execute appropriate actions
- MCP (Model Context Protocol) server exposes task management tools

#### MCP Server Integration
- Official MCP SDK implementation
- Complete tool set: add_task, list_tasks, complete_task, delete_task, update_task
- Proper authentication and user isolation
- Stateless architecture following 11-step flow

#### Conversation Management
- Message storage in database with proper user_id and conversation_id
- Conversation history accessible through API
- Proper integration with frontend chat interface

#### Real-time Search
- Search tasks by title as you type
- Results update instantly without page refresh
- Case-insensitive search functionality

#### Priority Filtering
- Filter tasks by priority level (High, Medium, Low, or All)
- Case-insensitive comparison between UI and database values
- Dynamic filtering updates the task list immediately

#### Task Management
- Create new tasks with title, description, and priority
- Update existing tasks with inline editing
- Mark tasks as complete/incomplete with one click
- Delete tasks with confirmation

## 🎯 Hackathon II Mission - Phase III Implementation

Taskify Phase III demonstrates the Nine Pillars of AI-Driven Development:

1. **Spec-Driven Development**: Complete specifications in `/specs/` directory with MCP and AI agent requirements
2. **Reusable Intelligence**: Agent skills and subagent development for task management
3. **Full-Stack Development**: Next.js frontend, FastAPI backend, SQLModel ORM, Neon Serverless Database
4. **AI Agent Development**: OpenAI Agents SDK integration with Official MCP SDK
5. **Cloud-Native Deployment**: Ready for deployment with Docker, Kubernetes
6. **Event-Driven Architecture**: MCP protocol enables event-based tool calls
7. **AIOps**: Claude Code integration for development automation
8. **Cloud-Native Blueprints**: Spec-Driven Deployment configurations
9. **AI-Native Architecture**: Natural language interface to traditional CRUD operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Issues

If you encounter any issues or bugs, please open an issue in the GitHub repository with detailed information about the problem and steps to reproduce it.