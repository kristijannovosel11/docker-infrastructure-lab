# Scenario 2: Backend unavailable

## Fault introduced
Stopped the API service with:
docker compose stop api

## Symptoms
- Requests through Nginx returned HTTP 504 Gateway Time-out.
- Nginx remained running.
- The API container showed Exited (0).

## Investigation
Checked all containers with docker compose ps -a.
Nginx logs reported:
upstream timed out (110: Operation timed out) while connecting to upstream

The upstream target used the correct application port, 8000.

## Root cause
The API container had been deliberately stopped.
Nginx could not establish a connection to the backend before
the configured connection timeout expired.

## Resolution
Started the existing API container with:
docker compose start api

## Verification
After the API became healthy, a request through Nginx
returned HTTP 200 and {"status":"ok"}.

## Lessons
- A running proxy does not guarantee an available backend.
- Exited (0) indicates a clean exit, not necessarily an application crash.
- Diagnose proxy errors using container state and logs.
- HTTP status alone does not identify the root cause.
