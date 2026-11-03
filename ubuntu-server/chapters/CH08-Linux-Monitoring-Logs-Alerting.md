# CH08 — Linux Monitoring, Logs & Alerting

## Executive Summary

Implemented and validated an automated infrastructure health-check workflow in a personal VMware-based Ubuntu Server 24.04 LTS homelab.

The workflow uses Bash, curl, pg_isready, systemd services and timers, and journald to monitor Nginx, the Tomcat reverse proxy, and PostgreSQL.

Testing confirmed successful health checks, controlled connection-failure detection, non-zero exit codes, and systemd failure logging.

External alert delivery has not been implemented.

This is a personal training environment, not a production deployment.

## Environment

| Component | Configuration |
|---|---|
| Virtualization | VMware Workstation Pro |
| OS | Ubuntu Server 24.04 LTS |
| Web server | Nginx 1.24 |
| Application server | Apache Tomcat 10.1.55 |
| Database | PostgreSQL 16 |
| Health-check script | /usr/local/sbin/infrastructure-health-check.sh |
| systemd service | infrastructure-health-check.service |
| systemd timer | infrastructure-health-check.timer |
| Logging | systemd journal / journalctl |

## Objectives

- Inspect CPU load, memory, disk, and processes.
- Verify Nginx and Tomcat HTTP availability.
- Verify PostgreSQL connection readiness.
- Create a reusable Bash health-check script.
- Return exit code 0 for healthy and 1 for unhealthy results.
- Schedule checks using a systemd timer.
- Review successful and failed execution logs.
- Simulate a failure without disrupting running services.

## Architecture

    systemd timer (every ~5 minutes)
                  |
                  v
    infrastructure-health-check.service
                  |
                  v
    infrastructure-health-check.sh
                  |
                  +-- curl Nginx (port 80)
                  +-- curl Tomcat proxy (port 8081)
                  +-- pg_isready PostgreSQL (port 5432)
                  |
                  v
           HEALTHY / UNHEALTHY
                  |
                  v
            exit code 0 / 1
                  |
                  v
             systemd journal

## System Monitoring

Inspected system health using uptime, free, df, ps, and systemctl.

Confirmed that Nginx, the Tomcat reverse proxy, and PostgreSQL were responding normally.

## Health Check Implementation

The Bash script uses curl with a five-second timeout to test HTTP endpoints.

It expects HTTP 200 for the Nginx and Tomcat proxy checks.

PostgreSQL readiness is checked using pg_isready.

The script prints individual OK or FAIL results and a final HEALTHY or UNHEALTHY result.

A healthy execution exits with status 0; an unhealthy execution exits with status 1.

The root-owned script was installed with executable permissions.

## systemd Automation

The service uses Type=oneshot, DynamicUser=yes, and NoNewPrivileges=true.

The timer uses:

    OnBootSec=2min
    OnUnitActiveSec=5min
    AccuracySec=10s

The timer was enabled and repeated successful executions were observed in journalctl.

The interval may vary slightly because of timer accuracy settings.

## Successful Execution Evidence

    [OK] Nginx - HTTP 200
    [OK] Tomcat Proxy - HTTP 200
    [OK] PostgreSQL - accepting connections
    RESULT: HEALTHY
    EXIT_CODE=0

## Controlled Failure Simulation

A temporary test replaced the Nginx endpoint with port 19999, where no service was listening.

The original health-check script and running infrastructure services were not modified.

The corrected systemd-run test used Bash pipefail to preserve the failure exit status.

Observed journal output on November 3, 2026 UTC:

    curl: (7) Failed to connect to 127.0.0.1 port 19999
    [FAIL] Nginx - HTTP 000
    [OK] Tomcat Proxy - HTTP 200
    [OK] PostgreSQL - accepting connections
    RESULT: UNHEALTHY
    status=1/FAILURE
    Failed with result 'exit-code'

HTTP 000 is a curl output placeholder for a failed connection, not an HTTP response status.

The test demonstrated detection and logging of a simulated endpoint failure.

## Operational Lessons

- A running service does not necessarily guarantee application availability.
- Endpoint checks help verify application-level responsiveness.
- Non-zero exit codes allow systemd to record failed executions.
- journalctl provides timestamped evidence for troubleshooting.
- Monitoring and alert delivery are different capabilities.

## Limitations and Next Steps

- No email, SMS, or external alert delivery has been configured.
- The health check validates endpoint readiness, not full business transactions.
- Monitoring currently runs on the same VM as the monitored services.
- A host or VM outage could prevent the local monitoring process from running.
- Future improvements include external monitoring, alert routing, and additional application checks.
