from marshmallow import Schema, ValidationError, fields, validate, validates_schema


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True, validate=validate.Range(min=1))
    exercise_id = fields.Int(required=True, validate=validate.Range(min=1))
    sets = fields.Int(required=True, validate=validate.Range(min=1))
    reps = fields.Int(required=True, validate=validate.Range(min=1))
    duration = fields.Int(required=True, validate=validate.Range(min=1))
    workout = fields.Nested("WorkoutSchema", dump_only=True, exclude=("workout_exercises",))
    exercise = fields.Nested("ExerciseSchema", dump_only=True, exclude=("workout_exercises",))

    @validates_schema
    def validate_unique_pair(self, data, **kwargs):
        if data.get("workout_id") is None or data.get("exercise_id") is None:
            raise ValidationError("Workout and exercise are required.")


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=[validate.Length(min=2, max=80)])
    category = fields.Str(required=True, validate=[validate.Length(min=2, max=50)])
    description = fields.Str(allow_none=True, validate=[validate.Length(max=200)])
    workout_ids = fields.Method("get_workout_ids", dump_only=True)
    workout_exercises = fields.List(fields.Nested("WorkoutExerciseSchema", exclude=("exercise",)), dump_only=True)

    @staticmethod
    def get_workout_ids(obj):
        return [workout.id for workout in obj.workouts]

    @validates_schema
    def validate_name_and_category(self, data, **kwargs):
        if data.get("name") is not None and not str(data["name"]).strip():
            raise ValidationError("Exercise name cannot be blank.")
        if data.get("category") is not None and not str(data["category"]).strip():
            raise ValidationError("Exercise category cannot be blank.")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=[validate.Length(min=2, max=80)])
    focus = fields.Str(required=True, validate=[validate.Length(min=2, max=50)])
    duration = fields.Int(required=True, validate=validate.Range(min=1))
    exercise_ids = fields.Method("get_exercise_ids", dump_only=True)
    workout_exercises = fields.List(fields.Nested("WorkoutExerciseSchema", exclude=("workout",)), dump_only=True)

    @staticmethod
    def get_exercise_ids(obj):
        return [exercise.id for exercise in obj.exercises]

    @validates_schema
    def validate_name_and_focus(self, data, **kwargs):
        if data.get("name") is not None and not str(data["name"]).strip():
            raise ValidationError("Workout name cannot be blank.")
        if data.get("focus") is not None and not str(data["focus"]).strip():
            raise ValidationError("Workout focus cannot be blank.")
