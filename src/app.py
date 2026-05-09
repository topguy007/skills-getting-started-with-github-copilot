"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from copy import deepcopy
import os
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=current_dir / "static"),
    name="static",
)

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@mergington\.edu$")

INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
}

activities = deepcopy(INITIAL_ACTIVITIES)


def validate_student_email(email: str) -> str:
    normalized_email = email.strip().lower()
    if not EMAIL_REGEX.match(normalized_email):
        raise HTTPException(
            status_code=400,
            detail="Invalid student email. Use a mergington.edu email address.",
        )
    return normalized_email


def get_activity(activity_name: str):
    for name, details in activities.items():
        if name.lower() == activity_name.lower():
            return name, details
    return None, None


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    actual_name, activity = get_activity(activity_name)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    email = validate_student_email(email)
    if email in activity["participants"]:
        raise HTTPException(
            status_code=409,
            detail="Student is already signed up for this activity.",
        )

    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(
            status_code=409,
            detail="Activity is full.",
        )

    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {actual_name}"}
