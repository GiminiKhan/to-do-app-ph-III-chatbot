# Database Neon PostgreSQL Configuration Quickstart

## Prerequisites
- Python 3.9+
- PostgreSQL database (Neon account)
- Environment variables configured with DATABASE_URL

## Setup Instructions

### 1. Environment Configuration
```bash
# Add to your .env file
DATABASE_URL="postgresql://username:password@host:port/database?sslmode=require"
```

### 2. Install Dependencies
```bash
pip install asyncpg psycopg2-binary
```

### 3. Database Module Import
```python
from backend.src.core.database import get_async_session, get_session, create_db_and_tables
```

## Usage Examples

### Async Session Usage (Recommended)
```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_todo(todo_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.get(Todo, todo_id)
    return result
```

### Sync Session Usage (Backward Compatibility)
```python
from sqlmodel import Session

def get_todo_sync(todo_id: int, db: Session = Depends(get_session)):
    result = db.get(Todo, todo_id)
    return result
```

## Configuration Options

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string (required)
- `DB_POOL_SIZE`: Connection pool size (default: 5)
- `DB_MAX_OVERFLOW`: Maximum overflow connections (default: 10)
- `DB_ECHO`: Enable SQL logging (default: False)

### Connection Pool Settings
```python
# Example with custom pool settings
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    echo=False,
    pool_pre_ping=True,  # Validates connections before use
    pool_recycle=300     # Recycle connections every 5 minutes
)
```

## Testing Locally

### With Local PostgreSQL
```bash
# Install PostgreSQL locally or use Docker
docker run --name postgres-db -e POSTGRES_DB=myapp -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:14
```

### Environment for Testing
```bash
# .env.test
DATABASE_URL="postgresql://user:password@localhost:5432/myapp"
```

## Deployment to Vercel

### Environment Variables
Set `DATABASE_URL` in Vercel project settings to point to your Neon PostgreSQL database.

### Build Configuration
Ensure async drivers are properly included in deployment bundle.

## Troubleshooting

### Common Issues
1. **SSL Connection Problems**: Ensure sslmode=require in connection string
2. **Connection Timeout**: Check firewall settings and connection string
3. **Pool Exhaustion**: Increase pool size or optimize session usage

### Debugging
Enable DB_ECHO=true to log all SQL statements during development.