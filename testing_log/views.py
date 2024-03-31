from django.shortcuts import render
from django.http import HttpResponse
from decorators.trace_decorator import trace_function
from django.http import JsonResponse
from opentelemetry_test.opentelemetry_init import logger, tracer

# Create your views here.


@trace_function
def hello_world(request):
    return HttpResponse("Hello, world!")


@trace_function
def multiply(request, number):
    # Convert the number parameter to an integer
    number = int(number)

    # Multiply the number by itself
    result = number * number

    # Log the operation using OpenTelemetry logger
    # logger.info(f"Multiplying {number} by itself to get {result}")

    # Return the result as a JSON response
    return JsonResponse({'result': result})

# Previous Formation to check log

# def hello_world(request):
#     with tracer.start_as_current_span("hello_world"):
#         logger.info("This is a log message")
#     logger.info("Logging from Hello_world_view")
#     return HttpResponse("Hello, world!")
