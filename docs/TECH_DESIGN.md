# SA Esports Hub
## Technical Design Document

**Project Name:** SA Esports Hub  
**Document Type:** Technical Architecture  
**Document Version:** 1.0  
**Date:** 2024  

---

## What This Document Is

This document explains how SA Esports Hub is built from a technical standpoint. It covers the architecture, code structure, database design, security measures, and deployment setup. If you're a developer, technical reviewer, or system architect, this document gives you everything you need to understand the system.

---

## System Overview

SA Esports Hub is a full-stack web application built with the Django framework. It follows Django's standard MVT (Model-View-Template) architectural pattern and uses a relational database to manage all competitive gaming data.

The platform is structured into three main Django apps that work together. The accounts app handles all authentication and user profile management. The leagues app manages tournaments, registrations, and match results. The players app handles competitive player profiles and the scouting system. Each app is self-contained but they share data through Django's ORM and foreign key relationships.

At the highest level, the system works like this. A user opens their web browser and visits the site. The browser sends an HTTPS request to the Django application server. Django's URL router determines which view function should handle the request. The view function processes the business logic, queries the database through the ORM, and returns an HTML template populated with data. The browser receives the rendered HTML and displays it to the user. For dynamic interactions like button clicks, animations, and form submissions, vanilla JavaScript handles the frontend behavior without requiring any additional framework.

---

## Technology Stack

The platform uses Django 4.2.7 as its backend framework because Django provides a complete batteries-included approach with built-in ORM, authentication, admin panel, and security features. Python 3.10 or higher is required for the language runtime.

For the database, the development environment uses SQLite which requires zero configuration and stores data in a single file. The production environment uses PostgreSQL 14 or higher because it scales better under load and supports concurrent connections.

On the frontend, Bootstrap 5.3.2 provides the responsive grid system and base components. Bootstrap Icons 1.11 handles all iconography throughout the site. Two Google Fonts are loaded — Inter for body text and Rajdhani for headings — to give the site a premium gaming aesthetic.

For production deployment, WhiteNoise 6.6.0 serves compressed static files directly from the Django application without requiring a separate web server. Gunicorn 21.2.0 is the WSGI HTTP server that runs the Django application in production. python-decouple 3.8 manages environment variables so secrets never get committed to source code.

Several additional packages support specific features. Pillow 10.1.0 handles image processing for user avatars and league banner uploads. django-crispy-forms 2.1 with crispy-bootstrap5 0.7 renders Django forms with Bootstrap styling.

---

## Project Structure

The project is organized into a clean, maintainable structure that follows Django conventions. At the root level, there's a settings folder called sa_esports that contains the main project configuration including settings.py, urls.py, the WSGI entry point, and a custom admin module.

The accounts app contains the authentication logic. Its models.py defines the UserProfile model that extends Django's built-in User. The forms.py file contains the registration form with Gamertag validation, the styled login form, and the profile update forms. The views.py handles registration, login, logout, profile viewing, and profile updates. The urls.py maps URL patterns starting with /accounts/ to the appropriate views.

The leagues app manages everything tournament-related. The models.py defines three models — League for the tournaments themselves, LeagueRegistration for tracking who signed up, and Match for storing individual match results. The views.py implements full CRUD operations including listing, creating, viewing, editing, deleting, and the registration workflow. The forms.py contains league creation forms, search and filter forms, and the match result recording form.

The players app handles competitive player profiles. The Player model in models.py stores game-specific stats and rankings. The ScoutingReport model stores structured player evaluations. The views.py supports player CRUD plus the scouting report submission workflow.

Templates are organized in a top-level templates folder with subdirectories for each app. The base.html template provides the master layout with the navbar, footer, and animated background containers. Each app has its own subfolder containing list views, detail views, form pages, and confirmation dialogs.

Static assets live in a top-level static folder. The xbox_theme.css file contains all custom styling including the animated background system and glassmorphic effects. The main.js file handles the particle network animation, scroll animations, counter animations, and button ripple effects.

User-uploaded files like avatars and league banners go into the media folder which is served separately from static files.

---

## Database Schema

The database design centers around Django's built-in User model which handles authentication. Every User has a corresponding UserProfile through a one-to-one relationship. The UserProfile stores the Xbox Gamertag, avatar image, role (player, scout, organizer, or spectator), South African province, biography, and Xbox profile URL.

A user can optionally create a Player profile through another one-to-one relationship. The Player model stores their primary competitive game, skill tier ranging from Bronze through Grand Master, ranking points, national rank, wins, losses, draws, tournament wins, scouting availability flag, looking-for-team flag, and a URL to their highlight reel.

The League model has a foreign key to User identifying the organizer. Each league stores its name, game type, description, format (single elimination, double elimination, round robin, Swiss system, or group stage), status (upcoming, active, completed, or cancelled), maximum participant count, prize pool in South African Rand, start and end dates, registration deadline, banner image, and rules text.

LeagueRegistration is a junction model connecting Users to Leagues. Each registration tracks its status (pending, approved, rejected, or withdrawn), timestamp, and optional notes. A unique constraint ensures a user can only register once per league.

The Match model records individual matches within a league. It references the league, both players, the winner, the scores for each player, the round number, when it was played, and whether it's marked as completed.

ScoutingReport connects scouts to players. Each report stores four ratings from 1 to 10 covering overall skill, mechanics, game sense, and consistency. It includes notes from the scout and a recommendation flag. A unique constraint prevents a scout from submitting multiple reports on the same player.

All models include created_at and updated_at timestamps for audit purposes. Foreign keys use CASCADE deletion where appropriate so deleting a league removes its registrations and matches, but uses SET_NULL for the match winner so deleting a user doesn't destroy match history.

---

## Authentication and Authorization

Authentication uses Django's built-in session-based system extended with the custom UserProfile model. The registration flow validates the form data including Gamertag uniqueness, creates a new User object, automatically creates the linked UserProfile, logs the user in, and redirects to the home page with a success message.

The login flow uses Django's authenticate function to verify credentials, creates a session, and redirects either to the originally requested page or to the home page. Logout requires a POST request for security, destroys the session, and redirects to the login page.

Authorization is enforced through a combination of Django's @login_required decorator and ownership checks within views. Public actions like browsing leagues and viewing player profiles require no authentication. Write actions like creating leagues, registering for tournaments, and submitting scouting reports require an authenticated user. Edit and delete actions on specific resources additionally verify that the requesting user is either the owner of the resource or has staff privileges.

Specifically, league editing and deletion is restricted to the organizer who created the league or any staff user. Player profile editing is restricted to the profile owner or staff. Scouting reports prevent users from scouting themselves and limit each scout to one report per player. The Django admin panel at /admin/ requires staff or superuser permissions.

Security measures include CSRF tokens on every POST form, password hashing with Django's PBKDF2 algorithm, secure session cookies, HTTPS enforcement in production, and protection against XSS and SQL injection through Django's template auto-escaping and ORM parameterization. The SECRET_KEY is managed via environment variables using python-decouple so it never appears in source code. The ALLOWED_HOSTS setting restricts which domains can serve the application in production.

---

## URL Routing

The URL structure follows RESTful conventions. The root URL serves the home page. Authentication URLs live under /accounts/ including /register/, /login/, /logout/, /profile/, and /player/<username>/ for viewing any user's public profile.

League URLs live under /leagues/ with the index showing all leagues, /create/ for the creation form, /<pk>/ for league details, /<pk>/edit/ for editing, /<pk>/delete/ for deletion, /<pk>/register/ for joining, and /<pk>/match/ for recording match results.

Player URLs follow the same pattern under /players/ with /, /create/, /<pk>/, /<pk>/edit/, /<pk>/delete/, and /<pk>/scout/ for submitting scouting reports.

The admin panel is mounted at /admin/ with all standard Django admin URLs underneath.

Media files (user uploads) are served from /media/ in development. In production, this would typically move to cloud storage like AWS S3 or Cloudinary.

---

## Frontend Architecture

The visual design follows an Xbox-inspired dark theme using #0E0E0E as the primary background and Xbox Green #107C10 as the accent color. Typography combines Rajdhani for headings (which gives a gaming aesthetic) with Inter for body text (for readability). The entire interface uses a mobile-first responsive approach through Bootstrap 5's grid system.

The signature visual feature is a multi-layered animated background system that runs behind every page. Five distinct layers create the immersive effect. The first layer is a mesh gradient using shifting radial gradients with a 20-second animation loop. The second is a subtle dot grid that drifts diagonally on a 30-second loop with a radial mask to fade at the edges. The third layer consists of three floating green orbs blurred with CSS filters, each moving on independent paths with durations between 25 and 35 seconds. The fourth layer is a JavaScript canvas containing 80 particle dots that connect to nearby dots with thin lines and respond to mouse movement by repelling from the cursor. The fifth layer is a green horizon line that sweeps from top to bottom every 8 seconds.

All cards, panels, and the navbar use glassmorphism with backdrop-filter blur applied to semi-transparent backgrounds. This creates a frosted glass effect that lets the animated background show through subtly.

Interactive elements have layered animations. Buttons display a ripple effect on click, scale up slightly on hover, and have a glowing shadow. Stat cards animate their numbers from zero to the target value when scrolled into view. Player cards have a green accent bar that slides in from the left on hover. Active league status badges pulse with a soft glow.

Performance is carefully managed. CSS animations exclusively use transform and opacity properties which the browser can hardware-accelerate. The prefers-reduced-motion media query disables all animations for users with motion sensitivity. The particle canvas uses requestAnimationFrame for smooth 60fps animation. Backdrop blur is applied selectively only where needed to avoid expensive recalculations.

---

## CRUD Operations

The platform implements full Create, Read, Update, and Delete operations across all major resources, with appropriate permission checks for each operation.

User accounts can be created by anyone through the registration form, read publicly through profile pages, updated only by the owner, and deleted only by staff. User profiles are created automatically when a user registers and updated through the profile edit page.

Leagues can be created by any authenticated user who becomes the organizer. Reading league details is public. Updating and deleting a league requires being either the organizer or a staff member. The same permission pattern applies to player profiles.

League registrations are created by authenticated users joining a tournament. Reading them is public. Updating registration status (approving or rejecting) requires staff permissions. Match results can be recorded by the league organizer and edited or deleted by staff.

Scouting reports can be submitted by any authenticated user but with two important restrictions. A user cannot scout themselves, and each scout can only submit one report per player. This ensures fair, balanced evaluations and prevents abuse.

---

## Custom Admin Panel

The Django admin panel has been completely redesigned with a custom Xbox-themed interface that maintains all of Django's powerful functionality while providing a much better user experience.

The dashboard greets administrators with a personalized welcome message and a live clock that updates every second. Four animated stat cards show the current count of active leagues, ranked players, registered users, and scouting reports. Each card has an animated counter that ticks up from zero on page load and links directly to the corresponding management page.

A quick actions panel provides six one-click shortcuts for the most common administrative tasks — create league, add player, new user, log match, approve signups, and manage profiles. This dramatically reduces the clicks required for routine work.

The left sidebar contains a permanently visible navigation grouped into three sections. Overview includes the dashboard and a link to view the live site. Esports Hub contains leagues, registrations, matches, players, and scout reports. Members contains users, profiles, and groups.

A real-time activity feed on the right shows the latest 12 admin actions across the entire platform, color-coded by action type. Green dots indicate additions, yellow dots indicate modifications, and red dots indicate deletions. Each entry shows the affected object, the content type, and how long ago the action occurred.

The entire admin interface uses the same glassmorphic design language as the user-facing site, including the animated mesh gradient, floating orbs, particle network, and scan line effects. All form pages have been styled with the dark theme while preserving Django's built-in form rendering and validation.

---

## Deployment Architecture

The application deploys to Render.com's free tier which provides automatic HTTPS, continuous deployment from GitHub, and a managed PostgreSQL database. The deployment pipeline starts when code is pushed to the main branch of the GitHub repository. Render automatically detects the change, runs the build command which installs Python dependencies, collects static files with WhiteNoise compression, and applies any pending database migrations. After a successful build, Render starts the application using Gunicorn as the WSGI server.

Environment variables manage all secrets and environment-specific settings. SECRET_KEY contains a strong random string generated separately for production. DEBUG is set to False to prevent error pages from leaking sensitive information. ALLOWED_HOSTS restricts which domain names can serve the application. These variables are configured in Render's dashboard rather than in source code.

The free tier has a few characteristics worth noting. After 15 minutes of inactivity, the service spins down and the next request takes 2 to 3 seconds for a cold start. Subsequent requests are fast (typically under 500ms). The database is limited to 256MB which is plenty for thousands of users and matches. Media file storage is limited to 1GB for the entire application.

For higher traffic or larger media needs, the platform can scale to Render's paid tiers which provide always-on instances, larger databases, and dedicated resources. The Django architecture supports horizontal scaling through additional Gunicorn workers and can be adapted to use cloud storage services like AWS S3 for media files.

---

## Testing Approach

Manual testing has verified all core functionality. The authentication flows have been tested including registration with valid and invalid data, login with correct and incorrect credentials, logout, and password changes. All CRUD operations have been tested in both the user interface and the admin panel to confirm they create, read, update, and delete records correctly.

Permission enforcement has been verified by attempting to perform actions as different user types. Anonymous users cannot create resources. Authenticated non-owners cannot edit resources they don't own. Only staff users can access the admin panel and approve registrations.

Form validation has been tested with edge cases including duplicate gamertags, weak passwords, missing required fields, and overlapping date ranges. The responsive design has been verified across mobile (320px), tablet (768px), and desktop (1200px+) breakpoints. Cross-browser compatibility has been confirmed on Chrome, Edge, Firefox, and Safari on both desktop and mobile.

---

## Future Enhancements

While the current platform is fully functional, several enhancements would expand its capabilities. Real-time match score updates via WebSockets would let spectators follow tournaments live. Email notifications would alert players about upcoming matches, registration deadlines, and ranking changes. Automatic tournament bracket generation would eliminate the manual work of creating elimination structures.

A team and clan management system would extend the platform beyond individual players to support multi-player squads. Payment integration for prize pools would enable automatic prize distribution to winners. Native mobile apps for iOS and Android would provide better access on phones. Xbox Live API integration could verify gamertag ownership and pull actual match statistics automatically.

Streaming platform integration with Twitch and YouTube would embed live broadcasts directly in league pages. A REST API would enable third-party developers to build companion apps and integrations. An advanced analytics dashboard specifically for sponsors would show engagement metrics, demographic breakdowns, and ROI calculations.

---

## Technical Skills Demonstrated

This project demonstrates competency across the full web development stack. On the backend, it shows mastery of Django's MVT architecture, ORM-based database modeling, function-based view development, form handling with validation, authentication and authorization implementation, and custom admin interface development.

On the frontend, it demonstrates responsive design with Bootstrap, advanced CSS including animations and glassmorphism, vanilla JavaScript canvas programming for the particle network, and intersection observers for scroll-triggered animations.

On the infrastructure side, it covers production deployment with Gunicorn and WhiteNoise, environment-based configuration management, static file optimization, and database migration workflows. The project also demonstrates documentation-driven development with comprehensive technical and user-facing documentation.

---

## Conclusion

SA Esports Hub represents a complete, production-ready web application built with industry-standard tools and best practices. The architecture is clean and maintainable, the security measures are comprehensive, and the user experience is polished. The codebase serves as both a functional platform for South African esports and a portfolio demonstration of full-stack Django development skills.

The technical decisions throughout the project balance simplicity with capability. Django provides power without complexity. SQLite enables instant development setup. PostgreSQL handles production scale. WhiteNoise simplifies static file serving. Custom CSS achieves a premium look without heavy frameworks. The result is a platform that's easy to deploy, simple to maintain, and pleasant to use.

---

*End of Technical Design Document*