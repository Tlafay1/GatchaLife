# Logging Update

I have replaced all `print` statements in the backend with proper `structlog` logging calls.

## Changes

1.  **`gatchalife/gamification/views.py`**:
    *   Imported `structlog`.
    *   Initialized `logger`.
    *   Replaced `print(f"Image generation failed: {e}")` with `logger.error("image_generation_failed", error=str(e))`.

2.  **`gatchalife/generated_image/services.py`**:
    *   Imported `structlog`.
    *   Initialized `logger`.
    *   Replaced `print(payload)` with `logger.info("generating_image_payload", payload=payload)`.
    *   Replaced `print(response)` with `logger.info("generated_image_response", status_code=response.status_code, response_text=response.text)`.

## Verification
- **Grep Search**: Confirmed no `print(` statements remain in the backend python files.
- **Backend Restart**: Restarted the backend service to apply changes.
