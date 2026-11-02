# INC-0006 — PostgreSQL Backup Job Failure

## Incident Overview

| Field | Details |
|---|---|
| Incident ID | INC-0006 |
| Category | Database Operations / Backup Automation |
| Environment | Ubuntu Server 24.04 LTS, PostgreSQL 16 |
| Date | November 2, 2026 |
| Severity | Low — controlled homelab simulation |
| Status | Resolved |
| Impact | Isolated test backup job failed; production-like lab backup remained unaffected |

## Summary

Simulated a PostgreSQL backup failure by configuring an isolated systemd service to back up a nonexistent database.

The purpose was to validate failure detection, exit-code propagation, journald visibility, and isolation from the normal backup workflow.

This was an intentional homelab incident, not an unexpected production outage.

## Expected Behaviour

A backup job targeting a nonexistent database should:

1. Fail rather than report success.
2. Return a nonzero exit code.
3. Record an actionable error in journald.
4. Preserve the normal backup service and timer.
5. Avoid creating a misleading successful backup artifact.

## Failure Injection

A separate test script was configured to target:

    lab_db_nonexistent

The test used:

    /usr/local/sbin/pg-lab-backup-failure-test.sh

It was executed through:

    pg-lab-backup-failure-test.service

This isolated the simulation from the normal pg-lab-backup.service.

## Observed Failure

At approximately 19:24:58 UTC, the test service failed.

PostgreSQL reported:

    FATAL: database "lab_db_nonexistent" does not exist

systemd recorded:

    ActiveState=failed
    Result=exit-code
    ExecMainStatus=1

The failure was visible in the service journal.

## Root Cause

The backup script targeted a database name that did not exist.

The PostgreSQL pg_dump operation therefore failed, and the script returned a nonzero status.

This was an intentionally introduced configuration error.

## Troubleshooting and Validation

The investigation focused on:

- Checking the failing service's systemd result.
- Inspecting journald for PostgreSQL error messages.
- Confirming the failure was caused by the nonexistent database.
- Checking the normal backup service independently.
- Verifying the daily backup timer remained active.

The normal backup service subsequently completed successfully with:

    Result=success
    ExecMainStatus=0

The normal timer remained enabled and waiting.

## Recovery

After collecting the evidence, the failed state of the isolated test service was cleared using systemd reset-failed.

The service returned to:

    ActiveState=inactive
    SubState=dead
    Result=success

Historical journal entries remained available for review.

No database recreation or data restoration was required because the failure affected only the isolated test job.

## Impact Assessment

The incident did not interrupt PostgreSQL availability or modify application data.

The normal backup script, service, and timer were not intentionally changed during the failure simulation.

No production systems were involved.

## Lessons Learned

- A backup job must fail visibly when its source database is unavailable.
- Nonzero exit codes are essential for reliable service monitoring.
- systemd and journald provide useful local incident evidence.
- Failure tests should be isolated from working backup automation.
- Resetting a failed service state does not erase historical journal evidence.
- Local logging should eventually be complemented by external alerts.

## Recommended Improvements

1. Add alerting when a backup service fails.
2. Monitor the age of the latest successful backup.
3. Replicate backups to independent storage.
4. Automate periodic restore verification.
5. Document recovery objectives and escalation procedures.

## Interview Summary

I simulated a PostgreSQL backup failure using a separate systemd service configured with an invalid database name. I confirmed that pg_dump failed, systemd captured exit status 1, and journald recorded the error. I then verified that the normal backup service and timer were unaffected and cleared the test service's failed state while retaining the incident logs.

## Final Status

**Resolved — controlled failure detected and isolated successfully.**

The incident demonstrated local backup failure detection. Automated external alerting remains a future improvement.
