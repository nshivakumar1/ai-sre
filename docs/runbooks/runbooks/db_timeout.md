# Database Connection Timeout Runbook

## Description
This alert indicates that the application services are unable to establish a connection to the primary database within the configured timeout period (usually 5-10 seconds). This can result in widespread HTTP 500 errors across the platform.

## Troubleshooting Steps
1. **Check DB Health**: Verify if the database server itself is up. Use Prometheus to check database-specific metrics (e.g., PostgreSQL or MySQL exporter).
2. **Check Connection Pool**: Inspect the application's connection pool metrics in Grafana. If the active connections equal the max pool size, connection starvation is occurring.
3. **Analyze Slow Queries**: A sudden spike in slow, unoptimized queries can lock rows or exhaust the connection pool. Check the database's slow query log.
4. **Network Partition**: Check if there are broader network connectivity issues between the application subnet and the database subnet.

## Remediation Actions
- **Immediate Mitigation (Restart DB Connection Pools)**: Restart the application instances to aggressively clear and reset connection pools, dropping stuck connections.
- **Kill Long-Running Queries**: If specific queries have been running for minutes and blocking the pool, manually kill those database sessions.
- **Scale Database Compute**: If the database is hitting 100% CPU/Memory limit causing timeouts, vertically scale the database instance size.
- **Increase Pool Size**: If resources are available but the app is legitimately requiring more connections, temporarily hot-patch the application config to increase `MAX_CONNECTIONS`.
