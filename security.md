# Security Model (Threats & Mitigations)

## Goal
Run LLM inference on-prem with **controlled ingress**, **restricted egress**, and **minimal attack surface**.

## Assumptions
- Ollama is **not** exposed to host ports.
- Nginx is the **only ingress** entrypoint.
- Model weights are stored locally in a Docker volume.

---

## Threats & Mitigations

### 1) Unauthorized access to the LLM endpoint
**Threat:** External users hit Ollama directly or abuse the proxy.  
**Mitigations:**
- No host ports on Ollama (internal network only).
- Nginx rate limit + security headers.
- (Optional) Add Basic Auth / OAuth2 proxy / IP allowlist.

### 2) Prompt injection / data leakage via RAG (future)
**Threat:** Retrieved docs or user input cause exfiltration of sensitive data.  
**Mitigations:**
- Tenant isolation and auth at proxy/app layer.
- Strict data classification; deny retrieval of secrets.
- Logging + redaction policies (PII, credentials).
- Allowlist tools/actions (deny-by-default).

### 3) Container escape / privilege abuse
**Threat:** A compromised container impacts host.  
**Mitigations:**
- Run with least privilege (drop capabilities where possible).
- Keep images updated; scan with Trivy in CI.
- Avoid mounting sensitive host paths.

### 4) Denial of Service (resource exhaustion)
**Threat:** Large payloads or request floods.  
**Mitigations:**
- Rate limiting + request size limits.
- Timeouts tuned to prevent stuck connections.

### 5) Supply chain risk (images, scripts)
**Threat:** Malicious upstream image or dependency.  
**Mitigations:**
- Pin versions when possible.
- CI: config/vuln scanning + lint gates.
- Optional: signed images / SBOM.

---

## Recommended Hardening (Next)
- TLS termination with real certs (Let’s Encrypt or internal PKI).
- Add auth layer (OIDC) in front of Nginx.
- Egress controls (firewall rules / network policies).
- Centralized logging + audit trail.
