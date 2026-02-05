# ADR 2: Automatic Database URL Transformation for Async Compatibility

## Status
Accepted

## Date
2026-01-31

## Context
SQLAlchemy async engines require specific driver prefixes (like `postgresql+asyncpg://`) to work properly with async operations, while standard PostgreSQL URLs from providers like Neon use formats like `postgresql://` or `postgres://`. Manually editing these URLs for different environments creates operational overhead and potential for errors during deployment.

## Decision
We will implement automatic URL transformation that detects standard PostgreSQL URL formats and converts them to async-compatible formats when creating async engines. This eliminates the need for manual URL editing while maintaining compatibility with sync operations.

## Alternatives Considered

### Alternative 1: Manual URL Editing
- Pros: Simple implementation
- Cons: Requires manual intervention in multiple environments, error-prone, maintenance overhead
- Rejected because of operational complexity

### Alternative 2: Separate Environment Variables
- Pros: Clear separation between sync and async URLs
- Cons: Doubles the configuration complexity, requires managing multiple variables
- Rejected because it increases configuration burden

### Alternative 3: Runtime Detection and Conversion
- Pros: Automatic, transparent to users, minimal configuration changes
- Cons: Slight complexity in URL manipulation logic
- Chosen because it provides the best balance of automation and simplicity

## Implementation
- Read DATABASE_URL from environment variables
- Apply transformation logic: `postgres://` → `postgresql+asyncpg://` and `postgresql://` → `postgresql+asyncpg://`
- Use transformed URL only for async engine creation
- Preserve original URL for sync engine creation
- Maintain all URL parameters and query strings during transformation

## Consequences

### Positive
- Zero manual URL editing required for different environments
- Seamless deployment across local, staging, and production
- Reduced configuration errors and operational overhead
- Transparent to existing code and developers

### Negative
- Slight complexity in URL manipulation logic
- Potential confusion if developers examine engine URLs directly

## Notes
This transformation is transparent to application code and significantly reduces deployment complexity while maintaining full backward compatibility with existing sync operations.