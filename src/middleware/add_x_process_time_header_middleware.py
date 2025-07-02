import time
from typing import Callable, Awaitable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class AddXProcessTimeHeaderMiddleware(
    BaseHTTPMiddleware
):  # pylint: disable=too-few-public-methods
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable]
    ):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
