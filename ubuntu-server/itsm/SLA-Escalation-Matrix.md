# CH11 — SLA and Escalation Matrix

## Scope

Personal IT Operations homelab simulation.

These targets are hypothetical training values,
not WestJet policies or contractual SLAs.

## Incident Priority Matrix

| Priority | Severity | Response Target | Recovery Target | Update Frequency |
|---|---|---|---|---|
| P1 | Critical | 5 minutes | 1 hour | 15 minutes |
| P2 | High | 15 minutes | 4 hours | 30 minutes |
| P3 | Medium | 1 hour | 1 business day | 2 hours |
| P4 | Low | 4 hours | 3 business days | 1 business day |

## Escalation Levels

### L1 — Service Desk / IT Operations

- Acknowledge the incident.
- Confirm business impact and urgency.
- Record affected users and locations.
- Perform initial health checks.
- Document findings and timestamps.

### L2 — Application / Infrastructure Support

- Investigate application and server failures.
- Review system and application logs.
- Diagnose network and database connectivity.
- Apply approved recovery procedures.

### L3 — Engineering / Vendor Support

- Investigate complex application defects.
- Analyze recurring infrastructure failures.
- Coordinate vendor troubleshooting.
- Recommend permanent corrective actions.

## Major Incident Escalation

Escalate immediately when:

- A critical service experiences widespread disruption.
- Passenger or operational impact becomes severe.
- Multiple locations are affected.
- Recovery requires cross-team coordination.

## INC-0009 Example

Incident: Simulated check-in application outage

Initial priority: P2 (provisional)

Technical evidence:
- Service inactive
- Port 8100 not listening
- Application unavailable
- Nginx remained healthy

Recovery:
- Service restarted
- Port 8100 listening
- HTTP 200 verified

Business impact was hypothetical and not measured.

## Communication Principles

1. State what is confirmed.
2. Explain the known business impact.
3. Identify the responsible team.
4. Communicate the next update time.
5. Avoid promising an unverified resolution time.
6. Record escalation and communication history.
