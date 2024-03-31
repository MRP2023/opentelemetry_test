from functools import wraps
from opentelemetry import trace
import logging
import json
from django.http import JsonResponse, HttpResponse
# import requests


def trace_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get logger instance
        logger = logging.getLogger(__name__)

        # Start tracing
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(func.__name__):

            # # Log message
            # logger.info("Logging from {}".format(func.__name__))

            # Log message indicating function call and its arguments
            logger.info("Calling {} with args: {} and kwargs: {}".format(func.__name__, args, kwargs))

            # Lets Call the original function and capture its return value
            response = func(*args, **kwargs)

            # Check response type (assuming HTTPResponse or something else)
            if isinstance(response, JsonResponse):
                # Handle HTTP response
                content = response.content.decode('utf-8')
                try:
                    result = json.loads(content).get('result')
                    # Log and return extracted data (similar to Scenario 1 in previous explanation)
                    logger.info("Function {} returned: {}".format(func.__name__, result))
                    return JsonResponse({'result': result})
                    # return result
                except (json.JSONDecodeError, KeyError):
                    # Handle potential errors during JSON parsing or key access
                    logger.error("Error processing JSON response from {}".format(func.__name__))
                    # You can choose to return None, an error message, or raise an exception here
                    return None  # Replace with your desired error handling

            else:
                # Handle other response types (if applicable)
                # You can add logic to process different response types here
                logger.info("Function {} returned response of type: {}".format(func.__name__, type(response)))
                # Return the response object or handle it differently based on its type
                return response

            # # Previous state of stable Code commented below
            # print(type(response))
            # content = response.content.decode('utf-8')
            # result = json.loads(content).get('result')
            #
            # # Log the return value
            # logger.info("Function {} returned: {}".format(func.__name__, result))
            #
            # # return result
            #
            # return response

            # # Call the original function
            # return func(*args, **kwargs)

    return wrapper
