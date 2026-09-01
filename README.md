# Task API

A simple REST API built with **FastAPI** for managing tasks.

The API uses an in-memory list as its database, so data is reset whenever the server restarts.

## Features

* Get all tasks
* Get a task by ID
* Create a new task
* Update a task
* Delete a task
* Health check endpoint
* Automatic Swagger API documentation
* Input validation for new tasks

## Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd task-api
```

Install the dependencies:

```bash
pip install "fastapi[standard]"
```

## Run

Start the API with:

```bash
uvicorn main:app --reload --port 8000 or fastapi dev main.py
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint      | Description         |
| ------ | ------------- | ------------------- |
| GET    | `/`           | Get API information |
| GET    | `/health`     | Check API health    |
| GET    | `/tasks`      | Get all tasks       |
| GET    | `/tasks/{id}` | Get a task by ID    |
| POST   | `/tasks`      | Create a new task   |
| PUT    | `/tasks/{id}` | Update a task       |
| DELETE | `/tasks/{id}` | Delete a task       |

## Example

Create a new task:

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```
or if you use command prompt
```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

Example response:

```text
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Error Handling

If a task does not exist:

```text
GET /tasks/99
```

The API returns:

```json
{
  "error": "Task 99 not found"
}
```

with HTTP status:

```text
404 Not Found
```

If the title is missing or empty when creating a task, the API returns:

```json
{
  "error": "Title is required and cannot be empty"
}
```

with HTTP status:

```text
400 Bad Request
```

## Swagger Documentation

The API provides interactive Swagger documentation through FastAPI.

Open:

```text
http://localhost:8000/docs
```

## Project Structure

```text
task-api/
├── main.py
├── requirements.txt
├── README.md
├── swagger.png
└── .gitignore
```

## [Swagger API Documentation]
Command
<img width="1917" height="968" alt="all-command" src="https://github.com/user-attachments/assets/7471d55d-ab9b-41cf-b979-7a8c5f1e6515" />
Root
<img width="1917" height="971" alt="root" src="https://github.com/user-attachments/assets/7de668da-70c8-4631-a9a9-5e8f6c64d63e" />
Get Health
<img width="1917" height="975" alt="get-health" src="https://github.com/user-attachments/assets/cc1b7dab-0b1b-407e-8ad7-ec811bf800b1" />
Get Tasks (before)
<img width="1917" height="966" alt="get-tasks" src="https://github.com/user-attachments/assets/20b18e87-774a-4611-a41e-620d66361993" />
Post Tasks
<img width="1917" height="968" alt="post-tasks (1)" src="https://github.com/user-attachments/assets/f48064a0-c3dd-46e7-9ca8-93bd938a85dc" />
<img width="1917" height="970" alt="post-tasks (2)" src="https://github.com/user-attachments/assets/32e16672-a472-4a56-a7ec-77569609ae0d" />
Get Tasks 
<img width="1917" height="967" alt="get-tasks (id)" src="https://github.com/user-attachments/assets/fa1dd070-64fa-4f5d-946a-f35464cbfb3e" />
Put Tasks
<img width="1917" height="966" alt="put-tasks (1)" src="https://github.com/user-attachments/assets/f92a4e8a-b89d-4435-9f6f-94479f93b4ad" />
<img width="1917" height="972" alt="put-tasks (2)" src="https://github.com/user-attachments/assets/f153c177-7321-4349-9bdd-48e233c7d3fe" />
Get Tasks (after)
<img width="1917" height="972" alt="get-tasks (after)" src="https://github.com/user-attachments/assets/bd3ac326-ef96-4530-ad87-e498dec823d4" />
Delete Tasks
<img width="1917" height="967" alt="delete-tasks" src="https://github.com/user-attachments/assets/2a89ca64-d18c-4748-9cca-937bc78d822c" />
