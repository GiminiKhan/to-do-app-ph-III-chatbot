# Data Model for TypeScript Arithmetic Error Fix

## Overview
This fix does not modify any data models. It only adds type-safe conversion in the sorting logic of existing data.

## Task Object (Unchanged)
- id: number/string - Unique identifier for the task
- title: string - Title of the task
- description: string - Description of the task
- priority: string - Priority level ("High", "Medium", "Low")
- status: string - Status of the task ("completed", "pending")
- created_at: string - Creation timestamp in ISO format
- updated_at: string - Last update timestamp in ISO format

## Date Fields
- created_at: String representation of date in ISO format
- updated_at: String representation of date in ISO format

## Sorting Parameters
- sortBy: string - Either "Newest" or "Priority"
- priorityFilter: string - Either "All", "High", "Medium", or "Low"