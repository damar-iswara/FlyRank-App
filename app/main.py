from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
from app.database import get_connection, init_db, check_id_exists, check_title_not_empty


# ------------ Context Manager ------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup function
    init_db()

    yield

    # Shutdown function
    print("Aplikasi sedang dimatikan...")


app = FastAPI(lifespan=lifespan)



# ------------ API Endpoints ------------
@app.get("/")
def read_root():
    return {
        "name": "Task PostgreSQL",
        "version": "3.0",
        "endpoints": ["/tasks"]
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}


# GET /tasks
@app.get("/tasks")
def get_tasks():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()

    tasks = [
        {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }
        for row in rows
    ]

    return tasks


# GET /tasks/{id}
@app.get("/tasks/{id}")
def get_task(id: int):
    # Check if the task with the given ID exists
    if not check_id_exists(id):
        return error_404_id_not_exists(id)

    # Get task with given id
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks WHERE id = %s", (id,))
            row = cursor.fetchone()

    task = {
        "id": row[0],
        "title": row[1],
        "done": row[2]
    }

    return task


# POST /tasks
@app.post("/tasks")
def create_task(task: dict):
    # Validate title if provided
    if "title" not in task or not check_title_not_empty(task["title"]):
        return error_400_title_empty()

    # Connect to database and insert new task
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Insert the new task into the database
            cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *", (task["title"], False))
            row = cursor.fetchone()

        conn.commit()

    # Return created task
    return return_201_response({
        "id": row[0],
        "title": row[1],
        "done": row[2]
    })
    

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
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Update the task in the database
            if "title" in task and task["title"].strip():
                cursor.execute("UPDATE tasks SET title = %s WHERE id = %s", (task["title"], id))
            if "done" in task:
                cursor.execute("UPDATE tasks SET done = %s WHERE id = %s", (bool(task["done"]), id))

        conn.commit()

    # Return updated task
    return return_200_response({
        "title": task["title"], 
        "done": bool(task["done"])
    })


# DELETE /tasks/{id}
@app.delete("/tasks/{id}")
def delete_task(id: int):
    # Check if the task with the given ID exists
    if not check_id_exists(id):
        return error_404_id_not_exists(id)

    # Connect to database and insert new task
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Delete the task from the database
            cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))

        conn.commit()

    # Return no content response
    return return_204_response()
    

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
    return Response(status_code=204)

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