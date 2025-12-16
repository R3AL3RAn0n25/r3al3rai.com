#!/usr/bin/env python3
"""
R3AL3R AI - OpenWebText Dataset Integration Script
Loads and integrates the openwebtext dataset into the storage facility
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
import requests
from datasets import load_dataset

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('openwebtext_integration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class OpenWebTextIntegrator:
    """Integrates the OpenWebText dataset into the R3AL3R storage facility"""

    def __init__(self, storage_host='localhost', storage_port=3003, max_entries=1000):
        self.storage_host = storage_host
        self.storage_port = storage_port
        self.dataset_name = "openwebtext"
        self.entries_processed = 0
        self.entries_stored = 0
        self.errors = 0
        self.max_entries = max_entries

        # Storage facility connection
        self.storage_url = f"http://{storage_host}:{storage_port}"

    def check_storage_facility(self):
        """Check if storage facility is available"""
        try:
            response = requests.get(f"{self.storage_url}/api/facility/status", timeout=10)
            if response.status_code == 200:
                logging.info("Storage facility is available")
                return True
            else:
                logging.error(f"Storage facility returned status {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"Cannot connect to storage facility: {e}")
            return False

    def load_dataset(self):
        """Load the OpenWebText dataset"""
        try:
            logging.info(f"Loading dataset: {self.dataset_name}")
            self.dataset = load_dataset(
                self.dataset_name,
                split='train',
                streaming=True,
                trust_remote_code=True
            )
            logging.info("Dataset loaded successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to load dataset: {e}")
            return False

    def process_entry(self, entry):
        """Process a single dataset entry"""
        try:
            # Extract text content
            if isinstance(entry, dict) and 'text' in entry:
                text = entry['text'].strip()
            elif isinstance(entry, str):
                text = entry.strip()
            else:
                logging.warning(f"Skipping entry with unknown format: {type(entry)}")
                return None

            # Skip empty or very short entries
            if not text or len(text) < 50:
                return None

            # Create knowledge entry
            knowledge_entry = {
                "id": f"openwebtext_{self.entries_processed:06d}",
                "content": text,
                "title": f"Web Text Sample {self.entries_processed}",
                "category": "web_knowledge",
                "source": "OpenWebText Dataset",
                "metadata": {
                    "type": "web_content",
                    "dataset": "openwebtext",
                    "entry_number": self.entries_processed,
                    "content_length": len(text),
                    "timestamp": datetime.now().isoformat()
                }
            }

            return knowledge_entry

        except Exception as e:
            logging.warning(f"Error processing entry: {e}")
            return None

    def store_entry(self, entry):
        """Store an entry in the storage facility"""
        try:
            # Determine unit based on content analysis
            content = entry['content'].lower()

            # Simple categorization - use correct unit names
            if any(word in content for word in ['physics', 'quantum', 'science', 'mathematics', 'math']):
                unit = 'quantum'  # Physics/math content goes to quantum unit
            elif any(word in content for word in ['computer', 'programming', 'software', 'algorithm']):
                unit = 'quantum'  # Programming/AI goes to quantum unit
            elif any(word in content for word in ['cryptography', 'encryption', 'security', 'blockchain']):
                unit = 'crypto'
            elif any(word in content for word in ['biology', 'chemistry', 'medicine', 'health']):
                unit = 'physics'  # Science content goes to physics unit
            else:
                unit = 'users'  # General knowledge goes to users unit

            # Store the entry - API expects 'entries' array
            store_url = f"{self.storage_url}/api/unit/{unit}/store"
            store_payload = {
                'entries': [entry]  # Wrap single entry in array as expected by API
            }
            response = requests.post(store_url, json=store_payload, timeout=30)

            if response.status_code == 200:
                logging.info(f"✓ Stored entry: {entry['id']} in {unit}")
                self.entries_stored += 1
                return True
            else:
                logging.error(f"✗ Failed to store entry {entry['id']}: {response.status_code} - {response.text}")
                self.errors += 1
                return False

        except Exception as e:
            logging.error(f"✗ Error storing entry {entry.get('id', 'unknown')}: {e}")
            self.errors += 1
            return False

    def integrate_dataset(self):
        """Main integration process"""
        if not self.check_storage_facility():
            return False

        if not self.load_dataset():
            return False

        logging.info(f"Processing up to {self.max_entries} entries from OpenWebText dataset")

        batch_size = 100
        current_batch = []

        try:
            for entry in self.dataset:
                if self.entries_processed >= self.max_entries:
                    break

                processed_entry = self.process_entry(entry)
                if processed_entry:
                    current_batch.append(processed_entry)
                    self.entries_processed += 1

                    # Process batch
                    if len(current_batch) >= batch_size:
                        logging.info(f"Processing batch: entries {self.entries_processed - len(current_batch)} to {self.entries_processed - 1}")
                        for batch_entry in current_batch:
                            self.store_entry(batch_entry)
                        current_batch = []

                        # Progress update
                        success_rate = (self.entries_stored / self.entries_processed) * 100 if self.entries_processed > 0 else 0
                        logging.info(f"Progress: {self.entries_processed}/{self.max_entries} processed, {self.entries_stored} stored, {self.errors} errors ({success_rate:.1f}% success)")

            # Process remaining batch
            if current_batch:
                logging.info(f"Processing final batch: {len(current_batch)} entries")
                for batch_entry in current_batch:
                    self.store_entry(batch_entry)

        except Exception as e:
            logging.error(f"Error during integration: {e}")
            return False

        return True

    def run(self):
        """Run the complete integration process"""
        start_time = time.time()
        logging.info("Starting OpenWebText dataset integration")

        success = self.integrate_dataset()

        end_time = time.time()
        duration = end_time - start_time

        logging.info("=" * 50)
        logging.info("INTEGRATION COMPLETE")
        logging.info(f"Total entries processed: {self.entries_processed}")
        logging.info(f"Entries successfully stored: {self.entries_stored}")
        logging.info(f"Errors encountered: {self.errors}")
        success_rate = (self.entries_stored / self.entries_processed) * 100 if self.entries_processed > 0 else 0
        logging.info(f"Success rate: {success_rate:.1f}%")
        logging.info("=" * 50)
        logging.info(f"Integration completed in {duration:.2f} seconds")

        if success and self.entries_stored > 0:
            logging.info("OpenWebText dataset integration successful!")
            return True
        else:
            logging.error("OpenWebText dataset integration failed!")
            return False

if __name__ == "__main__":
    integrator = OpenWebTextIntegrator(max_entries=500)  # Start with 500 entries for testing
    success = integrator.run()
    sys.exit(0 if success else 1)