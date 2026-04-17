from fastapi import APIRouter, HTTPException
from app.schemas.task import Task

router = APIRouter()

tasks = []
task_id_counter = 1


@router.post("/tasks")
def create_task(task: Task):
    global task_id_counter

    new_task = task.dict()
    new_task["id"] = task_id_counter

    tasks.append(new_task)
    task_id_counter += 1

    return new_task


@router.get("/tasks")
def get_tasks():
    return tasks


@router.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["description"] = updated_task.description
            task["is_done"] = updated_task.is_done
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}

    raise HTTPException(status_code=404, detail="Task not found")