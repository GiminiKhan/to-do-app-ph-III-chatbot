---
id: 5
title: Fix database connection to use Neon instead of localhost
stage: green
date_iso: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.implement --force "The server is trying to connect to localhost:5432, but we are using Neon. Please check backend/src/core/config.py and backend/src/core/database.py. Make sure the DATABASE_URL is being read correctly from the .env file. Ensure that 'async_engine' is using the Neon connection string and NOT a local postgres address. We need to point back to the Neon cloud database immediately."
labels:
  - database
  - neon
  - configuration
  - environment
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/.env
  - backend/.env.example
  - backend/src/core/config.py
tests_yaml: |
  - backend/tests/test_config.py
prompt_text: |
  --force "The server is trying to connect to localhost:5432, but we are using Neon. Please check backend/src/core/config.py and backend/src/core/database.py. Make sure the DATABASE_URL is being read correctly from the .env file. Ensure that 'async_engine' is using the Neon connection string and NOT a local postgres address. We need to point back to the Neon cloud database immediately."
response_text: |
  Fixed the database connection issue by:
  1. Updated the .env file to use Neon PostgreSQL format instead of localhost
  2. Updated the .env.example file to show proper Neon configuration
  3. Fixed the config.py file to properly use Pydantic BaseSettings with env_file for environment variable loading
  4. Ensured the database engine creation uses the Neon connection string
outcome: |
  Successfully resolved the database connection issue. The application now correctly uses Neon PostgreSQL instead of attempting to connect to localhost:5432. The configuration properly loads environment variables from the .env file.
evaluation: |
  The database connection now points to Neon as required. The configuration properly handles environment variables and the async engines use the correct connection string format.
---