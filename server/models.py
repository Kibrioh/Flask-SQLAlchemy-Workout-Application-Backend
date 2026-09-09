from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    focus = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        overlaps="workout_exercises",
    )

    __table_args__ = (
        CheckConstraint("length(name) >= 2", name="ck_workout_name_length"),
        CheckConstraint("duration > 0", name="ck_workout_duration_positive"),
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Workout name is required.")
        if len(value.strip()) < 2:
            raise ValueError("Workout name must be at least 2 characters long.")
        return value.strip()

    @validates("focus")
    def validate_focus(self, key, value):
        if not value or not value.strip():
            raise ValueError("Workout focus is required.")
        return value.strip()

    @validates("duration")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Workout duration must be greater than 0.")
        return value


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        overlaps="workout_exercises",
    )

    __table_args__ = (
        CheckConstraint("length(name) >= 2", name="ck_exercise_name_length"),
        CheckConstraint("length(category) >= 2", name="ck_exercise_category_length"),
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name is required.")
        if len(value.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise category is required.")
        if len(value.strip()) < 2:
            raise ValueError("Exercise category must be at least 2 characters long.")
        return value.strip().title()


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    sets = db.Column(db.Integer, nullable=False, default=3)
    reps = db.Column(db.Integer, nullable=False, default=10)
    duration = db.Column(db.Integer, nullable=False, default=30)

    workout = db.relationship("Workout", back_populates="workout_exercises", overlaps="exercises,workouts")
    exercise = db.relationship("Exercise", back_populates="workout_exercises", overlaps="exercises,workouts")

    __table_args__ = (
        UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise"),
        CheckConstraint("sets > 0", name="ck_workout_exercise_sets_positive"),
        CheckConstraint("reps > 0", name="ck_workout_exercise_reps_positive"),
        CheckConstraint("duration > 0", name="ck_workout_exercise_duration_positive"),
    )

    @validates("sets")
    def validate_sets(self, key, value):
        if value <= 0:
            raise ValueError("Sets must be greater than 0.")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value <= 0:
            raise ValueError("Reps must be greater than 0.")
        return value

    @validates("duration")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Workout duration must be greater than 0.")
        return value
