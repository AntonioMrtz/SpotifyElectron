#!/bin/bash

# Build Docker images
docker compose -f docker-compose-dev.yml build

# Bring up the Docker containers
docker compose -f docker-compose-dev.yml up -d
