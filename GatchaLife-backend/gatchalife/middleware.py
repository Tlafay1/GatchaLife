import time
import uuid
import structlog
from django.utils.deprecation import MiddlewareMixin

logger = structlog.get_logger(__name__)

class StructLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.path,
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            ip=request.META.get("REMOTE_ADDR", ""),
        )
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, "start_time"):
            duration = time.time() - request.start_time
            status_code = response.status_code
            
            log_method = logger.info if status_code < 400 else (logger.warning if status_code < 500 else logger.error)
            
            log_method(
                "request_finished",
                status_code=status_code,
                duration=duration,
            )
        return response

    def process_exception(self, request, exception):
        logger.error("request_failed", exc_info=exception)
