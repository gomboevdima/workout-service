from fastapi import FastAPI, HTTPException
from workouts import get_workout_by_id, delete_workout

app = FastAPI()

workouts = [{"id": 1, "user_id": 1, "exercise": "push ups", "weight": 100, "reps": 15},
    {"id": 2, "user_id": 1, "exercise": "bench press", "weight": 100, "reps": 15},
    {"id": 3, "user_id": 2, "exercise": "deadlift", "weight": 100, "reps": 15},
    {"id": 4, "user_id": 3, "exercise": "pullover", "weight": 100, "reps": 15},
            ]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/workouts/{workout_id}")
def get(workout_id: int):
    workout = get_workout_by_id(workouts, workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@app.delete("/workouts/{workout_id}")
def delete(workout_id: int):
    deleted_workout = delete_workout(workouts, workout_id)
    if deleted_workout["status"] == "error":
        raise HTTPException(status_code=404, detail=deleted_workout["error"])
    return deleted_workout

