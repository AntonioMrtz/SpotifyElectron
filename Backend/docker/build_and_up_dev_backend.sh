#!/bin/bash

# Build Docker images
docker compose -f docker-compose-dev-backend.yml build

# Bring up the Docker containers
docker compose -f docker-compose-dev-backend.yml up -d
