import requests
import json
import time
import uuid

OTEL_COLLECTOR_URL = "http://localhost:4318/v1/traces"  # Change to your OTel collector URL

def create_span():
    trace_id = uuid.uuid4().hex
    span_id = uuid.uuid4().hex[:16]  # Span ID should be 16 hex characters

    span = {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "my-python-app"}}
                    ]
                },
                "scopeSpans": [
                    {
                        "scope": {"name": "test-3"},
                        "spans": [
                            {
                                "traceId": trace_id,
                                "spanId": span_id,
                                "name": "yash-span3",
                                "kind": 2,  # SpanKind.INTERNAL
                                "startTimeUnixNano": str(int(time.time() * 1e9)),
                                "endTimeUnixNano": str(int((time.time() + 1) * 1e9)),  # 1s duration
                                "attributes": [
                                    {"key": "test", "value": {"stringValue": "yash2"}}
                                ],
                                "events": [
                                    {
                                        "name": "test-event2",
                                        "timeUnixNano": str(int(time.time() * 1e9)),
                                        "attributes": [
                                            {"key": "attribute1", "value": {"test": "yash"}},
                                             {"key": "attribute2", "value": {"test2": "yash2"}}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return span

def send_span():
    headers = {"Content-Type": "application/json"}
    span_data = create_span()
    print(span_data)
    response = requests.post(OTEL_COLLECTOR_URL, headers=headers, data=json.dumps(span_data))

    if response.status_code == 200:
        print("Span sent successfully!")
    else:
        print(f"Failed to send span. Status code: {response.status_code}, Response: {response.text}")

send_span()
