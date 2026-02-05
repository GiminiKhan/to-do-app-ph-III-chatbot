# ADR 1: Database Migration from SQLite to Neon PostgreSQL with Async Support

## Status
Accepted

## Date
2026-01-31

## Context
The current application uses SQLite for data persistence, which is suitable for development but inadequate for production deployment, especially in serverless environments like Vercel. We need to migrate to Neon PostgreSQL to support:

- Production scalability requirements
- Concurrent access patterns
- Cloud-native deployment compatibility
- Better performance characteristics
- Team collaboration with shared database

## Decision
We will migrate from SQLite to Neon PostgreSQL and implement both sync and async database access patterns to:

1. Support async operations for improved performance in production
2. Maintain backward compatibility with existing sync code
3. Use environment variables for database configuration
4. Enable deployment compatibility with Vercel and other cloud platforms

## Alternatives Considered

### Alternative 1: Pure Async Migration
- Pros: Modern approach, better performance, aligns with cloud-native patterns
- Cons: Requires refactoring all existing database-dependent code simultaneously
- Rejected because of high risk and coordination complexity

### Alternative 2: Keep SQLite with file sharing
- Pros: Minimal code changes
- Cons: Not suitable for serverless deployment, concurrency issues, no collaboration
- Rejected because it doesn't meet production requirements

### Alternative 3: Different PostgreSQL provider
- Pros: Various PostgreSQL providers available
- Cons: Neon offers serverless, branching, and better integration with modern deployment platforms
- Chosen Neon for its serverless architecture and developer experience

## Implementation
- Update `backend/src/core/database.py` to use async SQLAlchemy with Neon PostgreSQL
- Maintain sync engine and session for backward compatibility
- Use environment variables (DATABASE_URL) for configuration
- Add proper error handling for missing configuration
- Update dependencies to include async PostgreSQL drivers

## Consequences

### Positive
- Improved scalability for production use
- Better performance with proper connection pooling
- Cloud-native deployment compatibility
- Enhanced collaboration capabilities
- Future-proof architecture for growth

### Negative
- Slightly increased complexity with dual sync/async patterns
- Additional dependencies for async operations
- Need to gradually migrate existing code to async patterns

## Notes
This change enables the foundation for production deployment while allowing gradual migration of existing code to async patterns. The backward compatibility ensures no breaking changes to existing functionality.