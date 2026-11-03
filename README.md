# IT Infrastructure & Systems Operations Homelab

Personal VMware homelab documenting Linux server administration, networking, application infrastructure, and incident response.

> These are controlled personal lab exercises, not professional production incidents or work performed for WestJet.

## Lab Environment

- Ubuntu Server 24.04 LTS on VMware Workstation Pro
- Bridged networking and SSH remote administration
- Nginx 1.24.0, Apache Tomcat 10.1.55, OpenJDK 21
- UFW, Linux service management, and network troubleshooting
- PostgreSQL 16, logical backup automation, and restore verification

## Architecture

```text
Mac Client -- SSH / HTTP --> Ubuntu Server VM
                              |-- SSH :22
                              |-- Nginx :80 (static website)
                              +-- Nginx :8081 --> Tomcat :8080
```

The reverse proxy on port 8081 was tested locally. Published IP addresses are anonymized examples.

## Completed Technical Chapters

| Chapter | Topic | Documentation |
|---|---|---|
| CH01 | Linux Server Setup | [Read Report](ubuntu-server/chapters/CH01-Linux-Server-Setup.md) |
| CH02 | Network Troubleshooting | [Read Report](ubuntu-server/chapters/CH02-Network-Troubleshooting.md) |
| CH03 | DNS, TCP & HTTP | [Read Report](ubuntu-server/chapters/CH03-DNS-TCP-HTTP.md) |
| CH04 | Nginx & Tomcat Reverse Proxy | [Read Report](ubuntu-server/chapters/CH04-Nginx-Tomcat.md) |
| CH05 | PostgreSQL Database Operations | [Read Report](ubuntu-server/chapters/CH05-PostgreSQL-Database-Operations.md) |
| CH06 | PostgreSQL Backup and Recovery | [Read Report](ubuntu-server/chapters/CH06-PostgreSQL-Backup-Recovery.md) |
| CH07 | PostgreSQL Backup Automation & Monitoring | [Read Report](ubuntu-server/chapters/CH07-PostgreSQL-Backup-Automation-Monitoring.md) |
| CH08 | Linux Monitoring, Logs & Alerting | [Read Report](ubuntu-server/chapters/CH08-Linux-Monitoring-Logs-Alerting.md) |

## Incident Response Simulations

| Incident | Scenario | Outcome | Report |
|---|---|---|---|
| INC-0001 | Missing Web Resource | HTTP 404 to 200 | [Read](ubuntu-server/incidents/INC-0001.md) |
| INC-0002 | Nginx Service Outage | Connection refused to HTTP 200 | [Read](ubuntu-server/incidents/INC-0002.md) |
| INC-0003 | Tomcat Upstream Failure | HTTP 502 to 200 | [Read](ubuntu-server/incidents/INC-0003.md) |
| INC-0004 | PostgreSQL Service Outage | Connection refused to restored service | [Read](ubuntu-server/incidents/INC-0004.md) |
| INC-0005 | Accidental Data Deletion | Five records restored | [Read](ubuntu-server/incidents/INC-0005.md) |
| INC-0006 | PostgreSQL Backup Job Failure | Controlled failure detected and isolated | [Read](ubuntu-server/incidents/INC-0006-PostgreSQL-Backup-Failure.md) |
| INC-0007 | Infrastructure Health Check Failure | Controlled failure detected by systemd | [Read](ubuntu-server/incidents/INC-0007-Infrastructure-Health-Check-Failure.md) |

## Documentation Standards

Each chapter documents the objective, environment, architecture, implementation, testing evidence, troubleshooting, resolution, lessons learned, and interview talking points.

These are controlled homelab exercises, not professional production incidents.

## Roadmap

- [x] Linux server setup and SSH
- [x] Network, DNS, TCP, and HTTP troubleshooting
- [x] Nginx and Tomcat reverse proxy
- [x] Incident simulations INC-0001 through INC-0005
- [x] PostgreSQL administration
- [x] INC-0004: Database Connection Failure
- [x] CH06: PostgreSQL Backup and Recovery
- [x] INC-0005: Accidental Data Deletion
- [x] CH07: PostgreSQL Backup Automation & Monitoring
- [x] INC-0006: PostgreSQL Backup Job Failure Simulation
- [x] CH08: Linux Monitoring, Logs & Alerting
- [x] INC-0007: Infrastructure Health Check Failure Simulation
- [ ] Oracle Database operations
- [ ] RHEL administration
- [ ] VLAN configuration and troubleshooting
- [ ] High availability and failover

## Professional Development

I have a B.Sc. in Computer Science, a Software Development diploma, and hands-on software engineering experience.

This homelab helps me build practical skills in enterprise IT infrastructure, Linux administration, networking, and incident response.

My goal is to understand how systems work together, identify potential problems early, and improve service reliability.

## Author

**Ryan Back**

- [GitHub](https://github.com/ho0405)
- [Portfolio](https://ryanback.vercel.app)

## PostgreSQL Operations and Incident Response

- [CH05 — PostgreSQL Database Operations](ubuntu-server/chapters/CH05-PostgreSQL-Database-Operations.md)
- [INC-0004 — PostgreSQL Connection Failure](ubuntu-server/incidents/INC-0004.md)

## CH09 — Load Balancing, Failover & Recovery

- [CH09 — High Availability, Load Balancing & Failover](ubuntu-server/chapters/CH09-High-Availability-Load-Balancing-Failover.md)
- [INC-0008 — Backend Failure & Failover](ubuntu-server/incidents/INC-0008-Backend-Failure-Failover.md)

**Lab results:** Nginx load balancing across two backends; 10/10 successful HTTP requests during a simulated backend outage; successful backend recovery and traffic redistribution.

**Scope:** Application-level failover within a single Ubuntu VM, not full infrastructure high availability.

## CH10 — VLAN / Layer 2 Networking

- [CH10 — VLAN and Layer 2 Networking](ubuntu-server/chapters/CH10-VLAN-Layer2-Networking.md)

Configured VLAN 10/20 segmentation, validated same-VLAN connectivity and cross-VLAN isolation, and tested an IEEE 802.1Q trunk in a Linux homelab.

## CH11 — ITSM, Incident & Change Management

Practiced IT service management workflows using a
simulated airport check-in application on Ubuntu Server.

### Technical Exercises

- Created and managed a systemd application service
- Simulated an application outage using a controlled service stop
- Investigated service status, listening ports, and systemd logs
- Restored service availability and verified HTTP 200 responses
- Documented incident priority, escalation, and SLA concepts
- Prepared stakeholder and vendor communication templates
- Created a change request with risk assessment and rollback plan
- Deployed an application health endpoint update
- Investigated an initial post-restart connection failure
- Restored the original application version from a verified backup
- Confirmed service health and file integrity after rollback

### Documentation

- [INC-0009 — Application Incident](ubuntu-server/itsm/INC-0009-Checkin-Application-Incident.md)
- [SLA & Escalation Matrix](ubuntu-server/itsm/SLA-Escalation-Matrix.md)
- [Incident Communication Runbook](ubuntu-server/itsm/Incident-Communication-Runbook.md)
- [CHG-0001 — Change and Rollback](ubuntu-server/itsm/CHG-0001-Checkin-Service-Change.md)
- [Check-in Simulator Source](ubuntu-server/itsm/checkin-simulator/server.py)

### Scope

All exercises were performed in a personal homelab.
No production airport systems, users, or vendors were involved.
SLA targets and incident scenarios are hypothetical.

## CH12 — Database Connectivity & Authentication Troubleshooting

Investigated PostgreSQL connectivity and authentication
failures in a controlled Ubuntu Server homelab.

### Technical Exercises

- Verified PostgreSQL 16 cluster health and service status
- Investigated TCP connectivity using ss, nc, and pg_isready
- Compared successful connections on port 5432 with connection failures on port 5433
- Examined peer and SCRAM-SHA-256 authentication rules
- Created a temporary PostgreSQL login role
- Verified successful authentication using valid credentials
- Reproduced password authentication failures
- Analyzed PostgreSQL logs and pg_hba.conf authentication rules
- Resolved role deletion dependencies using REVOKE
- Removed the temporary test account
- Verified database health and SQL execution after cleanup

### Documentation

- [INC-0010 — PostgreSQL Connectivity & Authentication Troubleshooting](ubuntu-server/database/INC-0010-PostgreSQL-Connectivity-Authentication.md)

### Key Lessons

- TCP connectivity and database authentication are separate troubleshooting layers
- Connection refused does not necessarily indicate a database service outage
- Database logs help identify authentication failures
- Database roles may have privilege dependencies that prevent deletion
- Troubleshooting should identify the root cause before restarting services

### Scope

All exercises were conducted in a personal VMware homelab.
PostgreSQL 16 was used for hands-on testing.
Oracle Database was not installed or tested.
No production database systems were involved.
