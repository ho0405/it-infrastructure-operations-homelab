# CH11 — Incident Communication Runbook

## Scope

Simulated airport check-in application incident.

All messages below are training examples.
No real users, vendors, or airport systems were affected.

## 1. Initial Incident Notification

Subject: [P2 - Investigating] Check-in Application Access Issue

We are investigating reports that several check-in agents
are unable to access the application.

The full impact is still being assessed.

Our IT Operations team is checking application availability,
network connectivity, and dependent services.

We will provide another update within 30 minutes,
or sooner if there is a significant change.

## 2. Technical Escalation

Subject: [P2 - Escalation] Check-in Application Unavailable

Hello Application Support Team,

We are investigating an application availability issue.

Initial findings from our simulated environment:

- Application service: inactive
- Application port: not listening
- HTTP health endpoint: unavailable
- Other Nginx service: healthy

Please assist with application-level investigation
and confirm whether additional dependencies are affected.

We will continue monitoring and coordinating recovery.

## 3. Vendor Escalation

Subject: [P2 - Assistance Required] Application Availability Issue

Hello Support Team,

We are requesting assistance with an application
availability incident affecting a simulated check-in service.

Please confirm receipt, provide a case reference,
and advise on the next troubleshooting steps.

We will share additional diagnostic information as needed.

## 4. Service Restoration Update

Subject: [Resolved - Technical Recovery Verified] Check-in Application

The affected service has been restarted successfully.

Technical verification completed:

- systemd service: active
- Application port: listening
- HTTP health check: 200 OK
- Application response: healthy

This confirms technical recovery in the lab environment.

In a production environment, we would also validate
end-user access and monitor service stability
before formally closing the incident.

## 5. Communication Rules

- Communicate confirmed facts.
- Avoid speculation about root cause.
- Identify the incident owner.
- Provide the next update time.
- Record communications in the incident ticket.
- Escalate when business impact or urgency increases.
- Do not promise an unverified restoration time.

## 6. Escalation When a Vendor Does Not Respond

1. Verify the support case was submitted correctly.
2. Check the agreed vendor response target.
3. Contact the vendor through an approved alternate channel.
4. Escalate through the vendor's support management process.
5. Notify the internal incident manager when appropriate.
6. Continue internal diagnosis and approved mitigation.
7. Record timestamps and escalation attempts.
8. Maintain stakeholder communication.

Do not wait passively for the vendor if critical
business operations are affected.
