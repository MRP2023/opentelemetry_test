from functools import wraps
from opentelemetry import trace
from opentelemetry_test.opentelemetry_init import tracer, current_span
import logging
import json
from django.http import JsonResponse, HttpResponse
# from opentelemetry_test.opentelemetry_init import logger, tracer
# import requests


def trace_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get logger instance
        logger = logging.getLogger(__name__)

        # Start tracing
        # tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(func.__name__) as span:
            try:
                print(args)
                print(*args)

                request = args[0]
                print(request)
                print(request.method)  # Prints the HTTP method (GET, POST, etc.)
                print(request.path)  # Prints the URL path of the request

                # request = args[0] if 'request' in args else kwargs.get('request')

                if request is None:
                    logger.error("Request object not found in args or kwargs.")
                    return HttpResponse(status=500, content="Internal Server Error")

                # span = current_span
                span.set_attribute("http.request.method", request.method)
                span.set_attribute("http.request.url", request.path)
                span.set_attribute("http.user_agent", request.META.get('HTTP_USER_AGENT'))
                span.set_attribute("http.client_ip", request.META.get('REMOTE_ADDR'))
                span.set_attribute("http.route", request.resolver_match.route)

                logger.info("Calling {} with args: {} and kwargs: {}".format(func.__name__, args, kwargs))

                response = func(*args, **kwargs)

                if isinstance(response, JsonResponse):
                    content = response.content.decode('utf-8')
                    try:
                        result = json.loads(content).get('result')
                        span.set_attribute("http.status_code", response.status_code)
                        span.set_attribute("result", result)
                        logger.info("Function {} returned: {}".format(func.__name__, result))
                        return JsonResponse({'result': result})
                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error("Error processing JSON response from {}: {}".format(func.__name__, e))
                        span.set_attribute("error", True)
                        span.set_attribute("error.message", "Error processing JSON response")
                        return HttpResponse(status=500, content="Internal Server Error")

                else:
                    logger.info("Function {} returned response of type: {}".format(func.__name__, type(response)))
                    span.set_attribute("http.status_code", response.status_code)
                    return response

            except Exception as e:
                logger.error("Error occurred during tracing: %s", e)
                span.set_attribute("error", True)
                span.set_attribute("error.message", str(e))
                return HttpResponse(status=500, content="Internal Server Error")

    return wrapper
