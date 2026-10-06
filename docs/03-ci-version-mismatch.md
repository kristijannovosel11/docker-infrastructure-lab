# Scenario 3: CI detects an unexpected version

## What I changed
I created a separate branch and a draft pull request.
I changed APP_VERSION from 0.1.0 to 0.2.0 in compose.yaml.
The smoke test still expected 0.1.0.

## What happened
The containers built and started successfully.
The Nginx configuration check passed.
The health endpoint responded successfully.
The smoke test failed with "Unexpected version" and exit code 1.
The workflow printed diagnostics and cleaned up the containers.

## How I fixed it
I restored APP_VERSION to 0.1.0.
I committed and pushed the fix to the same branch.
The pull request check ran again and passed.

## What I learned
A responding application can still return an unexpected result.
CI can detect this before I merge a change.
I checked the failed step before making the fix.

## Evidence
[Draft pull request and CI checks](https://github.com/kristijannovosel11/docker-infrastructure-lab/pull/1)
