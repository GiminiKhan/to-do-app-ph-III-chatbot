# Database URL Transformation Research

## Decision: URL Scheme Transformation Implementation
- **Rationale**: SQLAlchemy async engines require specific driver prefixes to work properly with async operations
- **Approach**: Transform standard PostgreSQL URLs to asyncpg-compatible URLs automatically

## Decision: Driver Selection (asyncpg)
- **Rationale**: asyncpg is the recommended async driver for PostgreSQL in SQLAlchemy
- **Implementation**: Convert URLs to use postgresql+asyncpg:// prefix for async operations

## Decision: Dual URL Handling
- **Rationale**: Need to maintain sync compatibility while enabling async operations
- **Approach**: Transform URL only for async engine, use original for sync engine

## Alternatives Considered

### Alternative 1: Manual URL Editing
- **Pros**: Simple implementation
- **Cons**: Requires manual intervention in multiple environments
- **Verdict**: Not chosen due to maintenance overhead

### Alternative 2: Separate Environment Variables
- **Pros**: Clear separation of concerns
- **Cons**: Requires managing multiple variables
- **Verdict**: Not chosen to simplify configuration

### Alternative 3: Runtime Detection
- **Pros**: Dynamic adaptation
- **Cons**: Complexity and potential performance impact
- **Verdict**: Not chosen for simplicity

## Best Practices Identified

### URL Transformation Patterns
- Always use non-destructive transformation
- Preserve original URL for sync operations
- Apply transformation only when necessary

### PostgreSQL Async Operations
- Use postgresql+asyncpg:// for async operations
- Maintain postgresql:// for sync operations
- Ensure both formats work with the same database

### Environment Configuration
- Support both postgres:// and postgresql:// legacy formats
- Provide clear error messages for invalid formats
- Allow for future driver additions

## Neon PostgreSQL Specific Considerations

### URL Format Compatibility
- Neon typically provides URLs in postgresql:// format
- Some legacy systems may use postgres:// format
- SSL requirements are preserved in transformed URLs

### Connection Pooling
- Asyncpg supports efficient connection pooling
- URL parameters (like sslmode) are preserved during transformation
- Connection parameters remain unchanged

## SQLAlchemy Async Engine Requirements

### Driver Compatibility
- Async engines require specific driver prefixes
- postgresql+asyncpg:// is the standard format
- Other drivers may be supported in the future

### Session Management
- Async sessions require async context managers
- Sync sessions continue to work with original URLs
- Mixed usage is supported during transition periods