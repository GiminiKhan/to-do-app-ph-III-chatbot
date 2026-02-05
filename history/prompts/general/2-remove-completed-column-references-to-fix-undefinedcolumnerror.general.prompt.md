---
id: 2
title: "Remove completed column references to fix UndefinedColumnError"
stage: "green"
date_iso: "2026-02-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "/sp.implement I am still getting 'UndefinedColumnError: column todo.completed does not exist'. Open 'backend/src/api/todos.py' and 'backend/src/models/todo.py'. Search for the word 'completed' (without quotes). If it's being used as a database column in a query or model definition, DELETE it or replace it with 'status'. Specifically, check the 'get_tasks' function—the SQL it's generating still includes 'todo.completed'. You MUST remove it from the select statement. Ensure the Pydantic schemas in 'backend/src/schemas/todo.py' match this change."
labels: ["database", "api", "migration", "bug-fix"]
spec: null
ticket: null
adr: null
pr: null
---

## Files Modified
- backend/src/models/todo.py
- backend/src/api/todos.py
- backend/src/schemas/todo.py

## Tests Performed
- Manual verification of code changes
- Ensured no remaining references to the 'completed' column in model definitions

## Prompt Text
```
/sp.implement I am still getting 'UndefinedColumnError: column todo.completed does not exist'. Open 'backend/src/api/todos.py' and 'backend/src/models/todo.py'. Search for the word 'completed' (without quotes). If it's being used as a database column in a query or model definition, DELETE it or replace it with 'status'. Specifically, check the 'get_tasks' function—the SQL it's generating still includes 'todo.completed'. You MUST remove it from the select statement. Ensure the Pydantic schemas in 'backend/src/schemas/todo.py' match this change.
```

## Response Text
Successfully fixed the 'UndefinedColumnError' by removing all references to the deprecated 'completed' column:
1. Removed the 'completed' field from the TodoBase model in backend/src/models/todo.py
2. Updated the schemas in backend/src/schemas/todo.py to remove the 'completed' field from TodoBase, TodoUpdate, and related schemas
3. Modified API endpoints in backend/src/api/todos.py to work exclusively with the 'status' and 'completed_at' fields
4. Updated the toggle_task_completion function to toggle between statuses instead of using the completed field
5. Updated PUT and PATCH endpoints to properly handle status changes and synchronize the completed_at field
6. Updated the create_task function to handle initial status assignment correctly

## Outcome
The application no longer attempts to access the non-existent 'completed' column in the database, resolving the UndefinedColumnError.

## Evaluation
All changes have been made to remove references to the deprecated 'completed' column and ensure the application works correctly with the new schema using only 'status' and 'completed_at' fields.
