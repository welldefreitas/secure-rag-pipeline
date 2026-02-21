# Changelog

## [v1.0.0] - Initial Release
- Implemented secure `docker-compose.yml` with `internal: true` network isolation.
- Configured Nginx Reverse Proxy with Rate Limiting and strict HTTPS enforcement.
- Automated local SSL certificate generation via `Makefile`.
- Established CI/CD pipeline for ShellCheck and Trivy security scanning.
- Documented comprehensive Threat Model in `security.md`.
