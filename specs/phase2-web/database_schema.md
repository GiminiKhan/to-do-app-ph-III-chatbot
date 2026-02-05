# Database Schema Definitions

## Shared Database Schema for Phase II Web Application

This document defines the shared database schema to eliminate duplication between specification and plan documents.

## Better Auth Tables (Managed by Better Auth)

### User Table
- id (UUID, primary key)
- email (VARCHAR, unique, not null)
- email_verified (BOOLEAN, default false)
- name (VARCHAR)
- username (VARCHAR, unique)
- locale (VARCHAR)
- image (TEXT)
- created_at (TIMESTAMP, default now)
- updated_at (TIMESTAMP, default now)

### Session Table
- id (UUID, primary key)
- user_id (UUID, foreign key to users, not null)
- expires_at (TIMESTAMP, not null)
- created_at (TIMESTAMP, default now)
- updated_at (TIMESTAMP, default now)

### Account Table
- id (UUID, primary key)
- user_id (UUID, foreign key to users, not null)
- account_type (VARCHAR, not null)
- provider_id (VARCHAR, not null)
- provider_account_id (VARCHAR, not null)
- refresh_token (TEXT)
- access_token (TEXT)
- expires_at (INTEGER)
- token_type (VARCHAR)
- scope (VARCHAR)
- created_at (TIMESTAMP, default now)
- updated_at (TIMESTAMP, default now)

### Verification Table
- id (UUID, primary key)
- identifier (VARCHAR, not null)
- value (VARCHAR, not null)
- expires_at (TIMESTAMP, not null)
- created_at (TIMESTAMP, default now)

## Application Tables

### Projects Table
- id (UUID, primary key)
- user_id (UUID, foreign key to better_auth_users.id)
- name (VARCHAR, not null)
- description (TEXT)
- color (VARCHAR, default '#000000')
- created_at (TIMESTAMP, default now)
- updated_at (TIMESTAMP, default now)

### To-Dos Table
- id (UUID, primary key)
- user_id (UUID, foreign key to better_auth_users.id)
- project_id (UUID, foreign key to projects)
- title (VARCHAR, not null)
- description (TEXT)
- status (ENUM: 'pending', 'in_progress', 'completed', default 'pending')
- priority (ENUM: 'low', 'medium', 'high', 'urgent', default 'medium')
- due_date (TIMESTAMP)
- completed_at (TIMESTAMP)
- created_at (TIMESTAMP, default now)
- updated_at (TIMESTAMP, default now)