# CHG-0001 — Check-in Service Configuration Change

## Change Information

- Change ID: CHG-0001
- Type: Simulated Normal Change
- Status: Completed — Lab Simulation
- Related Incident: INC-0009
- Environment: Personal Ubuntu Server Homelab
- Service: checkin-simulator.service
- Proposed Change: Update the application health-check configuration
- Production Impact: None

## Business Justification

Improve service health monitoring and make application
availability issues easier to identify and troubleshoot.

## Risk Assessment

Risk Level: Low in the isolated homelab.

Potential risks:
- Application fails to start after modification.
- Health endpoint returns an unexpected response.
- Monitoring reports incorrect service availability.

## Pre-Change Checklist

1. Confirm change approval before implementation.
2. Verify current application health.
3. Record current configuration.
4. Back up the application file.
5. Confirm rollback procedure.
6. Notify affected stakeholders if applicable.

## Implementation Plan

The following implementation steps were executed during the homelab exercise.

1. Back up server.py.
2. Modify the health-check configuration.
3. Validate Python syntax.
4. Restart the simulated application service.
5. Verify systemd service status.
6. Confirm TCP port 8100 is listening.
7. Confirm HTTP 200 from /health.
8. Review application logs.

## Rollback Plan

If validation fails:

1. Stop the simulated application service.
2. Restore the backed-up server.py.
3. Validate Python syntax.
4. Start the service.
5. Verify the original health endpoint.
6. Review logs.
7. Document rollback results.

## Validation Criteria

- Service state: active
- TCP port 8100: listening
- HTTP /health: 200 OK
- JSON status: healthy
- No unexpected application errors

## Approval and Execution

- Change approval: Self-authorized homelab exercise
- Implementation: Completed and verified
- Rollback: Completed and verified
- Post-change validation: Passed

## Lessons Learned

Document actual outcomes after an approved
change simulation is completed.


## Actual Implementation and Rollback Results

### Execution Scope

- Environment: Personal Ubuntu Server 24.04 homelab
- Service: checkin-simulator.service
- Change: Added version 1.1 to the health endpoint
- Production impact: None
- Approval: Self-directed lab exercise; no production approval

### Pre-Change Validation

- Service status: active
- Health endpoint: healthy
- Original file backup: created
- SHA-256 hashes: matched
- Backup file comparison: passed

### Deployment Results

- Candidate Python syntax validation: passed
- Candidate deployed to server.py
- Service restart: completed
- Initial HTTP health check: connection refused
- Subsequent investigation: service active
- TCP port 8100: listening
- HTTP response: 200 OK
- Application version: 1.1

The initial connection failure may have been
related to application readiness timing.
The exact cause was not confirmed.

### Rollback Results

- Original backup restored to server.py
- Service restarted successfully
- Initial HTTP connection attempt: refused
- Subsequent health check: successful
- Original JSON response: restored
- File integrity comparison: passed
- Final service state: active

### Final Outcome

Change deployment: Verified successful

Rollback exercise: Verified successful

Final application version: Original baseline

Production systems affected: None

### Operational Lessons

1. A running service does not guarantee application readiness.
2. Validate application endpoints after deployment.
3. Use bounded retries for startup health checks.
4. Preserve verified backups before making changes.
5. Confirm application functionality after rollback.
6. Record failures and recovery evidence accurately.
