# Otel-Collector-Dynatrace

## Setups

### 1. Create the OTel Collector Configuration File
- Create the OTel Collector Configuration File
- Create a `otel-collector-config.yaml` file to define how the Collector receives, processes, and exports data.

```yaml
receivers:
  otlp:
    protocols:
      http: # Receive OTLP/HTTP data on port 4318
        endpoint: "0.0.0.0:4318"
      grpc: # Receive OTLP/gRPC data on port 4317
        endpoint: "0.0.0.0:4317"
  zipkin: # Receive Zipkin spans (optional)
    endpoint: "0.0.0.0:9411"

exporters:
  otlphttp/dynatrace:
    endpoint: "https://{ENVIRONMENT_ID}.live.dynatrace.com/api/v2/otlp"
    headers:
      Authorization: "Api-Token {DYNATRACE_API_TOKEN}"

processors:
  batch: # Batch data before exporting
    send_batch_size: 1000
    timeout: 10s

service:
  pipelines:
    traces:
      receivers: [otlp, zipkin]
      processors: [batch]
      exporters: [otlphttp/dynatrace]
```

### 2. Create a Dockerfile

- Create a Dockerfile to build the OTel Collector image with your configuration

```dockerfile
FROM otel/opentelemetry-collector-contrib:latest
COPY config.yaml /etc/otelcol-contrib/config.yaml
```

### 3. Build and Run the Collector

- Build the Docker Image:
```bash
docker build -t otel-collector .
```
- Run the Container:

```bash
docker run -d -p 4317:4317 -p 4318:4318  -p 9411:9411  --name otel-collector  otel-collector
```

### 4. Run the python script to send trace.

- Create virtual Env
```bash
$ python -m venv .venv
$ source .venv/bin/activate
```
- Install dependencies
```bash
$ pip install -r requirements.txt
```
- Run Script
```bash
$ python send-json-to-collector.py
```

### 5. Verify Dynatrace

- Go To Distributed Tracing


<img width="1332" alt="Screenshot 2025-01-31 at 12 17 27 PM" src="https://github.com/user-attachments/assets/0c2905ae-94cd-4f6b-9e16-87a685eda1ea" />
<img width="1332" alt="Screenshot 2025-01-31 at 12 17 19 PM" src="https://github.com/user-attachments/assets/36505408-cddd-4ce0-93cd-1c820dc32a15" />
<img width="1332" alt="Screenshot 2025-01-31 at 12 16 57 PM" src="https://github.com/user-attachments/assets/0fc72840-c69d-49c8-bece-38f8911422e1" />
<img width="1332" alt="Screenshot 2025-01-31 at 12 16 41 PM" src="https://github.com/user-attachments/assets/5735da9d-85b1-4d1f-afd8-622644f10ea5" />



