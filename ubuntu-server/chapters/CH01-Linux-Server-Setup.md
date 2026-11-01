# CH01 — Linux Server Setup and Administration

## 1. Objective

Build a Linux server homelab using VMware Workstation to develop foundational infrastructure administration skills.

The environment supports practical exercises involving Linux services, networking, web applications, troubleshooting, and incident response.

## 2. Environment

### Physical Host
- Hypervisor: VMware Workstation Pro
- Host OS: Windows Home
- CPU: Intel Core i5-6600K
- Physical RAM: 16 GB

### Virtual Machine
- VM Name: dc-lab-srv01
- Linux Hostname: dc-labsrv01
- Operating System: Ubuntu Server 24.04 LTS
- vCPU: 2
- Allocated RAM: 4 GB
- Virtual Disk: 40 GB
- Storage: LVM
- Root Logical Volume: Approximately 19 GB
- Linux User: ryan

### Observed Memory
Command: free -h

Results:
- Total RAM: 3.8 GiB
- Used RAM: 621 MiB
- Available RAM: 3.2 GiB
- Total Swap: 3.8 GiB
- Used Swap: 0 B

These values represent the observed state on November 1, 2026.

## 3. Architecture

Windows Host
    |
    +-- VMware Workstation Pro
            |
            +-- Ubuntu Server 24.04 VM
                    |
                    +-- Linux systemd
                    +-- SSH Server
                    +-- UFW Firewall
                    +-- Nginx
                    +-- Apache Tomcat

The VM uses bridged networking.

Observed Network Configuration:
- Interface: ens33
- IPv4: 192.0.2.10/24
- Default Gateway: 192.0.2.1
- DNS Server: 192.0.2.1

## 4. Implementation

The homelab was configured with:
- Ubuntu Server 24.04 LTS
- VMware bridged networking
- SSH remote administration
- UFW firewall rules
- Nginx web server
- Apache Tomcat application server

Administration and diagnostic commands used across the lab include:

systemctl
ip addr
ip route
ss
curl
ping
resolvectl
free
journalctl

Detailed service implementation is documented in later chapters.

## 5. Testing and Evidence

### SSH
Remote SSH access from Apple computers to the Ubuntu VM was established during the lab.

### Networking
The Ubuntu VM was assigned IPv4 address 192.0.2.10.

### Web Services
Nginx successfully returned HTTP 200 responses.

### Service Administration
systemctl was used to stop, start, and inspect services during controlled incident exercises.

### Memory
The free -h command confirmed approximately 3.2 GiB of available RAM at the time of measurement.

## 6. Troubleshooting

The environment was subsequently used for controlled incident simulations:

- INC-0001: HTTP 404 resource investigation
- INC-0002: Nginx service outage
- INC-0003: Tomcat upstream outage

Incident reports are stored under:

~/homelab/incidents/

## 7. Resolution and Final State

The Linux server was successfully used for:
- Remote administration
- Network diagnostics
- Web server hosting
- Application server hosting
- Service troubleshooting
- Incident documentation

The observed incident recoveries were successful.

## 8. Lessons Learned

- Virtualization provides a safe environment for infrastructure experiments.
- Linux services can be managed and investigated using systemd.
- Network configuration and application availability must be tested separately.
- A running VM does not guarantee that every hosted service is healthy.
- Documented evidence is important for repeatable troubleshooting.

## 9. Interview Talking Points

"In my personal homelab, I configured an Ubuntu Server
environment using VMware Workstation with bridged networking.

I practiced remote Linux administration over SSH, configured
firewall rules, and deployed Nginx and Apache Tomcat.

I also simulated service failures and investigated them using
Linux service tools, HTTP tests, and application logs.

This helped me develop practical troubleshooting habits,
including verifying the actual service response rather than
assuming a successful restart means the application is healthy."

## 10. Verification Boundaries

Verified through prior homelab exercises:
- Ubuntu VM operation
- SSH connectivity
- Nginx HTTP responses
- Tomcat HTTP responses
- Controlled service recovery
- Memory measurement

Not established by this report:
- Production Linux administration experience
- Enterprise server hardware management
- High availability or automatic failover
- Production monitoring and alerting
- Formal performance or load testing

## 11. Related Documentation

- CH02-Network-Troubleshooting.md (planned)
- CH03-DNS-TCP-HTTP.md (planned)
- CH04-Nginx-Tomcat.md (planned)
- ../incidents/INC-0001.md
- ../incidents/INC-0002.md
- ../incidents/INC-0003.md
