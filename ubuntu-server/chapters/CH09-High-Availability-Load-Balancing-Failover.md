# CH09 — High Availability Concepts, Load Balancing & Failover

## Executive Summary

Configured and tested an Nginx load balancer with two Python HTTP backend servers in a personal Ubuntu Server 24.04 LTS homelab.

Validated request distribution, a controlled backend failure, continued application availability through the remaining backend, and recovery of the failed backend.

This exercise demonstrates application-level failover within a single VM. It does not provide host-level high availability.

## Environment

| Component | Configuration |
|---|---|
| Virtualization | VMware Workstation Pro |
| Operating system | Ubuntu Server 24.04 LTS |
| Load balancer | Nginx |
| Load balancer endpoint | 127.0.0.1:8090 |
| Backend A | Python HTTP server, 127.0.0.1:9001 |
| Backend B | Python HTTP server, 127.0.0.1:9002 |
| Test client | curl |
| Network scope | Loopback, single VM |

## Objectives

- Configure two independent HTTP backend processes.
- Configure Nginx upstream load balancing.
- Verify HTTP request distribution.
- Simulate a backend outage.
- Verify service continuity through the healthy backend.
- Restore the failed backend.
- Verify that both backends receive traffic again.

## Architecture

    curl client
         |
         v
    Nginx :8090
         |
         +---- Backend A :9001
         |
         +---- Backend B :9002

All endpoints were bound to the local VM.

## Implementation

Created separate directories and index.html files for Backend A and Backend B.

Started Python HTTP servers on ports 9001 and 9002.

Configured an Nginx upstream pool containing both backend endpoints.

Added a separate Nginx listener on 127.0.0.1:8090.

Existing Nginx ports 80 and 8081 were preserved.

Validated the configuration using nginx -t before reloading Nginx.

## Initial Backend Validation

Both backends returned HTTP 200 OK.

Backend A returned:

    Response from Backend A

Backend B returned:

    Response from Backend B

## Initial Load Balancing Test

Sent ten requests through Nginx on port 8090.

Observed results:

- Backend A: 6 responses.
- Backend B: 4 responses.
- Both backends successfully served requests.

Nginx used its default round-robin upstream selection.

## Controlled Backend Failure

Identified Backend A's Python process and sent SIGTERM to stop it.

Confirmed that port 9001 no longer accepted connections.

Observed:

    curl: (7) Failed to connect to 127.0.0.1 port 9001
    HTTP 000

Port 9002 remained listening.

HTTP 000 was curl's output for a connection failure, not an HTTP response status.

## Failover Validation

Sent ten requests to the Nginx load balancer while Backend A was unavailable.

Results:

- Backend B: 10 responses.
- HTTP 200: 10 out of 10 requests.
- No failed client requests were observed during this test.

This demonstrated that the remaining backend continued serving the tested requests.

## Recovery Validation

Restarted Backend A on port 9001.

Verified that Backend A returned HTTP 200 OK directly.

Sent another ten requests through the Nginx load balancer.

Results:

- Backend A: 4 responses.
- Backend B: 6 responses.
- Both backends received requests after recovery.

## Operational Lessons

- Load balancing distributes requests across multiple backend processes.
- A backend outage can be isolated without necessarily interrupting client requests.
- Direct backend checks help confirm that a failure was actually introduced.
- Recovery should be validated through the load balancer, not only through the backend endpoint.
- A single-VM architecture remains vulnerable to VM and host outages.

## Limitations and Future Improvements

- Both backends and Nginx run on one VM.
- The test does not demonstrate multi-host redundancy.
- The test does not measure recovery time objectives or recovery point objectives.
- Ten successful requests do not establish a production availability guarantee.
- Backend processes were started manually, not managed as persistent systemd services.
- Future exercises may include separate VMs, external monitoring, and additional load balancer redundancy.

## Interview Relevance

Practiced Nginx upstream configuration, HTTP troubleshooting, application-level failover, service recovery, and evidence-based incident validation.

All work was performed in a personal homelab.
