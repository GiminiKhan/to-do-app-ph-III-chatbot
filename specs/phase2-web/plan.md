# Phase II Web - Full-Stack Architecture Plan

## 1. Architecture Overview

### 1.1 High-Level Architecture
The application follows a modern full-stack architecture with a clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │    │    Backend       │    │    Database      │
│   (Next.js)     │◄──►│   (FastAPI)      │◄──►│  (Neon PG)       │
│                 │    │                  │    │                  │
│ - React UI      │    │ - API Services   │    │ - User Data      │
│ - State Mgmt    │    │ - Auth Service   │    │ - To-Do Items    │
│ - API Client    │    │ - Business Logic │    │ - Projects       │
└─────────────────┘    └──────────────────┘    └──────────────────┘
```

### 1.2 Deployment Architecture
- Frontend: Static hosting (Vercel, Netlify, or similar)
- Backend: Containerized API service (Docker)
- Database: Neon PostgreSQL serverless database

## 2. Technology Stack Decisions

### 2.1 Frontend Stack
- **Framework**: Next.js 15+ with App Router
  - Reason: Excellent SSR/SSG capabilities, built-in optimization, aligned with constitution requirement
- **Language**: TypeScript
  - Reason: Type safety, better developer experience
- **Styling**: Tailwind CSS with Indigo/Slate theme
  - Reason: Rapid UI development, utility-first approach, aligned with constitution requirement for modern attractive UI
- **State Management**: React Context + Custom Hooks
  - Reason: Lightweight, sufficient for application complexity

### 2.2 Backend Stack
- **Framework**: FastAPI
  - Reason: High performance, automatic OpenAPI docs, excellent Python typing support
- **Language**: Python 3.9+
  - Reason: Rich ecosystem, excellent for API development
- **Database ORM**: SQLAlchemy (async)
  - Reason: Mature ORM with async support, good PostgreSQL integration
- **Database**: Neon PostgreSQL
  - Reason: Serverless PostgreSQL with branching, scaling, and performance features

### 2.3 Authentication & Security
- **Authentication Method**: Better Auth (with JWT tokens)
  - Reason: Enhanced security features, built-in OAuth providers, easier maintenance
- **Password Hashing**: Better Auth's built-in security mechanisms
  - Reason: Industry-standard security with additional features like OAuth, email verification
- **API Protection**: Better Auth middleware
  - Reason: Secure token-based authentication with additional security features
- **OAuth Providers**: Google, GitHub, and other OAuth providers
  - Reason: Enhanced user experience with social logins

## 3. System Components

### 3.1 Frontend Components
```
src/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication pages (Better Auth managed)
│   │   ├── login/
│   │   ├── register/
│   │   ├── forgot-password/
│   │   └── oauth-callback/
│   ├── dashboard/         # Main dashboard
│   ├── todos/            # To-do related pages
│   ├── projects/         # Project management
│   ├── profile/          # User profile (integrates with Better Auth)
│   └── api/              # Next.js API routes
├── components/           # Reusable React components
│   ├── auth/            # Better Auth integration components
│   │   ├── login-button/
│   │   ├── register-form/
│   │   ├── oauth-providers/
│   │   └── user-menu/
│   ├── ui/              # Base UI components (buttons, inputs)
│   ├── forms/           # Form components
│   ├── layout/          # Layout components
│   └── todos/           # To-do specific components
├── lib/                 # Utility functions and API clients
│   ├── auth/            # Better Auth client utilities
│   └── api/             # API client for custom endpoints
├── hooks/               # Custom React hooks
│   ├── auth/            # Authentication state hooks
│   └── data/            # Data fetching hooks
├── types/               # TypeScript type definitions
└── styles/              # Global styles and Tailwind config
```

### 3.2 Backend Components
```
app/
├── main.py              # Application entry point
├── api/                 # API route definitions
│   ├── v1/             # API version 1
│   │   ├── auth.py     # Authentication endpoints (Better Auth integration)
│   │   ├── todos.py    # To-do endpoints
│   │   ├── projects.py # Project endpoints
│   │   └── users.py    # User endpoints (Better Auth integration)
├── models/              # SQLAlchemy models
│   ├── better_auth.py  # Better Auth models (managed by Better Auth)
│   ├── todo.py         # To-do model
│   └── project.py      # Project model
├── schemas/             # Pydantic schemas
│   ├── auth.py         # Authentication schemas (Better Auth integration)
│   ├── todo.py         # To-do schemas
│   └── user.py         # User schemas (Better Auth integration)
├── database/            # Database connection and session management
│   ├── base.py         # Base model
│   ├── session.py      # Database session
│   └── init_db.py      # Database initialization
├── core/                # Core utilities and configuration
│   ├── config.py       # Configuration settings
│   ├── security.py     # Security utilities (Better Auth integration)
│   └── deps.py         # Dependency injection
├── utils/               # Utility functions
│   ├── auth.py         # Authentication utilities (Better Auth integration)
│   └── validators.py   # Validation utilities
└── tests/               # Test files
```

## 4. Database Design

### 4.1 Entity Relationship Diagram
```
Better Auth Users (1) ─────── (N) To-Dos
        │                         │
        │                         │
        └── (1) Projects (N) ─────┘
              │
              └── (N) Sessions, Accounts, Verification
```

### 4.2 Table Specifications

The complete database schema is defined in the shared [database_schema.md](./database_schema.md) document to eliminate duplication between specification and plan documents.

#### Better Auth Managed Tables
Reference the shared schema document for detailed table definitions.

#### Application Tables
Reference the shared schema document for detailed table definitions including Projects and To-Dos tables.

### 4.3 Database Enumerations
```sql
CREATE TYPE todo_status_enum AS ENUM ('pending', 'in_progress', 'completed');
CREATE TYPE todo_priority_enum AS ENUM ('low', 'medium', 'high', 'urgent');
```

### 4.4 Database Indexing Strategy
The following indexes will be created to optimize query performance:

#### To-Dos Table Indexes:
- `idx_todos_user_id`: Index on user_id for efficient user-based queries (critical for user isolation)
- `idx_todos_project_id`: Index on project_id for efficient project-based queries
- `idx_todos_status`: Index on status for filtering by status
- `idx_todos_priority`: Index on priority for filtering by priority
- `idx_todos_due_date`: Index on due_date for deadline-based queries
- `idx_todos_created_at`: Index on created_at for chronological ordering
- `idx_todos_updated_at`: Index on updated_at for change tracking

#### Projects Table Indexes:
- `idx_projects_user_id`: Index on user_id for efficient user-based queries (critical for user isolation)
- `idx_projects_name`: Index on name for efficient name-based searches
- `idx_projects_created_at`: Index on created_at for chronological ordering

#### Composite Indexes (as needed):
- `idx_todos_user_status`: Composite index on (user_id, status) for common filtered queries
- `idx_todos_user_priority`: Composite index on (user_id, priority) for priority-based filtering

## 5. API Design

### 5.1 Authentication API
```
# Better Auth managed endpoints
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/session

# Additional custom endpoints
POST /api/auth/forgot-password
POST /api/auth/reset-password
GET  /api/auth/me - Get current user info (using Better Auth session)
POST /api/auth/oauth/:provider - OAuth provider login (Google, GitHub, etc.)
```

### 5.2 To-Do API
```
GET    /api/{user_id}/tasks
POST   /api/{user_id}/tasks
GET    /api/{user_id}/tasks/{id}
PUT    /api/{user_id}/tasks/{id}
PATCH  /api/{user_id}/tasks/{id}/complete
DELETE /api/{user_id}/tasks/{id}
GET    /api/{user_id}/tasks?status={status}&priority={priority}&project_id={project_id}
```

### 5.3 Project API
```
GET    /api/{user_id}/projects
POST   /api/{user_id}/projects
GET    /api/{user_id}/projects/{id}
PUT    /api/{user_id}/projects/{id}
DELETE /api/{user_id}/projects/{id}
GET    /api/{user_id}/projects/{id}/tasks
```

### 5.4 Error Handling
- Standardized error responses with consistent structure
- HTTP status codes following REST conventions
- Detailed error messages for debugging while protecting sensitive information

## 6. Security Considerations

### 6.1 Authentication & Authorization
- Better Auth managed JWT tokens with appropriate expiration times
- Secure token storage and transmission via Better Auth
- Role-based access control where applicable
- Rate limiting for authentication endpoints
- OAuth provider integration support (Google, GitHub, etc.)
- Email verification workflows via Better Auth
- Secure password reset mechanisms via Better Auth

### 6.2 Input Validation
- Request validation at API gateway level
- Sanitization of user inputs
- SQL injection prevention through ORM usage
- Cross-site scripting (XSS) protection

### 6.3 Data Protection
- Encryption at rest for sensitive data
- HTTPS enforcement
- Secure password policies
- Audit logging for critical operations

## 7. Performance & Scalability

### 7.1 Caching Strategy
- API response caching for static content
- Database query result caching
- CDN for static assets

### 7.2 Database Optimization
- Proper indexing strategy
- Connection pooling
- Query optimization
- Read replicas for read-heavy operations

### 7.3 Frontend Optimization
- Code splitting and lazy loading
- Image optimization
- Bundle size optimization
- Progressive web app features

## 8. Testing Strategy

### 8.1 Backend Testing
- Unit tests for business logic
- Integration tests for API endpoints
- Database integration tests
- Security tests

### 8.2 Frontend Testing
- Unit tests for React components
- Integration tests for UI flows
- End-to-end tests for critical user journeys
- Accessibility tests

## 9. Deployment & DevOps

### 9.1 Development Workflow
- Feature branching strategy
- Pull request reviews
- Automated testing on CI
- Database migration management

### 9.2 Deployment Pipeline
- Containerization with Docker
- Environment-specific configurations
- Health checks and monitoring
- Rollback procedures

## 10. Monitoring & Observability

### 10.1 Logging
- Structured logging with appropriate levels
- Centralized log aggregation
- Sensitive data filtering

### 10.2 Metrics
- API response times
- Error rates
- Database query performance
- Resource utilization

### 10.3 Alerting
- Critical error notifications
- Performance degradation alerts
- Security incident notifications