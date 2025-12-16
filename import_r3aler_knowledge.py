#!/usr/bin/env python3
"""
R3AL3R AI - R3AL3R Knowledge and Prompts Import Script
Imports all system prompts and knowledge sources from prompts.py into the storage facility as the 'r3aler_knowledge' unit.
"""
import os
import sys
import logging
import requests
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), 'AI_Core_Worker'))
from prompts import R3AELERPrompts

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('r3aler_knowledge_import.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

STORAGE_URL = os.getenv('STORAGE_FACILITY_URL', 'http://localhost:3003')
UNIT = 'r3aler_knowledge'

# Collect all prompts and knowledge
entries = []

# System Personality
entries.append({
    "id": "r3aler_personality",
    "content": R3AELERPrompts.SYSTEM_PERSONALITY.strip(),
    "title": "R3AL3R AI System Personality",
    "category": "personality",
    "source": "prompts.py",
    "metadata": {"type": "system_personality", "timestamp": datetime.now().isoformat()}
})

# All system prompts
for attr in dir(R3AELERPrompts):
    if attr.endswith('_SYSTEM_PROMPT'):
        value = getattr(R3AELERPrompts, attr)
        entries.append({
            "id": f"r3aler_{attr.lower()}",
            "content": value.strip(),
            "title": attr.replace('_', ' ').title(),
            "category": "system_prompt",
            "source": "prompts.py",
            "metadata": {"type": "system_prompt", "timestamp": datetime.now().isoformat()}
        })

# Knowledge sources
for source in getattr(R3AELERPrompts, 'KNOWLEDGE_SOURCES', []):
    entries.append({
        "id": f"r3aler_knowledge_{source['name']}",
        "content": str(source),
        "title": f"Knowledge Source: {source['name']}",
        "category": "knowledge_source",
        "source": "prompts.py",
        "metadata": {"type": "knowledge_source", "timestamp": datetime.now().isoformat()}
    })

# Store all entries in storage facility
store_url = f"{STORAGE_URL}/api/unit/{UNIT}/store"
store_payload = {"entries": entries}
try:
    response = requests.post(store_url, json=store_payload, timeout=30)
    if response.status_code == 200:
        logging.info(f"✓ Imported {len(entries)} R3AL3R knowledge entries into '{UNIT}' unit.")
    else:
        logging.error(f"✗ Failed to import entries: {response.status_code} - {response.text}")
except Exception as e:
    logging.error(f"✗ Error importing entries: {e}")
