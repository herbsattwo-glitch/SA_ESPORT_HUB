
---

### `docs/CASE_DOCUMENT.md`

```markdown
# SA Esports Hub — Case Document

**Project Type:** Full-Stack Web Application  
**Framework:** Django 4.2  
**Theme:** Xbox  
**Scope:** South African Esports Infrastructure  
**Document Version:** 1.0  
**Date:** 2024  

---

## 1. Executive Summary

South Africa has a rapidly growing competitive gaming community spanning
titles such as EA FC (FIFA), Call of Duty, Tekken 8, Street Fighter 6,
Killer Instinct, and Forza Horizon 6. Despite this growth, the ecosystem
lacks unified infrastructure: there is no single platform where leagues
are registered, players are ranked nationally, or scouts can evaluate
emerging talent.

SA Esports Hub is a Django-based web application that fills this gap. It
provides league organisers, players, and scouts with a shared digital space
to run, track, and grow South African competitive gaming.

---

## 2. Problem Statement

### 2.1 Current State

| Problem | Impact |
|---|---|
| Leagues run on Discord/WhatsApp with no persistent records | Results are lost; history cannot be referenced |
| No national ranking system | Players cannot prove their standing to sponsors |
| No formal scouting layer | Talent development is entirely word-of-mouth |
| Province-level isolation | Players in Limpopo never interact with Western Cape scene |
| No registration management | Organisers manually track sign-ups in spreadsheets |

### 2.2 Affected Stakeholders

- **Players** — Cannot build a verifiable competitive resume.
- **League Organisers** — Spend excessive time on administration.
- **Scouts / Coaches** — Have no structured way to evaluate or compare players.
- **Sponsors** — Cannot assess the size or quality of the SA esports market.

---

## 3. Objectives

1. Provide a unified authentication system linking real identities to Xbox Gamertags.
2. Enable full CRUD lifecycle for leagues (create, browse, join, close, delete).
3. Maintain a live national player ranking sorted by earned points.
4. Offer a structured scouting report system with quantified ratings.
5. Ensure the platform is deployable on free-tier cloud infrastructure.
6. Deliver an Xbox-inspired visual identity that resonates with the target audience.

---

## 4. Scope

### 4.1 In Scope

- User registration and authentication (custom forms + Django auth)
- UserProfile with Gamertag, role, and province
- League management (full CRUD + registration + match results)
- Player directory with rankings and stats
- Scouting report submission and display
- Responsive Xbox-themed frontend (Bootstrap 5 + custom CSS)
- Admin panel via Django admin
- SQLite database (development)
- Static file serving via WhiteNoise
- Deployment configuration (Gunicorn + Render)

### 4.2 Out of Scope (Future Phases)

- Real-time match streaming or score updates via WebSockets
- Payment gateway for prize pools
- Mobile native applications
- Integration with Xbox Live API
- Automated bracket generation
- Team/clan management

---

## 5. System Architecture

Browser (User)
│
▼
Django Views (Function-Based)
│
├── accounts/ ──► UserProfile Model ──► SQLite DB
├── leagues/ ──► League, Match, LeagueRegistration Models
└── players/ ──► Player, ScoutingReport Models
│
▼
Django Templates (Jinja-style, Xbox Themed)
│
▼
Static Files (CSS / JS via WhiteNoise)



---

## 6. Data Models

### 6.1 accounts

| Model | Key Fields |
|---|---|
| `UserProfile` | `user (FK)`, `gamertag`, `role`, `province`, `avatar` |

### 6.2 leagues

| Model | Key Fields |
|---|---|
| `League` | `name`, `game`, `organizer (FK)`, `status`, `format`, `start_date`, `prize_pool` |
| `LeagueRegistration` | `league (FK)`, `player (FK)`, `status` |
| `Match` | `league (FK)`, `player_one (FK)`, `player_two (FK)`, `winner (FK)`, `scores` |

### 6.3 players

| Model | Key Fields |
|---|---|
| `Player` | `user (FK)`, `primary_game`, `skill_tier`, `ranking_points`, `wins`, `losses` |
| `ScoutingReport` | `player (FK)`, `scout (FK)`, `overall_rating`, `mechanics_rating`, `notes` |

---

## 7. Authentication System

The platform uses Django's built-in `django.contrib.auth` system extended
with a custom `UserProfile` model.

### 7.1 Registration Flow

User fills XboxRegistrationForm
│
▼
Form validates (Gamertag uniqueness, password strength)
│
▼
User object created (django.contrib.auth.User)
│
▼
UserProfile created (linked via OneToOneField)
│
▼
User logged in automatically (login(request, user))
│
▼
Redirect to home with success message



### 7.2 Permission Model

| Action | Requirement |
|---|---|
| Browse leagues / players | Public (no login required) |
| Register for a league | Authenticated |
| Create a league | Authenticated |
| Edit/Delete own league | Authenticated + Is Organiser |
| Edit/Delete any league | Staff / Superuser |
| Create player profile | Authenticated |
| Edit own player profile | Authenticated + Is Owner |
| Submit scouting report | Authenticated + Not same as target |
| Admin panel | Superuser |

---

## 8. CRUD Operations Summary

| Resource | Create | Read | Update | Delete |
|---|---|---|---|---|
| League | ✅ Organiser | ✅ Public | ✅ Organiser/Staff | ✅ Organiser/Staff |
| Player Profile | ✅ Any user | ✅ Public | ✅ Owner/Staff | ✅ Owner/Staff |
| Scouting Report | ✅ Any (once) | ✅ Public | ❌ | ❌ |
| Match Result | ✅ Organiser | ✅ Public | ❌ | ❌ |
| User Profile | ✅ (on register) | ✅ Public | ✅ Owner | ❌ |

---

## 9. User Roles

| Role | Description | Key Capabilities |
|---|---|---|
| Spectator | Default role. Browser only. | View leagues, view players |
| Player | Active competitor. | Create player profile, join leagues |
| Scout | Talent evaluator. | Submit scouting reports |
| Organiser | League manager. | Create and manage leagues |
| Staff/Admin | Platform admin. | Full access via admin panel |

---

## 10. Technology Decisions

| Decision | Rationale |
|---|---|
| Django FBVs over CBVs | More readable for teams new to Django |
| SQLite for development | Zero configuration, easy to reset during dev |
| Bootstrap 5 | Rapid responsive layout with strong component library |
| WhiteNoise | Simplest static file solution for single-dyno deployment |
| python-decouple | Keeps secrets out of source code cleanly |
| Gunicorn | Standard production WSGI server for Django |

---

## 11. Security Considerations

- CSRF protection on all POST forms (`{% csrf_token %}`)
- Django auth password validators enforced on registration
- Ownership checks before edit/delete operations
- `@login_required` decorator on all write operations
- `SECRET_KEY` managed via environment variable
- `DEBUG=False` enforced in production via decouple
- `ALLOWED_HOSTS` restricted to deployment domain

---

## 12. Deployment Guide

### Step-by-Step: Render Free Tier

1. Push code to a GitHub repository.
2. Go to [render.com](https://render.com) → New Web Service.
3. Connect your GitHub repo.
4. Configure:
   - **Build Command:**
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command:**
     ```
     gunicorn sa_esports.wsgi:application
     ```
5. Set environment variables:
   - `SECRET_KEY` — generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — `your-app.onrender.com`
6. Deploy. Render provides a free HTTPS URL.

---

## 13. Testing Checklist

### Manual Test Cases

| # | Test | Expected Result | Pass |
|---|---|---|---|
| 1 | Register with valid Gamertag | Account created, redirected home | ☐ |
| 2 | Register with duplicate Gamertag | Validation error shown | ☐ |
| 3 | Login with correct credentials | Session created, redirected | ☐ |
| 4 | Login with wrong password | Error message shown | ☐ |
| 5 | Create league (logged in) | League appears in list | ☐ |
| 6 | Create league (logged out) | Redirected to login | ☐ |
| 7 | Edit league as non-organiser | Permission error | ☐ |
| 8 | Register for league | Pending registration created | ☐ |
| 9 | Register for full league | Error: league is full | ☐ |
| 10 | Create player profile | Profile in rankings | ☐ |
| 11 | Submit scouting report | Report shows on player page | ☐ |
| 12 | Submit second report (same player) | Blocked, warning shown | ☐ |
| 13 | Scout own profile | Blocked, error shown | ☐ |
| 14 | Delete league as organiser | League removed from list | ☐ |
| 15 | Admin panel access | Staff can access /admin/ | ☐ |

---

## 14. Known Limitations & Future Work

| Limitation | Suggested Solution |
|---|---|
| SQLite not suitable for concurrent production load | Migrate to PostgreSQL on Render |
| No automated bracket generation | Integrate bracket library |
| Rankings updated manually | Add signal-based auto-recalculation |
| No email verification | Add `django-allauth` or SMTP setup |
| No real-time updates | Add Django Channels for WebSocket support |
| No team/clan system | Add `Team` model with many-to-many Players |
| No pagination | Add `django.core.paginator.Paginator` to list views |

---

## 15. Glossary

| Term | Definition |
|---|---|
| Gamertag | Xbox username used for online identity |
| LFT | Looking for Team — a status flag indicating a player wants to join a squad |
| FBV | Function-Based View — Django view written as a plain Python function |
| CRUD | Create, Read, Update, Delete — standard database operations |
| Skill Tier | Rank classification from Bronze to Grand Master |
| Scouting Report | A structured evaluation of a player submitted by a scout |
| League Organiser | User role with permission to create and manage leagues |
| SQLite | File-based relational database used during development |

---

*Document prepared for SA Esports Hub v1.0*  
*Framework: Django 4.2 | Theme: Xbox | Region: South Africa*
