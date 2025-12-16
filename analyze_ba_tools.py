#!/usr/bin/env python3
"""Analyze BlackArch tools integration and functionality"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Tools'))

from blackarch_tools_manager import BlackArchToolsManager
import json

def analyze_tools():
    manager = BlackArchToolsManager()
    
    # First, scan system for installed tools
    print("Scanning system for installed tools...")
    installed_count = manager.scan_installed_tools()
    print(f"Scan complete: Found {installed_count} installed tools\n")
    
    tools = manager.blackarch_tools
    
    # Categories of tools
    categories = {
        'GUI Tools': [],
        'Network Scanners': [],
        'Password Tools': [],
        'Web Tools': [],
        'Exploitation': [],
        'Forensics': [],
        'Wireless': [],
        'Other': []
    }
    
    # GUI tools list
    gui_keywords = ['gui', 'graphical', 'interface', 'gtk', 'qt']
    known_gui_tools = ['wireshark', 'zenmap', 'burpsuite', 'ettercap', 'armitage']
    
    # Categorize each tool
    for name, tool in tools.items():
        desc_lower = tool.description.lower()
        
        if name in known_gui_tools or any(kw in desc_lower for kw in gui_keywords):
            categories['GUI Tools'].append(name)
        
        if any(kw in desc_lower for kw in ['scan', 'network', 'port', 'nmap']):
            categories['Network Scanners'].append(name)
        
        if any(kw in desc_lower for kw in ['password', 'hash', 'crack', 'brute']):
            categories['Password Tools'].append(name)
        
        if any(kw in desc_lower for kw in ['web', 'http', 'sql', 'xss']):
            categories['Web Tools'].append(name)
        
        if any(kw in desc_lower for kw in ['exploit', 'metasploit', 'payload']):
            categories['Exploitation'].append(name)
        
        if any(kw in desc_lower for kw in ['forensic', 'analysis', 'recovery']):
            categories['Forensics'].append(name)
        
        if any(kw in desc_lower for kw in ['wireless', 'wifi', '802.11', 'aircrack']):
            categories['Wireless'].append(name)
    
    # Count installed vs not installed
    installed = [name for name, tool in tools.items() if tool.installed]
    not_installed = [name for name, tool in tools.items() if not tool.installed]
    
    # Print report
    print("=" * 80)
    print("BLACKARCH TOOLS INTEGRATION ANALYSIS")
    print("=" * 80)
    print(f"\nTotal Tools: {len(tools)}")
    print(f"Installed: {len(installed)} ({len(installed)/len(tools)*100:.1f}%)")
    print(f"Not Installed: {len(not_installed)} ({len(not_installed)/len(tools)*100:.1f}%)")
    
    print("\n" + "=" * 80)
    print("TOOL CATEGORIES")
    print("=" * 80)
    for category, tool_list in categories.items():
        if tool_list:
            print(f"\n{category} ({len(tool_list)} tools):")
            for tool_name in sorted(tool_list)[:10]:  # Show first 10
                tool = tools[tool_name]
                status = "✓ Installed" if tool.installed else "✗ Not Installed"
                print(f"  - {tool_name}: {status}")
            if len(tool_list) > 10:
                print(f"  ... and {len(tool_list) - 10} more")
    
    print("\n" + "=" * 80)
    print("GUI TOOLS REQUIRING SPECIAL HANDLING")
    print("=" * 80)
    gui_tools = categories['GUI Tools']
    for tool_name in sorted(gui_tools):
        tool = tools[tool_name]
        status = "✓ Installed" if tool.installed else "✗ Not Installed"
        print(f"  {tool_name}: {status}")
        print(f"    Description: {tool.description[:80]}...")
    
    print("\n" + "=" * 80)
    print("RECOMMENDED INSTALLATIONS FOR FULL FUNCTIONALITY")
    print("=" * 80)
    
    # Essential tools that should be installed
    essential_tools = [
        'nmap', 'wireshark', 'metasploit', 'burpsuite', 'sqlmap',
        'nikto', 'hydra', 'john', 'aircrack-ng', 'ettercap'
    ]
    
    for tool_name in essential_tools:
        if tool_name in tools:
            tool = tools[tool_name]
            if not tool.installed:
                print(f"  ✗ {tool_name}: {tool.description[:60]}...")
            else:
                print(f"  ✓ {tool_name}: Already installed")
    
    print("\n" + "=" * 80)
    print("TOOLS WITH SPECIAL REQUIREMENTS")
    print("=" * 80)
    
    special_requirements = {
        'wireshark': 'Requires --version flag or tshark for headless operation',
        'zenmap': 'GUI for nmap - use nmap CLI instead in headless mode',
        'burpsuite': 'Requires X11 display - cannot run in headless WSL',
        'metasploit': 'Use msfconsole for CLI access',
        'ettercap': 'Has both GUI and CLI modes - use -T for text mode',
        'aircrack-ng': 'Wireless tools - requires wireless adapter access'
    }
    
    for tool_name, requirement in special_requirements.items():
        if tool_name in tools:
            status = "✓" if tools[tool_name].installed else "✗"
            print(f"  {status} {tool_name}:")
            print(f"     {requirement}")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    analyze_tools()
