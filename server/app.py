
from flask import Flask, jsonify, request
from flask_migrate import Migrate

from server.models import Exercise, Workout, WorkoutExercise, db
from server.schemas import ExerciseSchema, WorkoutExerciseSchema, WorkoutSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

exercise_schema = ExerciseSchema()
exercise_list_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workout_list_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workout_list_schema.dump(workouts))


@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return jsonify(workout_schema.dump(workout))


@app.route("/workouts", methods=["POST"])
def create_workout():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Request body is required."}), 400

    try:
        data = workout_schema.load(payload)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    workout = Workout(**data)
    db.session.add(workout)
    db.session.commit()
    return jsonify(workout_schema.dump(workout)), 201


@app.route("/workouts/<int:workout_id>", methods=["PUT"])
def update_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Request body is required."}), 400

    try:
        data = workout_schema.load(payload, partial=True)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    for key, value in data.items():
        setattr(workout, key, value)

    db.session.commit()
    return jsonify(workout_schema.dump(workout))


@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted successfully."})


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercise_list_schema.dump(exercises))


@app.route("/exercises/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return jsonify(exercise_schema.dump(exercise))


@app.route("/exercises", methods=["POST"])
def create_exercise():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Request body is required."}), 400

    try:
        data = exercise_schema.load(payload)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    exercise = Exercise(**data)
    db.session.add(exercise)
    db.session.commit()
    return jsonify(exercise_schema.dump(exercise)), 201


@app.route("/exercises/<int:exercise_id>", methods=["PUT"])
def update_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Request body is required."}), 400

    try:
        data = exercise_schema.load(payload, partial=True)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    for key, value in data.items():
        setattr(exercise, key, value)

    db.session.commit()
    return jsonify(exercise_schema.dump(exercise))


@app.route("/exercises/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted successfully."})


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def create_workout_exercise(workout_id, exercise_id):
    workout = Workout.query.get_or_404(workout_id)
    exercise = Exercise.query.get_or_404(exercise_id)
    payload = request.get_json() or {}
    payload["workout_id"] = workout.id
    payload["exercise_id"] = exercise.id

    try:
        data = workout_exercise_schema.load(payload)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    existing = WorkoutExercise.query.filter_by(workout_id=workout.id, exercise_id=exercise.id).first()
    if existing:
        return jsonify({"error": "This exercise is already assigned to the workout."}), 400

    workout_exercise = WorkoutExercise(**data)
    db.session.add(workout_exercise)
    db.session.commit()
    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


@app.route("/workout_exercises/<int:workout_exercise_id>", methods=["DELETE"])
def delete_workout_exercise(workout_exercise_id):
    join_record = WorkoutExercise.query.get_or_404(workout_exercise_id)
    db.session.delete(join_record)
    db.session.commit()
    return jsonify({"message": "Workout exercise deleted successfully."})


if __name__ == "__main__":
    app.run(port=5555, debug=True)
