# Workspace Instructions for GitHub Copilot

## Project Overview

This repository is a GitHub Skills exercise for "Getting Started with GitHub Copilot". It implements a simple FastAPI application that allows students to view and sign up for extracurricular activities at Mergington High School.

The application consists of:
- A FastAPI backend serving REST API endpoints
- A vanilla JavaScript frontend for user interaction
- In-memory data storage (resets on server restart)

## Architecture & Component Boundaries

- **Backend** (`src/app.py`): FastAPI application with two endpoints:
  - `GET /activities`: Returns all activities with details
  - `POST /activities/{activity_name}/signup`: Signs up a student via query param email
- **Frontend** (`src/static/`): HTML, CSS, and JS for the web interface
- **Data Model**: Activities stored as dict with name keys; each activity has description, schedule, max_participants, participants list

## Key Conventions

- Activity names contain spaces and must be URL-encoded in API requests
- Student emails follow the pattern `name@mergington.edu`
- Static files are served from `/static` path
- Root path redirects to the static index.html

## Build/Test Commands

- **Install dependencies**: `pip install -r requirements.txt`
- **Run application**: `cd src && python app.py` (starts on http://localhost:8000)
- **Run tests**: `pytest` (configured via pytest.ini)

## Potential Pitfalls

- No duplicate signup prevention
- No enforcement of max_participants limit
- No email format validation
- Activity names are case-sensitive
- Data is stored in memory only (lost on restart)

## Key Files & Patterns

- [src/app.py](src/app.py): Main API application
- [src/static/index.html](src/static/index.html): Frontend UI
- [src/static/app.js](src/static/app.js): Frontend JavaScript logic
- [src/README.md](src/README.md): Detailed API documentation and data model

## Related Documentation

- [src/README.md](src/README.md): Complete API reference, endpoints, and data model details</content>
<parameter name="filePath">/workspaces/skills-getting-started-with-github-copilot/.github/copilot-instructions.md