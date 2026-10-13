from workouts import create_workout, get_workout_by_id, update_workout_weight, delete_workout, get_user_total_volume


def test_create_workout_success():
    test_workouts = [{"id": 1, "user_id": 1, "exercise": "squat", "weight": 100, "reps": 5},
                     {"id": 2, "user_id": 1, "exercise": "bench press", "weight": 80, "reps": 6},
                     {"id": 3, "user_id": 2, "exercise": "deadlift", "weight": 100, "reps": 3}
                     ]
    len_without_new_workout = len(test_workouts)
    result = create_workout(test_workouts, {"id": 4, "user_id": 2, "exercise": "squat", "weight": 100, "reps": 5})
    my_created_workout = get_workout_by_id(test_workouts, 4)
    assert my_created_workout is not None
    assert my_created_workout["id"] == 4
    assert my_created_workout["user_id"] == 2
    assert my_created_workout["exercise"] == "squat"
    assert my_created_workout["weight"] == 100
    assert my_created_workout["reps"] == 5
    assert len_without_new_workout == len(test_workouts) - 1
    assert result["status"] == "created"


def test_create_workout_duplicate_id():
    test_case_of_workouts = [{"id": 1, "user_id": 1, "exercise": "squat", "weight": 100, "reps": 5}
                             ]
    len_without_new_workout = len(test_case_of_workouts)
    copy_workout = get_workout_by_id(test_case_of_workouts, 1)
    assert copy_workout is not None
    copy_workout = copy_workout.copy()
    copy_workout["exercise"] = "deadlift"
    copy_workout["weight"] = 200
    result = create_workout(test_case_of_workouts, copy_workout)
    assert result["status"] == "error"
    assert result["error"] == "Workout id already exists"
    assert len_without_new_workout == len(test_case_of_workouts)
    my_case = get_workout_by_id(test_case_of_workouts, 1)
    assert my_case is not None
    assert my_case["exercise"] == "squat"
    assert my_case["weight"] == 100


def test_create_workout_invalid_weight():
    my_works = [
        {"id": 1, "user_id": 1, "exercise": "squat", "weight": 100, "reps": 5},
        {"id": 2, "user_id": 2, "exercise": "bench press", "weight": 70, "reps": 8},
        {"id": 3, "user_id": 1, "exercise": "deadlift", "weight": 140, "reps": 3}
    ]
    len_of_works = len(my_works)
    new_working = {"id": 4, "user_id": 2, "exercise": "deadlift", "weight": -70, "reps": 8}
    new_workout = create_workout(my_works, new_working)
    assert new_workout["status"] == "error"
    assert new_workout["error"] == "Weight must be positive"
    assert len_of_works == len(my_works)
    assert get_workout_by_id(my_works, 4) is None


def test_update_workouts_success():
    my_works = [
        {"id": 1, "user_id": 1, "exercise": "squat", "weight": 100, "reps": 5},
        {"id": 2, "user_id": 1, "exercise": "bench press", "weight": 70, "reps": 8}
    ]
    len_works = len(my_works)
    status = update_workout_weight(my_works, 2, 80)
    assert status["status"] == "updated"
    a = get_workout_by_id(my_works, 2)
    b = get_workout_by_id(my_works, 1)
    assert a is not None
    assert a["weight"] == 80
    assert b is not None
    assert b["weight"] == 100
    assert len_works == len(my_works)
    assert status["workout"]["id"] == 2


def test_update_workout_invalid_weight():
    my_works = [
        {"id": 1, "user_id": 1, "exercise": "deadlift", "weight": 100, "reps": 5},
        {"id": 2, "user_id": 1, "exercise": "bench press", "weight": 70, "reps": 8}
    ]
    len_trains = len(my_works)
    update = update_workout_weight(my_works, 1, -50)
    assert update["status"] == "error"
    assert update["error"] == "Weight must be positive"
    my_train_exercise = get_workout_by_id(my_works, 1)
    assert my_train_exercise is not None
    assert my_train_exercise["weight"] == 100
    assert len_trains == len(my_works)


def test_update_workout_not_found():
    my_works = [
        {"id": 1, "user_id": 1, "exercise": "deadlift", "weight": 100, "reps": 5},
        {"id": 2, "user_id": 1, "exercise": "bench press", "weight": 70, "reps": 8}
    ]
    len_of_train = len(my_works)
    a = get_workout_by_id(my_works, 1)
    assert a is not None
    a = a.copy()
    b = get_workout_by_id(my_works, 2)
    assert b is not None
    b = b.copy()
    update = update_workout_weight(my_works, 999, 80)
    assert update["status"] == "error"
    assert update["error"] == "Workout not found"
    assert a == get_workout_by_id(my_works, 1)
    assert b == get_workout_by_id(my_works, 2)
    assert len_of_train == len(my_works)


def test_delete_workout_success():
    my_works = [
        {"id": 1, "user_id": 1, "exercise": "deadlift", "weight": 100, "reps": 5},
        {"id": 2, "user_id": 1, "exercise": "bench press", "weight": 70, "reps": 8}
    ]
    len_of_trains = len(my_works)
    b = get_workout_by_id(my_works, 2)
    assert b is not None
    b = b.copy()
    deleting = delete_workout(my_works, 1)
    assert deleting["status"] == "deleted"
    assert deleting["workout"]["id"] == 1
    assert get_workout_by_id(my_works, 1) is None
    assert get_workout_by_id(my_works, 2) is not None
    assert len_of_trains == len(my_works) + 1
    assert b == get_workout_by_id(my_works, 2)


def test_delete_workout_not_found():
    my_works = [
        {"id": 1, "user_id": 1, "exercise": "deadlift", "weight": 200, "reps": 5},
        {"id": 2, "user_id": 1, "exercise": "bench press", "weight": 70, "reps": 8}
    ]
    len_of_works = len(my_works)
    a = get_workout_by_id(my_works, 1)
    assert a is not None
    a = a.copy()
    b = get_workout_by_id(my_works, 2)
    assert b is not None
    b = b.copy()
    test = delete_workout(my_works, 999)
    assert test["status"] == "error"
    assert test["error"] == "Workout not found"
    assert a == get_workout_by_id(my_works, 1)
    assert b == get_workout_by_id(my_works, 2)
    assert len_of_works == len(my_works)


def test_get_user_total_volume_skips_invalid():
    my_works = [
        {"id": 1, "user_id": 1, "exercise": "deadlift", "weight": 100, "reps": 5},
        {"id": 2, "user_id": 1, "exercise": "bench press", "weight": -70, "reps": 8},
        {"id": 3, "user_id": 2, "exercise": "bench press", "weight": 70, "reps": 8}
    ]
    total = get_user_total_volume(my_works, 1)
    assert total["user_id"] == 1
    assert total["total_volume"] == 500


if __name__ == "__main__":
    test_delete_workout_not_found()
    test_delete_workout_success()
    test_update_workout_invalid_weight()
    test_create_workout_invalid_weight()
    test_create_workout_duplicate_id()
    test_create_workout_success()
    test_update_workout_not_found()
    test_update_workouts_success()
    test_get_user_total_volume_skips_invalid()
    print("All checks passed")
