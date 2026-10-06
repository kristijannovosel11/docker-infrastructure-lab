# Scenario 1: Wrong upstream port

## Fault introduced
Changed Nginx proxy_pass from http://api:8000 to http://api:8001
and reloaded the configuration.

## Symptoms
- Requests through Nginx returned HTTP 502 Bad Gateway.
- Both containers remained running.
- The API healthcheck remained healthy.

## Investigation
- Checked container status with docker compose ps.
- Inspected Nginx logs.
- Found: connect() failed (111: Connection refused).
- Confirmed that Nginx was attempting to connect to port 8001.
- Requested http://api:8000/health from the Nginx container.
  The API returned {"status":"ok"}.

## Root cause
Nginx targeted port 8001, but Gunicorn was listening on port 8000.

## Resolution
Restored proxy_pass to http://api:8000, validated the configuration
with nginx -t, and reloaded Nginx.

## Verification
A repeated request through Nginx returned HTTP 200 and {"status":"ok"}.
The first request immediately after reload still returned 502;
a later request succeeded. Reload timing was a possible explanation,
but was not independently verified.

## Lessons
- A healthy backend does not guarantee a working proxy path.
- Valid configuration syntax does not guarantee correct connectivity.
- Verify recovery with an actual HTTP request after reloading.
