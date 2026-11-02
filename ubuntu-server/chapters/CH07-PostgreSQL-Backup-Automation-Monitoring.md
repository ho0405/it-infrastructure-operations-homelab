# CH07 — PostgreSQL Backup Automation & Monitoring

## Executive Summary

Implemented and tested PostgreSQL backup automation in a personal VMware-based Ubuntu Server 24.04 LTS homelab.

The workflow uses Bash, PostgreSQL 16, pg_dump, pg_restore, systemd services and timers, and journald.

The exercise included backup creation, seven-day retention, controlled failure simulation, isolated database restoration, and data integrity verification.

This is a personal training environment, not a production deployment.

## Environment

| Component | Configuration |
|---|---|
| Virtualization | VMware Workstation Pro |
| OS | Ubuntu Server 24.04 LTS |
| Database | PostgreSQL 16 |
| Source database | lab_db |
| Backup format | PostgreSQL custom archive |
| Backup directory | /var/backups/postgresql |
| Backup script | /usr/local/sbin/pg-lab-backup.sh |
| systemd service | pg-lab-backup.service |
| systemd timer | pg-lab-backup.timer |
| Recovery database | lab_db_ch07_verify |

## Objectives

- Automate PostgreSQL logical backups.
- Schedule daily execution using systemd.
- Restrict backup directory and file permissions.
- Implement a seven-day retention policy.
- Detect and record backup failures.
- Restore a backup into an isolated database.
- Verify recovered records and sequence state.

## Architecture

    systemd timer (03:00 UTC)
              |
              v
    pg-lab-backup.service
              |
              v
    pg-lab-backup.sh
              |
              +-- pg_dump -Fc
              +-- Temporary .partial archive
              +-- pg_restore --list inspection
              +-- Final .dump archive (mode 600)
              +-- Seven-day retention
              +-- journald logging

## Backup Implementation

The backup directory was created with owner postgres and permissions 700.

The backup script:

1. Verifies that it runs as the postgres account.
2. Generates a UTC timestamped backup filename.
3. Uses pg_dump -Fc to create a custom-format archive.
4. Writes to a temporary .partial file.
5. Inspects archive structure using pg_restore --list.
6. Rejects empty backup files.
7. Renames the completed archive and sets permissions to 600.
8. Logs BACKUP_CREATED.
9. Finds matching backups older than seven days.
10. Deletes expired backups and logs retention events.
11. Records SUCCESS after retention processing.

The script was improved to detect retention scan and deletion failures.

Archive inspection alone does not guarantee recoverability; a separate restore test was performed.

## systemd Automation

The service is configured as Type=oneshot and runs under the postgres account.

The timer uses:

    OnCalendar=*-*-* 03:00:00
    Persistent=true
    AccuracySec=1min

The timer was enabled successfully.

Observed status:

    ActiveState=active
    SubState=waiting

The next scheduled execution was reported as November 3, 2026, at 03:00 UTC.

Manual service executions were verified. The first timer-triggered execution had not yet been observed.

## Backup Execution Evidence

Generated backup archives included:

    lab_db_20261102T155039Z.dump
    lab_db_20261102T160000Z.dump
    lab_db_20261102T193037Z.dump
    lab_db_20261102T193847Z.dump

The revised script produced these events at 19:38:47 UTC:

    START database=lab_db
    BACKUP_CREATED database=lab_db file=/var/backups/postgresql/lab_db_20261102T193847Z.dump
    SUCCESS database=lab_db file=/var/backups/postgresql/lab_db_20261102T193847Z.dump retention=completed

systemd reported successful completion.

An inactive state after successful execution is normal for a oneshot service.

## Retention Policy Verification

A test file named lab_db_retention-test.dump was created and assigned a modification time ten days in the past.

After running the backup service:

- A new backup was created.
- The expired test file was deleted.
- Existing valid backups remained.
- The deletion was recorded in journald.

Observed event:

    RETENTION deleted=/var/backups/postgresql/lab_db_retention-test.dump

This verifies retention under the tested conditions, not every possible failure scenario.

## Restore Verification

A separate database, lab_db_ch07_verify, was created.

The archive lab_db_20261102T193037Z.dump was restored using pg_restore with --exit-on-error.

The restore completed without errors.

Restored objects included:

- lab_assets table
- lab_assets_asset_id_seq sequence
- Table data
- Primary key constraint
- Hostname unique constraint

### Restored Records

| Asset ID | Hostname |
|---|---|
| 1 | dc-web-01 |
| 2 | dc-db-01 |
| 3 | dc-app-01 |
| 4 | dc-switch-01 |
| 5 | dc-backup-01 |

### Data Integrity Comparison

The original and restored lab_assets tables produced matching MD5 digests:

    lab_db:             a5865dec9e8360d3480f59c40dde972d
    lab_db_ch07_verify: a5865dec9e8360d3480f59c40dde972d

This supports equality of the compared table contents at the time of verification. It does not prove full database equivalence.

### Sequence Verification

Both databases returned:

    last_value = 5
    is_called = true

The inspected sequence state matched.

## Failure Detection

A separate failure-test service targeted a nonexistent database named lab_db_nonexistent.

The resulting systemd status was:

    ActiveState=failed
    Result=exit-code
    ExecMainStatus=1

The normal backup service returned Result=success and ExecMainStatus=0.

The backup timer remained active.

The failure-test state was later reset without removing historical journal records.

See INC-0006 for the detailed incident report.

## Monitoring Commands

    systemctl list-timers --all pg-lab-backup.timer
    systemctl status pg-lab-backup.service
    sudo journalctl -u pg-lab-backup.service --no-pager
    sudo journalctl -t pg-lab-backup --since "24 hours ago"
    sudo ls -lah /var/backups/postgresql/

These commands provide local observability. External alert notifications were not implemented.

## Risks and Limitations

### Same-Host Backup Storage

The backups reside on the same VM filesystem as the PostgreSQL database.

Host or filesystem failure could destroy both the source and backups.

Off-host backup storage is required for stronger disaster recovery protection.

### No Point-in-Time Recovery

This lab uses logical dumps. WAL archiving and point-in-time recovery were not configured.

### No Automatic Alerts

Failures are recorded locally through systemd and journald, but no email, Slack, or centralized monitoring alerts were implemented.

### Scheduled Execution Not Yet Observed

The timer was configured and enabled, but its first scheduled execution was not verified during this exercise.

### Limited Restore Verification

One archive was successfully restored, and one application table and its sequence were verified.

This was not a complete production disaster recovery test.

## Lessons Learned

- A successful backup command does not guarantee recoverability.
- Restore verification is essential.
- systemd exit codes provide useful failure signals.
- Retention errors should not be silently ignored.
- Backup creation and retention completion should be logged separately.
- Local backups alone are insufficient for comprehensive disaster recovery.

## Interview Talking Points

**How did you automate PostgreSQL backups?**

I created a Bash backup workflow using pg_dump and integrated it with a systemd service and daily timer. I implemented archive inspection, restrictive file permissions, seven-day retention, and journal logging.

**How did you verify recovery?**

I restored a generated backup into an isolated PostgreSQL database, checked five recovered asset records, compared the original and restored table contents using a digest, and verified the sequence state.

**How did you test failure handling?**

I created a separate backup service targeting a nonexistent database. The job failed with exit status 1, and systemd recorded the failure. I verified that the normal backup service and timer remained unaffected.

**What would you improve for production?**

I would add off-host backup replication, automated restore testing, proactive alerting, capacity monitoring, and documented recovery objectives.

## Final Status

Manual backup execution, retention testing, failure detection, and isolated restore verification were successful.

Scheduled timer execution, off-host backup replication, external alerts, and point-in-time recovery remain future improvements.
