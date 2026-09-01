from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# In-memory database
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a REST API", "done": False},
    {"id": 3, "title": "Practice API testing", "done": True},
]


@app.get("/")
def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health_check():
    return {"status": "ok"}


# GET /tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# GET /tasks/{id}
@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

# POST /tasks
@app.post("/tasks")
def create_task(task: dict):

    # Validate title
    if "title" not in task or not task["title"].strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    # Generate next free ID
    new_id = max([task["id"] for task in tasks], default=0) + 1

    # Create new task
    new_task = {
        "id": new_id,
        "title": task["title"],
        "done": False
    }

    # Add to database
    tasks.append(new_task)

    # Return created task
    return JSONResponse(
        status_code=201,
        content=new_task
    )

# PUT /tasks/{id}
@app.put("/tasks/{id}")
def update_task(id: int, task: dict):
    for existing_task in tasks:

        if existing_task["id"] == id:         
            # Update title if provided
            if "title" in task and task["title"].strip():
                existing_task["title"] = task["title"]
                
            # Update done status if provided
            if "done" in task:
                existing_task["done"] = bool(task["done"])
            return existing_task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.delete("/tasks/{id}")
def delete_task(id: int):
    for existing_task in tasks:
        if existing_task["id"] == id:
            # Remove the task from the list
            tasks.remove(existing_task)

            return JSONResponse(status_code=204, content=None)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

