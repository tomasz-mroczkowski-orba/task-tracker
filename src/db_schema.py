from db_init import engine
from base import Base
from model.task import Task # pylint: disable=unused-import

Base.metadata.create_all(bind=engine)
