# CH10 — VLAN and Layer 2 Networking

## Executive Summary

Built a VLAN-aware virtual network using Linux network namespaces,
virtual Ethernet pairs, and a Linux Bridge on Ubuntu Server 24.04 LTS.

Configured VLAN 10 and VLAN 20 access ports, tested Layer 2
segmentation, and implemented an IEEE 802.1Q trunk carrying
both VLANs over one virtual Ethernet connection.

All testing was performed within a personal VMware-based homelab.

## Environment

- OS: Ubuntu Server 24.04 LTS
- Virtualization: VMware Workstation Pro
- Virtual switch: Linux Bridge (`br-vlan-lab`)
- VLAN filtering: Enabled
- VLAN protocol: IEEE 802.1Q
- Network tools: iproute2, bridge, ping

## Network Architecture

| Namespace | Interface | IP Address | VLAN |
|---|---|---|---|
| vlan10-host | veth10 | 192.168.10.10/24 | 10 |
| vlan10-host2 | veth10b | 192.168.10.20/24 | 10 |
| vlan20-host | veth20 | 192.168.20.10/24 | 20 |
| trunk-host | veth-trunk.10 | 192.168.10.30/24 | 10 |
| trunk-host | veth-trunk.20 | 192.168.20.30/24 | 20 |

All virtual hosts connected through the VLAN-aware Linux Bridge.

## Implementation

### 1. Network Namespace Configuration

Created independent network namespaces to simulate separate hosts.

### 2. Virtual Ethernet

Created veth pairs connecting the namespaces to the Linux Bridge.

### 3. VLAN-Aware Bridge

Created `br-vlan-lab` with VLAN filtering enabled.

### 4. Access Port Configuration

Assigned:

- `veth10-br` to VLAN 10, PVID, egress untagged
- `veth10b-br` to VLAN 10, PVID, egress untagged
- `veth20-br` to VLAN 20, PVID, egress untagged

Removed the default VLAN 1 membership from these access ports.

### 5. Layer 2 Segmentation

Configured an explicit host route for cross-VLAN testing.

Attempted communication from VLAN 10 to VLAN 20.

Results:

- 3 packets transmitted
- 0 packets received
- 100% packet loss
- ARP neighbor state: INCOMPLETE

The results were consistent with VLAN-based Layer 2 isolation.

### 6. Same-VLAN Connectivity

Tested connectivity between:

- 192.168.10.10
- 192.168.10.20

Results:

- 3 packets transmitted
- 3 packets received
- 0% packet loss
- ARP neighbor state: REACHABLE

### 7. IEEE 802.1Q Trunk

Created `trunk-host` with a single veth connection.

Configured the Bridge trunk port to carry tagged VLANs 10 and 20.

Created VLAN subinterfaces:

- `veth-trunk.10` — VLAN 10
- `veth-trunk.20` — VLAN 20

Verified both subinterfaces were UP and using IEEE 802.1Q.

### 8. Trunk Connectivity Validation

VLAN 10:

- Source: 192.168.10.30
- Destination: 192.168.10.10
- Result: 3/3 successful pings

VLAN 20:

- Source: 192.168.20.30
- Destination: 192.168.20.10
- Result: 3/3 successful pings

Both ARP neighbor entries were REACHABLE.

## Key Technical Concepts

- Layer 2 switching and MAC address resolution
- Network namespaces and virtual Ethernet pairs
- VLAN segmentation
- Access ports and PVID
- Tagged versus untagged Ethernet frames
- IEEE 802.1Q trunking
- IP subnetting and routing boundaries
- ARP troubleshooting

## Operational Lessons

A successful interface configuration does not necessarily prove
network connectivity. Connectivity must be tested.

Cross-VLAN packet loss should be interpreted alongside routing
information, VLAN membership, and ARP state.

Same-VLAN connectivity provides a useful positive control
when validating VLAN isolation.

An 802.1Q trunk can carry multiple VLANs over one connection.

A trunk host with interfaces in two VLANs can communicate
with both networks without enabling routing between other hosts.

## Limitations

- All devices were simulated within one Ubuntu VM.
- No physical managed switch was configured.
- No physical switch port or cabling was tested.
- Inter-VLAN routing was not implemented.
- VLAN configuration was created manually and is not persistent
  across a reboot unless separately automated.

## Interview Relevance

Demonstrates hands-on familiarity with VLAN membership,
802.1Q tagging, virtual switching, network segmentation,
ARP troubleshooting, and structured connectivity validation.

This was a personal homelab exercise, not production network administration.
