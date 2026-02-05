# Database Data Model for Neon PostgreSQL Configuration

## Entities

### Database Configuration
- **Name**: Database Configuration
- **Fields**:
  - DATABASE_URL (String, required): PostgreSQL connection string from environment
  - ENGINE_TYPE (String, default: "async"): Engine type configuration
  - POOL_SIZE (Integer, default: 5): Connection pool size
  - MAX_OVERFLOW (Integer, default: 10): Maximum overflow connections
- **Relationships**: None (configuration entity)
- **Validation**: Must be valid PostgreSQL connection string format
- **State Transitions**: None (immutable configuration at runtime)

### Database Engine
- **Name**: Database Engine
- **Fields**:
  - async_engine (SQLAlchemy AsyncEngine): Async SQLAlchemy engine instance
  - sync_engine (SQLAlchemy Engine): Sync SQLAlchemy engine instance (for backward compatibility)
  - is_connected (Boolean): Connection status indicator
- **Relationships**: Associated with Database Configuration
- **Validation**: Must successfully connect to database
- **State Transitions**: disconnected → connected

### Database Session
- **Name**: Database Session
- **Fields**:
  - async_session (AsyncSession): Async database session
  - sync_session (Session): Sync database session (for backward compatibility)
  - transaction_active (Boolean): Transaction status
- **Relationships**: Created from Database Engine
- **Validation**: Must be associated with valid Database Engine
- **State Transitions**: inactive → active → closed

## Database Schema Updates

### PostgreSQL-Specific Types
- UUID primary keys (instead of auto-increment integers)
- Proper timezone-aware timestamp columns
- PostgreSQL enum types for status fields
- JSONB columns for flexible data storage

### Indexing Strategy
- Primary key indexes (automatic)
- Foreign key indexes
- Composite indexes for common query patterns
- Partial indexes for filtered queries

## Migration Considerations

### From SQLite to PostgreSQL
- Data type mapping (INTEGER → INTEGER, TEXT → TEXT, etc.)
- Auto-increment handling (ROWID → SERIAL or UUID)
- Case sensitivity differences
- Transaction handling differences