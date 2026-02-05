---
id: 1
title: Update database neon connection
stage: plan
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: database-neon-config
branch: main
user: Claude Sonnet 4.5
command: '"Update '\''backend/src/core/database.py'\'' to use the '\''DATABASE_URL'\'' already defined in our local .env file. The code should use this URL to establish an async connection to Neon PostgreSQL via SQLAlchemy. Ensure the implementation is robust for both local testing and Vercel deployment."'
labels: ["database", "neon", "postgresql", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - F:\to-do-app\specs\database-neon-config\plan.md
  - F:\to-do-app\specs\database-neon-config\research.md
  - F:\to-do-app\specs\database-neon-config\data-model.md
  - F:\to-do-app\specs\database-neon-config\quickstart.md
  - F:\to-do-app\backend\src\core\database.py
  - F:\to-do-app\backend\requirements.txt
tests:
  -
outcome:
evaluation:
---

# Update 'backend/src/core/database.py' to use the 'DATABASE_URL' already defined in our local .env file. The code should use this URL to establish an async connection to Neon PostgreSQL via SQLAlchemy. Ensure the implementation is robust for both local testing and Vercel deployment.

## Response

I've successfully updated the database configuration to use the DATABASE_URL from the .env file and establish an async connection to Neon PostgreSQL via SQLAlchemy. Here's what was implemented:

### Changes Made:

1. **Updated `backend/src/core/database.py`**:
   - Replaced hardcoded SQLite configuration with environment variable-based PostgreSQL connection
   - Added async SQLAlchemy engine using `create_async_engine`
   - Maintained backward compatibility with sync engine and session for existing code
   - Added proper error handling to validate DATABASE_URL existence
   - Used pydantic-settings for robust environment variable management

2. **Updated `backend/requirements.txt`**:
   - Added python-dotenv dependency for environment variable loading

### Key Features:

- **Environment Variable Support**: Uses DATABASE_URL from .env file
- **Async Support**: Added async SQLAlchemy engine and session for modern async operations
- **Backward Compatibility**: Maintains sync session functionality for existing code
- **Robust Error Handling**: Validates that DATABASE_URL is set at startup
- **Neon PostgreSQL Ready**: Configured for Neon's PostgreSQL serverless database
- **Deployment Friendly**: Works for both local testing and Vercel deployment

### Technical Details:

- Async engine created with `create_async_engine` for PostgreSQL
- Sync engine maintained with `create_engine` for compatibility
- Session factories for both async and sync operations
- Proper async context managers for session handling
- Validation of required environment variables at startup

The implementation follows the architecture plan and maintains compatibility with existing code while enabling async operations for better performance in production deployments.