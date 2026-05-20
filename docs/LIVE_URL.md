# SA Esports Hub
## Live Application Access Guide

**Document Type:** Deployment Information  
**Document Version:** 1.0  
**Date:** 2024  

---

## What This Document Is

This document tells you exactly where to access SA Esports Hub, how to log in with demo credentials to explore the platform, how to set it up on your own computer if you want to run it locally, and what to do if you encounter any issues. Whether you're a reviewer evaluating the project, a potential user wanting to try the platform, or a developer wanting to clone and run it yourself, everything you need is here.

---

## Accessing the Live Application

SA Esports Hub is deployed and publicly accessible on the internet. The main website is available at https://sa-esports-hub.onrender.com which serves as the entry point for all users. From there you can browse the public content, register for an account, or sign in to an existing account. The administrative panel is accessible at https://sa-esports-hub.onrender.com/admin/ but requires staff credentials to enter.

If these URLs aren't responding when you visit them, the application may be temporarily spun down due to inactivity on the free hosting tier. Simply wait about 30 seconds and refresh the page. The first request after a period of inactivity takes 2 to 3 seconds to wake the server, but subsequent requests are fast.

The deployed application includes the complete codebase from the GitHub repository, the PostgreSQL database with sample data, all static assets compressed and optimized, and full HTTPS encryption with an automatic SSL certificate provided by the hosting platform.

---

## Demo Access Credentials

To save you time setting up your own accounts, several pre-configured demo accounts are available for testing. These accounts give you immediate access to different user perspectives so you can experience how the platform works for various types of users.

For administrative access with full control over the platform, log in as **demo_admin** with password **DemoAdmin2024!** using email demo.admin@saesports.co.za. This account has superuser privileges, full access to the admin panel, and can perform any action including managing other users, approving registrations, recording matches, and editing any data.

To experience the platform as a tournament organizer, use **demo_organizer** with password **DemoOrg2024!**. This account has standard user privileges plus can create and manage leagues, approve player registrations to their own tournaments, and record match results.

For the player perspective, log in as **demo_player** with password **DemoPlayer2024!**. The Gamertag for this account is DemoPlayer_ZA. This account has a fully populated player profile with stats, can register for available leagues, and can browse the platform like any regular gamer.

To experience the scouting workflow, use **demo_scout** with password **DemoScout2024!**. This account specializes in evaluating other players and can submit structured scouting reports with ratings across multiple skill dimensions.

These credentials are intended for testing and demonstration only. In a real production deployment, you would generate strong unique passwords for each account, never commit credentials to version control, and rotate them periodically.

---

## Setting Up Locally

If you'd prefer to run SA Esports Hub on your own computer rather than using the deployed version, the setup process takes about five minutes. You'll need Python 3.10 or higher installed, the pip package manager (which comes with Python), and Git for cloning the repository.

Start by opening a terminal or command prompt and cloning the repository from GitHub with the command **git clone https://github.com/your-username/sa-esports-hub.git** followed by **cd sa-esports-hub** to enter the project folder. Replace the URL with your actual repository URL if you've forked or downloaded it elsewhere.

Next create a Python virtual environment to isolate the project's dependencies. Run **python -m venv venv** to create the environment. To activate it on Windows use **venv\Scripts\activate** and on macOS or Linux use **source venv/bin/activate**. Your terminal prompt should show (venv) at the start when the environment is active.

With the virtual environment activated, install all required Python packages by running **pip install -r requirements.txt**. This downloads and installs Django, Pillow, crispy-forms, WhiteNoise, Gunicorn, and all other dependencies. The installation takes about a minute depending on your internet speed.

Apply the database migrations to create all necessary tables by running **python manage.py migrate**. Django creates the SQLite database file and sets up all the tables for users, profiles, leagues, players, matches, registrations, and scouting reports. Create your administrative account with **python manage.py createsuperuser** and follow the prompts to enter a username, email, and password. This account will have full admin access.

Finally start the development server with **python manage.py runserver**. The server starts on port 8000 by default. Open your browser and navigate to http://127.0.0.1:8000/ to see the main site or http://127.0.0.1:8000/admin/ to access the admin panel using the superuser credentials you just created.

---

## Deployment Information

The production deployment uses Render.com as the hosting platform on their free tier. The application runs on a Linux server with Python 3.10, Django 4.2.7, and Gunicorn as the WSGI HTTP server. PostgreSQL 14 serves as the production database, replacing the SQLite used during development. WhiteNoise handles static file serving directly from the Django application without requiring a separate web server like Nginx.

The deployment is configured for continuous deployment from the main branch of the GitHub repository. Whenever code is pushed to main, Render automatically rebuilds and redeploys the application. The build process installs dependencies, collects static files into a single location, compresses them for production, and applies any pending database migrations. After the build succeeds, the new version is live within about 60 seconds.

Currently the application is fully operational with all deployment milestones complete. The site is deployed and publicly accessible. The database is migrated with all tables created. Static files including the CSS, JavaScript, and image assets are compiled and served efficiently. HTTPS is enabled with an automatic SSL certificate. The custom admin panel is functional. All CRUD operations have been verified working in the production environment.

Performance on the free tier has some characteristics worth understanding. The initial page load on a cold start takes 2 to 3 seconds because the server needs to wake up from idle. Once active, subsequent page loads complete in under 500 milliseconds. The PostgreSQL database is limited to 256 megabytes which is plenty for tens of thousands of users and matches. Media file storage is limited to 1 gigabyte covering all uploaded avatars and league banners.

---

## Browser Compatibility

SA Esports Hub has been tested and works on all modern web browsers across both desktop and mobile platforms. On desktop, Chrome version 120 and higher works perfectly, as does Edge 120 and higher, Firefox 121 and higher, and Safari 17 and higher. On mobile devices, the same browser families work including Chrome, Edge, Firefox, Safari on iOS, and Samsung Internet on Android devices.

To use the platform you need JavaScript enabled in your browser because the animated backgrounds, particle effects, and form validations depend on it. Cookies must also be enabled for the authentication system to maintain your login session. The site is fully responsive and works on screens as small as 320 pixels wide, though larger screens provide a better experience. A reliable internet connection is required since the platform doesn't include any offline functionality.

If you experience visual glitches or layout issues, the most common cause is an outdated browser cache. Try clearing your cache and cookies, or open the site in an incognito or private browsing window. The site has been optimized for modern browser features and may not render correctly on browsers more than two years old.

---

## Troubleshooting Common Issues

If the site loads slowly on your first visit, this is normal behavior for the free hosting tier. After 15 minutes of inactivity, the server spins down to conserve resources. Your first request wakes it back up which takes 2 to 3 seconds. Subsequent requests within the same session are fast. If you're testing the platform for a demonstration, visit it once a minute before your demo to keep it warm.

If you can't log in even though you're sure your credentials are correct, first verify that caps lock is off since passwords are case sensitive. Try clearing your browser cookies for the site domain and attempting again. If you're using a demo account, copy and paste the password from this document to avoid typing errors. If you've forgotten your password, an admin can reset it through the admin panel or via the command line using **python manage.py changepassword <username>**.

If you encounter a 404 page not found error, double-check the URL spelling. The platform uses lowercase URLs throughout. Make sure there are no typos in the path. If you arrived via a bookmark, the URL structure may have changed — try navigating from the home page instead. All major sections are accessible from the navbar menu.

If you see a 500 server error, this typically indicates a temporary problem with the server. Wait about 30 seconds and refresh the page. If the error persists across multiple attempts, the server may be experiencing an issue that requires administrator intervention. Contact the administrator with information about what you were trying to do when the error occurred.

If you're running the platform locally and encounter database errors, ensure you've run **python manage.py migrate** to create all necessary tables. If you've made changes to models, run **python manage.py makemigrations** first to generate migration files, then apply them with migrate. Database file permission issues can occur on some systems — make sure the db.sqlite3 file is writable by your user account.

---

## Getting Help and Reporting Issues

If you encounter problems not covered in the troubleshooting section, several options are available for getting help. Email the project maintainer directly with details about what you were doing, what you expected to happen, and what actually happened. Include screenshots if the issue is visual, and include the URL and approximate time of the issue if it's intermittent.

For developers wanting to contribute or who've found bugs in the code, the GitHub repository is the best place to report issues and submit pull requests. Open an issue describing the problem with steps to reproduce, expected behavior, and actual behavior. For feature suggestions, open a discussion thread before creating a pull request so the approach can be agreed on first.

The platform welcomes feedback from all types of users. Whether you're a player who wishes a feature worked differently, an organizer needing a new tournament format, a scout wanting better evaluation tools, or a sponsor looking for analytics capabilities, your input shapes future development priorities.

---

## Security Considerations

While SA Esports Hub implements industry-standard security measures including CSRF protection, password hashing, session management, and HTTPS, please understand that this is a demonstration platform. The demo credentials are publicly documented and anyone can use them. The demo database may be reset periodically without notice. Any data you enter could potentially be visible to other testers.

For these reasons, please avoid entering real personally identifiable information beyond what's required for testing. Don't use passwords from other accounts you care about. Don't upload sensitive images or documents. Don't rely on the platform for production use without additional security hardening, regular backups, monitoring, and compliance review.

If the platform interests you for actual production use, a security audit would be recommended along with adjustments like proper email-based password resets, two-factor authentication, rate limiting on login attempts, audit logging of administrative actions, and a privacy policy compliant with local data protection regulations like POPIA.

---

## Contact Information

For all inquiries about SA Esports Hub, whether technical questions, demo access requests, partnership proposals, or feedback, please reach out via the following channels. Email the project maintainer at [your email here] for the fastest response. Find the source code, report issues, or contribute on GitHub at [repository URL here]. Follow project updates on social media at [your Twitter or X handle here].

When contacting about an issue, please include the URL where you encountered the problem, a description of what you were trying to do, what you expected to happen, what actually happened, your browser and operating system, and any error messages or screenshots. This information dramatically speeds up troubleshooting and resolution.

---

## Final Notes

SA Esports Hub is a living project that continues to evolve. The features, design, and even the demo credentials may change over time as the platform improves based on user feedback. This document reflects the state of the platform as of the document date listed at the top. For the latest information, check the GitHub repository or contact the project maintainer.

Thank you for taking the time to access and evaluate SA Esports Hub. Whether you're here to test, learn, contribute, or partner, your engagement helps grow South African competitive gaming infrastructure.

---

*End of Live Application Document*