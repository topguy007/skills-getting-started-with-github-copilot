import copy
import pytest

from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(app_module.INITIAL_ACTIVITIES))


def test_get_activities_returns_all_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity_succeeds():
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in app_module.activities["Chess Club"]["participants"]


def test_signup_for_activity_rejects_invalid_email():
    response = client.post("/activities/Chess%20Club/signup?email=bad-email@example.com")
    assert response.status_code == 400
    assert "Invalid student email" in response.json()["detail"]


def test_signup_for_activity_rejects_duplicate_signups():
    existing_email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={existing_email}")
    assert response.status_code == 409
    assert "already signed up" in response.json()["detail"]


def test_signup_for_activity_rejects_full_activity():
    activity = app_module.activities["Chess Club"]
    # Fill the activity to its capacity
    activity["participants"] = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]

    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 409
    assert "Activity is full" in response.json()["detail"]


def test_root_redirects_to_index():
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 302)
    assert response.headers["location"] == "/static/index.html"
