<!--
SYNC IMPACT REPORT:
Version change: 2.0.0 → 3.0.0
Modified principles:
  - IV. Clean Architecture: Updated from 'Cloud-Native Architecture (FastAPI + Neon PostgreSQL)' to 'AI-Native Architecture (FastAPI + SQLModel + Neon PostgreSQL + OpenAI Agents SDK + MCP SDK)'
  - IX. Added new principle for MCP Server implementation
  - X. Added new principle for OpenAI Agents integration
  - XI. Added new principle for Stateless Architecture
  - XII. Added new principle for OpenAI ChatKit integration
Updated sections: Security Protocol, Frontend Standard to reflect AI-native evolution
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: Update all templates to reflect new AI-native architecture principles
-->

# Evolution of Todo - Taskify Phase III Constitution (AI-Native Evolution)

## Core Principles

### I. Spec-Driven Development (SDD)
Spec-Driven Development is the foundational approach for all development activities. All features and changes must be specified before implementation begins, ensuring clear requirements and acceptance criteria. This remains unchanged as the fundamental methodology for AI-native development.

### II. No Manual Code
All code must be generated through Claude Code or integrated agents. No manual code writing is permitted. This ensures consistency, quality, and adherence to established patterns and practices across AI-native implementations.

### III. Agentic Stack
The technology stack must utilize UV, Python 3.13+, Claude Code, and the MCP SDK as required components. This agentic approach ensures automation and consistency across the AI-native development lifecycle.

### IV. Clean Architecture
The codebase must maintain modular and clean architecture principles using AI-Native Architecture (FastAPI + SQLModel + Neon PostgreSQL + OpenAI Agents SDK + MCP SDK). This ensures maintainability, testability, scalability, and robust data persistence across the AI-native system.

### V. Process Integrity
Every code change must reference a Task ID before implementation. This ensures traceability, accountability, and proper change management throughout the AI-native development process.

### VI. Security Protocol
Better Auth with JWT must be implemented as the mandatory security protocol for all authentication and authorization flows. This ensures secure user access, token management, and protection of sensitive data across all application layers, including AI interaction endpoints.

### VII. Frontend Standard
Next.js 15+ App Router must be used as the standard for all frontend development. This ensures modern React development practices, server-side rendering capabilities, optimized performance, and consistent routing patterns across the application, supporting AI chat interfaces.

### VIII. UI/UX Standards
Modern & Attractive UI must be implemented using Tailwind CSS with Indigo/Slate theme instead of simple black & white designs. This ensures consistent visual identity, responsive design, accessibility compliance, and enhanced user experience across all interfaces, especially AI-powered chat experiences.

### IX. MCP Server Implementation
An MCP Server must be implemented using the official SDK to expose CRUD operations as tools (add_task, list_tasks, complete_task, delete_task, update_task). This ensures standardized, interoperable AI tool integration and maintains clean separation between AI logic and business operations.

### X. OpenAI Agents Integration
OpenAI Agents SDK must be utilized for all conversational logic implementation. This ensures sophisticated natural language processing, consistent AI behavior, and standardized agent orchestration across the AI-native application.

### XI. Stateless Architecture
Maintain a stateless architecture: Fetch conversation history from Neon DB for every request to maintain context. This ensures scalable AI interactions, consistent user experience across sessions, and reliable context restoration for AI conversations.

### XII. OpenAI ChatKit Integration
Integrate OpenAI ChatKit in the frontend for a conversational UI that interacts with the backend agent. This provides a seamless, rich chat experience that leverages the full power of the AI backend while maintaining responsive frontend performance.

## Development Workflow
All development activities must follow the Spec-Driven Development methodology with emphasis on AI-native patterns. Features must be fully specified in a spec document before any implementation work begins. This includes acceptance criteria, edge cases, AI interaction flows, and testing requirements. The workflow must incorporate AI-native architecture considerations, security protocols, modern UI/UX standards, MCP server integration, and OpenAI agent patterns as mandatory elements of all feature specifications.

## Quality Standards
Code quality is maintained through automated generation, consistent AI-native architecture patterns, strict process adherence, and compliance with AI integration best practices. All code must pass through the Claude Code generation process to ensure compliance with architectural standards, security protocols, AI integration patterns, and UI/UX guidelines. Automated testing must cover AI agent interactions, MCP server communications, database interactions, and responsive UI components.

## Governance
This constitution supersedes all other development practices and guidelines. Any amendments to this constitution must be documented, approved, and include a migration plan for existing code and processes. All pull requests and code reviews must verify compliance with these principles, particularly regarding AI-native architecture, security protocols, MCP server implementation, OpenAI agent integration, frontend standards, and UI/UX requirements. Migration from Phase II to Phase III principles must be completed systematically with appropriate testing and validation procedures in place.

**Version**: 3.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07