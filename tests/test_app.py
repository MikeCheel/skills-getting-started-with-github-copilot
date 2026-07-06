from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog():
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == activities["Chess Club"]["max_participants"]


def test_signup_for_activity_adds_participant():
    # Arrange
    email = "new.student@mergington.edu"
    path = "/activities/Chess Club/signup"
    params = {"email": email}

    # Act
    response = client.post(path, params=params)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_unknown_activity_returns_404():
    # Arrange
    path = "/activities/Robotics Club/signup"
    params = {"email": "new.student@mergington.edu"}

    # Act
    response = client.post(path, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity_removes_participant():
    # Arrange
    email = activities["Chess Club"]["participants"][0]
    path = f"/activities/Chess Club/participants/{email}"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404():
    # Arrange
    path = "/activities/Chess Club/participants/missing.student@mergington.edu"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}