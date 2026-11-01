# CH06 — PostgreSQL Backup and Recovery

## Lab Environment
- Host: dc-labsrv01 (Ubuntu Server 24.04 LTS, VMware Workstation Pro)
- PostgreSQL: 16.15
- Source database: lab_db
- Recovery database: lab_db_recovery
- Backup: /tmp/ch06_lab_db_backup.dump
- Exercise date: November 1, 2026 (UTC timestamps)

> Controlled personal homelab exercise, not a production incident.

## Objective
Create a PostgreSQL logical backup, inspect its contents, restore it into an isolated database, simulate accidental data deletion, and validate successful recovery.

## Architecture
Source DB (lab_db) -> pg_dump custom archive -> Recovery DB (lab_db_recovery) -> simulated deletion -> data-only restore.

## 1. Baseline and Test Data
Created public.lab_assets with an identity primary key, unique hostname, asset type, status, and creation timestamp.
Inserted five fictional infrastructure assets: four active and one in maintenance.
Verified all five records with SELECT ordered by asset_id.

## 2. Logical Backup
Command: sudo -u postgres pg_dump -Fc -d lab_db -f /tmp/ch06_lab_db_backup.dump
Result: Backup file created successfully; reported size 3.0K.
Archive timestamp: 2026-11-01 22:30:11 UTC.
Archive format: CUSTOM; compression: gzip; PostgreSQL version: 16.15.

## 3. Backup Inspection
Command: sudo -u postgres pg_restore --list /tmp/ch06_lab_db_backup.dump
Verified archive entries for TABLE, TABLE DATA, SEQUENCE, SEQUENCE SET, primary key, and unique hostname constraint.
Archive inspection verifies readable metadata, but does not independently prove successful data restoration.

## 4. Isolated Restore Test
Command: sudo -u postgres createdb lab_db_recovery
Command: sudo -u postgres pg_restore --verbose --exit-on-error -d lab_db_recovery /tmp/ch06_lab_db_backup.dump
Result: Table, sequence, table data, sequence state, and constraints restored without reported errors.
Post-restore SQL verification returned all five original asset records with matching IDs, hostnames, asset types, and statuses.

## 5. INC-0005: Accidental Data Deletion
Scenario: A DELETE statement without a WHERE clause removed all five asset records from the isolated recovery database.
Command: sudo -u postgres psql -d lab_db_recovery -c "DELETE FROM lab_assets;"
Observed result: DELETE 5.
Verification: SELECT COUNT(*) FROM lab_assets returned 0.
Impact: 100% of the five test records in lab_db_recovery were deleted. The source lab_db was not modified.

## 6. Data Recovery
Command: sudo -u postgres pg_restore --verbose --exit-on-error --data-only -d lab_db_recovery /tmp/ch06_lab_db_backup.dump
Observed result: pg_restore processed table data and executed SEQUENCE SET without reported errors.
Recovery verification: All five asset records were restored with their original IDs, hostnames, asset types, and statuses.
Source comparison: lab_db|5|1|5 and lab_db_recovery|5|1|5 (database, count, minimum ID, maximum ID).
Sequence verification: last_value=5 and is_called=true.
Recovery outcome: The five deleted test records were successfully restored from the logical backup.

## 7. Recovery Objectives and Limitations
- RPO: No formal recovery point objective was configured or measured. The logical backup restores data as of its creation time.
- RTO: No recovery time objective was defined, and elapsed recovery time was not measured.
- This exercise demonstrates logical backup and restore, not point-in-time recovery (PITR), WAL archiving, replication, or automatic failover.
- The backup was stored in /tmp on the same VM. This is temporary lab storage, not a durable off-host backup strategy.
- Data-only restoration is appropriate here because the target table existed and was verified empty. Restoring into a populated table may cause duplicate-key conflicts.

## 8. Production Considerations
- Schedule automated backups and monitor backup job failures.
- Store encrypted backup copies outside the database host, with appropriate access controls and retention policies.
- Periodically test restoration in an isolated environment and validate record counts, constraints, and application functionality.
- Define RPO and RTO based on business requirements; evaluate WAL archiving and PITR where necessary.
- Use least-privilege database roles and restrict destructive operations.
- Prefer explicit transactions and reviewed WHERE clauses for high-risk data changes.

## 9. Lessons Learned and Interview Talking Points
- A successful pg_dump command does not prove that a backup can be restored.
- Archive inspection, isolated restoration, SQL verification, and sequence validation provide stronger recovery evidence.
- A committed DELETE without a WHERE clause cannot be reversed with a later ROLLBACK.
- I practiced diagnosing a controlled data-loss incident and recovering five records from a PostgreSQL logical backup.
- This was a personal homelab simulation, not a production incident.
