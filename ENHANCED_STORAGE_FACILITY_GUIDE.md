# R3ÆL3R Enhanced Storage Facility - Reliability & Monitoring Guide

## Overview

The R3ÆL3R Self-Hosted Storage Facility has been enhanced with advanced reliability features including:

- **Real-time Monitoring**: Continuous health monitoring with alerts
- **Automated Failover**: Automatic database failover for high availability
- **Predictive Maintenance**: AI-driven maintenance recommendations

## Architecture

### Core Components

1. **StorageFacility**: Main storage facility with PostgreSQL schemas
2. **StorageMonitor**: Real-time monitoring and alerting system
3. **FailoverManager**: Automated failover management
4. **PredictiveMaintenance**: Predictive analytics for maintenance

### Monitoring Features

#### Real-time Metrics
- Connection health and response times
- Storage utilization per unit
- System resources (CPU, memory, disk)
- Error rates and failure patterns

#### Alert System
- Configurable alert thresholds
- Severity levels: LOW, MEDIUM, HIGH, CRITICAL
- Alert acknowledgment system
- Historical alert tracking

### Failover Features

#### Automated Failover
- Primary database health monitoring
- Automatic switch to backup databases
- Configurable failover policies
- Failover testing capabilities

#### Configuration
```json
{
  "name": "backup_db_1",
  "db_config": {
    "host": "backup1.example.com",
    "port": 5432,
    "database": "r3aler_backup",
    "user": "r3aler_user",
    "password": "secure_password"
  }
}
```

### Predictive Maintenance

#### Analytics
- Storage growth prediction
- Performance trend analysis
- Error pattern detection
- Maintenance recommendations

#### Maintenance Types
- **Storage**: Capacity planning and optimization
- **Performance**: Query optimization and indexing
- **Reliability**: Connection stability and error resolution

## API Endpoints

### Monitoring Endpoints

#### GET `/api/monitoring/metrics`
Returns current monitoring metrics summary.

**Response:**
```json
{
  "connection_response_time": {
    "current": 0.15,
    "average": 0.12,
    "min": 0.08,
    "max": 0.25,
    "count": 50
  },
  "total_entries": {
    "current": 15420,
    "average": 15380,
    "min": 15200,
    "max": 15500,
    "count": 50
  }
}
```

#### GET `/api/monitoring/alerts`
Returns active alerts.

#### POST `/api/monitoring/alerts/{alert_id}/acknowledge`
Acknowledges an alert.

#### GET `/api/monitoring/health`
Detailed health check with monitoring data.

### Failover Endpoints

#### GET `/api/failover/status`
Returns current failover status.

#### POST `/api/failover/enable`
Enables automated failover with configurations.

**Request:**
```json
{
  "configs": [
    {
      "name": "primary",
      "db_config": { ... }
    },
    {
      "name": "backup1",
      "db_config": { ... }
    }
  ]
}
```

#### POST `/api/failover/disable`
Disables automated failover.

#### POST `/api/failover/test`
Tests failover configuration.

### Predictive Maintenance Endpoints

#### GET `/api/predictive/status`
Returns current predictions and recommendations.

#### POST `/api/predictive/analyze`
Triggers immediate predictive analysis.

#### GET `/api/predictive/maintenance`
Returns maintenance recommendations.

### Enhanced Status

#### GET `/api/facility/status/enhanced`
Returns comprehensive facility status including monitoring, failover, and predictive data.

## Configuration

### Alert Thresholds

Default thresholds (configurable):

```python
alert_thresholds = {
    'response_time': 2.0,        # seconds
    'error_rate': 0.05,          # 5%
    'connection_failures': 3,    # per hour
    'storage_growth_rate': 100   # MB per day
}
```

### Monitoring Intervals

- Metrics collection: Every 30 seconds
- Health checks: Every 30 seconds
- Failover checks: Every 60 seconds
- Predictive analysis: Every hour

## Usage Examples

### Basic Monitoring

```bash
# Check health with monitoring data
curl http://localhost:3003/api/monitoring/health

# Get current metrics
curl http://localhost:3003/api/monitoring/metrics

# View active alerts
curl http://localhost:3003/api/monitoring/alerts
```

### Failover Setup

```bash
# Enable failover with backup databases
curl -X POST http://localhost:3003/api/failover/enable \
  -H "Content-Type: application/json" \
  -d '{
    "configs": [
      {
        "name": "backup1",
        "db_config": {
          "host": "backup.example.com",
          "port": 5432,
          "database": "r3aler_backup",
          "user": "r3aler",
          "password": "password"
        }
      }
    ]
  }'
```

### Predictive Maintenance

```bash
# Get maintenance recommendations
curl http://localhost:3003/api/predictive/maintenance

# Trigger analysis
curl -X POST http://localhost:3003/api/predictive/analyze
```

## System Requirements

### Dependencies

- PostgreSQL 12+
- Python 3.8+
- Flask
- psycopg2
- psutil (optional, for system monitoring)

### Installation

```bash
# Install optional system monitoring
pip install psutil
```

## Troubleshooting

### Common Issues

#### Monitoring Not Starting
- Check PostgreSQL connection
- Verify database credentials
- Check log file: `storage_monitor.log`

#### Failover Not Working
- Verify backup database configurations
- Check network connectivity to backups
- Review failover logs

#### High Alert Frequency
- Adjust alert thresholds in configuration
- Check system resources
- Review database performance

### Logs

Monitoring logs are written to `storage_monitor.log` with the following levels:
- INFO: Normal operations
- WARNING: Potential issues
- ERROR: Errors requiring attention
- CRITICAL: Critical failures

## Performance Considerations

### Resource Usage

- Monitoring: ~1-2% CPU, minimal memory
- Predictive analysis: Runs hourly, ~5-10% CPU during analysis
- Failover checks: Minimal overhead

### Scaling

- Metrics stored in memory (last 1000 values per metric)
- Alerts retained for 7 days
- Automatic cleanup of old data

## Security

### Database Security

- Use strong passwords
- Implement connection pooling
- Regular credential rotation

### API Security

- Implement authentication for production
- Use HTTPS in production
- Rate limiting for API endpoints

### Monitoring Security

- Secure log file permissions
- Encrypt sensitive configuration
- Regular security audits

## Future Enhancements

### Planned Features

- **Advanced Analytics**: Machine learning-based anomaly detection
- **Multi-region Failover**: Geographic redundancy
- **Automated Scaling**: Dynamic resource allocation
- **Integration APIs**: Third-party monitoring integration

### Extensibility

The system is designed to be extensible:
- Custom metrics collection
- Additional alert types
- Custom maintenance rules
- Integration with external monitoring systems

## Support

For issues or questions:
1. Check the logs in `storage_monitor.log`
2. Review API responses for error messages
3. Verify PostgreSQL connectivity
4. Check system resources

## Changelog

### Version 2.0 - Enhanced Reliability
- Added real-time monitoring system
- Implemented automated failover
- Added predictive maintenance
- Enhanced API with monitoring endpoints
- Improved error handling and logging