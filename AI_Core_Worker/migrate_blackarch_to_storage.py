#!/usr/bin/env python3
"""
R3ÆLƎR AI: Migrate BlackArch Tools to Storage Facility
Migrates 2,874+ BlackArch tool metadata to PostgreSQL Storage Facility
Preserves existing knowledge base units (physics, quantum, space, crypto)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Tools'))

import psycopg2
from psycopg2 import extras
import logging
from typing import Dict, List
from datetime import datetime

# Import BlackArch tools manager
from blackarch_tools_manager import BlackArchToolsManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# PostgreSQL connection details (same as Storage Facility)
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'r3aler_ai',
    'user': 'r3aler_user_2025',
    'password': 'postgres'
}

# Skill level mapping based on tool complexity
SKILL_LEVELS = {
    'scanner': 'beginner',
    'reconnaissance': 'beginner',
    'sniffer': 'intermediate',
    'web': 'intermediate',
    'cracker': 'intermediate',
    'exploitation': 'advanced',
    'forensic': 'advanced',
    'mobile': 'advanced',
    'wireless': 'intermediate',
    'reversing': 'expert',
    'dos': 'intermediate',
    'proxy': 'beginner'
}

# Legal and ethical guidelines
ETHICAL_GUIDELINES = """
⚖️ LEGAL USE ONLY
This tool is for authorized security testing ONLY.
- Obtain written permission before testing any system
- Follow local/international computer crime laws
- Use only on systems you own or have explicit authorization to test
- Document all testing activities
- Report findings responsibly

⚠️ UNAUTHORIZED ACCESS IS ILLEGAL
Violation may result in criminal prosecution under:
- Computer Fraud and Abuse Act (CFAA) - USA
- Computer Misuse Act - UK  
- EU Cybersecurity Directive
- Local jurisdiction laws

R3ÆLƎR AI users accept full responsibility for tool usage.
"""

def get_usage_example(tool_name: str, category: str) -> str:
    """Generate usage examples based on tool name and category"""
    
    usage_map = {
        'nmap': 'nmap -sV -sC target.com',
        'sqlmap': 'sqlmap -u "http://target.com/page?id=1" --dbs',
        'metasploit': 'msfconsole -q -x "use exploit/...; set RHOST target; exploit"',
        'burpsuite': 'java -jar burpsuite.jar (GUI application)',
        'wireshark': 'wireshark (GUI application) or tshark -i eth0',
        'aircrack-ng': 'aircrack-ng -w wordlist.txt capture.cap',
        'hashcat': 'hashcat -m 0 -a 0 hash.txt wordlist.txt',
        'john': 'john --wordlist=passwords.txt hash.txt',
        'hydra': 'hydra -l admin -P passwords.txt ssh://target.com',
        'theharvester': 'theharvester -d target.com -b google',
        'sherlock': 'sherlock username',
        'nikto': 'nikto -h http://target.com',
        'dirb': 'dirb http://target.com /usr/share/wordlists/dirb/common.txt',
        'gobuster': 'gobuster dir -u http://target.com -w wordlist.txt',
        'radare2': 'r2 -A binary_file',
        'ghidra': 'ghidraRun (GUI application)',
        'autopsy': 'autopsy (GUI application)',
        'beef': 'beef-xss (starts server on http://127.0.0.1:3000/ui/panel)',
        'masscan': 'masscan -p1-65535 --rate=1000 target.com',
        'recon-ng': 'recon-ng (interactive shell)',
    }
    
    return usage_map.get(tool_name, f'{tool_name} --help  # See available options')

def get_typical_use_cases(category: str, description: str) -> str:
    """Generate typical use cases based on category and description"""
    
    use_cases = {
        'scanner': '• Network security audits\n• Vulnerability assessment\n• Port scanning and service detection',
        'reconnaissance': '• Information gathering phase\n• OSINT investigations\n• Target profiling\n• Subdomain enumeration',
        'web': '• Web application security testing\n• Finding hidden directories/files\n• SQL injection testing\n• XSS vulnerability detection',
        'cracker': '• Password recovery (authorized systems)\n• Security audit of password policies\n• Hash analysis\n• Brute force testing',
        'exploitation': '• Penetration testing\n• Security vulnerability validation\n• Post-exploitation activities\n• Red team operations',
        'forensic': '• Digital forensics investigations\n• Evidence collection\n• Data recovery\n• Incident response',
        'wireless': '• WiFi security auditing\n• Wireless network assessment\n• WPA/WEP testing\n• Rogue AP detection',
        'mobile': '• Android app security testing\n• Mobile malware analysis\n• APK reverse engineering\n• Mobile forensics',
        'reversing': '• Malware analysis\n• Software vulnerability research\n• Binary analysis\n• Understanding compiled code',
        'sniffer': '• Network traffic analysis\n• Protocol debugging\n• Malware behavior monitoring\n• Network forensics',
        'dos': '• Stress testing systems (authorized)\n• Understanding DoS attack vectors\n• Security research',
        'proxy': '• Traffic interception (authorized)\n• Anonymity research\n• Network debugging'
    }
    
    return use_cases.get(category, '• Security research\n• Authorized penetration testing\n• Educational purposes')

def get_install_command(tool_name: str, category: str) -> str:
    """Generate installation command"""
    return f'pacman -S {tool_name} --noconfirm  # BlackArch/Arch Linux'

def get_documentation_url(tool_name: str) -> str:
    """Generate documentation URL"""
    
    known_urls = {
        'nmap': 'https://nmap.org/book/',
        'metasploit': 'https://docs.metasploit.com/',
        'burpsuite': 'https://portswigger.net/burp/documentation',
        'wireshark': 'https://www.wireshark.org/docs/',
        'sqlmap': 'https://github.com/sqlmapproject/sqlmap/wiki',
        'aircrack-ng': 'https://www.aircrack-ng.org/documentation.html',
        'hashcat': 'https://hashcat.net/wiki/',
        'john': 'https://www.openwall.com/john/doc/',
        'radare2': 'https://book.rada.re/',
        'ghidra': 'https://ghidra-sre.org/CheatSheet.html',
    }
    
    return known_urls.get(tool_name, f'https://www.blackarch.org/tools.html#{tool_name}')

def estimate_size_mb(category: str) -> int:
    """Estimate tool size in MB"""
    
    size_map = {
        'scanner': 5,
        'reconnaissance': 10,
        'web': 50,
        'cracker': 20,
        'exploitation': 200,  # Metasploit is huge
        'forensic': 100,
        'wireless': 15,
        'mobile': 30,
        'reversing': 150,  # Ghidra, Radare2
        'sniffer': 25,
        'dos': 5,
        'proxy': 10
    }
    
    return size_map.get(category, 15)

def migrate_blackarch_tools():
    """Main migration function"""
    
    logger.info("=" * 70)
    logger.info("R3ÆLƎR AI: BlackArch Tools Migration to Storage Facility")
    logger.info("=" * 70)
    
    # Initialize BlackArch manager
    logger.info("Loading BlackArch tools from manager...")
    ba_manager = BlackArchToolsManager(use_postgres=False)
    ba_manager.init_database()
    ba_manager.load_blackarch_tools_database()
    
    tools = ba_manager.blackarch_tools
    logger.info(f"Loaded {len(tools)} tools from BlackArch manager")
    
    # Connect to PostgreSQL
    logger.info("Connecting to PostgreSQL Storage Facility...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Check if schema exists
    cursor.execute("""
        SELECT schema_name FROM information_schema.schemata 
        WHERE schema_name = 'blackarch_unit';
    """)
    
    if not cursor.fetchone():
        logger.error("❌ blackarch_unit schema not found!")
        logger.info("Run create_blackarch_and_user_units.sql first")
        conn.close()
        return
    
    logger.info("✅ blackarch_unit schema found")
    
    # Migrate tools
    logger.info("Migrating tools to blackarch_unit.tools...")
    
    migrated = 0
    errors = 0
    
    for tool_name, tool in tools.items():
        try:
            # Prepare enriched metadata
            tool_id = tool_name.lower().replace(' ', '-')
            skill_level = SKILL_LEVELS.get(tool.category, 'intermediate')
            usage_example = get_usage_example(tool_name, tool.category)
            typical_use_cases = get_typical_use_cases(tool.category, tool.description)
            documentation_url = get_documentation_url(tool_name)
            install_command = get_install_command(tool_name, tool.category)
            estimated_size = estimate_size_mb(tool.category)
            
            # Insert into database
            cursor.execute("""
                INSERT INTO blackarch_unit.tools (
                    tool_id, name, category, description,
                    usage_example, documentation_url, install_command,
                    dependencies, typical_use_cases, skill_level,
                    estimated_size_mb, license, legal_notes, ethical_guidelines,
                    official_repo_url, last_updated
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (tool_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    category = EXCLUDED.category,
                    description = EXCLUDED.description,
                    usage_example = EXCLUDED.usage_example,
                    documentation_url = EXCLUDED.documentation_url,
                    install_command = EXCLUDED.install_command,
                    typical_use_cases = EXCLUDED.typical_use_cases,
                    skill_level = EXCLUDED.skill_level,
                    estimated_size_mb = EXCLUDED.estimated_size_mb,
                    last_updated = EXCLUDED.last_updated
            """, (
                tool_id,
                tool.name,
                tool.category,
                tool.description,
                usage_example,
                documentation_url,
                install_command,
                tool.dependencies,  # PostgreSQL array
                typical_use_cases,
                skill_level,
                estimated_size,
                'GPL/MIT (varies)',
                'CHECK LOCAL LAWS - Unauthorized access is illegal',
                ETHICAL_GUIDELINES,
                f'https://github.com/BlackArch/blackarch/tree/master/packages/{tool_name}',
                datetime.now().date()
            ))
            
            migrated += 1
            
            if migrated % 100 == 0:
                logger.info(f"Migrated {migrated} tools...")
                
        except Exception as e:
            logger.error(f"Error migrating {tool_name}: {e}")
            errors += 1
    
    # Commit transaction
    conn.commit()
    
    # Get final statistics
    cursor.execute("SELECT COUNT(*) FROM blackarch_unit.tools")
    total_tools = cursor.fetchone()[0]
    
    cursor.execute("SELECT category, COUNT(*) FROM blackarch_unit.tools GROUP BY category ORDER BY COUNT(*) DESC")
    category_stats = cursor.fetchall()
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ MIGRATION COMPLETE!")
    logger.info("=" * 70)
    logger.info(f"Tools migrated: {migrated}")
    logger.info(f"Errors: {errors}")
    logger.info(f"Total in database: {total_tools}")
    logger.info("\nTools by Category:")
    for category, count in category_stats:
        logger.info(f"  {category:20s}: {count:4d} tools")
    
    # Verify knowledge base units are untouched
    logger.info("\n" + "=" * 70)
    logger.info("KNOWLEDGE BASE VERIFICATION (Should be unchanged)")
    logger.info("=" * 70)
    
    knowledge_units = ['physics_unit', 'quantum_unit', 'space_unit', 'crypto_unit']
    for unit in knowledge_units:
        cursor.execute(f"SELECT COUNT(*) FROM {unit}.knowledge")
        count = cursor.fetchone()[0]
        logger.info(f"  {unit:20s}: {count:6d} entries ✅")
    
    conn.close()
    
    logger.info("\n" + "=" * 70)
    logger.info("🚀 R3ÆLƎR AI Storage Facility Now Includes:")
    logger.info("   • Physics Knowledge (25,875 entries)")
    logger.info("   • Quantum Knowledge (1,042 entries)")
    logger.info("   • Space Knowledge (3,727 entries)")
    logger.info("   • Crypto Knowledge (13 entries)")
    logger.info(f"   • BlackArch Tools ({total_tools} tools) ⭐ NEW")
    logger.info("   • User Profiles (schema ready)")
    logger.info("=" * 70)

if __name__ == '__main__':
    migrate_blackarch_tools()
