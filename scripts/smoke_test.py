import json
import os
import sys
from urllib.request import urlopen

base_url = os.getenv("BASE_URL", "http://127.0.0.1:8080").rstrip("/")
expected_version = os.getenv("EXPECTED_VERSION", "0.1.0")


def get_json(path):
    with urlopen(f"{base_url}{path}", timeout=5) as response:
        if response.status != 200:
            raise RuntimeError(f"{path}: HTTP {response.status}")
        return json.load(response)


try:
    health = get_json("/health")
    if health.get("status") != "ok":
        raise RuntimeError(f"Unexpected health response: {health}")

    info = get_json("/")
    if info.get("service") != "docker-infrastructure-lab":
        raise RuntimeError(f"Unexpected service: {info}")
    if info.get("version") != expected_version:
        raise RuntimeError(f"Unexpected version: {info}")

except (OSError, ValueError, RuntimeError, AttributeError) as error:
    print(f"FAIL: {error}", file=sys.stderr)
    sys.exit(1)

print(f"PASS: health and service verified at {base_url}")
