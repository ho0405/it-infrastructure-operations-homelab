# CH03 — DNS, TCP and HTTP Troubleshooting

## 1. Objective

Practice diagnosing network services across the DNS,
TCP and HTTP layers using an Ubuntu Server homelab.

Learning objectives:
- Understand DNS resolution and caching
- Inspect TCP listening sockets
- Test client-to-server TCP connectivity
- Interpret HTTP status codes
- Distinguish network failures from application failures
- Use evidence-based troubleshooting

## 2. Environment

- Hypervisor: VMware Workstation Pro
- OS: Ubuntu Server 24.04 LTS
- Hostname: dc-labsrv01
- Server IP: 192.0.2.10/24
- DNS Server: 192.0.2.1
- Default Gateway: 192.0.2.1
- Remote Client: Mac mini
- Client IP: 192.0.2.20
- Web Server: Nginx 1.24.0

## 3. Architecture

Mac mini (192.0.2.20)
        |
        | TCP / HTTP
        |
Ubuntu Server (192.0.2.10)
        |
        +-- SSH :22
        +-- Nginx :80
        |
        +-- systemd-resolved
                |
                +-- DNS: 192.0.2.1

DNS resolution and direct IP-based HTTP connectivity
were investigated as separate operations.

## 4. Implementation

### 4.1 DNS Resolution

Command:

resolvectl query example.com

Observed:
- Initial network resolution: 317.8 ms
- Subsequent cached resolution: 1.1 ms

Interpretation:

The second lookup was substantially faster and
was reported as a cached result.

This demonstrates the performance benefit of
DNS caching in the observed test.

The first lookup time alone does not establish
a DNS performance problem.

### 4.2 DNS Cache Statistics

Command:

sudo resolvectl statistics

Observed:
- Cache hits: 9
- Cache misses: 23
- No DNS timeouts reported

The statistics were cumulative at the time
of observation and do not represent a
controlled benchmark.

A DNS cache flush was also performed
during the exercise.

The post-flush cache state was not
separately verified.

### 4.3 TCP Listening Sockets

Command:

sudo ss -lntp

Observed:
- SSH listening on TCP 22
- Nginx listening on TCP 80

Purpose:

Identify whether expected services have
active listening TCP sockets.

A listening socket confirms that a process
is accepting connection attempts at the
transport layer, but does not prove that
the application is functioning correctly.

### 4.4 Remote TCP Connectivity

Command executed on macOS:

nc -vz -G 3 192.0.2.10 80

Observed:
TCP connection succeeded.

The -G argument applies to the macOS
netcat implementation used in this test.

### 4.5 HTTP Connectivity

Command:

curl -i http://192.0.2.10/

Observed:
- HTTP 200 OK
- Nginx default HTML page returned

This confirmed successful application-layer
communication with the web server.

### 4.6 Firewall

UFW was configured to deny unsolicited
incoming traffic by default.

Allowed inbound services:
- OpenSSH: TCP 22
- HTTP: TCP 80

The later Nginx reverse proxy listener on
port 8081 was tested locally.

Remote access to port 8081 was not verified.

## 5. Testing and Evidence

### DNS

Initial query:
317.8 ms

Cached query:
1.1 ms

Observed cache statistics:
9 hits, 23 misses.

### TCP

Port 22:
SSH service listening.

Port 80:
Nginx service listening.

Mac mini TCP connection to port 80:
Successful.

### HTTP

Request:
GET http://192.0.2.10/

Result:
HTTP 200 OK.

Expected Nginx HTML content returned.

## 6. Troubleshooting

### HTTP 404

Related Incident:
INC-0001

Cause:
Requested resource was absent from the
configured Nginx document root.

Resolution:
Created the missing test resource.

Verification:
HTTP 200 locally and remotely.

### TCP Connection Refused

Related Incident:
INC-0002

Cause:
Nginx was intentionally stopped.

Evidence:
- systemctl showed inactive service
- TCP port 80 was not listening
- curl reported connection refused

Resolution:
Restarted Nginx.

Verification:
HTTP 200 from local and remote clients.

### HTTP 502 Bad Gateway

Related Incident:
INC-0003

Cause:
Tomcat upstream service was intentionally stopped.

Evidence:
Nginx reported upstream connection refusal.

Resolution:
Restarted Tomcat.

Verification:
HTTP 200 through the Nginx reverse proxy.

The Tomcat incident is covered in greater
detail in CH04.

## 7. Resolution and Final State

Verified outcomes:
- DNS resolution succeeded
- Cached DNS lookup was observed
- SSH and HTTP listening ports identified
- Remote TCP connectivity succeeded
- Remote HTTP 200 response confirmed
- Controlled HTTP 404, connection refusal,
  and HTTP 502 scenarios were investigated
  and resolved in the homelab

## 8. Lessons Learned

- DNS, TCP and HTTP are different diagnostic layers.
- DNS caching can reduce repeated lookup latency.
- A successful TCP connection does not guarantee
  a successful HTTP response.
- HTTP 404, TCP connection refused and HTTP 502
  indicate different failure conditions.
- Application logs and service status should
  be examined before choosing a recovery action.
- A successful service restart should be followed
  by an actual application request.

## 9. Interview Talking Points

"In my personal infrastructure homelab,
I practiced troubleshooting connectivity
at the DNS, TCP and HTTP layers.

I used resolvectl to inspect DNS resolution
and caching, ss to inspect listening ports,
and curl and netcat to verify connectivity.

I also simulated different failure scenarios,
including HTTP 404, a stopped Nginx service,
and a Tomcat upstream failure returning 502.

These exercises helped me understand why
it's important to isolate the failing layer
before taking corrective action."

## 10. Verification Boundaries

Verified:
- DNS resolution and cached response
- DNS cache statistics at observation time
- TCP 22 and 80 listeners
- Remote TCP port 80 connectivity
- HTTP 200 response
- Controlled incident recovery

Not verified:
- Root cause of transient ICMP latency spikes
- DNS performance under sustained load
- Remote access to proxy port 8081
- Enterprise DNS administration
- Production incident management
- Automated monitoring or alerting

## 11. Related Documentation

- CH01-Linux-Server-Setup.md
- CH02-Network-Troubleshooting.md
- CH04-Nginx-Tomcat.md (planned)
- ../incidents/INC-0001.md
- ../incidents/INC-0002.md
- ../incidents/INC-0003.md

## 12. Chapter Status

Status: Documented from verified homelab observations
Environment: Personal homelab
Production experience claimed: No
