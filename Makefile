SHELL := /bin/bash

.PHONY: help up down logs ps lint scan trivy compose-validate

help:
	@echo "Targets:"
	@echo "  up               - Start stack (Docker Compose)"
	@echo "  down             - Stop stack and remove volumes"
	@echo "  logs             - Follow logs"
	@echo "  ps               - Show containers"
	@echo "  compose-validate - Validate compose config"
	@echo "  lint             - Run local lint checks (yamllint + shellcheck)"
	@echo "  trivy            - Run security scan (Trivy container)"
	@echo "  scan             - Alias for trivy"

up:
	docker compose up -d

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

compose-validate:
	docker compose config -q

lint:
	yamllint -d "{extends: relaxed, rules: {line-length: {max: 140}}}" .
	shellcheck scripts/*.sh

trivy:
	docker run --rm -v "$$PWD:/repo" aquasec/trivy:latest fs \
	  --security-checks vuln,config,secret \
	  --severity HIGH,CRITICAL \
	  --exit-code 1 \
	  /repo

scan: trivy
