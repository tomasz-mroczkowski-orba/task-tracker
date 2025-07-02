from fastapi import HTTPException, Path, APIRouter
from starlette import status

from db_init import db_dependency
from model.task import Task
from request.task_request import TaskRequest

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_tasks(db: db_dependency):
    return db.query(Task).all()


@router.get("/task/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(db: db_dependency, task_id: int = Path(gt=0)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.post("/task", status_code=status.HTTP_201_CREATED)
async def create_task(task_request: TaskRequest, db: db_dependency):
    task = Task(**task_request.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.put("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(
    task_request: TaskRequest, db: db_dependency, task_id: int = Path(gt=0)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_request.model_dump().items():
        setattr(task, key, value)

    db.commit()


@router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(db: db_dependency, task_id: int = Path(gt=0)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
