# Enterprise Grade Logging Implementation

I have implemented a structured logging system for the backend using `structlog`. This provides machine-readable JSON logs that are perfect for debugging and can be easily ingested by log management tools in the future.

## Features

1.  **Structured JSON Output**: All logs are now output as JSON objects, making them easy to parse and filter.
    *   Example: `{"event": "request_finished", "status_code": 200, "duration": 0.045, ...}`
2.  **Request Context**: Every log entry includes context about the request:
    *   `request_id`: A unique ID for tracing a request across multiple log lines.
    *   `method`: HTTP method (GET, POST, etc.).
    *   `path`: The requested URL path.
    *   `ip`: The client's IP address.
    *   `user_agent`: The client's user agent.
3.  **Performance Monitoring**: The middleware logs the duration of every request, allowing you to spot slow endpoints.
4.  **Application Logic Tracing**: Added detailed logging to the `zapier_webhook` to trace:
    *   Incoming webhook payloads.
    *   Duplicate task detection.
    *   Reward calculation breakdowns (base, difficulty, streak, crit).
    *   Level-up events.

## How to View Logs

Since the application is running in Docker, you can view the logs using the standard Docker command:

```bash
docker logs -f gatchalife-backend
```

You can use tools like `jq` to filter and pretty-print the logs:

```bash
# View all logs pretty-printed
docker logs -f gatchalife-backend | jq .

# Filter for errors
docker logs -f gatchalife-backend | jq 'select(.level == "error")'

# Filter for a specific request ID
docker logs -f gatchalife-backend | jq 'select(.request_id == "YOUR_REQUEST_ID")'
```

## Configuration

The configuration is located in `gatchalife/settings.py` under the `LOGGING` and `structlog.configure` sections. The middleware is defined in `gatchalife/middleware.py`.
