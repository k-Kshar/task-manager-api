from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.api import tasks
# from app.db.base import Base
# from app.db.session import engine

# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

app.include_router(tasks.router)


# временное хранилище (как "мини база")
tasks = []
task_id_counter = 1


# схема задачи (валидация)
class Task(BaseModel):
    title: str
    description: str
    is_done: bool = False


@app.get("/")
def health_check():
    return {"status": "ok"}


# создать задачу
@app.post("/tasks")
def create_task(task: Task):
    global task_id_counter

    new_task = task.dict()
    new_task["id"] = task_id_counter

    tasks.append(new_task)
    task_id_counter += 1

    return new_task

# получить все задачи
@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["is_done"] = updated_task.is_done
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}

    raise HTTPException(status_code=404, detail="Task not found")