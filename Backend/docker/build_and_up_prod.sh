#!/bin/bash

# Build Docker images
docker-compose -f docker-compose-prod.yml build

# Bring up the Docker containers
docker-compose -f docker-compose-prod.yml up -d
