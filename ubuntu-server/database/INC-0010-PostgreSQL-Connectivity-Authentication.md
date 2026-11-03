# INC-0010 — PostgreSQL Connectivity and Authentication Troubleshooting

## Environment
- Ubuntu Server 24.04 LTS
- PostgreSQL 16.15
- PostgreSQL cluster: 16/main
- Database port: 5432
- Listening address: 127.0.0.1
- Environment: Personal VMware homelab

## Incident Type
Simulated database connectivity and authentication failures.

## Scenario 1 — Incorrect TCP Port

### Symptoms
- Connection to port 5432 succeeded.
- Connection to port 5433 returned Connection refused.

### Investigation
- Checked PostgreSQL cluster using pg_lsclusters.
- Verified listening ports using ss.
- Tested TCP connectivity using nc.

### Root Cause
Incorrect database port configuration in the simulated client connection.

### Resolution
Use the correct PostgreSQL port, 5432.

## Scenario 2 — Authentication Failure

### Symptoms
PostgreSQL returned:

FATAL: password authentication failed for user "ch12_lab_user"

### Investigation
- Verified PostgreSQL was accepting connections.
- Confirmed TCP authentication used SCRAM-SHA-256.
- Successfully authenticated using the correct password.
- Reproduced authentication failure using an incorrect password.
- Reviewed PostgreSQL server logs.
- Confirmed the connection matched pg_hba.conf line 125.

### Root Cause
Incorrect password supplied by the test client.

### Resolution
Verified successful authentication using the correct credentials.

No PostgreSQL restart was required.

## Cleanup and Validation
- Revoked CONNECT privileges from the temporary lab role.
- Successfully removed ch12_lab_user.
- Confirmed the role no longer existed.
- Verified PostgreSQL remained online.
- Confirmed pg_isready accepted connections.
- Successfully executed SELECT 1.

## Lessons Learned
1. TCP connectivity and database authentication are separate troubleshooting layers.
2. Connection refused does not necessarily mean the database service is down.
3. Authentication failures should be investigated using database logs and authentication rules.
4. Database role dependencies must be resolved before removing roles.
5. Service restarts should not be the default response to application connectivity errors.

## Outcome
Completed — Personal Homelab Simulation

This exercise was conducted in a controlled lab environment and does not represent a production incident.
