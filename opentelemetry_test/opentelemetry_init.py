# opentelemetry_init.py
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# for console check
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
# from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter


# For Zipkin
# from opentelemetry.exporter.zipkin import ZipkinSpanExporter
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.resources import Resource


# Initialize the exporter

# exporter = InMemorySpanExporter()
exporter = ZipkinExporter(endpoint="http://localhost:9411/api/v2/spans")

# Configure the tracer provider with the exporter
resource = Resource(attributes={"service.name": "open-telemetry-service"})
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(SimpleSpanProcessor(exporter))

# Register the tracer provider
trace.set_tracer_provider(trace_provider)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
