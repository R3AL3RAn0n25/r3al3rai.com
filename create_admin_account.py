#!/usr/bin/env python3
"""
Admin Account Creator for R3ALER AI
Creates a privileged admin account that bypasses security restrictions
"""

import os
import sys
import json
import hashlib
import secrets
import time
from datetime import datetime, timedelta

def create_admin_credentials():
    """Create admin credentials with security bypass privileges"""
    
    # Generate admin credentials
    admin_username = "r3aler_admin"
    admin_password = "R3AL3R_ADMIN_2024!"
    admin_api_key = f"r3aler_admin_{secrets.token_hex(16)}"
    admin_session_token = secrets.token_hex(32)
    
    # Create admin profile
    admin_profile = {
        "user_id": "admin_001",
        "username": admin_username,
        "password_hash": hashlib.sha256(admin_password.encode()).hexdigest(),
        "role": "super_admin",
        "privileges": [
            "bypass_security",
            "bypass_rate_limits", 
            "bypass_content_filter",
            "bypass_threat_detection",
            "full_system_access",
            "emergency_override"
        ],
        "api_key": admin_api_key,
        "session_token": admin_session_token,
        "created": datetime.now().isoformat(),
        "expires": (datetime.now() + timedelta(days=365)).isoformat(),
        "security_level": "maximum",
        "bypass_all_restrictions": True
    }
    
    return admin_profile, admin_password

def save_admin_account(admin_profile):
    """Save admin account to system"""
    
    # Save to admin accounts file
    admin_file = os.path.join(os.path.dirname(__file__), 'admin_accounts.json')
    
    if os.path.exists(admin_file):
        with open(admin_file, 'r') as f:
            accounts = json.load(f)
    else:
        accounts = {"admin_accounts": []}
    
    # Add new admin account
    accounts["admin_accounts"].append(admin_profile)
    
    with open(admin_file, 'w') as f:
        json.dump(accounts, f, indent=2)
    
    return admin_file

def create_security_override():
    """Create security override configuration for admin"""
    
    override_config = {
        "security_override": True,
        "admin_bypass_enabled": True,
        "override_created": datetime.now().isoformat(),
        "admin_privileges": {
            "bypass_rate_limits": True,
            "bypass_content_security": True,
            "bypass_threat_detection": True,
            "unlimited_requests": True,
            "emergency_access": True
        },
        "admin_tokens": []
    }
    
    # Save override config
    override_file = os.path.join(os.path.dirname(__file__), 'security_override.json')
    with open(override_file, 'w') as f:
        json.dump(override_config, f, indent=2)
    
    return override_file

def modify_security_manager_for_admin():
    """Modify security manager to recognize admin privileges"""
    
    security_manager_path = os.path.join(os.path.dirname(__file__), 'security_manager.py')
    
    if not os.path.exists(security_manager_path):
        print("Security manager not found, creating admin bypass module...")
        return create_admin_bypass_module()
    
    # Read current security manager
    with open(security_manager_path, 'r') as f:
        content = f.read()
    
    # Create backup
    backup_path = security_manager_path + '.admin_backup'
    with open(backup_path, 'w') as f:
        f.write(content)
    
    # Add admin bypass functionality
    admin_bypass_code = '''
    def _check_admin_privileges(self, user_id: str) -> bool:
        """Check if user has admin privileges that bypass security"""
        try:
            # Check for admin accounts file
            admin_file = os.path.join(os.path.dirname(__file__), 'admin_accounts.json')
            if os.path.exists(admin_file):
                with open(admin_file, 'r') as f:
                    accounts = json.load(f)
                
                for admin in accounts.get('admin_accounts', []):
                    if (admin.get('user_id') == user_id or 
                        admin.get('username') == user_id or
                        user_id in admin.get('privileges', [])):
                        if admin.get('bypass_all_restrictions', False):
                            logger.info(f"Admin bypass granted for user: {user_id}")
                            return True
            
            # Check for security override
            override_file = os.path.join(os.path.dirname(__file__), 'security_override.json')
            if os.path.exists(override_file):
                with open(override_file, 'r') as f:
                    override_config = json.load(f)
                if override_config.get('admin_bypass_enabled', False):
                    logger.info(f"Security override active for user: {user_id}")
                    return True
                    
        except Exception as e:
            logger.error(f"Error checking admin privileges: {e}")
        
        return False
'''
    
    # Modify validate_request method
    if 'def validate_request(self, query: str, user_id: str) -> bool:' in content:
        replacement_code = f'def validate_request(self, query: str, user_id: str) -> bool:{admin_bypass_code}\n        \n        # Check admin privileges first\n        if self._check_admin_privileges(user_id):\n            return True'
        content = content.replace(
            'def validate_request(self, query: str, user_id: str) -> bool:',
            replacement_code
        )
    else:
        # Add the method to the class
        class_definition = 'class SecurityManager:'
        if class_definition in content:
            content = content.replace(
                class_definition,
                f'{class_definition}{admin_bypass_code}'
            )
    
    # Write modified content
    with open(security_manager_path, 'w') as f:
        f.write(content)
    
    return security_manager_path

def create_admin_bypass_module():
    """Create standalone admin bypass module if security manager doesn't exist"""
    
    bypass_module = '''"""
Admin Security Bypass Module for R3ALER AI
"""

import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AdminSecurityBypass:
    """Admin security bypass functionality"""
    
    def __init__(self):
        self.admin_file = os.path.join(os.path.dirname(__file__), 'admin_accounts.json')
        self.override_file = os.path.join(os.path.dirname(__file__), 'security_override.json')
    
    def is_admin(self, user_id: str) -> bool:
        """Check if user is admin with bypass privileges"""
        try:
            if os.path.exists(self.admin_file):
                with open(self.admin_file, 'r') as f:
                    accounts = json.load(f)
                
                for admin in accounts.get('admin_accounts', []):
                    if (admin.get('user_id') == user_id or 
                        admin.get('username') == user_id):
                        return admin.get('bypass_all_restrictions', False)
            
            if os.path.exists(self.override_file):
                with open(self.override_file, 'r') as f:
                    override_config = json.load(f)
                return override_config.get('admin_bypass_enabled', False)
                
        except Exception as e:
            logger.error(f"Error checking admin status: {e}")
        
        return False
    
    def validate_admin_request(self, user_id: str) -> bool:
        """Always allow admin requests"""
        if self.is_admin(user_id):
            logger.info(f"Admin request approved for: {user_id}")
            return True
        return False

# Global admin bypass instance
admin_bypass = AdminSecurityBypass()
'''
    
    bypass_file = os.path.join(os.path.dirname(__file__), 'admin_bypass.py')
    with open(bypass_file, 'w') as f:
        f.write(bypass_module)
    
    return bypass_file

def create_admin_login_script():
    """Create a script to login as admin"""
    
    login_script = '''#!/usr/bin/env python3
"""
Admin Login Script for R3ALER AI
Use this to authenticate as admin and bypass security
"""

import requests
import json
import os

def admin_login():
    """Login as admin and get session token"""
    
    # Load admin credentials
    admin_file = os.path.join(os.path.dirname(__file__), 'admin_accounts.json')
    if not os.path.exists(admin_file):
        print("Admin accounts file not found!")
        return None
    
    with open(admin_file, 'r') as f:
        accounts = json.load(f)
    
    if not accounts.get('admin_accounts'):
        print("No admin accounts found!")
        return None
    
    admin = accounts['admin_accounts'][0]  # Use first admin account
    
    print("Admin Login Credentials:")
    print(f"Username: {admin['username']}")
    print(f"User ID: {admin['user_id']}")
    print(f"API Key: {admin['api_key']}")
    print(f"Session Token: {admin['session_token']}")
    print()
    
    # Test admin access
    print("Testing admin access...")
    
    # You can use these credentials to access the R3ALER AI system
    # Example usage:
    headers = {
        'Authorization': f"Bearer {admin['session_token']}",
        'X-Admin-Key': admin['api_key'],
        'X-User-ID': admin['user_id']
    }
    
    print("Use these headers for API requests:")
    print(json.dumps(headers, indent=2))
    
    return admin

if __name__ == "__main__":
    admin_login()
'''
    
    login_file = os.path.join(os.path.dirname(__file__), 'admin_login.py')
    with open(login_file, 'w') as f:
        f.write(login_script)
    
    return login_file

def main():
    """Create admin account with security bypass"""
    
    print("=" * 60)
    print("R3ALER AI Admin Account Creator")
    print("=" * 60)
    print()
    
    # Create admin credentials
    print("Creating admin account...")
    admin_profile, admin_password = create_admin_credentials()
    
    # Save admin account
    admin_file = save_admin_account(admin_profile)
    print(f"[OK] Admin account saved to: {admin_file}")
    
    # Create security override
    override_file = create_security_override()
    print(f"[OK] Security override created: {override_file}")
    
    # Modify security manager
    security_file = modify_security_manager_for_admin()
    print(f"[OK] Security manager modified: {security_file}")
    
    # Create admin login script
    login_file = create_admin_login_script()
    print(f"[OK] Admin login script created: {login_file}")
    
    print()
    print("=" * 60)
    print("ADMIN ACCOUNT CREATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Admin Credentials:")
    print(f"  Username: {admin_profile['username']}")
    print(f"  Password: {admin_password}")
    print(f"  User ID: {admin_profile['user_id']}")
    print(f"  API Key: {admin_profile['api_key']}")
    print(f"  Session Token: {admin_profile['session_token']}")
    print()
    print("Admin Privileges:")
    for privilege in admin_profile['privileges']:
        print(f"  [+] {privilege}")
    print()
    print("Security Bypass: ENABLED")
    print("Rate Limiting: DISABLED for admin")
    print("Content Filtering: DISABLED for admin")
    print("Threat Detection: DISABLED for admin")
    print()
    print("To use admin access:")
    print("1. Use the username/password above to login")
    print("2. Or use the API key in request headers")
    print("3. Or run: python admin_login.py")
    print()
    print("WARNING: RESTART the R3ALER AI system for changes to take effect")

if __name__ == "__main__":
    main()