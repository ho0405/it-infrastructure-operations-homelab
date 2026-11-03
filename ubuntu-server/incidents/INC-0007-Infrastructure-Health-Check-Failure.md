# INC-0007 — Infrastructure Health Check Failure Simulation

## Incident Summary

| Field | Details |
|---|---|
| Incident ID | INC-0007 |
| Date | 2026-11-03 (UTC) |
| Environment | Personal Ubuntu Server 24.04 LTS Homelab |
| Category | Application Availability Monitoring |
| Type | Controlled Failure Simulation |
| Status | Test Completed |
| Production Impact | None |

## Executive Summary

Conducted a controlled failure simulation to validate the infrastructure health-check monitoring workflow.

The Nginx health-check endpoint was temporarily replaced with an unused local port (19999) without modifying the original script or stopping the running Nginx service.

The monitoring script detected the simulated connection failure, reported an UNHEALTHY result, and returned a non-zero exit status.

systemd recorded the failed execution in journald.

This was a personal homelab exercise, not a production incident.

## Expected Behaviour

The health-check workflow should:

1. Check Nginx HTTP availability.
2. Check Tomcat reverse-proxy availability.
3. Check PostgreSQL connection readiness.
4. Report individual service health.
5. Return exit code 1 if any required check fails.
6. Record the failed execution through systemd and journald.

## Failure Injection

Executed the health-check script through a temporary systemd unit.

The test substituted:

    http://127.0.0.1/

with:

    http://127.0.0.1:19999/

The command used Bash pipefail to preserve the failing script's exit status through the pipeline.

The original script and production-like homelab services remained unchanged.

## Observed Evidence

Timestamp: 2026-11-03 00:33:23 UTC

    curl: (7) Failed to connect to 127.0.0.1 port 19999
    [FAIL] Nginx - HTTP 000
    [OK] Tomcat Proxy - HTTP 200
    [OK] PostgreSQL - accepting connections
    RESULT: UNHEALTHY

systemd reported:

    Main process exited, code=exited, status=1/FAILURE
    Failed with result 'exit-code'

HTTP 000 indicates that curl did not receive a valid HTTP response. It is not an HTTP status code.

## Impact Assessment

- The failure was intentionally introduced into a temporary test execution.
- The actual Nginx service was not stopped.
- Tomcat and PostgreSQL checks continued to pass.
- No production systems, customers, or airport operations were affected.

## Root Cause Analysis

The simulated failure was caused by directing the Nginx HTTP check to port 19999, where no service was listening.

The resulting TCP connection failure caused curl to fail.

The health-check script correctly identified the failed endpoint and returned exit code 1.

The systemd unit correctly recorded the non-zero exit status.

No underlying infrastructure outage was identified.

## Resolution and Validation

No service restart or configuration rollback was required because the failure was isolated to the temporary test execution.

Validation confirmed:

- Nginx endpoint failure was detected.
- Tomcat and PostgreSQL remained healthy.
- The overall result was UNHEALTHY.
- systemd recorded status=1/FAILURE.
- journald retained timestamped diagnostic evidence.

## Lessons Learned

- A successful systemd service start does not guarantee a successful execution.
- Exit codes provide machine-readable execution outcomes.
- journalctl supports incident investigation and evidence collection.
- Controlled fault injection can validate monitoring without disrupting services.
- Monitoring detection does not automatically mean an external alert was delivered.

## Preventive and Follow-Up Actions

1. Preserve the health-check script and test documentation.
2. Continue validating both healthy and unhealthy execution paths.
3. Add external alert notifications in a future chapter.
4. Consider monitoring from a separate host to detect VM-level failures.
5. Extend health checks beyond endpoint readiness to application functionality.

## Interview Relevance

This exercise demonstrates practical experience with:

- Linux service monitoring
- Incident triage
- Controlled failure simulation
- Root cause analysis
- systemd and journalctl
- Exit-code-based failure detection
- Technical incident documentation

All work was completed in a personal homelab environment.
