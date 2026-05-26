# SA Esports Hub

## Technical Design Document (Senior Developer Edition)

**Project Name:** SA Esports Hub
**Document Type:** Technical Architecture & Engineering Design
**Audience:** Senior Developers, Technical Leads, Architects, DevOps Engineers
**Version:** 3.0
**Date:** 2026

---

# 1. Executive Summary

SA Esports Hub is a production-oriented Django platform designed to provide foundational infrastructure for the South African esports ecosystem. The system centralizes player discovery, tournament operations, scouting workflows, rankings, and esports administration into a unified web application.

The platform addresses several structural problems currently present in South African esports:

* Fragmented tournament operations
* Non-persistent player data
* Lack of discoverable talent infrastructure
* No unified ranking ecosystem
* No standardized scouting workflow
* Weak historical data retention
* Minimal operational tooling for organizers

From an engineering perspective, the system demonstrates:

* Modular Django application architecture
* Relational domain modeling
* Role-based authorization
* Multi-entity workflow orchestration
* Production deployment practices
* Server-side rendered responsive frontend design
* Scalable application structuring suitable for future service decomposition

The current implementation prioritizes:

* Rapid feature delivery
* Maintainability
* Conventional Django best practices
* Production deployability
* Extensibility for future platform scaling

---

# 2. Architectural Philosophy

The platform intentionally follows a **monolithic modular architecture** using Django’s MVT pattern instead of microservices.

This decision was made because:

| Consideration             | Decision                       |
| ------------------------- | ------------------------------ |
| Team size                 | Small / solo development       |
| Infrastructure complexity | Kept intentionally low         |
| Deployment simplicity     | Single deployable unit         |
| Feature velocity          | Faster iteration cycles        |
| Operational overhead      | Minimal                        |
| Cost efficiency           | Optimized for Render free tier |

The application is logically separated into bounded domains using Django apps:

| Domain            | Responsibility                     |
| ----------------- | ---------------------------------- |
| `accounts`        | Identity, profiles, authentication |
| `players`         | Competitive ecosystem              |
| `leagues`         | Tournament management              |
| `core` (implicit) | Shared infrastructure              |

Although deployed as a monolith, the architecture intentionally preserves clear domain boundaries so future extraction into services remains viable.

Potential future service decomposition:

| Future Service       | Extracted From            |
| -------------------- | ------------------------- |
| Auth Service         | `accounts`                |
| Tournament Service   | `leagues`                 |
| Ranking Engine       | `players`                 |
| Analytics Service    | reporting modules         |
| Media Service        | uploads/static processing |
| Notification Service | async messaging layer     |

---

# 3. High-Level System Architecture

## Runtime Request Flow

```text
Browser
   ↓
HTTPS Request
   ↓
Render Edge Network
   ↓
Gunicorn WSGI Workers
   ↓
Django Application
   ↓
URL Router
   ↓
View Layer
   ↓
Business Logic
   ↓
Django ORM
   ↓
PostgreSQL
   ↓
Template Rendering
   ↓
HTTP Response
```

---

## Architectural Layers

### Presentation Layer

Responsibilities:

* HTML rendering
* Bootstrap UI composition
* Form rendering
* User interaction
* Client-side animation logic

Technologies:

* Django Templates
* Bootstrap 5.3
* Vanilla JavaScript
* Crispy Forms

---

### Application Layer

Responsibilities:

* Request handling
* Authorization
* Validation
* Domain orchestration
* Workflow execution

Technologies:

* Django Views
* Middleware
* Form classes
* Decorators

---

### Domain Layer

Responsibilities:

* Business rules
* Tournament logic
* Ranking state
* Scouting constraints
* Registration lifecycle

Technologies:

* Django Models
* ORM relationships
* Model methods
* Signals (future candidate)

---

### Persistence Layer

Responsibilities:

* Data durability
* Relational integrity
* Query optimization
* Transaction consistency

Technologies:

* PostgreSQL
* SQLite (development)
* Django ORM

---

# 4. Domain-Driven Breakdown

## 4.1 Accounts Domain

### Responsibilities

The accounts domain manages:

* Authentication
* User identity
* Role assignment
* Province metadata
* Avatar management
* Public-facing user information

---

## Core Model: UserProfile

### Relationship Strategy

```python
UserProfile -> OneToOne(User)
```

Django’s built-in `User` model is extended instead of replaced.

### Rationale

Benefits:

* Leverages Django auth ecosystem
* Avoids custom auth complexity
* Maintains admin compatibility
* Simplifies migrations
* Retains third-party package compatibility

Tradeoff:

* Requires joins for profile access

Accepted due to manageable scale.

---

## Role System

Current roles:

```python
PLAYER
SCOUT
ORGANIZER
SPECTATOR
ADMIN
```

### Authorization Model

Authorization currently combines:

* Django permissions
* Ownership checks
* Role inspection
* View decorators

Example:

```python
@login_required
def league_create(request):
    if request.user.userprofile.role != "ORGANIZER":
        return HttpResponseForbidden()
```

### Future Recommendation

Move toward:

* Policy-based authorization
* Permission matrix abstraction
* Centralized access-control service

---

# 5. Players Domain

The players domain represents the competitive ecosystem.

Core responsibilities:

* Competitive profiles
* Ranking visibility
* Talent discovery
* Scouting workflows
* Availability signaling

---

## Core Entity: Player

### Key Design Decision

A `Player` entity exists separately from `UserProfile`.

### Why?

Not every user is a competitor.

Examples:

* Organizers
* Scouts
* Spectators

This separation:

* Avoids null-heavy schemas
* Keeps competitive metadata isolated
* Improves domain clarity

---

## Ranking System

Current ranking system:

* Manually maintained ranking points
* Ordered leaderboard queries
* Public visibility

Current query pattern:

```python
Player.objects.order_by("-ranking_points")
```

---

## Future Ranking Engine

Current implementation intentionally leaves room for a future ELO/MMR engine.

Potential architecture:

```text
Match Result
   ↓
Ranking Processor
   ↓
ELO Calculation
   ↓
Player Rating Update
   ↓
Historical Snapshot
```

Potential improvements:

* ELO
* Glicko-2
* Bayesian ranking systems
* Seasonal ladders
* Regional rankings
* Match-weighted scoring

---

## Scouting System

### Core Entity: ScoutingReport

```python
Scout -> Player
```

### Constraint

One scout report per scout per player.

Implemented via:

```python
UniqueConstraint(
    fields=["scout", "player"]
)
```

### Why This Matters

Prevents:

* Rating spam
* Artificial inflation
* Duplicate evaluations
* Scout abuse

---

## Scouting Metrics

Current metrics:

* Mechanics
* Game Sense
* Consistency
* Overall

These are intentionally decomposed dimensions rather than a single scalar score.

This allows:

* Statistical analysis
* Future ML profiling
* Scout reliability weighting
* Comparative talent analytics

---

# 6. Leagues Domain

The leagues domain manages tournament operations.

---

## Core Entities

| Entity               | Purpose                 |
| -------------------- | ----------------------- |
| `League`             | Tournament metadata     |
| `LeagueRegistration` | Participation lifecycle |
| `Match`              | Competitive outcomes    |

---

# 6.1 League Entity

## Supported Formats

```python
SINGLE_ELIMINATION
DOUBLE_ELIMINATION
ROUND_ROBIN
SWISS
GROUP_STAGE
```

### Design Consideration

Formats are enum-driven to support:

* Validation safety
* UI consistency
* Future bracket engines

---

## League Lifecycle

```text
UPCOMING
   ↓
ACTIVE
   ↓
COMPLETED
```

Alternative states:

* CANCELLED
* ARCHIVED (future)

---

## Registration Workflow

### Current Flow

```text
Player Registers
   ↓
Pending Approval
   ↓
Organizer Review
   ↓
Approved / Rejected
```

### Why Manual Approval?

Prevents:

* Bracket pollution
* Fake registrations
* Skill mismatches
* Spam entries

---

# 6.2 Match System

The current match system stores:

* Participants
* Scores
* Winner
* League relationship
* Recorded timestamps

---

## Future Expansion Candidates

### Bracket Engine

Potential future architecture:

```text
League
   ↓
Bracket Generator
   ↓
Round Builder
   ↓
Match Nodes
   ↓
Result Propagation
```

---

### Real-Time Match Updates

Current architecture is synchronous request/response.

Future:

* Django Channels
* Redis Pub/Sub
* WebSocket broadcasts
* Live brackets

---

# 7. Database Architecture

## Current Databases

| Environment | Database   |
| ----------- | ---------- |
| Development | SQLite     |
| Production  | PostgreSQL |

---

# 7.1 Why PostgreSQL?

PostgreSQL was selected because:

* Strong relational integrity
* Excellent indexing support
* JSON support for future extensibility
* Transaction reliability
* Mature production tooling
* Future analytics compatibility

---

# 7.2 ORM Strategy

The system uses Django ORM exclusively.

### Why?

Benefits:

* Rapid development
* Migration management
* Query abstraction
* Security protections
* Cross-database portability

Tradeoffs:

* Reduced SQL-level optimization
* ORM abstraction overhead

Acceptable at current scale.

---

# 7.3 Query Optimization Opportunities

Future improvements:

* `select_related`
* `prefetch_related`
* query caching
* Redis caching
* materialized ranking views
* pagination optimization

Potential bottlenecks:

* ranking aggregation
* league participant queries
* scouting joins

---

# 8. Frontend Engineering

The frontend intentionally avoids React/Vue.

---

## Why Server-Side Rendering?

Benefits:

* Faster initial delivery
* Lower JS payload
* Better SEO
* Simpler deployment
* Reduced hydration complexity
* Lower maintenance overhead

Tradeoff:

* Less reactive UI

Accepted due to project scope.

---

# 8.1 UI Stack

| Layer     | Technology       |
| --------- | ---------------- |
| Layout    | Bootstrap 5.3    |
| Icons     | Bootstrap Icons  |
| Forms     | Crispy Forms     |
| Animation | Vanilla JS       |
| Fonts     | Rajdhani + Inter |

---

# 8.2 Animation System

The platform includes:

* particle rendering
* mesh gradients
* hover transitions
* animated counters
* scanline effects

### Performance Considerations

Animations rely primarily on:

* `transform`
* `opacity`

Avoided:

* layout thrashing
* repaint-heavy effects

---

# 8.3 Accessibility

Implemented:

* reduced-motion support
* semantic HTML
* responsive layouts
* keyboard-safe navigation

Future improvements:

* ARIA audit
* contrast compliance audit
* screen reader testing

---

# 9. Security Architecture

---

## Authentication

Uses Django session authentication:

* PBKDF2 password hashing
* CSRF protection
* secure session cookies
* authentication middleware

---

## Authorization

Current enforcement:

* `@login_required`
* ownership checks
* role restrictions

---

## File Upload Security

Avatar uploads currently rely on:

* Pillow validation
* Django media handling

Future recommendations:

* MIME validation
* image scanning
* CDN-backed storage
* upload size throttling

---

## Production Security Recommendations

Not yet implemented but recommended:

| Feature               | Priority |
| --------------------- | -------- |
| 2FA                   | High     |
| Rate limiting         | High     |
| CSP headers           | Medium   |
| S3 media isolation    | Medium   |
| Audit logging         | High     |
| Admin IP restrictions | Medium   |
| Redis session backend | Medium   |

---

# 10. Deployment Architecture

## Hosting Platform

Current deployment:

* Render.com

---

## Runtime Stack

```text
Render
   ↓
Gunicorn
   ↓
Django WSGI
   ↓
PostgreSQL
```

---

## Static Asset Pipeline

Handled by:

* WhiteNoise
* collectstatic

Benefits:

* no external CDN dependency
* simplified deployment
* compressed asset serving

---

## Environment Variables

```env
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
DATABASE_URL=
```

Managed through:

* Render environment dashboard
* `python-decouple`

---

# 11. Scalability Considerations

Current architecture is suitable for:

* MVP scale
* regional esports platforms
* low-to-medium concurrency

---

## Current Constraints

Potential scaling limitations:

| Area            | Limitation            |
| --------------- | --------------------- |
| WSGI            | no async support      |
| SQLite dev      | non-concurrent writes |
| Media storage   | local filesystem      |
| Ranking queries | uncached              |
| Live updates    | polling only          |

---

## Recommended Scaling Roadmap

### Phase 1

* Redis caching
* PostgreSQL optimization
* query tuning
* CDN integration

### Phase 2

* Celery background workers
* async notifications
* task queues

### Phase 3

* WebSockets
* real-time tournaments
* live standings

### Phase 4

* Service extraction
* Kubernetes deployment
* event-driven architecture

---

# 12. Engineering Practices

## Current Standards

Implemented:

* modular app structure
* environment separation
* migration-based schema management
* REST-like URL patterns
* reusable templates

---

## Recommended Improvements

### Testing

Current project lacks comprehensive testing.

Recommended:

* pytest
* factory_boy
* integration tests
* coverage enforcement

---

### CI/CD

Recommended:

* GitHub Actions
* automated linting
* security scans
* deployment pipelines

---

### Code Quality

Recommended tooling:

* black
* isort
* flake8
* mypy
* bandit

---

# 13. Observability & Monitoring

Current observability is minimal.

Recommended additions:

| Capability        | Tool        |
| ----------------- | ----------- |
| Error tracking    | Sentry      |
| Metrics           | Prometheus  |
| Dashboards        | Grafana     |
| Log aggregation   | Loki        |
| Uptime monitoring | UptimeRobot |

---

# 14. Future Platform Evolution

---

## Real-Time Infrastructure

Potential stack:

* Django Channels
* Redis
* WebSockets

Use cases:

* live brackets
* match notifications
* live standings
* activity feeds

---

## API Layer

Future API strategy:

* Django REST Framework
* JWT authentication
* rate limiting
* public developer APIs

Potential consumers:

* mobile apps
* third-party tournament systems
* sponsor dashboards

---

## Analytics Layer

Future analytics possibilities:

* province participation heatmaps
* talent progression tracking
* tournament engagement metrics
* sponsorship analytics
* player growth curves

---

## AI/ML Possibilities

Potential future systems:

* talent prediction
* fraud detection
* smurf detection
* matchmaking recommendations
* scout reliability scoring

---

# 15. Technical Debt Assessment

---

## Acceptable Debt

Current technical debt is intentionally acceptable because:

* project maturity is early-stage
* feature validation matters more than optimization
* architecture remains clean enough for refactoring

---

## Highest Priority Improvements

| Priority | Improvement           |
| -------- | --------------------- |
| High     | Automated testing     |
| High     | Async job processing  |
| High     | Rate limiting         |
| Medium   | Redis caching         |
| Medium   | API abstraction       |
| Medium   | Bracket engine        |
| Low      | Service decomposition |

---

# 16. Conclusion

SA Esports Hub is more than a CRUD application — it is a domain-oriented competitive gaming infrastructure platform built using pragmatic engineering decisions optimized for maintainability, deployability, and future scalability.

The system demonstrates:

* production Django architecture
* relational domain modeling
* modular application design
* secure authentication practices
* scalable domain separation
* operational deployment knowledge

Most importantly, the architecture intentionally leaves room for future evolution into:

* real-time tournament systems
* advanced ranking engines
* analytics infrastructure
* mobile ecosystems
* continental esports infrastructure

The platform establishes a credible technical foundation for building a national esports ecosystem at scale.

---

# Appendix A — Technology Stack

| Category         | Technology          |
| ---------------- | ------------------- |
| Backend          | Django 4.2.7        |
| Language         | Python 3.10+        |
| Database         | PostgreSQL / SQLite |
| Frontend         | Bootstrap 5.3       |
| Forms            | django-crispy-forms |
| Static Files     | WhiteNoise          |
| Server           | Gunicorn            |
| Hosting          | Render              |
| Image Processing | Pillow              |
| Config           | python-decouple     |

---

# Appendix B — Suggested Enterprise Roadmap

| Stage | Objective                          |
| ----- | ---------------------------------- |
| MVP   | Core esports workflows             |
| V2    | Real-time tournaments              |
| V3    | Mobile ecosystem                   |
| V4    | Analytics platform                 |
| V5    | Continental infrastructure         |
| V6    | Public APIs & partner integrations |

---

# Appendix C — Suggested Production Architecture (Future)

```text
Client Apps
   ↓
CDN / Edge Layer
   ↓
Load Balancer
   ↓
API Gateway
   ↓
Auth Service
Tournament Service
Ranking Service
Notification Service
Analytics Service
   ↓
Redis / PostgreSQL / Object Storage
```

---

**End of Technical Design Document**
**SA Esports Hub — Engineering the Infrastructure Layer of South African Esports**
