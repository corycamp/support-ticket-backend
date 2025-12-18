# Makefile for common development tasks

.PHONY: build up down run test docker-test shell

build:
	@echo "Building Docker image..."
	docker build -t support-ticket-backend:test .

up:
	@echo "Starting services with docker-compose..."
	docker-compose up --build

down:
	@echo "Stopping services..."
	docker-compose down

run:
	@echo "Running container..."
	docker run --rm -p 8000:8000 support-ticket-backend:test

test:
	@echo "Running test suite..."
	python -m pytest tests -q

docker-test:
	@echo "Running tests inside image..."
	docker run --rm support-ticket-backend:test pytest -q

shell:
	@echo "Open shell inside container..."
	docker run --rm -it support-ticket-backend:test /bin/sh
