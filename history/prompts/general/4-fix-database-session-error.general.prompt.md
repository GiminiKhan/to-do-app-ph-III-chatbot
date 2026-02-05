---
id: 4
title: Fix database session error in auth logic
stage: green
date_iso: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.implement --force "I got a 400 Bad Request error: '_AsyncGeneratorContextManager' object has no attribute 'execute'. This means the database session is being used incorrectly in the auth logic. 1. Go to the registration and login service/endpoints. 2. Ensure you are 'awaiting' the session or using 'async with get_async_session() as session'. 3. The session object must be extracted from the generator before calling .execute() or .add(). Fix this in all authentication-related files."
labels:
  - database
  - auth
  - async
  - session
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/core/database.py
  - backend/src/api/auth.py
  - backend/src/api/deps.py
  - backend/src/api/todos.py
  - backend/src/api/projects.py
  - backend/src/api/users.py
tests_yaml: |
  - backend/tests/test_auth.py
  - backend/tests/test_todos.py
prompt_text: |
  --force "I got a 400 Bad Request error: '_AsyncGeneratorContextManager' object has no attribute 'execute'. This means the database session is being used incorrectly in the auth logic. 1. Go to the registration and login service/endpoints. 2. Ensure you are 'awaiting' the session or using 'async with get_async_session() as session'. 3. The session object must be extracted from the generator before calling .execute() or .add(). Fix this in all authentication-related files."
response_text: |
  Fixed the database session error by:
  1. Updating the get_async_session function in backend/src/core/database.py to work properly with FastAPI dependency injection
  2. Updated all API endpoints (auth, deps, todos, projects, users) to use async sessions consistently
  3. Ensured all database operations properly await async methods like .execute(), .commit(), .refresh(), and .delete()
  4. Made sure all dependency injections use the async session variant (AsyncSession) instead of sync (Session)
outcome: |
  Successfully resolved the database session error by ensuring consistent use of async database sessions across all API endpoints. The error occurred because there was an inconsistency between sync and async database session usage in different parts of the application.
evaluation: |
  All auth-related endpoints now properly handle async database sessions, eliminating the '_AsyncGeneratorContextManager' error. The application now consistently uses async database operations throughout.
---