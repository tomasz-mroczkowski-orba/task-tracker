from fastapi import FastAPI

from middleware.add_x_process_time_header_middleware import (
    AddXProcessTimeHeaderMiddleware,
)
from middleware.log_request_basic_information_middleware import (
    LogRequestBasicInformationMiddleware,
)
from routers import manage

import db_init # pylint: disable=unused-import
import db_schema # pylint: disable=unused-import

app = FastAPI(title="Task Tracker API")
app.add_middleware(AddXProcessTimeHeaderMiddleware)
app.add_middleware(LogRequestBasicInformationMiddleware)

app.include_router(manage.router)
