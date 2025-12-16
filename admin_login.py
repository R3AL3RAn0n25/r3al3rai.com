#!/usr/bin/env python3
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
