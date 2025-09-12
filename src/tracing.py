import uuid
from contextvars import ContextVar
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

trace_id_ctx_var: ContextVar[str] = ContextVar("trace_id", default="-")

def formatter(record):
    trace_id = trace_id_ctx_var.get()
    record["extra"]["trace_id"] = trace_id
    return (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | trace_id={extra[trace_id]} | "
        "{name}:{function}:{line} - {message}\n"
    )

logger.remove()
logger.add(
    sink=lambda msg: print(msg, end=""),
    format=formatter,
    level="INFO",
    backtrace=True,
    diagnose=True
)

class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        trace_id_ctx_var.set(trace_id)
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("Unhandled exception")
            raise
        response.headers["X-Trace-ID"] = trace_id
        return response

