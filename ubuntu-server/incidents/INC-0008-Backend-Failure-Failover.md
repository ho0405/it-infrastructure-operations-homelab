# INC-0008 — Backend Failure and Load Balancer Failover

## Incident Summary

| Field | Details |
|---|---|
| Incident ID | INC-0008 |
| Date | 2026-11-03 (UTC) |
| Environment | Personal Ubuntu Server Homelab |
| Category | Application Availability |
| Type | Controlled Backend Failure Simulation |
| Status | Resolved and Validated |
| Production Impact | None |

## Executive Summary

Simulated a failure of Backend A in a two-backend Nginx load-balancing environment.

Confirmed that Backend A was unavailable, verified that Nginx continued serving client requests through Backend B, and restored Backend A.

This was a controlled personal lab exercise, not a production incident.

## Architecture

    Client -> Nginx :8090
                    |
                    +-> Backend A :9001
                    +-> Backend B :9002

## Incident Timeline

1. Verified that both backend servers returned HTTP 200.
2. Confirmed request distribution through Nginx: A=6, B=4.
3. Stopped Backend A using SIGTERM.
4. Verified that port 9001 refused connections.
5. Confirmed that Backend B remained listening on port 9002.
6. Sent ten requests through Nginx during the failure.
7. Observed ten HTTP 200 responses from Backend B.
8. Restarted Backend A.
9. Confirmed direct HTTP 200 response from Backend A.
10. Repeated the load-balancing test and observed A=4, B=6.

## Detection and Evidence

Backend A direct connection test:

    curl: (7) Failed to connect to 127.0.0.1 port 9001
    HTTP 000

Listening-port inspection showed Backend B on port 9002 and no listener on port 9001.

During failover testing:

    Backend B: 10/10 responses
    HTTP 200: 10/10 requests

After recovery:

    Backend A: 4/10 responses
    Backend B: 6/10 responses

## Impact Assessment

The failure was intentionally introduced into a personal lab.

The affected component was one Python HTTP backend process.

No production users or external services were affected.

The tested requests through Nginx continued to succeed during the backend outage.

## Root Cause Analysis

The immediate cause of the simulated outage was intentional termination of the Backend A Python HTTP process.

The process was no longer listening on port 9001, causing direct TCP connection attempts to fail.

Nginx continued handling the tested client requests using Backend B.

No unexpected infrastructure failure was identified.

## Resolution

Restarted Backend A on port 9001.

Validated its direct HTTP response.

Confirmed that Nginx resumed distributing requests across both backends.

## Lessons Learned

- Verify the failed component before claiming failover success.
- A load balancer can preserve application availability when one backend becomes unavailable.
- Validate both failure behavior and post-recovery traffic distribution.
- Application-level failover does not eliminate the single-VM failure domain.

## Follow-Up Actions

1. Preserve Nginx configuration and test evidence.
2. Consider managing backend services with systemd.
3. Test application-level failures beyond connection refusal.
4. Explore multi-VM redundancy in a future exercise.
5. Document escalation and recovery procedures.

## Interview Relevance

Demonstrates controlled incident simulation, troubleshooting, impact verification, application failover, recovery testing, and technical documentation.

This was a personal homelab exercise.
