---
id: 002
title: Update backend API specifications constitution alignment
stage: spec
date_iso: 2026-02-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase2-web
branch: main
user: claude
command: /sp.specify
labels: ["api", "specification", "duplication", "constitution"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/phase2-web/spec.md
  - specs/phase2-web/plan.md
  - specs/phase2-web/database_schema.md
tests_yaml: |
  - Specification alignment verified
  - Duplication issues resolved
outcome: "Successfully updated backend API specifications to match constitution and resolve duplication issues D1 and D2"
evaluation: "Specifications now reference shared schema to eliminate duplication and align with updated constitution"
---

# Update backend API specifications to match constitution and resolve duplication

## Summary
Updated the backend API specifications to match the updated constitution, align all endpoint paths to '/api/{user_id}/tasks' format, and resolve duplication issues (D1, D2) mentioned in the analysis report.

## Changes Made

### 1. Aligned API Endpoint Paths
- Updated spec.md to use /api/{user_id}/tasks format for all endpoints
- Updated spec.md project endpoints to use /api/{user_id}/projects format
- Verified all endpoints follow the Hackathon II requirements

### 2. Resolved Duplication Issues
- Created shared database_schema.md to eliminate duplication between spec and plan
- Updated both spec.md and plan.md to reference the shared schema document
- Removed duplicated table definitions from both documents

### 3. Updated Project Endpoints
- Updated spec.md to include proper /api/{user_id}/projects endpoints
- Updated plan.md to include proper /api/{user_id}/projects endpoints
- Added missing GET /api/{user_id}/projects/{id}/tasks endpoint

## Specification Quality Improvements

### Eliminated Duplication (D1, D2)
- **Before**: User and To-Do table definitions were duplicated in both spec and plan
- **After**: Both documents reference the shared database_schema.md document
- **Benefit**: Single source of truth for database schema, reducing maintenance overhead

### Constitution Alignment
- All API endpoints now follow the required /api/{user_id}/tasks format
- Specification maintains focus on WHAT and WHY rather than HOW
- Maintains consistency with Better Auth integration requirements

## Files Updated
- specs/phase2-web/spec.md: Updated API endpoints and schema references
- specs/phase2-web/plan.md: Updated API endpoints and schema references
- specs/phase2-web/database_schema.md: Created shared schema definitions