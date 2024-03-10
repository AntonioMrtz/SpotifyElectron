#!/bin/bash

# Build Docker images
docker-compose build

# Bring up the Docker containers
docker-compose up -d
