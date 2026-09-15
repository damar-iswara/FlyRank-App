# Task API

This project is a small FastAPI service for managing tasks with PostgreSQL. It is designed so a stranger can clone the repo, copy the sample environment file, and run the full stack with one command.

## What this is

A minimal task-management API with:

- FastAPI for the REST interface
- PostgreSQL for persistent storage
- Docker Compose for the full stack
- automatic database table creation and seed data
- Swagger UI for interactive API testing

## Features

- List all tasks
- Fetch a task by ID
- Create a new task
- Update an existing task
- Delete a task
- Health check endpoint
- Automatic Swagger documentation
- PostgreSQL-backed persistence
- Automatic table creation and seed data

## Tech Stack

- Python 3.10+
- FastAPI
- PostgreSQL
- psycopg
- Docker Compose
- Python-dotenv

## Project Structure

```text
FlyRank-App/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── database.py
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── README.md
└── .env
```

## One-command setup

```bash
cp .env.example .env && docker compose up
```

This starts both the API and the PostgreSQL database together.

> Important: `.env` is ignored by Git, and `.env.example` is committed so new users can copy it safely.

## Environment variables

Copy `.env.example` to `.env` and update the value if needed.

```env
DATABASE_URL=postgresql://postgres:dev@db:5432/tasks
```

| Variable | Required | Description |
| --- | --- | --- |
| `DATABASE_URL` | Yes | PostgreSQL connection string used by the API container |

Use the value above for Docker Compose. The host is `db` because the API runs in a container and connects to the PostgreSQL service by container name.

## Run everything

```bash
docker compose up
```

Then open:

- API: http://localhost:3000
- Swagger docs: http://localhost:3000/docs
- Health check: http://localhost:3000/health

## API endpoints

| Method | Endpoint      | Description         |
| ------ | ------------- | ------------------- |
| GET    | `/`           | Get API information |
| GET    | `/health`     | Check API health    |
| GET    | `/tasks`      | Get all tasks       |
| GET    | `/tasks/{id}` | Get a task by ID    |
| POST   | `/tasks`      | Create a new task   |
| PUT    | `/tasks/{id}` | Update a task       |
| DELETE | `/tasks/{id}` | Delete a task       |

## Example request

```bash
curl -i http://localhost:3000/tasks
```

Example response:

```http
HTTP/1.1 200 OK
content-type: application/json

[
  {"id":1,"title":"Learn FastAPI","done":false},
  {"id":2,"title":"Build a REST API","done":false},
  {"id":3,"title":"Practice API testing","done":true}
]
```

## Data model

The app initializes a `tasks` table automatically:

| Column  | Type                | Description                             |
| ------- | ------------------- | --------------------------------------- |
| `id`    | INTEGER PRIMARY KEY | Automatically generated task ID         |
| `title` | TEXT                | Task title                              |
| `done`  | BOOLEAN             | Completion status, stored as `0` or `1` |

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
)
```

If the table is empty, it seeds the following example tasks:

- Learn FastAPI
- Build a REST API
- Practice API testing

## Database verification

The project is meant to be validated with the real database, not a mock.

### Example database check

```bash
docker exec -it <postgres_container_name> psql -U postgres -d tasks -c "\dt"
docker exec -it <postgres_container_name> psql -U postgres -d tasks -c "SELECT * FROM tasks;"
```

Or use a GUI such as DBeaver, pgAdmin, or TablePlus to confirm the seeded rows are visible.

Example screenshot expected in the project documentation:

- `\dt` showing the `tasks` table
- `SELECT * FROM tasks;` returning seeded rows

## Round-trip check for a clean clone

A stranger should be able to do this:

```bash
git clone <repo-url>
cd <repo-folder>
cp .env.example .env
docker compose up
```

Then the API should be reachable at `http://localhost:3000` and `GET /tasks` should return the seeded tasks without any manual database setup.


## Notes
- `.env.example` is the template that new contributors copy.
- Swagger UI is available at `/docs`.
- The API auto-creates the database table and seeds default tasks on startup.