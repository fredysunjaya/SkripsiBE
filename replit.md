# SecureVote Backend

## Overview
SecureVote Backend is a Django REST API for managing voting systems. It provides endpoints for user management, voting creation, candidate management, and vote tracking.

## Project Status
The project has been successfully set up and configured for the Replit environment. The Django development server is running on port 5000 with all necessary migrations applied.

## Recent Changes (December 1, 2025)
- Configured Django settings for Replit environment (ALLOWED_HOSTS set to accept all hosts)
- Changed database from PostgreSQL to SQLite for easier development
- Added CORS support with django-cors-headers for API access
- Fixed bugs in user_details view function (proper exception handling and variable scoping)
- Created .gitignore for Python/Django project
- Configured workflow to run Django development server on port 5000 with 0.0.0.0 host
- Applied all database migrations successfully

## Project Architecture

### Tech Stack
- Python 3.11
- Django 5.2.8
- Django REST Framework 3.16.1
- SQLite database
- django-cors-headers for CORS support

### Project Structure
```
SecureVoteBE/
├── restapi/                  # Main REST API application
│   ├── models/              # Database models
│   │   ├── users.py         # User model
│   │   ├── votings.py       # Voting model
│   │   ├── voting_candidates.py  # Candidate model
│   │   ├── voting_choices.py     # Choice model
│   │   └── voting_participants.py # Participant model
│   ├── serializers/         # DRF serializers
│   ├── views/               # API views
│   │   └── users.py         # User-related endpoints
│   ├── migrations/          # Database migrations
│   └── assets/              # Static assets
├── settings.py              # Django settings
├── urls.py                  # URL routing
├── wsgi.py                  # WSGI configuration
└── manage.py                # Django management script
```

### Database Models
The project includes models for:
- Users (name, email, password, photo)
- Votings
- Voting Candidates
- Voting Choices
- Voting Participants

### API Endpoints
- `GET /users/` - List all users
- `POST /users/` - Create a new user
- `GET /users/id[]` - Get user details
- `PUT /users/id[]` - Update user
- `DELETE /users/id[]` - Delete user
- `/admin/` - Django admin interface

## Running the Project
The Django development server is configured to run automatically on port 5000. It will start when you run the Repl.

Command: `python manage.py runserver 0.0.0.0:5000`

## Development Notes
- The server uses SQLite instead of PostgreSQL for easier local development
- ALLOWED_HOSTS is set to '*' for development (should be restricted in production)
- CORS is enabled for all origins (should be restricted in production)
- The database file is `db.sqlite3` in the project root
- All migrations have been applied successfully

## Security Considerations (Important for Production)
The current implementation has several security concerns that should be addressed before production deployment:

1. **Password Storage**: The User model stores passwords in plain text. This is a critical security vulnerability. Before going to production, you should:
   - Use Django's built-in User model with password hashing
   - Or implement proper password hashing using `make_password()` and `check_password()` from `django.contrib.auth.hashers`

2. **Settings Configuration**: Current settings are optimized for development only:
   - `DEBUG = True` should be `False` in production
   - `SECRET_KEY` is hardcoded and should use environment variables
   - `ALLOWED_HOSTS = ['*']` should be restricted to your actual domain
   - `CORS_ALLOW_ALL_ORIGINS = True` should be restricted to trusted origins

3. **Database**: SQLite is suitable for development but consider PostgreSQL for production with higher traffic

## User Preferences
None specified yet.
