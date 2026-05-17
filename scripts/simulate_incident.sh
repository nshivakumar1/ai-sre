#!/bin/bash
# simulate_incident.sh
# Sends a mock Prometheus Alertmanager webhook payload to the alert-router service.

ROUTER_URL="http://localhost:8001/webhook"

echo "Simulating High CPU Usage Incident..."

curl -X POST $ROUTER_URL \
  -H "Content-Type: application/json" \
  -d '{
    "receiver": "webhook",
    "status": "firing",
    "alerts": [
      {
        "status": "firing",
        "labels": {
          "alertname": "HighCPUUsage",
          "severity": "critical",
          "instance": "web-server-01"
        },
        "annotations": {
          "description": "CPU usage is above 90% for 5 minutes."
        }
      }
    ]
  }'

echo -e "\nPayload sent to $ROUTER_URL."
