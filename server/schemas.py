from marshmallow import Schema, ValidationError, fields, validate


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=[validate.Length(min=2, max=80)])
    category = fields.Str(required=True, validate=[validate.Length(min=2, max=50)])
    description = fields.Str(allow_none=True, validate=[validate.Length(max=200)])
    workout_ids = fields.Method("get_workout_ids", dump_only=True)

    @staticmethod
    def get_workout_ids(obj):
        return [workout.id for workout in obj.workouts]


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=[validate.Length(min=2, max=80)])
    focus = fields.Str(required=True, validate=[validate.Length(min=2, max=50)])
    duration = fields.Int(required=True, validate=validate.Range(min=1))
    exercise_ids = fields.Method("get_exercise_ids", dump_only=True)

    @staticmethod
    def get_exercise_ids(obj):
        return [exercise.id for exercise in obj.exercises]


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(required=True, validate=validate.Range(min=1))
    reps = fields.Int(required=True, validate=validate.Range(min=1))
    duration = fields.Int(required=True, validate=validate.Range(min=1))

    @staticmethod
    def validate_unique_pair(data):
        if data.get("workout_id") is None or data.get("exercise_id") is None:
            raise ValidationError("Workout and exercise are required.")
        return data
