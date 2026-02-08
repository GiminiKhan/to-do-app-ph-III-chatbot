# Data Model: MCP Server and AI Agent Integration for Taskify Phase III

## Overview
This document defines the data models for the MCP server and AI agent integration as specified in the corresponding specification document. The models are designed to support the AI-native architecture requirements while maintaining compatibility with existing systems where appropriate.

## Version Information
- **Data Model Version**: 1.0.0
- **Constitution Compliance**: v3.0.0 (AI-Native Evolution)
- **Date Created**: 2026-02-07
- **Author**: Spec-Kit Plus

## Entity Relationship Diagram (Conceptual)

```
[User] 1----* [Conversation] 1----* [Message]
                |
                *----* [Task]
```

## Core Entities

### 1. Task Entity
**Purpose**: Represents a task that can be managed through the AI system

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID/String | Primary Key, Not Null | Unique identifier for the task |
| title | String(255) | Not Null | Title of the task |
| description | Text(1000) | Optional | Detailed description of the task |
| priority | Enum | Values: low, medium, high; Default: medium | Priority level of the task |
| due_date | DateTime | Optional | Due date for the task |
| status | Enum | Values: pending, completed; Default: pending | Current status of the task |
| created_at | DateTime | Not Null | Timestamp when task was created |
| updated_at | DateTime | Not Null | Timestamp when task was last updated |
| completed_at | DateTime | Optional | Timestamp when task was completed |
| user_id | UUID/String | Foreign Key, Not Null | Reference to the user who owns the task |

**Validation Rules**:
- Title must be between 1-255 characters
- Description must be under 1000 characters if provided
- Priority must be one of the allowed values
- Status transition from completed back to pending is not allowed
- Due date cannot be in the past when creating/updating

### 2. Conversation Entity
**Purpose**: Represents a conversation thread between user and AI assistant

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID/String | Primary Key, Not Null | Unique identifier for the conversation |
| user_id | UUID/String | Foreign Key, Not Null | Reference to the user who owns the conversation |
| title | String(255) | Optional | Auto-generated title based on first message |
| created_at | DateTime | Not Null | Timestamp when conversation was started |
| updated_at | DateTime | Not Null | Timestamp when conversation was last updated |
| ai_thread_id | String(255) | Not Null | External ID for OpenAI thread |
| metadata | JSON | Optional | Additional conversation metadata |

**Validation Rules**:
- Each user can have multiple conversations
- ai_thread_id must be unique across the system
- Title is auto-generated from first message if not provided

### 3. Message Entity
**Purpose**: Represents an individual message in a conversation

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID/String | Primary Key, Not Null | Unique identifier for the message |
| conversation_id | UUID/String | Foreign Key, Not Null | Reference to the conversation |
| role | Enum | Values: user, assistant, system; Not Null | Role of the message sender |
| content | Text | Not Null | Content of the message |
| timestamp | DateTime | Not Null | When the message was sent |
| metadata | JSON | Optional | Additional message metadata |

**Validation Rules**:
- Messages must belong to a valid conversation
- Role must be one of the allowed values
- Content cannot be empty

### 4. User Entity
**Purpose**: Represents a user in the system (extends existing user model)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID/String | Primary Key, Not Null | Unique identifier for the user |
| email | String(255) | Unique, Not Null | User's email address |
| username | String(255) | Unique, Optional | User's chosen username |
| created_at | DateTime | Not Null | Timestamp when user was created |
| updated_at | DateTime | Not Null | Timestamp when user was last updated |
| preferences | JSON | Optional | User preferences for AI interactions |

**Validation Rules**:
- Email must be a valid email format
- Username must be unique if provided
- Preferences structure must follow defined schema

## MCP Tool Schemas

### add_task Tool Schema
```json
{
  "name": "add_task",
  "description": "Create a new task in the system",
  "input_schema": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "Title of the task (max 255 characters)",
        "maxLength": 255
      },
      "description": {
        "type": "string",
        "description": "Detailed description of the task (max 1000 characters)",
        "maxLength": 1000
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high"],
        "description": "Priority level of the task",
        "default": "medium"
      },
      "due_date": {
        "type": "string",
        "format": "date-time",
        "description": "Due date for the task in ISO 8601 format"
      }
    },
    "required": ["title"]
  }
}
```

### list_tasks Tool Schema
```json
{
  "name": "list_tasks",
  "description": "Retrieve a list of tasks with optional filtering",
  "input_schema": {
    "type": "object",
    "properties": {
      "status": {
        "type": "string",
        "enum": ["pending", "completed", "all"],
        "description": "Filter tasks by status",
        "default": "all"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high"],
        "description": "Filter tasks by priority"
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "description": "Maximum number of tasks to return",
        "default": 10
      },
      "offset": {
        "type": "integer",
        "minimum": 0,
        "description": "Number of tasks to skip",
        "default": 0
      }
    }
  }
}
```

### complete_task Tool Schema
```json
{
  "name": "complete_task",
  "description": "Mark a task as completed",
  "input_schema": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "Unique identifier of the task to complete"
      }
    },
    "required": ["task_id"]
  }
}
```

### delete_task Tool Schema
```json
  "name": "delete_task",
  "description": "Remove a task from the system",
  "input_schema": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "Unique identifier of the task to delete"
      }
    },
    "required": ["task_id"]
  }
}
```

### update_task Tool Schema
```json
{
  "name": "update_task",
  "description": "Modify an existing task's properties",
  "input_schema": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "Unique identifier of the task to update"
      },
      "title": {
        "type": "string",
        "description": "New title for the task (max 255 characters)",
        "maxLength": 255
      },
      "description": {
        "type": "string",
        "description": "New description for the task (max 1000 characters)",
        "maxLength": 1000
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high"],
        "description": "New priority level for the task"
      },
      "due_date": {
        "type": "string",
        "format": "date-time",
        "description": "New due date for the task in ISO 8601 format"
      },
      "status": {
        "type": "string",
        "enum": ["pending", "completed"],
        "description": "New status for the task"
      }
    },
    "required": ["task_id"]
  }
}
```

## Indexes and Performance Considerations

### Task Entity Indexes
- **Primary Index**: id (automatically created)
- **User Tasks Index**: user_id, status (for efficient user task retrieval)
- **Due Date Index**: due_date (for sorting by due date)
- **Status Index**: status (for filtering by status)

### Conversation Entity Indexes
- **Primary Index**: id (automatically created)
- **User Conversations Index**: user_id (for retrieving user conversations)
- **AI Thread Index**: ai_thread_id (for quick lookup by external ID)

### Message Entity Indexes
- **Primary Index**: id (automatically created)
- **Conversation Messages Index**: conversation_id, timestamp (for chronological retrieval)
- **Role Index**: role (for filtering by message type)

## Migration Considerations

### From Phase I (Console App) Models
- Phase I likely used in-memory storage or simple file-based storage
- Need to migrate any existing tasks to the new Task entity
- Map old user data to the new User entity structure

### From Phase II (Basic Web App) Models
- Phase II likely had simpler Task model without AI integration fields
- May need to add fields like completed_at to existing Task model
- Conversation and Message entities are new additions

## Security Considerations

### Data Access Controls
- Users can only access their own tasks and conversations
- Proper foreign key constraints to prevent data leakage
- Validation of user ownership in all queries

### Data Encryption
- Sensitive fields may require encryption at rest
- Consider encrypting conversation content if required
- Secure storage of external AI thread IDs

## API Response Formats

### Task Response Format
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "priority": "high",
  "due_date": "2023-12-25T10:00:00Z",
  "status": "pending",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z",
  "completed_at": null
}
```

### Conversation Response Format
```json
{
  "id": "uuid-string",
  "title": "Conversation title",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z",
  "ai_thread_id": "thread-external-id"
}
```

### List Response Format
```json
{
  "items": [...],
  "total": 100,
  "limit": 10,
  "offset": 0,
  "has_more": true
}
```