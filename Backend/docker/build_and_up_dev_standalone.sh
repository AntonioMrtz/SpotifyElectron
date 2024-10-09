#!/bin/bash

# Build Docker images
docker compose -f docker-compose-dev-standalone.yml build

# Bring up the Docker containers
docker compose -f docker-compose-dev-standalone.yml up -d
