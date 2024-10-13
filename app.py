### Various Steps required to complete the task described below:
# 1. create_task(): Creates a new task with a title property and a boolean determining whether the task has been completed. A new unique id would be created for each new task
# 2. list_tasks(): Lists all tasks created
# 3. get_task(): Gets a specific task
# 4. delete_task(): Deletes a specified task
# 5. update_task(): Edits the title or completion of a specific task
# 6. bulk_create_tasks(): Bulk add multiple tasks in one request
# 7. bulk_delete_tasks(): Bulk delete multiple tasks in one request

# Importing necessary libraries
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
from typing import List
from database import SessionLocal, engine


# Initialize the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/v1/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(title=task.title)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/v1/tasks", response_model=List[schemas.TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@app.get("/v1/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/v1/tasks/{task_id}", status_code=204)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.is_completed = task.is_completed
    db.commit()
    return

@app.delete("/v1/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return
@app.post("/v1/tasks/bulk", status_code=201)
def bulk_create_tasks(tasks: List[schemas.TaskCreate], db: Session = Depends(get_db)):
    new_tasks = [models.Task(title=task.title) for task in tasks]
    db.add_all(new_tasks)
    db.commit()
    return [{"id": task.id} for task in new_tasks]
@app.delete("/v1/tasks/bulk", status_code=204)
def bulk_delete_tasks(task_ids: List[int], db: Session = Depends(get_db)):
    db.query(models.Task).filter(models.Task.id.in_(task_ids)).delete(synchronize_session=False)
    db.commit()
    return
