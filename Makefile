# Alzheimer's Disease Analysis Database Makefile

.PHONY: help install test clean build-sandbox start stop logs sample-data

help:  ## Show this help message
	@echo "Alzheimer's Disease Analysis Database - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install Python dependencies
	pip install -r requirements.txt

test:  ## Run tests
	pytest tests/ -v

clean:  ## Clean up containers and artifacts
	docker-compose down -v
	docker system prune -f
	rm -rf artifacts/*

build-sandbox:  ## Build sandbox Docker image
	./scripts/build_sandbox.sh

start:  ## Start development environment
	./scripts/start_dev.sh

stop:  ## Stop all services
	docker-compose down

logs:  ## View service logs
	docker-compose logs -f

sample-data:  ## Create sample dataset
	python scripts/create_sample_data.py

dev:  ## Start development mode
	python -m app.main

build:  ## Build all Docker images
	docker-compose build

status:  ## Check service status
	docker-compose ps

restart:  ## Restart all services
	docker-compose restart

shell:  ## Open shell in web container
	docker-compose exec web bash

worker-shell:  ## Open shell in worker container
	docker-compose exec worker bash

redis-cli:  ## Open Redis CLI
	docker-compose exec redis redis-cli

# Development shortcuts
setup: install build-sandbox sample-data  ## Complete setup for development
full-start: setup start  ## Complete setup and start

# Production helpers
prod-build:  ## Build production images
	docker build -t dementia-db:prod .
	cd docker && docker build -f sandbox.Dockerfile -t dementia-sandbox:prod .

prod-deploy:  ## Deploy to production
	docker-compose -f docker-compose.prod.yml up -d

# Utility commands
lint:  ## Run code linting
	flake8 app/ tests/
	black --check app/ tests/

format:  ## Format code
	black app/ tests/
	isort app/ tests/

docs:  ## Generate documentation
	pdoc --html app/ --output-dir docs/

# Default target
all: help
