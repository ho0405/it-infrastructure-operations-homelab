# CH04 — Nginx and Apache Tomcat Reverse Proxy

## 1. Objective

Deploy and troubleshoot a multi-service web environment
using Nginx and Apache Tomcat on Ubuntu Server.

Learning objectives:
- Manage Linux web services using systemd
- Understand reverse proxy architecture
- Configure Nginx proxy_pass
- Verify HTTP connectivity
- Investigate HTTP 502 Bad Gateway errors
- Restore application availability
- Document controlled incidents

## 2. Environment

- Hypervisor: VMware Workstation Pro
- OS: Ubuntu Server 24.04 LTS
- Hostname: dc-labsrv01
- Server IP: 192.0.2.10
- Nginx: 1.24.0
- Apache Tomcat: 10.1.55
- Java: OpenJDK 21.0.12.1
- Firewall: UFW

Service Ports:
- SSH: 22
- Nginx Static Website: 80
- Apache Tomcat: 8080
- Nginx Reverse Proxy: 8081

## 3. Architecture

Remote Mac mini
      |
      | HTTP Port 80
      v
Nginx Static Website
      |
      +-- /var/www/html

Local HTTP Client
      |
      | HTTP Port 8081
      v
Nginx Reverse Proxy
      |
      | proxy_pass
      v
Apache Tomcat
127.0.0.1:8080
      |
      +-- Tomcat ROOT Application

The reverse proxy uses a separate Nginx
listener on port 8081 to preserve the
existing website on port 80.

Port 8081 was tested locally.
Remote access to port 8081 was not verified.

## 4. Implementation

### 4.1 Nginx Installation and Operation

Nginx was configured to serve its default
static website on TCP port 80.

Document Root:
/var/www/html

Default Location Rule:
try_files $uri $uri/ =404;

The configuration returns HTTP 404 when
a requested resource cannot be found.

### 4.2 Apache Tomcat

Apache Tomcat 10 was installed through
the Ubuntu package manager.

Service:
tomcat10.service

HTTP Connector:
TCP 8080

Default Application:
/var/lib/tomcat10/webapps/ROOT

Direct Verification Command:

curl -i --max-time 5 http://127.0.0.1:8080/

Observed:
- HTTP 200
- Apache Tomcat default HTML
- "It works !" message

### 4.3 Reverse Proxy Configuration

Configuration File:
/etc/nginx/conf.d/tomcat-proxy.conf

Configured Nginx Server:

server {
    listen 8081;
    server_name _;

    location /tomcat/ {
        proxy_pass http://127.0.0.1:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

The trailing slash in proxy_pass causes
the matching /tomcat/ location prefix
to be replaced with / when forwarding
requests to the upstream application.

Example:

Client Request:
GET /tomcat/

Upstream Request:
GET /

### 4.4 Configuration Validation

Command:

sudo nginx -t

Observed:
- Syntax OK
- Configuration test successful

### 4.5 Configuration Reload

Command:

sudo systemctl reload nginx

The reload command returned without
an error message.

Subsequent HTTP testing confirmed that
the reverse proxy configuration was active.

## 5. Testing and Evidence

### Test A — Direct Tomcat Access

Request:
http://127.0.0.1:8080/

Result:
HTTP 200

Content:
Apache Tomcat default HTML

### Test B — Reverse Proxy Access

Request:
http://127.0.0.1:8081/tomcat/

Result:
HTTP 200

Response Server:
nginx/1.24.0 (Ubuntu)

Content:
Apache Tomcat default HTML

This confirmed the Nginx-to-Tomcat
reverse proxy path.

### Test C — Existing Website Regression

Request:
http://127.0.0.1/

Result:
HTTP 200

Content:
Welcome to nginx!

This confirmed that the original
port 80 website remained available
after the reverse proxy was configured.

## 6. Troubleshooting

### INC-0001 — HTTP 404

Symptom:
HTTP 404 Not Found

Cause:
Requested file was missing from
the Nginx document root.

Resolution:
Created the missing test resource.

Verification:
HTTP 200 locally and from Mac mini.

### INC-0002 — Nginx Service Outage

Symptom:
TCP connection refused on port 80.

Cause:
Nginx was intentionally stopped.

Evidence:
- systemctl inactive (dead)
- No listening socket on port 80
- curl connection refused

Resolution:
sudo systemctl start nginx

Verification:
HTTP 200 locally and remotely.

### INC-0003 — Tomcat Upstream Outage

Incident Type:
Controlled application outage simulation

Symptom:
HTTP 502 Bad Gateway

Incident Time:
2026-11-01 20:36:50 UTC

Request:
GET /tomcat/

Observed Response:
HTTP/1.1 502 Bad Gateway

Nginx Error Log:
connect() failed (111: Connection refused)
while connecting to upstream

Upstream:
http://127.0.0.1:8080/

Root Cause:
Apache Tomcat was intentionally stopped.

Nginx remained available but could not
connect to its upstream application.

Resolution Command:

sudo systemctl start tomcat10

Recovery Verification:

curl -i --max-time 5 http://127.0.0.1:8081/tomcat/

Observed Recovery:
- HTTP 200
- Server: nginx/1.24.0 (Ubuntu)
- Content-Length: 1905 bytes
- Apache Tomcat HTML returned
- "It works !" message displayed

Recovery Response Time:
2026-11-01 20:44:58 UTC

The interval between the recorded 502
response and the recorded successful
HTTP response was 8 minutes 8 seconds.

This is an observation interval,
not a measured production outage duration.

## 7. Resolution and Final State

Verified:
- Nginx served HTTP requests on port 80
- Tomcat served HTTP requests on port 8080
- Nginx proxied requests on port 8081
- Existing Nginx website remained functional
- Controlled Tomcat outage produced HTTP 502
- Error logs identified upstream connection refusal
- Restarting Tomcat restored HTTP 200

Final Incident Status:
INC-0003 Resolved

## 8. Lessons Learned

- Nginx and Tomcat are separate services
  with different responsibilities.

- HTTP 502 may indicate an unavailable
  upstream application.

- A functioning reverse proxy does not
  guarantee backend application health.

- Error logs help distinguish upstream
  failures from proxy configuration issues.

- Service recovery must be verified
  through an actual application request.

- Changes should be regression-tested
  against existing services.

- Incident reports should distinguish
  controlled simulations from production
  failures.

## 9. Interview Talking Points

"In my personal homelab, I deployed
Nginx and Apache Tomcat on Ubuntu Server.

I configured Nginx as a reverse proxy
so requests to port 8081 were forwarded
to Tomcat on port 8080.

I also made sure the existing Nginx
website on port 80 continued working.

To practice troubleshooting, I intentionally
stopped Tomcat and reproduced a 502
Bad Gateway error.

I checked the Nginx error logs and found
that the upstream connection was refused.

After identifying the stopped Tomcat
service as the cause, I restarted it
and verified that the application
returned HTTP 200 through Nginx.

That exercise taught me to isolate
the failing component and verify
recovery end to end."

## 10. Verification Boundaries

Verified:
- Local Nginx and Tomcat operation
- Reverse proxy configuration
- HTTP 200 through the proxy
- HTTP 502 during controlled outage
- Nginx upstream connection error
- Successful Tomcat recovery
- Existing port 80 website regression test

Not verified:
- External access to proxy port 8081
- TLS/HTTPS configuration
- Production application deployment
- Load balancing across multiple backends
- Automatic failover
- Production monitoring and alerting
- Enterprise Tomcat administration

## 11. Related Documentation

- CH01-Linux-Server-Setup.md
- CH02-Network-Troubleshooting.md
- CH03-DNS-TCP-HTTP.md
- ../incidents/INC-0001.md
- ../incidents/INC-0002.md
- ../incidents/INC-0003.md

## 12. Chapter Status

Status: Completed and documented
Environment: Personal VMware homelab
Production experience claimed: No
