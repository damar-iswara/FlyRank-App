import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

DATABASE = "tasks.db"

# ------------ Database setup ------------
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Create tasks table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
    )
""")

# Seed example tasks only if table is empty
cursor.execute("SELECT COUNT(*) FROM tasks")
count = cursor.fetchone()[0]

if count == 0:
    # Seed example tasks
    example_tasks = [
        ("Learn FastAPI", 0),
        ("Build a REST API", 0),
        ("Practice API testing", 1)
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        example_tasks
    )
    conn.commit()

conn.close()


# Define API endpoints
@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}


# GET /tasks
@app.get("/tasks")
def get_tasks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    tasks = [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in rows]

    conn.close()
    return tasks


# GET /tasks/{id}
@app.get("/tasks/{id}")
def get_task(id: int):
    # Check if the task with the given ID exists
    if not check_id_exists(id):
        return error_404_id_not_exists(id)
    
    # Connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch the task with the given ID
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()

    task = {"id": row[0], "title": row[1], "done": bool(row[2])}

    conn.close()
    return task


# POST /tasks
@app.post("/tasks")
def create_task(task: dict):
    # Validate title if provided
    if "title" not in task or not check_title_not_empty(task["title"]):
        return error_400_title_empty()

    # Connect to database and insert new task
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Insert the new task into the database
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task["title"], False))

    conn.commit()
    conn.close()

    # Return created task
    return return_201_response({"title": task["title"], "done": False})
    

# PUT /tasks/{id}
@app.put("/tasks/{id}")
def update_task(id: int, task: dict):
    # Check if the task with the given ID exists
    if not check_id_exists(id):
        return error_404_id_not_exists(id)

    # Validate title if provided
    if "title" not in task or not check_title_not_empty(task["title"]):
        return error_400_title_empty()

    # Connect to database and insert new task
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Update the task in the database
    if "title" in task and task["title"].strip():
        cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (task["title"], id))
    if "done" in task:
        cursor.execute("UPDATE tasks SET done = ? WHERE id = ?", (bool(task["done"]), id))

    conn.commit()
    conn.close()

    # Return updated task
    return return_200_response({"title": task["title"], "done": bool(task["done"])})


# DELETE /tasks/{id}
@app.delete("/tasks/{id}")
def delete_task(id: int):
    # Check if the task with the given ID exists
    if not check_id_exists(id):
        return error_404_id_not_exists(id)

    # Connect to database and insert new task
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Delete the task from the database
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    # Return no content response
    return return_204_response()
    

# ------------ Helper functions ------------
def check_id_exists(id: int):
    # Check if the task with the given ID exists in the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM tasks WHERE id = ? LIMIT 1", (id,))
    exists = cursor.fetchone() is not None

    conn.close()
    return exists

def check_title_not_empty(title: str):
    # Check if the title is not empty
    return bool(title.strip())

#------------ Response functions ------------
def return_200_response(content: dict):
    # return a 200 response with the given content
    return JSONResponse(
        status_code=200,
        content=content
    )

def return_201_response(content: dict):
    # return a 201 response with the given content
    return JSONResponse(
        status_code=201,
        content=content
    )

def return_204_response():
    # return a 204 response with no content
    return JSONResponse(
        status_code=204,
        content=None
    )

# ----------- Error response functions ------------
def error_404_id_not_exists(id: int):
    # return a 404 error response if the task with the given ID does not exist
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

def error_400_title_empty():
    # return a 400 error response if the title is empty
    return JSONResponse(
        status_code=400,
        content={"error": "Title cannot be empty"}
    )