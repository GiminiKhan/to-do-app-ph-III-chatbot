# Quickstart Guide: Phase 4 To-Do Management

## Overview
This guide provides setup and development instructions for the To-Do Management feature with user-isolated CRUD operations using /api/{user_id}/tasks endpoints.

## Prerequisites

### System Requirements
- Python 3.13+
- Node.js 18+ (for frontend development)
- PostgreSQL-compatible database (Neon PostgreSQL recommended)
- Git
- pip (Python package manager)

### Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd to-do-app

# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_app
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Database Setup

### Initial Migration
```bash
# Run database migrations
alembic upgrade head
```

### Sample Data (Optional)
```bash
# Create initial admin user and sample tasks
python -m src.core.init_db
```

## Running the Application

### Backend (Development)
```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Start the development server
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend (Development)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### To-Do Management
All endpoints require authentication via JWT token in the Authorization header.

**Headers required**:
```
Authorization: Bearer <jwt-token>
```

#### Get All Tasks for User
```
GET /api/{user_id}/tasks
```
Parameters:
- `user_id`: UUID of the authenticated user (must match JWT token)
- Query params: `status`, `priority`, `project_id`, `limit`, `offset`

#### Create New Task
```
POST /api/{user_id}/tasks
```
Path Parameters:
- `user_id`: UUID of the authenticated user

Body:
```json
{
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "due_date": "2023-12-31T10:00:00Z"
}
```

#### Get Specific Task
```
GET /api/{user_id}/tasks/{task_id}
```
Path Parameters:
- `user_id`: UUID of the authenticated user
- `task_id`: UUID of the task to retrieve

#### Update Task
```
PUT /api/{user_id}/tasks/{task_id}
```
Path Parameters:
- `user_id`: UUID of the authenticated user
- `task_id`: UUID of the task to update

Body:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2023-12-31T10:00:00Z"
}
```

#### Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{task_id}/complete
```
Path Parameters:
- `user_id`: UUID of the authenticated user
- `task_id`: UUID of the task to update

#### Delete Task
```
DELETE /api/{user_id}/tasks/{task_id}
```
Path Parameters:
- `user_id`: UUID of the authenticated user
- `task_id`: UUID of the task to delete

## Authentication Flow

1. Register user via Better Auth
2. Login to obtain JWT token
3. Include JWT token in Authorization header for all requests
4. Token is validated against user_id in URL path

## Testing

### Backend Tests
```bash
# Run all backend tests
pytest

# Run tests with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_todos.py
```

### Frontend Tests
```bash
# Run all frontend tests
npm test

# Run tests in watch mode
npm run test:watch
```

## Development Workflow

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Update data models in `src/models/`
3. Create API endpoints in `src/api/`
4. Write tests in `tests/`
5. Update documentation
6. Submit pull request

### API Contract Testing
All endpoints follow the standardized response format:
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful",
  "timestamp": "2023-12-01T10:00:00Z"
}
```

Error responses:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  },
  "timestamp": "2023-12-01T10:00:00Z"
}
```

## Deployment

### Production Build
```bash
# Backend (containerized)
docker build -t todo-backend .
docker run -p 8000:8000 todo-backend

# Frontend build
cd frontend
npm run build
```

### Environment Configuration
Production environment variables:
```env
DATABASE_URL=postgresql+asyncpg://production-db-url
SECRET_KEY=production-secret-key
DEBUG=false
LOG_LEVEL=INFO
```

## Troubleshooting

### Common Issues
- **403 Forbidden**: Check that user_id in URL matches authenticated user ID
- **404 Not Found**: Verify task exists and belongs to the authenticated user
- **500 Internal Server Error**: Check server logs for detailed error information

### Debugging Tips
- Enable debug mode by setting `DEBUG=true` in environment
- Check database connectivity with `alembic current`
- Verify JWT token validity and expiration
- Ensure user_id in URL matches the authenticated user's ID

## API Documentation
Auto-generated OpenAPI documentation available at:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)
- `http://localhost:8000/openapi.json` (OpenAPI JSON)