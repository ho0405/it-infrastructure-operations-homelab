# CH05 — PostgreSQL Database Operations

## Lab Scope
Personal Ubuntu Server 24.04 VMware homelab. Controlled simulation, not production experience.

## Environment
- PostgreSQL 16.15, cluster 16/main, TCP port 5432
- Data directory: /var/lib/postgresql/16/main
- Log: /var/log/postgresql/postgresql-16-main.log
- Application role: lab_app (non-superuser)
- Application database: lab_db (owned by lab_app)

## Installation and Verification
- Installed postgresql and postgresql-contrib using apt.
- Verified cluster status with pg_lsclusters.
- Verified PostgreSQL version and administrator SQL access.
- Created lab_app with LOGIN, NOSUPERUSER, NOCREATEDB, NOCREATEROLE, NOREPLICATION.
- Created lab_db with lab_app as owner and verified ownership through pg_database.
- Set the application password interactively using psql password command.
- Verified authenticated TCP connectivity to 127.0.0.1:5432.
- Confirmed current_user=lab_app and current_database=lab_db.
- Inspected current client sessions using pg_stat_activity.

## Incident Exercise
Simulated a PostgreSQL shutdown, investigated connection refusal and missing TCP listener, reviewed shutdown logs, and verified recovery with an authenticated SQL query.
See ../incidents/INC-0004.md for detailed evidence and root cause analysis.

## Key Lessons
- Service status and successful application queries are separate health checks.
- Connection refused occurs before database password authentication.
- pg_stat_activity shows current sessions, not historical sessions.
- Recovery requires an end-to-end SQL verification.

## Scope Limitations
- TCP connectivity was tested locally on the Ubuntu VM.
- No Tomcat-to-PostgreSQL application integration was performed.
- Production-grade role separation and backup/restore remain future work.

## Operational Command Reference

### Cluster and Administrator Verification
`pg_lsclusters`
`sudo -u postgres psql -c "SELECT current_database(), current_user, version();"`

### Role and Database Provisioning
`sudo -u postgres psql -c "CREATE ROLE lab_app WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;"`
`sudo -u postgres createdb -O lab_app lab_db`
`sudo -u postgres psql -c "SELECT datname, pg_get_userbyid(datdba) FROM pg_database WHERE datname = 'lab_db';"`

### Authentication and Application Connectivity
`sudo -u postgres psql -c "\password lab_app"`
`psql -h 127.0.0.1 -p 5432 -U lab_app -d lab_db -W -c "SELECT current_user, current_database(), inet_server_port(), now();"`

### Incident Diagnostics and Recovery
`sudo pg_ctlcluster 16 main stop && pg_lsclusters`
`psql -h 127.0.0.1 -p 5432 -U lab_app -d lab_db -w -c "SELECT 1;"`
`sudo ss -lntp '( sport = :5432 )'`
`sudo tail -n 40 /var/log/postgresql/postgresql-16-main.log`
`sudo pg_ctlcluster 16 main start && pg_lsclusters`

### Verified Recovery
- Cluster returned to online state.
- Application password authentication succeeded.
- SQL returned lab_app, lab_db, port 5432, and timestamp 2026-11-01 21:37:21 UTC.
- No database backup, restore, or external application integration was tested in this chapter.
