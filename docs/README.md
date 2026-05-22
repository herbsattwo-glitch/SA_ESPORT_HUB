# SA Esports Hub

> South Africa's unified esports infrastructure platform — Xbox themed, Django powered.

![Django](https://img.shields.io/badge/Django-4.2-107C10?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-107C10?style=flat-square&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-107C10?style=flat-square&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-107C10?style=flat-square)

---

## What Is SA Esports Hub?

SA Esports Hub is a full-stack Django web application that solves a real
infrastructure gap in South African esports: there is no unified system for
league management, player scouting, or national rankings across the six
major titles played competitively in the country.

**Games Supported**

| Title | Genre |
|---|---|
| EA FC (FIFA) | Football Simulation |
| Call of Duty | FPS |
| Tekken 8 | Fighting |
| Street Fighter 6 | Fighting |
| Killer Instinct | Fighting |
| Forza Horizon 6 | Racing |

---

## Features

### Authentication
- Custom registration with Xbox Gamertag
- Role-based accounts (Player, Scout, Organiser, Spectator)
- Province selection (all 9 SA provinces)
- Login / Logout with session management
- Profile management with avatar upload

### League Management (Full CRUD)
- Create leagues with game type, format, dates, prize pool
- Multi-format support (single/double elimination, round robin, Swiss)
- Registration system with approval workflow
- Match result recording by organiser
- Status lifecycle: Upcoming → Active → Completed

### Player Directory & Rankings
- National ranking table sorted by points
- Skill tier system (Bronze → Grand Master)
- Game-specific filtering
- LFT (Looking for Team) flag
- Scouting availability flag

### Scouting System
- Scouts submit structured reports per player
- Four-dimension rating: Overall, Mechanics, Game Sense, Consistency
- Recommendation flag
- One report per scout per player enforced

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 |
| Database | SQLite (dev) |
| Frontend | Bootstrap 5.3 + Custom CSS |
| Icons | Bootstrap Icons 1.11 |
| Forms | django-crispy-forms |
| Static Files | WhiteNoise |
| Server | Gunicorn |
| Config | python-decouple |

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/herbsattwo-glitch/SA_ESPORT_HUB.git

cd sa-esports-hub

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables (optional for dev)
# Create a .env file in the project root:
# SECRET_KEY=your-secret-key-here
# DEBUG=True
# ALLOWED_HOSTS=localhost,127.0.0.1

# 5. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create an admin superuser
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Start the development server
python manage.py runserver

Visit http://127.0.0.1:8000 in your browser.

Admin panel: http://127.0.0.1:8000/admin/

sa_esports/
├── accounts/      # Auth, UserProfile, registration, login
├── leagues/       # League CRUD, registrations, match results
├── players/       # Player profiles, rankings, scouting reports
├── templates/     # All HTML templates (Xbox themed)
├── static/        # CSS, JS, images
├── docs/          # README and Case Document
└── sa_esports/    # Django settings, root URLs

URL Map
URL	View	Description
/	home	Landing page
/accounts/register/	register_view	New user registration
/accounts/login/	login_view	Sign in
/accounts/logout/	logout_view	Sign out
/accounts/profile/	profile_view	Edit own profile
/accounts/player/<username>/	public_profile_view	View any profile
/leagues/	league_list	Browse all leagues
/leagues/create/	league_create	Create a league
/leagues/<pk>/	league_detail	League detail
/leagues/<pk>/edit/	league_update	Edit a league
/leagues/<pk>/delete/	league_delete	Delete a league
/leagues/<pk>/register/	league_register	Join a league
/leagues/<pk>/match/	record_match	Record match result
/players/	player_list	Rankings table
/players/create/	player_create	Create player profile
/players/<pk>/	player_detail	Player detail
/players/<pk>/edit/	player_update	Edit player profile
/players/<pk>/delete/	player_delete	Delete player profile
/players/<pk>/scout/	submit_scouting_report	Submit scout report


Deployment
Render (recommended free tier)
Push your project to GitHub.
Create a new Web Service on render.com.

Set the build command:
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

Set the start command:
gunicorn sa_esports.wsgi:application

Add environment variables in the Render dashboard:
SECRET_KEY — a long random string
DEBUG — False
ALLOWED_HOSTS — your Render domain

Environment Variables Reference
Variable	Example	Description
SECRET_KEY	abc123...	Django secret key
DEBUG	False	Debug mode
ALLOWED_HOSTS	myapp.onrender.com	Allowed hostnames

Contributing
Fork the repository.
Create a feature branch: git checkout -b feature/my-feature
Commit your changes: git commit -m 'Add my feature'
Push and open a Pull Request.
License
MIT License — see LICENSE for details.

Xbox is a registered trademark of Microsoft Corporation.
This project is an independent community platform and is not affiliated with Microsoft.