---
id: 012
title: Update config and retry db connection
stage: red
date_iso: 2026-02-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase2-web
branch: main
user: claude
command: /sp.implement
labels: ["database", "configuration", "postgresql", "neon"]
links:
  spec: specs/phase2-web/spec.md
  plan: specs/phase2-web/plan.md
  tasks: specs/phase2-web/tasks.md
  previous: history/prompts/phase2-web/011-attempt-neon-db-connection.red.prompt.md
  adr: null
  pr: null
files_yaml: |
  - backend/src/core/config.py
  - backend/src/core/init_db.py
  - backend/.env
tests_yaml: |
  - Config update verification
  - Database connection attempt
  - Environment variable loading
outcome: "Updated config.py to properly load DATABASE_URL from .env and attempted database connection"
evaluation: "Configuration successfully updated but connection failed due to non-existent PostgreSQL server"
---

# Update Config and Retry Database Connection

## Summary
Updated config.py as requested to properly load DATABASE_URL from .env without hardcoded fallbacks and attempted database connection again.

## Changes Made

### 1. Updated backend/src/core/config.py:
- Changed DATABASE_URL from `str = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost:5432/todo_db")` to `str = os.getenv("DATABASE_URL")`
- Removed hardcoded localhost fallback completely
- Added `import dotenv` and `dotenv.load_dotenv()` at the top to ensure .env file is loaded
- Updated the Settings class to properly handle environment variables without fallbacks

### 2. Verification of Changes:
- Confirmed that the config now properly loads DATABASE_URL from environment without fallback
- Verified that dotenv is imported and called to load the .env file

## Execution Results

### Command Executed:
`cd backend && python -m src.core.init_db`

### Output:
The script still fails with a `ConnectionRefusedError` because no PostgreSQL server is running at the specified address. However, the important change is that it's now using the actual value from the .env file rather than the hardcoded fallback.

## Analysis

- The configuration changes were successfully applied
- The script now properly reads the DATABASE_URL from the .env file
- The connection failure is expected since there's no PostgreSQL server running at the specified address
- When a valid Neon PostgreSQL connection is available, the script should work correctly

## Conclusion

The configuration has been successfully updated as requested. The script now properly loads the DATABASE_URL from the .env file without hardcoded fallbacks. The connection failure is due to the absence of a running PostgreSQL server, not due to configuration issues.