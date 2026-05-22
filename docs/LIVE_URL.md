# SA Esports Hub

## Live Application Access Guide

**Document Type:** Deployment Information
**Document Version:** 1.1
**Date:** 2026

---

## What This Document Is

This document explains where to access SA Esports Hub, how to log in using the provided credentials, how to set the project up locally, and how to troubleshoot common issues. Whether you're evaluating the platform, testing features, or contributing as a developer, this guide contains everything needed to get started.

---

## Accessing the Live Application

SA Esports Hub is deployed and publicly accessible online.

### Main Website

The live application is available at:

[https://sa-esport-hub.onrender.com](https://sa-esport-hub.onrender.com)

This is the main entry point where users can browse the platform, create accounts, sign in, view leagues, and interact with the esports ecosystem.

### Admin Panel

The Django admin panel is available at:

[https://sa-esport-hub.onrender.com/admin/login/?next=/admin/](https://sa-esport-hub.onrender.com/admin/login/?next=/admin/)

The admin panel allows authorized administrators to manage users, leagues, registrations, scouting reports, matches, and all platform data.

If the website initially loads slowly or appears unavailable, the Render free hosting tier may have temporarily spun down the server due to inactivity. Wait approximately 30 seconds and refresh the page. Once the application wakes up, performance becomes significantly faster.

The deployed platform includes:

* Full Django application deployment
* PostgreSQL production database
* Optimized static asset delivery
* HTTPS encryption with SSL certificates
* Responsive design for desktop and mobile
* Production-ready admin management system

---

## Demo / Admin Credentials

The following administrative credentials are available for accessing the platform:

### Administrator Account

* **Username:** admin45
* **Email:** [admin45@gmail.com](mailto:admin45@gmail.com)
* **Password:** teddy@45

This account has full administrative privileges including:

* User management
* League and tournament management
* Match result recording
* Registration approvals
* Content moderation
* Full Django admin access

These credentials are intended strictly for demonstration and testing purposes.

---

## GitHub Repository

The full source code for SA Esports Hub is available on GitHub:

[https://github.com/herbsattwo-glitch/SA_ESPORT_HUB.git](https://github.com/herbsattwo-glitch/SA_ESPORT_HUB.git)

Developers can clone the repository, contribute improvements, submit pull requests, and report issues directly through GitHub.

---

## Setting Up Locally

To run SA Esports Hub locally, ensure you have the following installed:

* Python 3.10 or higher
* Git
* pip package manager

### Step 1 — Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/herbsattwo-glitch/SA_ESPORT_HUB.git
cd SA_ESPORT_HUB
```

### Step 2 — Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Apply Database Migrations

```bash
python manage.py migrate
```

### Step 5 — Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 6 — Run the Development Server

```bash
python manage.py runserver
```

Visit the application locally at:

* [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Deployment Information

SA Esports Hub is deployed on Render using Django and PostgreSQL.

### Technology Stack

* Python 3.10
* Django 4.2.7
* PostgreSQL
* Gunicorn
* WhiteNoise
* Render Hosting Platform

### Deployment Features

* Automatic deployments from GitHub
* HTTPS enabled
* Optimized static file serving
* Production PostgreSQL database
* Responsive frontend interface
* Admin dashboard functionality

### Performance Notes

On the free Render hosting tier:

* Cold starts may take 2–3 seconds
* Warm requests typically load in under 500ms
* The server may sleep after inactivity

---

## Browser Compatibility

SA Esports Hub works on all major modern browsers including:

### Desktop Browsers

* Google Chrome
* Microsoft Edge
* Mozilla Firefox
* Safari

### Mobile Browsers

* Chrome Mobile
* Safari iOS
* Samsung Internet
* Firefox Mobile

JavaScript and cookies must be enabled for proper functionality.

---

## Troubleshooting

### Slow Initial Load

The Render free tier may spin down the application after inactivity. Wait 30 seconds and refresh.

### Login Problems

* Ensure credentials are typed correctly
* Check caps lock
* Clear browser cookies if needed
* Try an incognito/private window

### Database Errors (Local Setup)

Run:

```bash
python manage.py migrate
```

If models changed:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 404 Errors

Verify URLs are typed correctly and use lowercase paths.

### 500 Server Errors

Refresh after 30 seconds. Persistent issues may require administrator intervention.

---

## Security Notice

This platform is intended for demonstration and educational purposes.

Please avoid:

* Uploading sensitive information
* Reusing personal passwords
* Storing confidential documents

Recommended production improvements include:

* Two-factor authentication
* Login rate limiting
* Security auditing
* Backup automation
* POPIA compliance review

---

## Contact and Support

### GitHub Repository

[https://github.com/herbsattwo-glitch/SA_ESPORT_HUB.git](https://github.com/herbsattwo-glitch/SA_ESPORT_HUB.git)

For bug reports or feature suggestions:

* Open a GitHub issue
* Include reproduction steps
* Include screenshots when applicable
* Specify browser and operating system

---

## Final Notes

SA Esports Hub is an evolving esports management platform focused on supporting South African competitive gaming communities.

Features, design, deployment configuration, and credentials may change over time as development continues.

Thank you for testing and supporting SA Esports Hub.

---

*End of Live Application Document*
