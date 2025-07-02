import os

env = os.getenv('APP_ENV', 'dev')

if (env == 'test'):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test/test.db"
else:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:lingaroPassSql@db:5432/task_tracker_db"