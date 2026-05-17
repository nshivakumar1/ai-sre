# HighCPUUsage Alert Runbook

## Description
This alert fires when the CPU usage of a specific server or container exceeds 90% for more than 5 minutes. High CPU usage can lead to application latency, dropped connections, and overall system instability.

## Troubleshooting Steps
1. **Identify the Process**: SSH into the affected node or use top/htop/kubectl top to identify which process is consuming the most CPU.
2. **Check Application Logs**: Look at the logs for the service running on that node (e.g., via Kibana or Loki). Look for infinite loops, large data processing tasks, or heavy garbage collection.
3. **Verify Traffic Spikes**: Check Grafana dashboards for a sudden influx of requests. If this is a legitimate traffic spike, the system should ideally auto-scale.
4. **Check for Deadlocks**: If the application is a JVM or Node.js app, take a thread dump to check for thread contention or deadlocks.

## Remediation Actions
- **Immediate Mitigation (Scale Up)**: Manually trigger a scale-out event for the affected service deployment to distribute the load across more replicas.
- **Restart Service**: If a single process is stuck in a loop and not serving traffic, safely restart the container or service (`kubectl delete pod <pod-name>`).
- **Rollback Deployment**: If this occurred immediately after a deployment, consider rolling back to the previous stable version.
- **Rate Limiting**: If caused by an abusive client, apply temporary rate limiting at the API Gateway or WAF level.
