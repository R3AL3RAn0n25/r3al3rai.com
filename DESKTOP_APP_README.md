# R3ÆLƎR Management System - Desktop Application

A standalone desktop application for managing the R3ÆLƎR AI system locally without web browser dependencies.

## Features

### 🤖 AI Management
- Initialize and control the AI Core
- Submit queries and receive AI responses
- Run AI benchmarks and performance tests
- Real-time AI status monitoring

### 🧠 Knowledge Base
- Intelligent search across knowledge databases
- Add new knowledge entries
- Import and export knowledge datasets
- Vector-based semantic search

### 💰 Wallet Analysis
- Analyze cryptocurrency wallet addresses
- Extract keys from wallet files
- Balance checking and transaction analysis
- Support for multiple wallet formats

### 🔒 BlackArch Integration
- Access to security tools
- Tool management and updates
- Execute security assessments
- Web interface for advanced tools

### 🗄️ Database Management
- PostgreSQL database connection
- Execute SQL queries
- View database structure
- Backup and restore functionality

### ⚙️ System Management
- Real-time system health monitoring
- Service management and restart
- Configuration management
- Log viewing and analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database (optional, for full functionality)
- Windows 10/11, macOS, or Linux

### Quick Start (Windows)
1. Double-click `launch_desktop_app.bat`
2. The application will automatically install dependencies and launch

### Manual Installation
```bash
# Install Python dependencies
pip install -r requirements_desktop.txt

# Launch the application
python r3aler_desktop_app.py
```

## Usage

### First Time Setup
1. Launch the application using `launch_desktop_app.bat`
2. The dashboard will show system initialization status
3. Configure database connection in the Database tab
4. Set API endpoints in the Settings tab

### Main Interface

#### Dashboard
- **System Status**: Real-time status of all components
- **Quick Actions**: Fast access to common functions
- **System Information**: Detailed system and component info

#### AI Management
- **Initialize AI Core**: Start the AI processing engine
- **Query Interface**: Submit questions and get AI responses
- **Benchmarking**: Test AI performance and capabilities

#### Knowledge Base
- **Search**: Find information using natural language queries
- **Management**: Add, import, and export knowledge data
- **Vector Search**: Semantic search across all knowledge sources

#### Wallet Analysis
- **Address Analysis**: Check wallet balances and transactions
- **File Analysis**: Extract keys from wallet files
- **Security Tools**: Advanced wallet recovery options

#### BlackArch Tools
- **Tool Management**: Install and update security tools
- **Tool Execution**: Run security assessments
- **Web Interface**: Access advanced tool configurations

#### Database
- **Connection**: Configure PostgreSQL connection
- **Query Execution**: Run SQL commands
- **Table Management**: View and modify database structure

#### Settings
- **API Configuration**: Set service endpoints
- **System Actions**: Health checks and service management
- **About**: System information and documentation

## Configuration

### Database Setup
1. Go to the Database tab
2. Enter your PostgreSQL connection details:
   - Host: localhost (or your server)
   - Port: 5432 (default)
   - Database: r3aler_ai
   - User: r3aler_user_2025
   - Password: (your password)
3. Click "Connect"

### API Endpoints
Configure the following services in Settings:
- **Storage Facility URL**: http://localhost:5003
- **Knowledge API URL**: http://localhost:5001
- **Enhanced API Port**: 5010

## Troubleshooting

### Common Issues

#### "AI Core not initialized"
- Click "Initialize AI Core" in the AI Management tab
- Check that all Python dependencies are installed

#### "Database connection failed"
- Verify PostgreSQL is running
- Check connection credentials
- Ensure database exists

#### "Component not available"
- Some features require additional setup
- Check system requirements
- Review error logs in the Settings tab

#### Application won't start
- Ensure Python 3.8+ is installed
- Run: `pip install -r requirements_desktop.txt`
- Check Windows PATH includes Python

### Logs and Debugging
- View application logs: Settings → View Logs
- Check system health: Settings → Check System Health
- Restart services: Settings → Restart Services

## Architecture

The desktop application provides a local interface to the R3ÆLƎR system:

```
┌─────────────────┐    ┌──────────────────┐
│   Desktop App   │────│   AI Core        │
│   (Tkinter)     │    │   (Quantum AI)   │
└─────────────────┘    └──────────────────┘
         │                       │
         └───────────────────────┼──────────────────────┐
                                 │                      │
                    ┌────────────▼────────┐   ┌─────────▼────────┐
                    │  Knowledge API     │   │  Database        │
                    │  (Vector Search)   │   │  (PostgreSQL)    │
                    └────────────────────┘   └──────────────────┘
                             │
                    ┌────────▼────────┐
                    │  BlackArch      │
                    │  Tools          │
                    └─────────────────┘
```

## Security Notes

- Database passwords are stored in memory only
- Wallet analysis is performed locally
- No sensitive data is transmitted without encryption
- Review logs regularly for security events

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review system logs
3. Ensure all prerequisites are met
4. Check component initialization status

## Development

The desktop application is built with:
- **Tkinter**: Cross-platform GUI framework
- **Threading**: Background task processing
- **Logging**: Comprehensive error tracking
- **Modular Design**: Easy feature extension

To extend functionality, modify `r3aler_desktop_app.py` and add new tabs or features following the existing patterns.