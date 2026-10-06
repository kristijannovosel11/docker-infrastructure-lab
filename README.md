# Docker Infrastructure Lab

I started this project to get hands-on practice with Docker,
Linux and basic infrastructure troubleshooting.

I used an Ubuntu Server VM in VirtualBox.
I built the lab with guidance and tested the setup myself.

## What I did

- Set up SSH access from my Windows computer.
- Installed Docker Engine and Docker Compose.
- Created a small Python API with Flask and Gunicorn.
- Wrote a Dockerfile and built the application image.
- Configured the API to run as a non-root user.
- Added Nginx as a reverse proxy.
- Connected both services using Docker Compose.
- Added an API healthcheck and a Python smoke test.

## How it works

Nginx receives requests on host port 8080.
It forwards them to the API on port 8000.

Both containers use the same Docker network.
Only Nginx has a published host port.

The API has two endpoints:

- `/` returns the service name, version and hostname.
- `/health` returns `{"status":"ok"}`.

## Problems I tested

### Wrong backend port

I changed the Nginx upstream port from 8000 to 8001.
Requests returned 502, although the API stayed healthy.

I checked the logs and tested the API from the Nginx container.
I restored the correct port and confirmed a 200 response.

[Scenario notes](docs/01-wrong-upstream-port.md)

### Stopped backend

I stopped the API container.
Nginx stayed running, but requests returned 504.

I checked the container status and Nginx logs.
I started the API again and confirmed recovery.

[Scenario notes](docs/02-backend-unavailable.md)

## Automated check

I added a smoke test for both endpoints.
It checks the HTTP response, service name and version.

I tested it with a wrong expected version and a stopped API.
Both checks failed. After recovery, the test passed again.

## Run the lab

Requires Docker Engine, Docker Compose and Python 3.
From the project root:

```bash
docker compose up -d --build --wait --wait-timeout 60
python3 scripts/smoke_test.py
```

Docker commands may require `sudo`.

Open http://localhost:8080 on the Docker host.
For access from Windows, I used VirtualBox NAT port forwarding.

## What I learned

I saw that a healthy API does not guarantee a working proxy path.
I practised checking container status, reading logs and testing
connectivity before changing the configuration.

## GitHub Actions

I added a CI workflow that runs on pushes to main and pull requests.
It builds and starts the containers.
It checks the Nginx configuration and runs my smoke test.
If a check fails, it prints container status and logs.
The first run passed on a GitHub-hosted Ubuntu runner.

## CI failure exercise

I deliberately changed the application version in a draft pull request.
The smoke test detected the mismatch.
I restored the version and confirmed that the next check passed.

[Scenario notes](docs/03-ci-version-mismatch.md)
