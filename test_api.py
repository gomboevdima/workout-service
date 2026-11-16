from fastapi.testclient import TestClient
from main import app
import main
import pytest

@pytest.fixture(autouse=True)
def reset_workouts(monkeypatch):
    monkeypatch.setattr(main, "workouts", [])

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_workout_not_found():
    response = client.get("/workouts/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Workout not found"}

def test_create_workout_api_success():
    payload = {
        "id": 100,
        "user_id": 1,
        "exercise": "squat",
        "weight": 80,
        "reps": 8,
    }

    create_response = client.post("/workouts", json=payload)
    get_response = client.get("/workouts/100")

    assert create_response.status_code == 201
    assert create_response.json() == payload
    assert get_response.status_code == 200
    assert get_response.json() == payload

def test_create_workout_api_duplicate_id():
    payload = {
        "id": 100,
        "user_id": 1,
        "exercise": "squat",
        "weight": 80,
        "reps": 10,
    }

    payload_copy = {
        "id": 100,
        "user_id": 1,
        "exercise": "squat",
        "weight": 120,
        "reps": 10,
    }

    first_create_response = client.post("/workouts", json=payload)
    assert first_create_response.status_code == 201
    assert first_create_response.json() == payload

    second_create_response = client.post("/workouts", json=payload_copy)
    assert second_create_response.status_code == 400
    assert second_create_response.json() == {"detail": "Workout id already exists"}

    get_response = client.get("/workouts/100")
    assert get_response.status_code == 200
    assert get_response.json() == first_create_response.json()

def test_create_workout_api_invalid_weight():
    payload = {
        "id": 100,
        "user_id": 1,
        "exercise": "squat",
        "weight": -80,
        "reps": 10,
    }

    create_response = client.post("/workouts", json=payload)
    assert create_response.status_code == 400
    assert create_response.json() == {"detail": "Weight must be positive"}

    get_response = client.get("/workouts/100")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Workout not found"}

def test_create_workout_api_missing_weight():
    payload = {
        "id": 100,
        "user_id": 1,
        "exercise": "squat",
        "reps": 10,
    }

    create_response = client.post("/workouts", json=payload)
    assert create_response.status_code == 422

    error = create_response.json()["detail"][0]
    assert error["loc"] == ["body", "weight"]
    assert error["type"] == "missing"

def test_update_workout_api_success():
    payload = {
        "id": 100,
        "user_id": 1,
        "exercise": "squat",
        "weight": 80,
        "reps": 10,
    }

    create_response = client.post("/workouts", json=payload)
    assert create_response.status_code == 201
    assert create_response.json() == payload

    update_response = client.patch("/workouts/100", json={"weight": 100})
    assert update_response.status_code == 200

    message = update_response.json()
    assert message["status"] == "updated"
    assert message["workout"]["id"] == 100
    assert message["workout"]["weight"] == 100

    payload_copy = payload.copy()
    payload_copy["weight"] = 100

    get_response = client.get("/workouts/100")
    assert get_response.status_code == 200
    assert get_response.json() == update_response.json()["workout"]
    assert payload_copy == get_response.json()

def test_update_workout_api_invalid_weight():
    payload = {
        "id": 100,
        "user_id": 1,
        "exercise": "squat",
        "weight": 80,
        "reps": 10,
    }

    create_response = client.post("/workouts", json=payload)
    assert create_response.status_code == 201
    assert create_response.json() == payload

    update_response = client.patch("/workouts/100", json={"weight": -50})
    assert update_response.status_code == 400
    assert update_response.json() == {"detail": "Weight must be positive"}

    get_response = client.get("/workouts/100")
    assert get_response.status_code == 200
    assert get_response.json() == payload

def test_update_workout_api_not_found():
    update_response = client.patch("/workouts/999", json={"weight": 90})
    assert update_response.status_code == 404
    assert update_response.json() == {"detail": "Workout not found"}

    get_response = client.get("/workouts/999")
    assert get_response.status_code == 404

def test_delete_workout_api_success():
    payload = {
        "id": 100,
        "user_id": 1,
        "exercise": "squat",
        "weight": 80,
        "reps": 10,
    }

    create_response = client.post("/workouts", json=payload)
    assert create_response.status_code == 201
    assert create_response.json() == payload

    delete_response = client.delete("/workouts/100")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"status": "deleted", "workout": payload}

    get_response = client.get("/workouts/100")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Workout not found"}

def test_delete_workout_api_not_found():
    delete_response = client.delete("/workouts/999")
    assert delete_response.status_code == 404
    assert delete_response.json() == {"detail": "Workout not found"}

    get_response = client.get("/workouts/999")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Workout not found"}
