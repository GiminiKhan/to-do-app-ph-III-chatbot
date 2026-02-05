# Data Model: Phase 4 To-Do Management

## Overview
This document defines the data models for the To-Do Management feature, following the shared database schema and ensuring proper user isolation through foreign key relationships.

## Entity Relationships

```
Better Auth User (1) ─────── (N) To-Do Items
        │                          │
        │                          │
        └── (1) Projects (N) ─────┘
```

## Entity Definitions

### To-Do Entity
**Table**: `todos`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the task |
| user_id | UUID | Foreign Key → user.id, Not Null | Links task to the owning user (enforces user isolation) |
| project_id | UUID | Foreign Key → project.id, Nullable | Links task to an optional project |
| title | VARCHAR(200) | Not Null, Min Length: 1 | Task title |
| description | TEXT | Nullable | Detailed task description |
| status | ENUM | Default: 'pending' | Task status: 'pending', 'in_progress', 'completed' |
| priority | ENUM | Default: 'medium' | Task priority: 'low', 'medium', 'high', 'urgent' |
| due_date | TIMESTAMP | Nullable | Task deadline |
| completed_at | TIMESTAMP | Nullable | When task was completed |
| created_at | TIMESTAMP | Default: NOW() | When task was created |
| updated_at | TIMESTAMP | Default: NOW() | When task was last updated |

**Validation Rules**:
- user_id must match an existing user in the better_auth_users table
- project_id must match an existing project owned by the same user
- title must be 1-200 characters
- status must be one of the allowed enum values
- priority must be one of the allowed enum values
- due_date cannot be in the past (validation may be configurable)

### Project Entity
**Table**: `projects`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the project |
| user_id | UUID | Foreign Key → user.id, Not Null | Links project to the owning user |
| name | VARCHAR(100) | Not Null, Min Length: 1 | Project name |
| description | TEXT | Nullable | Project description |
| color | VARCHAR(7) | Default: '#000000' | Project color code |
| created_at | TIMESTAMP | Default: NOW() | When project was created |
| updated_at | TIMESTAMP | Default: NOW() | When project was last updated |

**Validation Rules**:
- user_id must match an existing user in the better_auth_users table
- name must be 1-100 characters
- color must be a valid hex color code

## State Transitions

### To-Do Status Transitions
```
pending ──→ in_progress ──→ completed
   ↑                              │
   └────── blocked by user ───────┘
```

### Priority Levels
- low: Routine tasks with flexible deadlines
- medium: Standard priority tasks
- high: Important tasks requiring attention
- urgent: Immediate action required

## Business Rules

1. **User Isolation**: A user can only access/modify tasks that belong to their user_id
2. **Project Ownership**: A user can only assign tasks to projects they own
3. **Data Integrity**: All foreign key relationships must be validated at the database level
4. **Audit Trail**: created_at and updated_at timestamps are automatically managed
5. **Soft Deletes**: Consider implementing soft deletes for data recovery (optional)

## Indexes

### Required Indexes
- `idx_todos_user_id`: Index on user_id for efficient user-based queries
- `idx_todos_project_id`: Index on project_id for efficient project-based queries
- `idx_todos_status`: Index on status for filtering by status
- `idx_todos_due_date`: Index on due_date for deadline-based queries

### Performance Considerations
- Composite indexes may be needed for complex filtering (e.g., user_id + status)
- Consider partial indexes for frequently queried subsets
- Monitor query performance and adjust indexing strategy as needed

## API Mapping

### To-Do Entity to API
- GET /api/{user_id}/tasks → SELECT from todos WHERE user_id = {user_id}
- POST /api/{user_id}/tasks → INSERT into todos with user_id = {user_id}
- GET /api/{user_id}/tasks/{task_id} → SELECT from todos WHERE id = {task_id} AND user_id = {user_id}
- PUT /api/{user_id}/tasks/{task_id} → UPDATE todos SET ... WHERE id = {task_id} AND user_id = {user_id}
- DELETE /api/{user_id}/tasks/{task_id} → DELETE FROM todos WHERE id = {task_id} AND user_id = {user_id}
- PATCH /api/{user_id}/tasks/{task_id}/complete → UPDATE todos SET status = ... WHERE id = {task_id} AND user_id = {user_id}

## Security Considerations

1. **Foreign Key Constraints**: Enforce referential integrity at the database level
2. **User Validation**: Always validate that the authenticated user matches the record's user_id
3. **Input Validation**: Validate all input data before database operations
4. **SQL Injection Prevention**: Use parameterized queries through ORM
5. **Access Control**: Implement row-level security through user_id filtering