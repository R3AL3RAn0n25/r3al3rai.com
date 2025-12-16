#!/usr/bin/env python3
"""
R3AL3R AI - Dev/Prod Mode Switcher CLI Tool
Easily switch between development and production modes from command line
"""

import requests
import json
import sys
import os
from typing import Optional, Tuple

class ModeSwitcher:
    def __init__(self, base_url: str = 'http://localhost:3000'):
        self.base_url = base_url
        self.token = None
    
    def load_token(self) -> bool:
        """Load JWT token from environment or file"""
        # Try environment variable first
        self.token = os.getenv('R3AL3R_JWT_TOKEN')
        
        # Try file
        if not self.token and os.path.exists('.r3al3r_token'):
            with open('.r3al3r_token', 'r') as f:
                self.token = f.read().strip()
        
        return bool(self.token)
    
    def get_headers(self) -> dict:
        """Get authorization headers"""
        if not self.token:
            raise ValueError("JWT token not available")
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def get_mode(self) -> dict:
        """Get current mode and configuration"""
        r = requests.get(
            f'{self.base_url}/api/admin/mode',
            headers=self.get_headers()
        )
        if r.status_code == 200:
            return r.json()['data']
        raise Exception(f"Failed to get mode: {r.status_code}")
    
    def set_mode(self, mode: str) -> dict:
        """Set specific mode (development or production)"""
        if mode not in ('development', 'production'):
            raise ValueError("Mode must be 'development' or 'production'")
        
        r = requests.post(
            f'{self.base_url}/api/admin/mode/set',
            headers=self.get_headers(),
            json={'mode': mode}
        )
        if r.status_code == 200:
            return r.json()
        raise Exception(f"Failed to set mode: {r.status_code}")
    
    def toggle_mode(self) -> dict:
        """Toggle between development and production"""
        r = requests.post(
            f'{self.base_url}/api/admin/mode/toggle',
            headers=self.get_headers()
        )
        if r.status_code == 200:
            return r.json()
        raise Exception(f"Failed to toggle mode: {r.status_code}")

def print_mode_info(data: dict):
    """Pretty print mode information"""
    current = data['currentMode'].upper()
    config = data['config']
    
    mode_color = '\033[92m' if current == 'DEVELOPMENT' else '\033[91m'
    reset = '\033[0m'
    
    print(f"\n{mode_color}Current Mode: {current}{reset}")
    print(f"  Security Level:    {config['securityLevel']}")
    print(f"  Log Level:         {config['logLevel']}")
    print(f"  Rate Limit:        {config['rateLimitRequests']} req/min")
    print(f"  Test Endpoints:    {'Enabled' if config['allowTestEndpoints'] else 'Disabled'}")
    print(f"  Debug Mode:        {'Enabled' if config['debugEndpoints'] else 'Disabled'}")
    print(f"  Database Logging:  {'Enabled' if config['databaseLogging'] else 'Disabled'}")
    
    print(f"\n  Service Timeouts:")
    for service, settings in config['services'].items():
        print(f"    {service:<12} {settings['timeout']}ms (retries: {settings['retryAttempts']})")
    print()

def main():
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════╗
║           R3AL3R AI - Dev/Prod Mode Switcher                ║
╚══════════════════════════════════════════════════════════════╝

Usage:
  python mode_switcher.py <command> [options]

Commands:
  status              Show current mode and configuration
  dev                 Switch to development mode
  prod                Switch to production mode
  toggle              Toggle between dev and production
  
Options:
  --token <TOKEN>     Set JWT token (or use R3AL3R_JWT_TOKEN env var)
  --url <URL>         API base URL (default: http://localhost:3000)

Examples:
  python mode_switcher.py status
  python mode_switcher.py dev --token eyJhbGc...
  python mode_switcher.py toggle --token $R3AL3R_JWT_TOKEN
  python mode_switcher.py prod --url https://api.r3aler.ai
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    url = 'http://localhost:3000'
    token = None
    
    # Parse options
    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == '--url' and i + 1 < len(sys.argv):
            url = sys.argv[i + 1]
        elif arg == '--token' and i + 1 < len(sys.argv):
            token = sys.argv[i + 1]
    
    # Initialize switcher
    switcher = ModeSwitcher(url)
    
    # Load token
    if token:
        switcher.token = token
    elif not switcher.load_token():
        print("Error: JWT token not found. Set R3AL3R_JWT_TOKEN or use --token")
        sys.exit(1)
    
    try:
        if command == 'status':
            print("Fetching current mode...")
            data = switcher.get_mode()
            print_mode_info(data)
        
        elif command == 'dev':
            print("Switching to development mode...")
            result = switcher.set_mode('development')
            print(f"✓ {result['message']}")
            print_mode_info(result['config'])
        
        elif command == 'prod':
            print("Switching to production mode...")
            result = switcher.set_mode('production')
            print(f"✓ {result['message']}")
            print_mode_info(result['config'])
        
        elif command == 'toggle':
            current = switcher.get_mode()
            new_mode = 'production' if current['currentMode'] == 'development' else 'development'
            print(f"Toggling to {new_mode} mode...")
            result = switcher.toggle_mode()
            print(f"✓ {result['message']}")
            print_mode_info(result['config'])
        
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
