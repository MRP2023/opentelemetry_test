from functools import wraps
from opentelemetry import trace
import logging


def trace_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get logger instance
        logger = logging.getLogger(__name__)

        # Start tracing
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(func.__name__):
            # Log message
            logger.info("Logging from {}".format(func.__name__))
            # Call the original function
            return func(*args, **kwargs)

    return wrapper
