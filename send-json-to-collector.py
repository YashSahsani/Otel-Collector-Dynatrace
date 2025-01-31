import requests
import json
import time
import uuid

OTEL_COLLECTOR_URL = "http://localhost:4318/v1/traces"  # Change to your OTel collector URL

def create_span():
    # trace_id = uuid.uuid4().hex
    # span_id = uuid.uuid4().hex[:16]  # Span ID should be 16 hex characters

    # span = {
    #     "resourceSpans": [
    #         {
    #             "resource": {
    #                 "attributes": [
    #                     {"key": "service.name", "value": {"stringValue": "my-python-app"}}
    #                 ]
    #             },
    #             "scopeSpans": [
    #                 {
    #                     "scope": {"name": "test-3"},
    #                     "spans": [
    #                         {
    #                             "traceId": trace_id,
    #                             "spanId": span_id,
    #                             "name": "yash-span3",
    #                             "kind": 2,  # SpanKind.INTERNAL
    #                             "startTimeUnixNano": str(int(time.time() * 1e9)),
    #                             "endTimeUnixNano": str(int((time.time() + 1) * 1e9)),  # 1s duration
    #                             "attributes": [
    #                                 {"key": "test", "value": {"stringValue": "yash2"}}
    #                             ],
    #                             "events": [
    #                                 {
    #                                     "name": "test-event2",
    #                                     "timeUnixNano": str(int(time.time() * 1e9)),
    #                                     "attributes": [
    #                                         {"key": "attribute1", "value": {"test": "yash"}},
    #                                          {"key": "attribute2", "value": {"test2": "yash2"}}
    #                                     ]
    #                                 }
    #                             ]
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }
    trace_id = uuid.uuid4().hex[:32]  # 32-character hex string
    parent_span_id = uuid.uuid4().hex[:16]  # 16-character hex string
    child_span_id = uuid.uuid4().hex[:16]

    # Current time in nanoseconds
    current_time_ns = int(time.time() * 1e9)
    span = {
    "resourceSpans": [
        {
            "resource": {
                "attributes": [
                    {
                        "key": "service.name",
                        "value": {"stringValue": "my-python-app"}
                    }
                ]
            },
            "scopeSpans": [
                {
                    "scope": {"name": "http-server"},
                    "spans": [
                        # Parent Span
                        {
                            "traceId": trace_id,
                            "spanId": parent_span_id,
                            "parentSpanId": "",  # No parent (root span)
                            "name": "HTTP GET /api/users",
                            "kind": 2,  # SERVER span
                            "startTimeUnixNano": str(current_time_ns),
                            "endTimeUnixNano": str(current_time_ns + int(1e9)),  # 1s duration
                            "attributes": [
                                {"key": "http.route", "value": {"stringValue": "/api/users"}},
                                {"key": "http.method", "value": {"stringValue": "GET"}},
                                {"key": "user_agent", "value": {"stringValue": "PostmanRuntime/7.28.4"}}
                            ],
                            "events": [
                                {
                                    "name": "request_received",
                                    "timeUnixNano": str(current_time_ns),
                                    "attributes": [
                                        {"key": "event.type", "value": {"stringValue": "start"}}
                                    ]
                                }
                            ]
                        },
                        # Child Span
                        {
                            "traceId": trace_id,
                            "spanId": child_span_id,
                            "parentSpanId": parent_span_id,  # Links to parent span
                            "name": "Database Query",
                            "kind": 1,  # CLIENT span
                            "startTimeUnixNano": str(current_time_ns + int(1e8)),  # 0.1s after parent
                            "endTimeUnixNano": str(current_time_ns + int(5e8)),  # 0.4s duration
                            "attributes": [
                                {"key": "db.system", "value": {"stringValue": "postgresql"}},
                                {"key": "db.query", "value": {"stringValue": "SELECT * FROM users"}}
                            ],
                            "events": [
                                {
                                    "name": "query_started",
                                    "timeUnixNano": str(current_time_ns + int(1e8)),
                                    "attributes": [
                                        {"key": "event.status", "value": {"stringValue": "ok"}}
                                    ]
                                },
                                {
                                    "name": "query_completed",
                                    "timeUnixNano": str(current_time_ns + int(5e8)),
                                    "attributes": [
                                        {"key": "event.status", "value": {"stringValue": "ok"}},
                                        {"key": "rows.returned", "value": {"intValue": 10}}
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
