from db_init import engine
from base import Base
from model.task import Task

Base.metadata.create_all(bind=engine)