# Implementation Plan: Phase 4 To-Do Management

**Branch**: `phase2-web` | **Date**: 2026-02-01 | **Spec**: [specs/phase2-web/spec.md](../specs/phase2-web/spec.md)

**Note**: This plan details the implementation of To-Do Management functionality using the new /api/{user_id}/tasks endpoints and shared database schema.

## Summary

Implementation of full CRUD operations for to-do items using the standardized /api/{user_id}/tasks endpoints. The system will enforce user isolation through URL-based user_id validation, ensuring users can only access their own tasks. The implementation leverages the shared database schema with proper foreign key relationships to user accounts and project associations.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, Better Auth, Neon PostgreSQL
**Storage**: Neon PostgreSQL with async SQLAlchemy
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Cloud deployment with containerized backend
**Project Type**: web
**Performance Goals**: <500ms response time for simple operations, support 10,000+ tasks per user
**Constraints**: User isolation enforced, proper authentication and authorization, <2s page load times
**Scale/Scope**: Support thousands of users with multiple tasks each

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development (SDD)
- [X] All features and changes must be specified before implementation begins
- [X] Clear requirements and acceptance criteria must be documented in spec.md

### No Manual Code
- [X] All code must be generated through Claude Code or integrated agents
- [X] No manual code writing is permitted
- [X] Implementation must follow automated generation processes

### Agentic Stack
- [X] Technology stack utilizes UV, Python 3.13+, and Claude Code as required components
- [X] Agentic approach ensures automation and consistency across development lifecycle

### Clean Architecture
- [X] Codebase maintains modular and clean architecture principles using Cloud-Native Architecture (FastAPI + Neon PostgreSQL)
- [X] Architecture ensures maintainability, testability, scalability, and robust data persistence

### Process Integrity
- [X] Every code change references a Task ID before implementation
- [X] Traceability and accountability maintained throughout development process

### Security Protocol
- [X] Better Auth with JWT implemented as mandatory security protocol for all authentication and authorization flows
- [X] Secure user access, token management, and protection of sensitive data across all application layers

### Frontend Standard
- [X] Next.js 15+ App Router used as the standard for all frontend development
- [X] Modern React development practices, server-side rendering capabilities, and optimized performance ensured

### UI/UX Standards
- [X] Modern & Attractive UI implemented using Tailwind CSS with Indigo/Slate theme
- [X] Consistent visual identity, responsive design, accessibility compliance, and enhanced user experience maintained

## Project Structure

### Documentation (this feature)

```text
specs/phase2-web/
├── todo_management_plan.md  # This file
├── research.md              # Research findings
├── data-model.md            # Data model definitions
├── quickstart.md            # Quickstart guide
├── contracts/               # API contracts
└── database_schema.md       # Shared database schema
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py              # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── todos.py         # To-do endpoints using /api/{user_id}/tasks
│   │   ├── projects.py      # Project endpoints using /api/{user_id}/projects
│   │   ├── deps.py          # Dependency injection
│   │   └── responses.py     # Standardized response formatting
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   ├── todo.py          # To-do model with user_id foreign key
│   │   └── project.py       # Project model with user_id foreign key
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # User schemas
│   │   ├── todo.py          # To-do schemas
│   │   └── project.py       # Project schemas
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database connection
│   │   ├── exceptions.py    # Custom exceptions
│   │   └── security.py      # Security utilities
│   └── tests/
│       ├── conftest.py
│       ├── test_todos.py    # To-do API tests
│       ├── test_projects.py # Project API tests
│       └── test_auth.py     # Authentication tests
```

**Structure Decision**: Selected Option 2: Web application with separate backend and frontend directories. The backend implements the required CRUD operations for to-do management using the standardized API endpoints with user_id validation from URL parameters.

## Phase 0: Research & Unknown Resolution

### Research Findings

**Decision**: Use /api/{user_id}/tasks endpoints with user_id validation
**Rationale**: Enforces user isolation by validating that the user_id in the URL matches the authenticated user's ID, preventing unauthorized access to other users' tasks.

**Decision**: Implement standardized response format
**Rationale**: Ensures consistency across all API endpoints with proper success/error handling and metadata.

**Decision**: Use SQLModel with async support
**Rationale**: Provides type safety, integrates well with FastAPI, and supports async database operations for better performance.

## Phase 1: Data Model & Contracts

### Data Model (from shared schema)

**To-Dos Table**:
- id (UUID, primary key)
- user_id (UUID, foreign key to better_auth_users.id) - ensures user isolation
- project_id (UUID, foreign key to projects)
- title (VARCHAR, not null)
- description (TEXT)
- status (ENUM: 'pending', 'in_progress', 'completed', default 'pending')
- priority (ENUM: 'low', 'medium', 'high', 'urgent', default 'medium')
- due_date (TIMESTAMP)
- completed_at (TIMESTAMP)
- created_at (TIMESTAMP, default now)
- updated_at (TIMESTAMP, default now)

### API Contracts

**To-Do Management Endpoints**:
- GET /api/{user_id}/tasks - Retrieve all tasks for the specified user
- POST /api/{user_id}/tasks - Create a new task for the specified user
- GET /api/{user_id}/tasks/{task_id} - Retrieve a specific task for the specified user
- PUT /api/{user_id}/tasks/{task_id} - Update a specific task for the specified user
- PATCH /api/{user_id}/tasks/{task_id} - Partially update a specific task for the specified user
- PATCH /api/{user_id}/tasks/{task_id}/complete - Toggle completion status for a specific task
- DELETE /api/{user_id}/tasks/{task_id} - Delete a specific task for the specified user

### Security Implementation

Each endpoint validates that the user_id in the URL matches the authenticated user's ID to ensure proper user isolation and prevent unauthorized access to other users' tasks.

## Implementation Approach

1. **Backend Implementation**:
   - Enhance existing todos.py endpoints to validate user_id from URL against authenticated user
   - Implement proper error handling and response formatting
   - Add validation for all CRUD operations
   - Ensure all database queries filter by user_id for security

2. **Frontend Integration**:
   - Update API client to use new endpoint format
   - Implement user-specific task management UI
   - Add proper error handling and loading states

3. **Testing**:
   - Unit tests for all CRUD operations
   - Integration tests for user isolation validation
   - End-to-end tests for complete user workflows