#!/bin/bash
#
# R3AL3R-AI BlackArch Integration Startup Script
# Easy management script for BlackArch tools integration
#
# Usage:
#   ./start_blackarch.sh          - Start all services
#   ./start_blackarch.sh web      - Start only web interface
#   ./start_blackarch.sh status   - Check system status
#   ./start_blackarch.sh stop     - Stop all services
#   ./start_blackarch.sh install  - Install a tool
#   ./start_blackarch.sh list     - List available tools
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai"
VENV_PATH="$PROJECT_DIR/blackarch_venv"
TOOLS_DIR="$PROJECT_DIR/Tools"
WEB_PORT=8081

# Banner
print_banner() {
    echo -e "${CYAN}"
    echo "🛡️  R3AL3R-AI BlackArch Integration"
    echo "======================================"
    echo -e "${NC}"
}

# Check if virtual environment exists
check_venv() {
    if [ ! -d "$VENV_PATH" ]; then
        echo -e "${RED}❌ Virtual environment not found at $VENV_PATH${NC}"
        echo -e "${YELLOW}Run deployment script first: python3 Tools/deploy_blackarch_integration.py${NC}"
        exit 1
    fi
}

# Activate virtual environment
activate_venv() {
    source "$VENV_PATH/bin/activate"
}

# Start web interface
start_web() {
    echo -e "${BLUE}🌐 Starting BlackArch Web Interface...${NC}"
    cd "$PROJECT_DIR"
    activate_venv
    
    echo -e "${GREEN}✅ Web interface starting on http://localhost:$WEB_PORT${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    
    python3 "$TOOLS_DIR/blackarch_web_app.py"
}

# Check system status
check_status() {
    echo -e "${BLUE}📊 Checking BlackArch System Status...${NC}"
    cd "$PROJECT_DIR"
    activate_venv
    
    python3 "$TOOLS_DIR/blackarch_tools_manager.py" status
    
    echo -e "\n${BLUE}🌐 Web Interface Status:${NC}"
    if curl -s "http://localhost:$WEB_PORT/api/status" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Web interface is running on port $WEB_PORT${NC}"
    else
        echo -e "${RED}❌ Web interface is not running${NC}"
    fi
}

# List available tools
list_tools() {
    echo -e "${BLUE}🔧 Available BlackArch Tools:${NC}"
    cd "$PROJECT_DIR"
    activate_venv
    
    python3 "$TOOLS_DIR/blackarch_tools_manager.py" list | head -20
    echo -e "\n${YELLOW}Showing first 20 tools. Use 'python3 Tools/blackarch_tools_manager.py list' for complete list.${NC}"
}

# Install a tool
install_tool() {
    if [ -z "$2" ]; then
        echo -e "${RED}❌ Please specify a tool name${NC}"
        echo -e "${YELLOW}Usage: $0 install <tool_name>${NC}"
        echo -e "${YELLOW}Example: $0 install nmap${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}📦 Installing tool: $2${NC}"
    cd "$PROJECT_DIR"
    activate_venv
    
    python3 "$TOOLS_DIR/blackarch_tools_manager.py" install "$2"
}

# Execute a tool
execute_tool() {
    if [ -z "$2" ]; then
        echo -e "${RED}❌ Please specify a tool name${NC}"
        echo -e "${YELLOW}Usage: $0 execute <tool_name> [args]${NC}"
        echo -e "${YELLOW}Example: $0 execute nmap -sS 192.168.1.1${NC}"
        exit 1
    fi
    
    tool_name="$2"
    shift 2
    args="$@"
    
    echo -e "${BLUE}🚀 Executing tool: $tool_name $args${NC}"
    cd "$PROJECT_DIR"
    activate_venv
    
    python3 "$TOOLS_DIR/blackarch_tools_manager.py" execute "$tool_name" $args
}

# Stop services
stop_services() {
    echo -e "${BLUE}🛑 Stopping BlackArch services...${NC}"
    
    # Kill web interface if running
    if pgrep -f "blackarch_web_app.py" > /dev/null; then
        pkill -f "blackarch_web_app.py"
        echo -e "${GREEN}✅ Web interface stopped${NC}"
    else
        echo -e "${YELLOW}⚠️ Web interface was not running${NC}"
    fi
    
    echo -e "${GREEN}✅ All services stopped${NC}"
}

# Start all services
start_all() {
    echo -e "${BLUE}🚀 Starting all BlackArch services...${NC}"
    
    # Check status first
    cd "$PROJECT_DIR"
    activate_venv
    
    echo -e "${BLUE}📊 System Status:${NC}"
    python3 "$TOOLS_DIR/blackarch_tools_manager.py" status | head -5
    
    echo -e "\n${BLUE}🌐 Starting web interface...${NC}"
    echo -e "${GREEN}✅ Access the web interface at: http://localhost:$WEB_PORT${NC}"
    echo -e "${GREEN}✅ API available at: http://localhost:$WEB_PORT/api/${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
    
    start_web
}

# Show help
show_help() {
    echo -e "${BLUE}R3AL3R-AI BlackArch Integration Management${NC}"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo -e "  ${GREEN}start${NC}           Start all services (web interface)"
    echo -e "  ${GREEN}web${NC}             Start only web interface"
    echo -e "  ${GREEN}status${NC}          Check system status"
    echo -e "  ${GREEN}stop${NC}            Stop all services"
    echo -e "  ${GREEN}list${NC}            List available tools"
    echo -e "  ${GREEN}install <tool>${NC}  Install a specific tool"
    echo -e "  ${GREEN}execute <tool>${NC}  Execute a tool with arguments"
    echo -e "  ${GREEN}help${NC}            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start all services"
    echo "  $0 status                   # Check status"
    echo "  $0 list                     # List tools"
    echo "  $0 install nmap             # Install nmap"
    echo "  $0 execute nmap -sS 192.168.1.1  # Run nmap scan"
    echo ""
    echo "Web Interface: http://localhost:$WEB_PORT"
    echo "API Endpoints: http://localhost:$WEB_PORT/api/"
}

# Main script logic
main() {
    print_banner
    check_venv
    
    case "${1:-start}" in
        "start"|"")
            start_all
            ;;
        "web")
            start_web
            ;;
        "status")
            check_status
            ;;
        "stop")
            stop_services
            ;;
        "list")
            list_tools
            ;;
        "install")
            install_tool "$@"
            ;;
        "execute")
            execute_tool "$@"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $1${NC}"
            echo -e "${YELLOW}Use '$0 help' for available commands${NC}"
            exit 1
            ;;
    esac
}

# Trap Ctrl+C to stop services gracefully
trap 'echo -e "\n${YELLOW}🛑 Stopping services...${NC}"; stop_services; exit 0' INT

# Run main function
main "$@"