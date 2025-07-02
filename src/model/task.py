from base import Base
from sqlalchemy import Column, Integer, String, DateTime


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String)
    due_date = Column(DateTime)

    def __repr__(self):
        return (f"<Task(id={self.id}, title={self.title}, description={self.description}, "
                f"status={self.status}, due_date={self.due_date})>")
