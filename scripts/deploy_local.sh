#!/bin/bash
# deploy_local.sh
# Wrapper to build and deploy the local Docker Compose environment cleanly.

echo "Tearing down existing containers..."
docker-compose down

echo "Building containers (no-cache)..."
docker-compose build --no-cache

echo "Starting local environment..."
docker-compose up -d

echo "Local environment deployed successfully!"
echo "UI is available at: http://localhost:3002"
echo "Grafana is available at: http://localhost:3000"
