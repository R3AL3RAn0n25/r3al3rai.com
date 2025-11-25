# R3ÆLƎR AI Management System

A comprehensive web-based management interface for monitoring, controlling, and maintaining the R3ÆLƎR AI production system.

## Features

### 🖥️ System Monitoring
- Real-time service status monitoring (7 core services)
- System resource usage (CPU, Memory, Disk, Network)
- Key performance metrics and uptime tracking
- Live status indicators with automatic refresh

### 📊 Logs & Reports
- Real-time log viewing with filtering
- Multiple report types (Daily, Weekly, Monthly, Performance, Errors, Security)
- Log export functionality
- Error tracking and analysis

### 🤖 AI Details
- AI system component status
- Learning metrics and accuracy tracking
- Training progress monitoring
- AI capability testing interface

### ⚙️ System Control
- Start/Stop/Restart all services
- Individual service control
- System-wide operations
- Service health verification

### 📁 Dataset Management
- Drag-and-drop file upload
- Existing dataset listing and management
- Dataset analysis capabilities
- Secure file handling with size limits

### ⬆️ Upgrade System
- System upgrade file uploads
- Upgrade history tracking
- Automatic upgrade type detection
- Version management

## Installation

### Prerequisites
- Python 3.8+
- Nginx web server
- SSL certificates configured
- Administrative access for nginx configuration

### Deployment

1. **Run the deployment script as administrator:**
   ```powershell
   .\deploy-management.ps1
   ```

   This will:
   - Copy files to nginx web directory
   - Setup Python virtual environment
   - Install required dependencies
   - Reload nginx configuration

2. **Start the management system:**
   ```powershell
   cd "C:\var\www\r3al3rai.com\manage"
   .\start-management.ps1
   ```

## Access

Once deployed and running, access the management system at:
- **Management Interface:** `https://www.r3al3rai.com/manage/`
- **Management API:** `https://www.r3al3rai.com/api/`

## API Endpoints

### System Monitoring
- `GET /api/health` - Basic health check
- `GET /api/system/status` - Overall system status
- `GET /api/system/info` - System resource information
- `GET /api/metrics` - System metrics
- `GET /api/{service}/health` - Individual service health

### Logs & Reports
- `GET /api/logs` - System logs
- `GET /api/reports/{type}` - Generate reports

### AI System
- `GET /api/ai/details` - AI system details
- `GET /api/ai/test/{capability}` - Test AI capabilities

### System Control
- `POST /api/system/{action}` - System-wide actions (start/stop/restart/status)
- `POST /api/services/{service}/{action}` - Individual service control

### Dataset Management
- `POST /api/datasets/upload` - Upload dataset files
- `GET /api/datasets` - List datasets
- `DELETE /api/datasets/{id}` - Delete dataset

### Upgrades
- `POST /api/upgrades/upload` - Upload upgrade files
- `GET /api/upgrades/history` - Upgrade history

## Security

- All communications use HTTPS
- CORS configured for secure API access
- File uploads are validated and sanitized
- Administrative functions require proper authentication (future enhancement)

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │────│     Nginx       │────│ Management API  │
│                 │    │  (Port 443)    │    │  (Port 5000)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   R3ÆLƎR AI     │
                       │   Services      │
                       │ (Ports 3000-)   │
                       └─────────────────┘
```

## File Structure

```
manage/
├── index.html              # Main management interface
├── management_api.py       # Flask API server
├── requirements.txt        # Python dependencies
├── start-management.ps1    # Startup script
├── deploy-management.ps1   # Deployment script
├── uploads/                # Uploaded files
│   ├── datasets/          # Dataset files
│   └── upgrades/          # Upgrade files
└── logs/                  # System logs
    └── management.log     # API logs
```

## Troubleshooting

### Management Interface Not Loading
1. Check if management API is running on port 5000
2. Verify nginx configuration is reloaded
3. Check browser console for JavaScript errors

### API Calls Failing
1. Ensure management API is accessible
2. Check CORS headers in nginx configuration
3. Verify SSL certificates are valid

### File Upload Issues
1. Check file size limits (500MB default)
2. Verify upload directories have proper permissions
3. Check browser network tab for upload errors

### Service Control Not Working
1. Ensure proper permissions for process management
2. Check if services are configured correctly
3. Review system logs for error details

## Future Enhancements

- User authentication and authorization
- Role-based access control
- Advanced monitoring dashboards
- Automated backup and recovery
- Integration with external monitoring tools
- API rate limiting and security hardening

## Support

For issues or questions about the R3ÆLƎR AI Management System:
1. Check the logs in `logs/management.log`
2. Review nginx error logs
3. Test API endpoints directly
4. Check system resource usage

---

**R3ÆLƎR AI Management System v1.0**
*Comprehensive AI system management made simple*