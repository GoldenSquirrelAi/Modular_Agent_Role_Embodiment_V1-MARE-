# MARE System Deployment Guide

**Version:** 1.0.0  
**Created by:** DevOps Engineer REP  
**Date:** September 1, 2025

---

## Overview

This guide provides comprehensive instructions for deploying, operating, and monitoring the MARE (Modular Agent Role Embodiment) Protocol system in production environments.

## Quick Start

```bash
# Clone or navigate to MARE directory
cd MARE_modular_agent_role_embodiment

# Deploy complete system
./deploy.sh

# Access services
# MARE Demo: docker-compose exec mare-system python3 mare_live_demo.py
# Monitoring: http://localhost:9090 (Prometheus)
# Dashboards: http://localhost:3000 (Grafana, admin/mare2025)
```

## Prerequisites

### System Requirements

- **OS:** Linux, macOS, or Windows with WSL2
- **Memory:** Minimum 2GB, Recommended 4GB+
- **Storage:** Minimum 1GB free space
- **Network:** Internet access for container downloads

### Required Software

- **Docker:** Version 20.10+
- **Docker Compose:** Version 2.0+
- **Python:** 3.9+ (for local development)
- **Git:** For repository management

### Installation Verification

```bash
# Verify Docker
docker --version
docker ps

# Verify Docker Compose
docker-compose --version

# Verify permissions
docker run hello-world
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MARE PRODUCTION STACK                    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │    MARE     │  │ PROMETHEUS  │  │      GRAFANA        │  │
│  │   SYSTEM    │  │ MONITORING  │  │   DASHBOARDS        │  │
│  │   :8080     │  │    :9090    │  │      :3000          │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                │                     │             │
│         ▼                ▼                     ▼             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              DOCKER BRIDGE NETWORK              │        │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Persistent Volumes:                                         │
│  • mare-data     (SQLite database)                          │
│  • mare-logs     (Application logs)                         │
│  • prometheus    (Metrics storage)                          │
│  • grafana       (Dashboard configs)                        │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Options

### Option 1: Full Automated Deployment (Recommended)

```bash
# Full deployment with monitoring
./deploy.sh deploy

# Verify deployment
./deploy.sh status
./deploy.sh validate
```

### Option 2: Step-by-Step Deployment

```bash
# 1. Build Docker image
./deploy.sh build

# 2. Start services
./deploy.sh start

# 3. Run validation
./deploy.sh validate
```

### Option 3: Development Deployment

```bash
# Local development without containerization
python3 -m pip install -r requirements.txt
python3 demo_mare.py
```

## Service Configuration

### MARE System Configuration

**Environment Variables:**
```bash
MARE_ENV=production              # Deployment environment
MARE_LOG_LEVEL=INFO             # Logging level
MARE_DB_PATH=/app/data/mare_reps.db  # Database location
PYTHONPATH=/app/src             # Python module path
```

**Resource Limits:**
- CPU: 2.0 cores (limit), 0.5 cores (reserved)
- Memory: 1GB (limit), 256MB (reserved)
- Storage: Persistent volumes for data and logs

### Monitoring Configuration

**Prometheus Targets:**
- MARE System: `mare-system:8080/health`
- Prometheus Self: `localhost:9090`
- Docker Metrics: `host.docker.internal:9323`

**Data Retention:**
- Metrics: 30 days
- Logs: 100MB per file, 5 files max rotation

## Operations Guide

### Starting Services

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d mare-system

# Scale services
docker-compose up -d --scale mare-system=2
```

### Stopping Services

```bash
# Stop all services
docker-compose down

# Stop with volume cleanup
docker-compose down --volumes

# Emergency stop
docker-compose kill
```

### Viewing Logs

```bash
# All service logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f mare-system

# Last N lines
docker-compose logs --tail=100 mare-system
```

### Health Monitoring

```bash
# System health check
docker-compose exec mare-system python3 -c "
import sys; sys.path.insert(0, '/app/src')
from mare import MARESystem
s = MARESystem()
print(s.get_system_health())
s.shutdown()
"

# Container health
docker-compose ps

# Resource usage
docker stats
```

## Demo and Testing

### Interactive Demo

```bash
# Start interactive demo
docker-compose exec mare-system python3 mare_live_demo.py

# Run predefined scenarios
# 1. E-commerce Architecture
# 2. REST API Implementation  
# 3. Performance Testing Suite
# 4. Kubernetes Deployment
# 5. API Protocol Design
```

### Validation Suite

```bash
# Full validation suite
docker-compose exec mare-system python3 mare_validation_suite.py

# Benchmark comparison
docker-compose exec mare-system python3 mare_benchmark_comparison.py

# Quick system test
docker-compose exec mare-system python3 demo_mare.py
```

### Performance Testing

```bash
# Load testing (if jmeter available)
# Create JMeter test plan for API endpoints

# Memory usage monitoring
docker stats mare-system

# Database performance
docker-compose exec mare-system sqlite3 /app/data/mare_reps.db ".schema"
```

## Monitoring and Alerting

### Prometheus Metrics

Access: `http://localhost:9090`

**Key Metrics:**
- `mare_tasks_total` - Total tasks processed
- `mare_task_duration_seconds` - Task execution times
- `mare_rep_usage_total` - REP usage distribution
- `mare_confidence_score` - Confidence score distribution
- `mare_system_health` - Overall system health

**Sample Queries:**
```promql
# Average task execution time
rate(mare_task_duration_seconds_sum[5m]) / rate(mare_task_duration_seconds_count[5m])

# REP usage rate
rate(mare_rep_usage_total[5m])

# System error rate
rate(mare_errors_total[5m])
```

### Grafana Dashboards

Access: `http://localhost:3000` (admin/mare2025)

**Default Dashboards:**
- MARE System Overview
- Task Execution Metrics
- REP Performance Analysis
- System Health Monitoring

### Log Analysis

```bash
# Error pattern analysis
docker-compose logs mare-system | grep ERROR

# Performance pattern analysis  
docker-compose logs mare-system | grep "execution_time"

# REP usage analysis
docker-compose logs mare-system | grep "REP.*routed"
```

## Backup and Recovery

### Database Backup

```bash
# Create backup
docker-compose exec mare-system sqlite3 /app/data/mare_reps.db ".backup '/app/data/backup_$(date +%Y%m%d).db'"

# Copy backup to host
docker cp mare-system:/app/data/backup_$(date +%Y%m%d).db ./backups/

# Automated backup script
./scripts/backup.sh
```

### Volume Backup

```bash
# Backup all volumes
docker run --rm -v mare-data:/data -v $(pwd)/backups:/backups alpine tar czf /backups/mare-data-backup.tar.gz -C /data .

# Restore volumes
docker run --rm -v mare-data:/data -v $(pwd)/backups:/backups alpine tar xzf /backups/mare-data-backup.tar.gz -C /data
```

### Configuration Backup

```bash
# Backup configuration
cp docker-compose.yml ./backups/
cp -r monitoring ./backups/
cp -r config ./backups/
```

## Scaling and Performance

### Horizontal Scaling

```bash
# Scale MARE system instances
docker-compose up -d --scale mare-system=3

# Load balancer configuration (nginx example)
# upstream mare_backend {
#     server mare-system-1:8080;
#     server mare-system-2:8080; 
#     server mare-system-3:8080;
# }
```

### Performance Tuning

**Database Optimization:**
```sql
-- SQLite optimizations
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA cache_size=10000;
```

**Container Resources:**
```yaml
# docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '4.0'      # Increase for high load
      memory: 2G       # Increase for large REPs
```

**Python Optimizations:**
```bash
# Environment variables
PYTHONOPTIMIZE=2
PYTHONDONTWRITEBYTECODE=1
```

## Security Considerations

### Container Security

```bash
# Run as non-root user (already configured)
USER mareuser

# Read-only root filesystem
read_only: true

# Security scanning
docker scout quickview mare-protocol:latest
```

### Network Security

```bash
# Internal network isolation (already configured)
networks:
  mare-network:
    driver: bridge
    internal: true  # Add for complete isolation
```

### Data Security

```bash
# Encrypt sensitive data
# Add encryption layer for REP profiles
# Implement access controls for admin operations
```

## Troubleshooting

### Common Issues

**Issue: Container won't start**
```bash
# Check logs
docker-compose logs mare-system

# Check resource usage
docker system df
docker system prune

# Restart services
docker-compose restart
```

**Issue: Database corruption**
```bash
# Check database integrity
docker-compose exec mare-system sqlite3 /app/data/mare_reps.db "PRAGMA integrity_check;"

# Restore from backup
docker cp ./backups/backup_YYYYMMDD.db mare-system:/app/data/mare_reps.db
```

**Issue: High memory usage**
```bash
# Monitor memory
docker stats mare-system

# Adjust limits
# Edit docker-compose.yml memory limits

# Clear cache
docker-compose exec mare-system python3 -c "
import sys; sys.path.insert(0, '/app/src')
from mare import MARESystem
s = MARESystem()
s.cleanup_expired_contexts()
s.shutdown()
"
```

### Debug Mode

```bash
# Enable debug logging
docker-compose exec mare-system python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# ... rest of debug commands
"

# Interactive debug session
docker-compose exec mare-system python3
>>> import sys
>>> sys.path.insert(0, '/app/src')
>>> from mare import MARESystem
>>> system = MARESystem()
>>> # Interactive debugging
```

### Performance Debugging

```bash
# Profile task execution
docker-compose exec mare-system python3 -c "
import cProfile
import sys
sys.path.insert(0, '/app/src')
from mare import MARESystem

def profile_task():
    system = MARESystem()
    result = system.execute_task('Profile test', 'Performance data')
    system.shutdown()
    return result

cProfile.run('profile_task()')
"
```

## Maintenance

### Regular Maintenance Tasks

**Daily:**
- Check system health: `./deploy.sh status`
- Monitor disk usage: `docker system df`
- Review error logs: `docker-compose logs --since 24h mare-system | grep ERROR`

**Weekly:**
- Database cleanup: Clear old task history
- Log rotation: `docker-compose logs --tail=0 > /dev/null`
- Performance review: Analyze Grafana dashboards

**Monthly:**
- Update container images: `docker-compose pull && ./deploy.sh deploy`
- Security updates: Update base images
- Backup verification: Test restore procedures

### Updates and Upgrades

```bash
# Update to new version
git pull origin main
./deploy.sh stop
./deploy.sh build
./deploy.sh deploy

# Rollback if needed
docker tag mare-protocol:previous mare-protocol:latest
./deploy.sh start
```

## Support and Documentation

### Log Collection for Support

```bash
# Collect comprehensive logs
./scripts/collect-logs.sh

# System information
docker version > support-info.txt
docker-compose version >> support-info.txt  
docker system info >> support-info.txt
```

### Documentation Links

- MARE RFC Specification: `mare_protocol_rfc.md`
- System Architecture: `mare_system_architecture.md`
- API Reference: `src/mare/__init__.py`
- Troubleshooting: This guide, section above

---

## Appendix

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `MARE_ENV` | production | Deployment environment |
| `MARE_LOG_LEVEL` | INFO | Logging verbosity |
| `MARE_DB_PATH` | /app/data/mare_reps.db | Database file location |
| `MARE_MAX_CONCURRENT` | 5 | Max concurrent tasks |
| `MARE_CONTEXT_TIMEOUT` | 3600 | Context timeout seconds |

### Port Reference

| Service | Port | Description |
|---------|------|-------------|
| MARE System | 8080 | Main application |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Monitoring dashboards |

### File Locations

| Path | Description |
|------|-------------|
| `/app/data/` | Persistent data storage |
| `/app/logs/` | Application logs |
| `/app/src/` | MARE source code |
| `/app/config/` | Configuration files |

---

**Deployment Guide Complete**  
**DevOps Engineer REP v1.0.0**