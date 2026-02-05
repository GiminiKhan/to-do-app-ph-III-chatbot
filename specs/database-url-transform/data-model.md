# Database URL Transformation Data Model

## Entities

### Database URL Configuration
- **Name**: Database URL Configuration
- **Fields**:
  - raw_url (String, required): Original URL from environment variable
  - transformed_url (String, required): Transformed URL for async operations
  - driver_type (String, computed): Detected driver type (sync/async)
  - transformation_rule (String, enum): Applied rule (none, postgres_to_asyncpg, postgresql_to_asyncpg)
- **Relationships**: None (configuration entity)
- **Validation**: Must be valid PostgreSQL connection string format
- **State Transitions**: raw_url → transformed_url (applied transformation)

### URL Transformation Rule
- **Name**: URL Transformation Rule
- **Fields**:
  - input_pattern (String, required): Regex pattern for input URL
  - output_pattern (String, required): Replacement pattern for async URL
  - description (String): Purpose of the transformation
  - priority (Integer): Order of rule application
- **Relationships**: Applied to Database URL Configuration
- **Validation**: Must produce valid async SQLAlchemy URL
- **State Transitions**: None (immutable rules)

### Database Engine Configuration
- **Name**: Database Engine Configuration
- **Fields**:
  - sync_engine_config (Object): Configuration for sync engine using raw URL
  - async_engine_config (Object): Configuration for async engine using transformed URL
  - connection_pool_size (Integer): Size of connection pool
  - max_overflow (Integer): Maximum overflow connections
- **Relationships**: Created from Database URL Configuration
- **Validation**: Both sync and async engines must be creatable
- **State Transitions**: initialized → configured → ready

## Transformation Rules

### Rule 1: postgres:// to postgresql+asyncpg://
- **Input Pattern**: /^postgres:\/\//
- **Output Pattern**: postgresql+asyncpg://
- **Description**: Transform legacy postgres:// to asyncpg-compatible format
- **Priority**: 1

### Rule 2: postgresql:// to postgresql+asyncpg://
- **Input Pattern**: /^postgresql:\/\//
- **Output Pattern**: postgresql+asyncpg://
- **Description**: Transform standard postgresql:// to asyncpg-compatible format
- **Priority**: 2

### Rule 3: Default (No Transformation)
- **Input Pattern**: /*/ (fallback)
- **Output Pattern**: (no change)
- **Description**: Use URL as-is if no transformation rule matches
- **Priority**: 3

## Configuration Schema

### Environment Variables
- DATABASE_URL (String): PostgreSQL connection string with any supported format

### Engine Configuration Properties
- async_enabled (Boolean): Whether async engine is created
- sync_fallback (Boolean): Whether sync engine is created as fallback
- transformation_applied (Boolean): Whether URL transformation was applied
- original_format (String): Format of original URL (postgres, postgresql, other)