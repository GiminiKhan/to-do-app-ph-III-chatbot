# Database URL Transformation Quickstart

## Overview
This feature automatically transforms PostgreSQL database URLs to work with async SQLAlchemy engines, eliminating the need for manual URL edits when deploying to different environments.

## Setup Instructions

### 1. Environment Configuration
```bash
# Add to your .env file - no manual URL editing needed!
DATABASE_URL="postgresql://username:password@host:port/database?sslmode=require"
# OR
DATABASE_URL="postgres://username:password@host:port/database?sslmode=require"
```

### 2. No Code Changes Required
The transformation happens automatically when the database module is imported:
```python
from backend.src.core.database import get_async_session, get_session
```

## How It Works

### Automatic URL Transformation
```python
# Input (from environment):
"postgresql://user:pass@host:port/db"

# Automatically transformed to:
"postgresql+asyncpg://user:pass@host:port/db"

# For async operations while preserving original for sync operations
```

### Supported Formats
- `postgres://` → `postgresql+asyncpg://`
- `postgresql://` → `postgresql+asyncpg://`
- Other formats remain unchanged

## Usage Examples

### Async Session (Automatic Transformation)
```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_todo(todo_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.get(Todo, todo_id)
    return result
```

### Sync Session (Original URL Preserved)
```python
from sqlmodel import Session

def get_todo_sync(todo_id: int, db: Session = Depends(get_session)):
    result = db.get(Todo, todo_id)
    return result
```

## Configuration Options

The transformation happens automatically with no additional configuration needed. The system:

- Reads DATABASE_URL from environment variables
- Applies transformation rules automatically
- Creates both async and sync engines
- Preserves original URL for sync operations

## Deployment Scenarios

### Local Development
```bash
# .env file
DATABASE_URL="postgresql://localuser:localpass@localhost:5432/localdb"
# Automatically transformed for async operations
```

### Vercel Deployment
```bash
# Vercel environment variable
DATABASE_URL="postgres://neonuser:neonpass@ep-host.region.aws.neon.tech/neondb?sslmode=require"
# Automatically transformed for async operations
```

## Troubleshooting

### Common Issues
1. **Invalid URL Format**: Ensure your DATABASE_URL is a valid PostgreSQL connection string
2. **Missing Environment Variable**: Verify DATABASE_URL is set in your environment
3. **Driver Issues**: Confirm asyncpg is installed in your environment

### Verification
Check that the transformation is working by inspecting the engine URLs:
```python
from backend.src.core.database import async_engine, sync_engine
print(f"Async engine URL: {async_engine.url}")
print(f"Sync engine URL: {sync_engine.url}")
```

The async engine URL should have the `postgresql+asyncpg://` prefix while the sync engine uses the original format.