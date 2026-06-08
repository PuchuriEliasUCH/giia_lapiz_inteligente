# AGENTS.md

## Purpose

This repository contains the backend implementation of the Smart Pencil project.

Before making architectural, database, API, or implementation decisions, read the following documents:

* ./lib/BUSINESS_CONTEXT.md
* ./lib/ARCHITECTURE.md
* ./lib/DATABASE.md
* ./lib/API.md
* ./lib/MQTT.md
* ./lib/DEVELOPMENT.md

---

## Scope

This repository is backend-only.

Allowed responsibilities:

* FastAPI
* SQLAlchemy 2.0
* MySQL 8
* Alembic
* JWT Authentication
* MQTT Integration (server-side only)
* WebSockets (server-side only)
* Session Processing
* Metrics Calculation
* Data Persistence
* Docker
* Automated Testing

Not allowed:

* Android
* Kotlin
* React Native
* Flutter
* ESP32
* BLE
* Embedded Systems
* Hardware Design
* Sensor Configuration
* Electronics
* UI/UX Design

External systems must be treated as integration points.

---

## Development Principles

* Async-first development.
* Route → Service → ORM architecture.
* Business logic belongs in services.
* SQLAlchemy 2.0 conventions only.
* Prefer existing project patterns.
* Avoid unnecessary abstractions.
* Respect existing architectural decisions.
* **All functionality is restricted to registered users.** Every endpoint (HTTP, WebSocket, MQTT data ingestion) operates under an authenticated user context. Only `GET /health` and `POST /auth/*` are public. Resources must be validated as owned by the requesting user before any read or write operation.

---

## Quality Requirements

Before considering a task complete:

black .
pytest

must pass successfully.

---

## Priority Order

1. Authentication
2. Children Management
3. Exercise Management
4. Session Management
5. MQTT Integration
6. Metrics Processing
7. WebSocket Feedback
8. Dataset Generation
9. Rule-Based AI
10. Machine Learning

Machine Learning is never a priority over data quality.

---

## Decision Making

Before introducing a new dependency, framework, pattern, or architecture:

1. Reuse existing solutions.
2. Prefer simplicity.
3. Avoid overengineering.
4. Maintain consistency with the current codebase.
5. Justify breaking changes.
