# INC-0009 — Check-in Application Access Failure

## Incident Information

- Incident ID: INC-0009
- Type: Simulated Airport Systems Incident
- Status: Open — Investigation
- Initial Priority: P2 (High, provisional)
- Reported Time: 08:15 (simulated local time)
- Affected Service: Airport Check-in Application
- Assigned Team: IT Operations (simulated)

## Incident Description

Several airport check-in agents reported that they
could not access the check-in application during peak hours.

The full impact and root cause have not yet been confirmed.

## Business Impact

- Check-in processing may be delayed.
- Multiple agents are potentially affected.
- Passenger experience may be impacted.
- Operational disruption is possible.

## Priority Assessment

Impact: Potentially high
Urgency: High
Initial Priority: P2 (provisional)

Escalate to P1 if evidence confirms a critical
widespread outage or severe operational disruption,
according to the organization's priority matrix.

## Initial Response Plan

1. Acknowledge the incident and record the report.
2. Confirm affected users, locations, and functions.
3. Check whether the issue is reproducible.
4. Review application availability and monitoring alerts.
5. Check network connectivity and dependent services.
6. Escalate to the application and infrastructure teams.
7. Communicate status to affected stakeholders.
8. Document actions, timestamps, and findings.

## Escalation

Initial Owner: IT Operations
Potential Escalation: Application Support / Network / Infrastructure
Incident Manager: Assign if required by severity

## SLA Tracking

- SLA policy: Not specified (simulation)
- Acknowledgement deadline: To be defined
- Resolution target: To be defined
- Next status update: To be defined

## Investigation Log

| Time | Action | Result |
|---|---|---|
| 08:15 | Incident reported | Investigation opened |

## Resolution

Pending investigation.

## Lessons Learned

To be completed after the incident simulation.


## Technical Investigation and Recovery Evidence

### Simulation Scope

- Environment: Personal Ubuntu Server 24.04 homelab
- Service: checkin-simulator.service
- Endpoint: http://127.0.0.1:8100/health
- Failure injection: Intentional systemd service stop
- Production systems affected: None

### Verified Timeline

| Time (server local) | Event | Evidence |
|---|---|---|
| 02:40:39 | Service started | systemd journal |
| 02:40:44 | Healthy baseline | HTTP 200 |
| 02:42:08 | Service stopped | systemd journal |
| 02:42:59 | Service restarted | systemd journal |
| 02:44:02 | Recovery verified | HTTP 200 and healthy JSON |

### Diagnostic Findings

- systemctl: Service was inactive during the outage.
- ss: No process was listening on TCP port 8100.
- journalctl: Recorded a successful systemd stop.
- Nginx: Port 80 continued responding with HTTP 200.
- Root cause of simulated outage: Intentional service stop.

### Recovery Actions

1. Started checkin-simulator.service using systemctl.
2. Verified the service was active.
3. Confirmed TCP port 8100 was listening.
4. Sent an HTTP request to /health.
5. Confirmed HTTP 200 and status healthy.
6. Reviewed journal logs for recovery evidence.

### Recovery Metrics

- Service stopped: 02:42:08
- Service started: 02:42:59
- First recorded successful post-recovery check: 02:44:02
- Stop-to-start interval: 51 seconds
- Stop-to-verified-health interval: 1 minute 54 seconds

These are observed lab timestamps, not production SLA metrics.

### Operational Conclusion

Technical service recovery was verified.

In a production incident, final closure would also require
business-user validation, monitoring, and stakeholder updates.

### Lessons Learned — Technical

- A running service and a listening port should be checked separately.
- HTTP health checks provide application-level verification.
- systemd logs help establish the incident timeline.
- A successful restart alone is not sufficient evidence of recovery.
- Incident documentation should distinguish observed facts
  from assumptions about business impact.
