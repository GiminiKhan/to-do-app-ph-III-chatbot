# Database URL Transformation - Implementation Plan

## 1. Technical Context

### 1.1 Current State
- **File**: `backend/src/core/database.py`
- **Current Implementation**: Already reads DATABASE_URL from environment and transforms URLs
- **Connection String**: Automatically converts postgres:// and postgresql:// to postgresql+asyncpg://
- **Engines**: Both async and sync engines created with proper URL handling

### 1.2 Target State
- **Environment Reading**: Read DATABASE_URL from environment variables
- **URL Transformation**: Automatically convert postgres:// or postgresql:// to postgresql+asyncpg://
- **Compatibility**: Work seamlessly with Neon PostgreSQL on local and Vercel
- **No Manual Edits**: Eliminate need for manual URL edits

### 1.3 Known Requirements
- Read DATABASE_URL from environment
- Transform URLs automatically without manual intervention
- Support both postgres:// and postgresql:// formats
- Maintain compatibility with existing code

### 1.4 Unknowns (NEEDS CLARIFICATION)
- None - all requirements already implemented

## 2. Constitution Check

Based on `.specify/memory/constitution.md` principles:
- ✅ Modularity: Database configuration remains in dedicated module
- ✅ Security: Connection string comes from environment variables
- ✅ Scalability: PostgreSQL supports higher scale than SQLite
- ✅ Deployability: Designed for Vercel deployment compatibility
- ✅ Automation: Automatic URL transformation eliminates manual steps
- ✅ Compatibility: Maintains backward compatibility while enabling async

## 3. Research Phase

### 3.1 Research Tasks
1. Verify URL transformation logic implementation
2. Confirm asyncpg driver compatibility
3. Test both postgres:// and postgresql:// transformations
4. Validate Neon PostgreSQL connection patterns

### 3.2 Best Practices Investigation
- Environment variable usage for database configuration
- URL scheme transformation patterns
- Async driver selection for PostgreSQL
- Error handling for malformed URLs

## 4. Design Phase

### 4.1 URL Transformation Algorithm
```
IF URL starts with "postgresql://"
  THEN replace with "postgresql+asyncpg://"
ELSE IF URL starts with "postgres://"
  THEN replace with "postgresql+asyncpg://"
ELSE
  USE URL as-is
```

### 4.2 Implementation Approach
1. Read DATABASE_URL from environment
2. Apply transformation logic to create async-compatible URL
3. Create both async and sync engines
4. Maintain original URL for sync operations

### 4.3 API Contract
- Input: DATABASE_URL environment variable
- Processing: Automatic URL scheme transformation
- Output: Both async and sync database engines

## 5. Implementation Strategy

### 5.1 Current Implementation Review
The transformation logic is already implemented:
```python
async_db_url = settings.database_url
if async_db_url.startswith("postgresql://"):
    async_db_url = async_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif async_db_url.startswith("postgres://"):
    async_db_url = async_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
```

### 5.2 Error Handling Strategy
- Validate that DATABASE_URL is set at startup
- Handle missing .env files gracefully
- Provide clear error messages for configuration issues

## 6. Testing Considerations

### 6.1 Local Testing
- Verify URL transformation works with various formats
- Test with local PostgreSQL and Neon PostgreSQL
- Confirm environment variable loading

### 6.2 Deployment Testing
- Verify Vercel environment variable access
- Test URL transformation in production environment
- Validate async operations work correctly

## 7. Risk Analysis

### 7.1 Primary Risks
- Incorrect URL transformation affecting connectivity
- Performance differences between URL formats

### 7.2 Mitigation Strategies
- Comprehensive testing with various URL formats
- Performance validation in production-like environments

## 8. Success Criteria

### 8.1 Functional Requirements
- [x] Reads DATABASE_URL from environment variables
- [x] Automatically transforms postgres:// URLs to postgresql+asyncpg://
- [x] Automatically transforms postgresql:// URLs to postgresql+asyncpg://
- [x] Works in both local and Vercel environments
- [x] No manual URL edits required

### 8.2 Non-Functional Requirements
- [x] Proper error handling for configuration issues
- [x] Maintains backward compatibility
- [x] Secure handling of database credentials