from django.shortcuts import render
from django.http import HttpResponse
from decorators.trace_decorator import trace_function
from opentelemetry_test.opentelemetry_init import logger, tracer

# Create your views here.


@trace_function
def hello_world(request):
    return HttpResponse("Hello, world!")

# Previous Formation to check log

# def hello_world(request):
#     with tracer.start_as_current_span("hello_world"):
#         logger.info("This is a log message")
#     logger.info("Logging from Hello_world_view")
#     return HttpResponse("Hello, world!")
