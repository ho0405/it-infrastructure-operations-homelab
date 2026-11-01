# CH02 — Linux Network Configuration and Troubleshooting

## 1. Objective

Develop practical Linux networking and troubleshooting skills using a VMware-based Ubuntu Server homelab.

Focus areas:
- Bridged networking
- IPv4 addressing and subnetting
- Default gateway and routing
- Local network connectivity
- ARP and neighbor discovery
- SSH remote administration
- TCP connectivity testing
- Systematic fault isolation

## 2. Environment

### Virtualization
- Hypervisor: VMware Workstation Pro
- Guest OS: Ubuntu Server 24.04 LTS
- Hostname: dc-labsrv01
- Network Mode: Bridged

### Network Configuration
- Interface: ens33
- Server IP: 192.0.2.10
- Subnet: /24
- Default Gateway: 192.0.2.1
- DNS Server: 192.0.2.1
- Mac mini IP: 192.0.2.20

### Services
- SSH: TCP 22
- Nginx: TCP 80
- UFW: Enabled with SSH and HTTP access permitted

## 3. Architecture

Mac mini
192.0.2.20
     |
     | Local Network
     |
Router / Gateway
192.0.2.1
     |
     | Bridged VMware Network
     |
Ubuntu Server VM
192.0.2.10
     |
     +-- SSH :22
     +-- Nginx :80

Both observed endpoints use the 192.0.2.0/24 network.

Communication between the Mac mini and Ubuntu VM
was tested within the local network.

## 4. Implementation

### 4.1 IP Address Inspection

Command:

ip addr

Purpose:
Identify the active network interface and its
assigned IPv4 address.

Observed:
- Interface: ens33
- IPv4: 192.0.2.10/24

### 4.2 Routing Inspection

Command:

ip route

Purpose:
Inspect the routing table and identify the
default gateway.

Observed default gateway:
192.0.2.1

### 4.3 Neighbor Discovery

The Linux ARP/neighbor table was inspected
during network troubleshooting.

Purpose:
Understand how local IPv4 neighbors are
associated with link-layer addresses.

The exact historical neighbor-table output
is not preserved in this report.

### 4.4 ICMP Connectivity

Command:

ping

Purpose:
Test IP reachability and observe round-trip
latency and packet loss.

Observed:
- No packet loss during the recorded test
- Some transient latency spikes

The cause of the latency spikes was not
conclusively identified.

### 4.5 SSH Remote Administration

SSH access from Apple computers to the
Ubuntu Server VM was established.

Service:
TCP 22

Purpose:
Practice remote Linux administration.

### 4.6 TCP Connectivity

Command executed on macOS:

nc -vz -G 3 192.0.2.10 80

Observed:
TCP connection to port 80 succeeded.

Note:
The -G option was used with the macOS
implementation of netcat.

This option is not interchangeable with
every Linux netcat implementation.

## 5. Testing and Evidence

### Network Addressing
Ubuntu VM address:
192.0.2.10/24

### Routing
Default gateway:
192.0.2.1

### Remote Connectivity
Mac mini successfully connected to
the Ubuntu server over the local network.

### TCP Port Verification
A TCP connection to port 80 succeeded
from the Mac mini.

### HTTP Verification
Command:

curl -i http://192.0.2.10/

Observed:
HTTP 200 OK
Nginx default HTML returned.

This verified application-layer connectivity
in addition to basic network reachability.

## 6. Troubleshooting

### Observation: Transient Ping Latency

ICMP testing showed intermittent latency
variation without observed packet loss.

Potential areas for future investigation:
- Host resource contention
- VMware network scheduling
- Local network congestion
- Router or endpoint behavior

These are investigation possibilities,
not confirmed root causes.

### Diagnostic Approach

1. Identify the network interface.
2. Confirm the assigned IP address.
3. Inspect the routing table.
4. Verify gateway reachability.
5. Test remote endpoint connectivity.
6. Check the listening TCP port.
7. Test the application using HTTP.

## 7. Resolution and Final State

The Ubuntu VM maintained functional
bridged network connectivity.

Verified outcomes:
- Valid local IPv4 configuration
- Default route identified
- SSH remote access established
- TCP port 80 reachable from Mac mini
- HTTP 200 returned from Nginx

No specific corrective action was established
for the transient ICMP latency variation.

## 8. Lessons Learned

- Successful ping does not guarantee that
  an application is working.

- IP routing, TCP connectivity, and HTTP
  responses represent different diagnostic layers.

- A connection-refused error differs from
  a timeout or DNS resolution failure.

- Remote testing helps verify whether
  a service is reachable beyond localhost.

- Diagnostic observations should not be
  presented as confirmed root causes
  without sufficient evidence.

## 9. Interview Talking Points

"In my VMware homelab, I configured an
Ubuntu Server with bridged networking and
practiced troubleshooting connectivity
from a separate Mac computer.

I inspected IP addressing, routing,
neighbor information, and TCP connectivity.

I also tested SSH remote access and
verified that Nginx was reachable over
the network using HTTP requests.

One thing I learned is that successful
network connectivity doesn't necessarily
mean the application itself is healthy.

I try to troubleshoot layer by layer
instead of immediately assuming the
problem is with the network or server."

## 10. Verification Boundaries

Verified:
- Bridged VM network configuration
- Server IP and default gateway
- Remote SSH connectivity
- TCP port 80 connectivity
- Remote HTTP 200 response
- Ping latency variation

Not verified:
- Root cause of transient latency spikes
- VLAN segmentation
- Enterprise switch configuration
- Network redundancy
- High availability
- Production network administration

## 11. Related Documentation

- CH01-Linux-Server-Setup.md
- CH03-DNS-TCP-HTTP.md (planned)
- CH04-Nginx-Tomcat.md (planned)
- ../incidents/INC-0001.md
- ../incidents/INC-0002.md

## 12. Chapter Status

Status: Documented from prior homelab evidence

Environment: Personal homelab

Production experience claimed: No
