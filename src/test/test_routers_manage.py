from datetime import datetime
from typing import Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql.expression import text

from base import Base
from db_init import get_db
from main import app
from model.task import Task
from request.task_request import StatusEnum

SQLALCHEMY_DATABASE_URL = "sqlite:///./test/testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator:
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def _task_fixture():
    task = Task(
        title="Task 1",
        description="This is a test task item no 1.",
        status=StatusEnum.COMPLETED.value,
        due_date=datetime(2025, 8, 1, 11, 59, 59),
    )

    db = TestingSessionLocal()
    db.add(task)
    db.commit()
    yield task
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM tasks;"))
        connection.commit()


def test_read_all(_task_fixture):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "title": "Task 1",
            "description": "This is a test task item no 1.",
            "status": StatusEnum.COMPLETED.value,
            "due_date": "2025-08-01T11:59:59",
        }
    ]


def test_read_one(_task_fixture):
    response = client.get("/task/1")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)
    assert response.json() == {
        "id": 1,
        "title": "Task 1",
        "description": "This is a test task item no 1.",
        "status": StatusEnum.COMPLETED.value,
        "due_date": "2025-08-01T11:59:59",
    }


def test_delete_one(_task_fixture):
    response = client.delete("/task/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/task/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_modify_one(_task_fixture):
    response = client.put(
        "/task/1",
        json={
            "title": "Task 1 Updated",
            "description": "This is a test task item no 1 updated.",
            "status": StatusEnum.IN_PROGRESS.value,
            "due_date": "2025-08-01T11:59:59",
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/task/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Task 1 Updated",
        "description": "This is a test task item no 1 updated.",
        "status": StatusEnum.IN_PROGRESS.value,
        "due_date": "2025-08-01T11:59:59",
    }
