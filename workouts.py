from typing import Optional


def get_user_workouts_with_volume(workouts: list[dict], user_id: int) -> list[dict]:
    result = []

    for workout in workouts:
        if not validate_workout(workout)["valid"]:
            continue
        if workout["user_id"] == user_id:
            new_workout = workout.copy()
            new_workout["volume"] = workout["weight"] * workout["reps"]
            result.append(new_workout)

    return result


def get_user_total_volume(workouts: list[dict], user_id: int) -> dict:
    total_volume = 0

    for workout in workouts:
        if not validate_workout(workout)["valid"]:
            continue

        if workout["user_id"] == user_id:
            total_volume += workout["weight"] * workout["reps"]

    return {"user_id": user_id, "total_volume": total_volume}


def validate_workout(workout: dict) -> dict:
    if workout["id"] <= 0:
        return {"valid": False, "error": "Invalid id"}

    if workout["user_id"] <= 0:
        return {"valid": False, "error": "Invalid user_id"}

    if not workout["exercise"]:
        return {"valid": False, "error": "Exercise is required"}

    if workout["weight"] <= 0:
        return {"valid": False, "error": "Weight must be positive"}

    if workout["reps"] <= 0:
        return {"valid": False, "error": "Reps must be positive"}

    return {"valid": True, "error": None}


def create_workout(workouts: list[dict], workout: dict) -> dict:
    validation = validate_workout(workout)

    if not validation["valid"]:
        return {"status": "error", "error": validation["error"]}

    existing_workout = get_workout_by_id(workouts, workout["id"])

    if existing_workout is not None:
        return {"status": "error", "error": "Workout id already exists"}

    workouts.append(workout)
    return {"status": "created", "workout": workout}


def get_user_max_weight(workouts: list[dict], user_id: int, exercise: str) -> dict:
    new_workout = {"user_id": user_id, "exercise": exercise, "max_weight": None}
    max_weight = None

    for workout in workouts:

        if not validate_workout(workout)["valid"]:
            continue

        if workout["user_id"] == user_id:
            if workout["exercise"] == exercise:
                if max_weight is None or max_weight < workout["weight"]:
                    max_weight = workout["weight"]

    new_workout["max_weight"] = max_weight

    return new_workout


def update_workout_weight(workouts: list[dict], workout_id: int, new_weight: int) -> dict:
    if new_weight <= 0:
        return {"status": "error", "error": "Weight must be positive"}

    my_workout = get_workout_by_id(workouts, workout_id)

    if my_workout is None:
        return {"status": "error", "error": "Workout not found"}

    my_workout["weight"] = new_weight
    return {"status": "updated", "workout": my_workout}


def delete_workout(workouts: list[dict], workout_id: int) -> dict:
    my_workout = get_workout_by_id(workouts, workout_id)

    if my_workout is None:
        return {"status": "error", "error": "Workout not found"}
    workouts.remove(my_workout)

    return {"status": "deleted", "workout": my_workout}


def get_workout_by_id(workouts: list[dict], workout_id: int) -> Optional[dict]:
    for workout in workouts:
        if workout["id"] == workout_id:
            return workout

    return None