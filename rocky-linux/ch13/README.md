# CH13 — Rocky Linux Infrastructure Operations Lab

## Overview

Hands-on infrastructure operations lab using Rocky Linux 10.2 on VMware Fusion.

This chapter focuses on Linux security, Apache availability, incident troubleshooting, and firewall change management.

## Environment

- Host: Apple Silicon Mac mini M4
- Hypervisor: VMware Fusion
- Guest OS: Rocky Linux 10.2 ARM64
- Hostname: dc-lab-rhel01
- Network: VMware NAT
- Web Server: Apache HTTP Server 2.4.63
- Security: SELinux enforcing, firewalld enabled
- Remote Administration: SSH

## Practical Skills

- Linux server installation and configuration
- SSH remote administration
- Apache service management with systemctl
- SELinux file context inspection and restoration
- AVC audit log investigation with ausearch
- firewalld runtime and permanent rule management
- Local and remote HTTP connectivity troubleshooting
- Post-change validation and configuration backup

## Incident Reports

### INC-0011 — SELinux Access Denial

Apache returned HTTP 403 after a web content file received an incorrect SELinux context.

Diagnosed using AVC audit logs and restored the correct file context with restorecon.

Result: HTTP 200 OK.

### INC-0012 — Firewall Access Failure

Apache responded locally, but remote HTTP access from the Mac failed.

Identified the missing HTTP service rule in firewalld, updated the runtime and permanent configurations, and verified connectivity after reload.

Result: HTTP 200 OK from the Mac host.

## Scope

All activities were conducted in a controlled homelab.

The incidents were intentionally simulated and do not represent production outages.

Rocky Linux is RHEL-compatible, but this lab did not use a licensed Red Hat Enterprise Linux installation.
