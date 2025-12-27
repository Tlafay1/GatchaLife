import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class WorkflowHandler(ABC):
    """
    Abstract base class for workflow handlers.
    Each handler implementation must be registered with a unique job_type.
    """
    
    @abstractmethod
    def handle_success(self, job, data, files=None):
        """
        Called when the async job completes successfully.
        :param job: The AsyncJob instance.
        :param data: The JSON data returned by the workflow.
        :param files: Optional dictionary of uploaded files (e.g. from request.FILES).
        """
        pass

    @abstractmethod
    def handle_failure(self, job, error_message):
        """
        Called when the async job fails.
        :param job: The AsyncJob instance.
        :param error_message: Error details.
        """
        pass


class JobRegistry:
    _registry = {}

    @classmethod
    def register(cls, job_type):
        """
        Decorator to register a handler class for a specific job_type.
        """
        def wrapper(handler_cls):
            if job_type in cls._registry:
                logger.warning(f"Job type '{job_type}' is already registered. Overwriting with {handler_cls.__name__}.")
            cls._registry[job_type] = handler_cls
            return handler_cls
        return wrapper

    @classmethod
    def get_handler(cls, job_type):
        """
        Returns an instance of the handler registered for the given job_type.
        """
        handler_cls = cls._registry.get(job_type)
        if not handler_cls:
            return None
        return handler_cls()

    @classmethod
    def get_registered_types(cls):
        return list(cls._registry.keys())
