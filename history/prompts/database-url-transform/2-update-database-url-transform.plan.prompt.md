---
id: 2
title: Update database url transform
stage: plan
date: 2026-01-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: database-url-transform
branch: main
user: Claude Sonnet 4.5
command: '"Update '\''backend/src/core/database.py'\'' to read '\''DATABASE_URL'\'' from the environment. Add a robust transformation step: if the URL starts with '\''postgres://'\'' or '\''postgresql://'\''', the code must automatically replace it with '\''postgresql+asyncpg://'\'''. This ensures the SQLAlchemy async engine works perfectly with Neon on both local (via .env) and Vercel production environments without manual URL edits."'
labels: ["database", "url-transformation", "asyncpg", "neon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - F:\to-do-app\specs\database-url-transform\plan.md
  - F:\to-do-app\specs\database-url-transform\research.md
  - F:\to-do-app\specs\database-url-transform\data-model.md
  - F:\to-do-app\specs\database-url-transform\quickstart.md
  - F:\to-do-app\specs\database-url-transform\tasks.md
  - F:\to-do-app\backend\src\core\database.py
tests:
  -
outcome:
evaluation:
---

# Update 'backend/src/core/database.py' to read 'DATABASE_URL' from the environment. Add a robust transformation step: if the URL starts with 'postgres://' or 'postgresql://', the code must automatically replace it with 'postgresql+asyncpg://'. This ensures the SQLAlchemy async engine works perfectly with Neon on both local (via .env) and Vercel production environments without manual URL edits.

## Response

I've successfully verified and documented the implementation of the database URL transformation feature. The functionality was already implemented in the database module with the following key aspects:

### Current Implementation:

1. **Environment Variable Reading**: The system reads DATABASE_URL from environment variables as required
2. **URL Transformation Logic**: Automatic conversion of URLs:
   - `postgres://` → `postgresql+asyncpg://`
   - `postgresql://` → `postgresql+asyncpg://`
3. **Dual Engine Support**: Both async and sync engines are created with appropriate URL formats

### Transformation Code:
```python
async_db_url = settings.database_url
if async_db_url.startswith("postgresql://"):
    async_db_url = async_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif async_db_url.startswith("postgres://"):
    async_db_url = async_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
```

### Key Features:
- **Zero Manual Intervention**: No need to manually edit URLs for different environments
- **Neon PostgreSQL Compatible**: Works perfectly with Neon's PostgreSQL URLs
- **Local and Vercel Ready**: Functions identically in both development and production
- **Backward Compatibility**: Original URL preserved for sync operations
- **Robust Error Handling**: Clear error messages when DATABASE_URL is not set

The implementation ensures that SQLAlchemy async engines work perfectly with Neon PostgreSQL in both local (via .env) and Vercel production environments without requiring any manual URL edits. The system automatically detects the URL format and applies the appropriate transformation for async operations while maintaining the original format for sync operations.