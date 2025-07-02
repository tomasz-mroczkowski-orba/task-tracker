import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("./logs/system.log")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file_handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(file_handler)
logger.propagate = False


class LogRequestBasicInformationMiddleware(BaseHTTPMiddleware): # pylint: disable=too-few-public-methods
    async def dispatch(self, request: Request, call_next):
        logger.info("Request: %s %s", request.method, request.url.path)
        response = await call_next(request)
        return response
