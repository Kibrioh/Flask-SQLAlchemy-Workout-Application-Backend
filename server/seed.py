#!/usr/bin/env python3


from server.app import app
from server.models import Exercise, Workout, WorkoutExercise, db


with app.app_context():
    db.session.query(WorkoutExercise).delete()
    db.session.query(Workout).delete()
    db.session.query(Exercise).delete()

    push_ups = Exercise(name="Push Ups", category="Strength", description="Bodyweight press for chest and shoulders")
    squats = Exercise(name="Squats", category="Strength", description="Compound lower-body movement")
    lunges = Exercise(name="Lunges", category="Mobility", description="Single-leg balance and strength")
    planks = Exercise(name="Planks", category="Core", description="Stability exercise for the trunk")

    upper_body = Workout(name="Upper Body Blast", focus="Strength", duration=45)
    lower_body = Workout(name="Lower Body Power", focus="Strength", duration=50)

    db.session.add_all([push_ups, squats, lunges, planks, upper_body, lower_body])
    db.session.commit()

    upper_body_exercises = [
        WorkoutExercise(workout_id=upper_body.id, exercise_id=push_ups.id, sets=4, reps=12, duration=30),
        WorkoutExercise(workout_id=upper_body.id, exercise_id=planks.id, sets=3, reps=1, duration=20),
    ]
    lower_body_exercises = [
        WorkoutExercise(workout_id=lower_body.id, exercise_id=squats.id, sets=4, reps=12, duration=30),
        WorkoutExercise(workout_id=lower_body.id, exercise_id=lunges.id, sets=3, reps=10, duration=25),
    ]

    db.session.add_all(upper_body_exercises + lower_body_exercises)
    db.session.commit()

    print("Seed complete: 4 exercises and 2 workouts added.")
