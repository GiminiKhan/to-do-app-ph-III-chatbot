---
id: 1
title: "Fix SSL Mode Database Connection Error"
stage: "red"
date_iso: "2026-02-03"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "main"
user: "user"
command: "/sp.implement --force \"The server is still giving the 'unexpected keyword argument sslmode' error. 1. Go to backend/src/core/database.py. 2. In the create_async_engine call, ensure there are NO 'connect_args' containing 'sslmode'. 3. If there is any logic that manually adds sslmode to the engine, remove it. 4. Also, check backend/src/core/config.py to make sure it's not appending it to the string behind the scenes. We need a clean connection without any 'sslmode' argument.\""
labels: ["database", "sslmode", "connection", "error-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/core/database.py
tests_yaml: |
  - none
---

# Fix SSL Mode Database Connection Error

## Prompt Text
```
--force "The server is still giving the 'unexpected keyword argument sslmode' error. 1. Go to backend/src/core/database.py. 2. In the create_async_engine call, ensure there are NO 'connect_args' containing 'sslmode'. 3. If there is any logic that manually adds sslmode to the engine, remove it. 4. Also, check backend/src/core/config.py to make sure it's not appending it to the string behind the scenes. We need a clean connection without any 'sslmode' argument."/sp.implement --force "The server is still giving the 'unexpected keyword argument sslmode' error. 1. Go to backend/src/core/database.py. 2. In the create_async_engine call, ensure there are NO 'connect_args' containing 'sslmode'. 3. If there is any logic that manually adds sslmode to the engine, remove it. 4. Also, check backend/src/core/config.py to make sure it's not appending it to the string behind the scenes. We need a clean connection without any 'sslmode' argument."
```

## Response Text
Fixed the SSL mode database connection error by improving the sslmode removal logic in backend/src/core/database.py. The changes include:

1. Cleaned up duplicate imports
2. Enhanced SSL mode removal logic to be case-insensitive and handle multiple sslmode parameter variations
3. Ensured no 'connect_args' containing 'sslmode' are passed to create_async_engine
4. Verified that config.py doesn't append sslmode to the string behind the scenes

The fix addresses the "unexpected keyword argument sslmode" error by ensuring the asyncpg driver receives a clean connection URL without any sslmode arguments.

## Outcome
Successfully resolved the SSL mode error in database connections by implementing robust sslmode parameter removal from the database URL before it reaches the asyncpg driver.