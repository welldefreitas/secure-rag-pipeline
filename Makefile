SHELL := /usr/bin/env bash

.PHONY: help install run test lint format security up down logs smoke redteam

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install deps (dev)
	python -m pip install -U pip
	python -m pip install -e ".[dev]"

run: ## Run API locally (uvicorn)
	uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8000 --reload

test: ## Run unit tests
	pytest --maxfail=1

lint: ## Lint (ruff)
	ruff check .
	ruff format --check .

format: ## Auto-format (ruff)
	ruff format .

security: ## Basic security gates (pip-audit + bandit)
	pip-audit
	bandit -q -r app

up: ## Start local stack (docker compose)
	docker compose up --build -d

down: ## Stop local stack
	docker compose down -v

logs: ## Tail logs
	docker compose logs -f --tail=200

smoke: ## Quick smoke checks (health endpoints)
	bash scripts/smoke.sh

redteam: ## Run red-team prompt suite
	bash scripts/redteam.sh
