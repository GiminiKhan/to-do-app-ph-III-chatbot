---
id: 3
title: Remove Startup DB Creation
stage: refactor
date_iso: 2026-02-02
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: main
user: unknown
command: sp.implement --force "Remove the @app.on_event('startup') block and the create_db_and_tables() call from backend/src/main.py. Also remove the import for create_db_and_tables. We have already created the tables on Neon, so this step is no longer needed and is causing a MissingGreenlet error."
labels: ["refactor", "database", "startup", "error-fix"]
spec_url: null
ticket_url: null
adr_url: null
pr_url: null
files_yaml: |
  - F:\to-do-app\backend\src\main.py
tests_yaml: []
prompt_text: |
  --force "Remove the @app.on_event('startup') block and the create_db_and_tables() call from backend/src/main.py. Also remove the import for create_db_and_tables. We have already created the tables on Neon, so this step is no longer needed and is causing a MissingGreenlet error."
response_text: |
  Successfully removed the @app.on_event('startup') block and the create_db_and_tables() call from backend/src/main.py. Also removed the import for create_db_and_tables. This resolves the MissingGreenlet error that was occurring during startup since the tables have already been created on Neon.
outcome: |
  Successfully removed the startup database creation that was causing a MissingGreenlet error.
evaluation: |
  SUCCESS - Startup event handler removed, resolving the MissingGreenlet error
---

# Remove Startup Database Creation

## Summary
Removed the @app.on_event('startup') block and the create_db_and_tables() call from backend/src/main.py. Also removed the import for create_db_and_tables. This resolves the MissingGreenlet error that was occurring during startup since the tables have already been created on Neon.

## Implementation Details
- Removed the import statement: `from .core.database import create_db_and_tables`
- Removed the startup event handler: `@app.on_event('startup')` and associated function
- Verified that the database tables were already created via the previous force_init.py process

## Result
The MissingGreenlet error during startup has been resolved, as the application no longer attempts to create database tables on startup since they've already been created on the Neon database.