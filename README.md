# Workout Application API

A Flask REST API for creating workouts, maintaining an exercise library, and assigning exercises to workouts. Data is stored in SQLite through Flask-SQLAlchemy, with schema changes managed by Flask-Migrate.

## Requirements

- Python 3.8
- Pipenv

## Setup

Install the project dependencies:

```bash
pipenv install
```

Apply the database migration:

```bash
pipenv run flask db upgrade head
```

Load the sample workouts and exercises:

```bash
pipenv run python -m server.seed
```

> Running the seed command clears the existing workout, exercise, and workout-exercise records before adding the sample data.

Start the development server on port `5555`:

```bash
pipenv run flask run --port 5555 --debug
```

The API is available at `http://127.0.0.1:5555`.

## Database

The SQLite database is created at `instance/app.db`. The initial migration creates these tables:

- `workouts`: a named workout with a focus and duration.
- `exercises`: an exercise with a category and optional description.
- `workout_exercises`: the association between a workout and an exercise, including sets, reps, and duration.

Each workout-exercise pair must be unique. Names, categories, sets, reps, and durations are validated before they are stored.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/workouts` | List all workouts. |
| `POST` | `/workouts` | Create a workout. |
| `GET` | `/workouts/<workout_id>` | Get one workout. |
| `PUT` | `/workouts/<workout_id>` | Update a workout. |
| `DELETE` | `/workouts/<workout_id>` | Delete a workout. |
| `GET` | `/exercises` | List all exercises. |
| `POST` | `/exercises` | Create an exercise. |
| `GET` | `/exercises/<exercise_id>` | Get one exercise. |
| `PUT` | `/exercises/<exercise_id>` | Update an exercise. |
| `DELETE` | `/exercises/<exercise_id>` | Delete an exercise. |
| `POST` | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. |
| `DELETE` | `/workout_exercises/<workout_exercise_id>` | Remove an exercise from a workout. |

## Request Examples

Create a workout:

```bash
curl -X POST http://127.0.0.1:5555/workouts \
  -H 'Content-Type: application/json' \
  -d '{"name":"Morning Strength","focus":"Strength","duration":45}'
```

Create an exercise:

```bash
curl -X POST http://127.0.0.1:5555/exercises \
  -H 'Content-Type: application/json' \
  -d '{"name":"Push Ups","category":"Strength","description":"Bodyweight chest exercise"}'
```

Assign exercise `1` to workout `1`:

```bash
curl -X POST http://127.0.0.1:5555/workouts/1/exercises/1/workout_exercises \
  -H 'Content-Type: application/json' \
  -d '{"sets":3,"reps":12,"duration":30}'
```

## Useful Commands

```bash
# Create a new migration after changing models.
pipenv run flask db migrate -m "describe the change"

# Apply all pending migrations.
pipenv run flask db upgrade head

# Show the current migration revision.
pipenv run flask db current
```
