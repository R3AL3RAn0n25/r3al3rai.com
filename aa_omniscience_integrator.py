#!/usr/bin/env python3
"""
R3AL3R AI - WikiText Dataset Integration Script
Loads and integrates the WikiText dataset (Wikipedia articles) into the storage facility
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
import requests
from datasets import load_dataset
import psycopg2
from psycopg2.extras import execute_values

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wikitext_integration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class WikiTextIntegrator:
    """Integrates the WikiText dataset into the R3AL3R storage facility"""

    def __init__(self, storage_host='localhost', storage_port=3003):
        self.storage_host = storage_host
        self.storage_port = storage_port
        # Replace with a proper text knowledge dataset
        self.dataset_name = "wikitext"
        self.entries_processed = 0
        self.entries_stored = 0
        self.errors = 0

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
        """Load the WikiText dataset from Hugging Face"""
        try:
            logging.info(f"Loading dataset: {self.dataset_name}")
            # Load WikiText dataset which contains Wikipedia articles
            ds = load_dataset(self.dataset_name, 'wikitext-103-raw-v1')
            logging.info(f"Dataset loaded successfully. Splits: {list(ds.keys())}")

            # Get the train split
            dataset = ds['train']
            actual_length = len(dataset)
            logging.info(f"Using train split with {actual_length} entries")

            return dataset

        except Exception as e:
            logging.error(f"Failed to load dataset: {e}")
            return None

    def process_entry(self, entry):
        """Process a single dataset entry for storage"""
        try:
            # Extract relevant fields from WikiText entry
            # WikiText contains 'text' field with Wikipedia article text
            entry_data = {
                'id': f"wikitext_{self.entries_processed:06d}",
                'content': entry.get('text', '').strip(),
                'title': f"Wikipedia Article Sample {self.entries_processed}",
                'category': 'wikipedia_knowledge',
                'source': 'WikiText Dataset (Wikipedia articles)',
                'metadata': {
                    'dataset': self.dataset_name,
                    'entry_type': 'wikipedia_article',
                    'content_length': len(entry.get('text', '')),
                    'timestamp': datetime.now().isoformat(),
                    'processed_by': 'WikiText_Integrator'
                }
            }

            # Clean and validate content
            if not entry_data['content'] or len(entry_data['content'].strip()) < 100:
                return None  # Skip empty or too short entries

            return entry_data

        except Exception as e:
            logging.warning(f"Error processing entry: {e}")
            return None

    def store_entry(self, entry_data):
        """Store entry in the storage facility"""
        try:
            # Determine which unit to store in based on category
            unit_mapping = {
                'physics': 'physics',
                'quantum': 'quantum',
                'mathematics': 'quantum',
                'computer_science': 'quantum',
                'biology': 'physics',
                'chemistry': 'physics',
                'space': 'space',
                'astronomy': 'space',
                'cryptography': 'crypto',
                'security': 'blackarch',
                'programming': 'quantum',
                'ai': 'quantum',
                'machine_learning': 'quantum',
                'wikipedia_knowledge': 'users'  # General knowledge goes to users unit
            }

            category = entry_data['category'].lower()
            unit = 'user_unit'  # Default unit

            for key, mapped_unit in unit_mapping.items():
                if key in category:
                    unit = mapped_unit
                    break

            # Store in the appropriate unit
            store_url = f"{self.storage_url}/api/unit/{unit}/store"

            # API expects entries array
            store_payload = {
                'entries': [entry_data]
            }

            response = requests.post(store_url, json=store_payload, timeout=30)

            if response.status_code == 200:
                self.entries_stored += 1
                if self.entries_stored % 100 == 0:
                    logging.info(f"Stored {self.entries_stored} entries so far")
                return True
            else:
                logging.warning(f"Failed to store entry: {response.status_code} - {response.text}")
                self.errors += 1
                return False

        except Exception as e:
            logging.error(f"Error storing entry: {e}")
            self.errors += 1
            return False

    def integrate_dataset(self, batch_size=100):
        """Main integration function"""
        logging.info("Starting AA-Omniscience dataset integration")

        # Check storage facility
        if not self.check_storage_facility():
            logging.error("Storage facility not available. Aborting integration.")
            return False

        # Load dataset
        dataset = self.load_dataset()
        if dataset is None:
            return False

        # Process entries in batches
        total_entries = len(dataset)
        logging.info(f"Processing {total_entries} entries in batches of {batch_size}")

        for i in range(0, total_entries, batch_size):
            batch_end = min(i + batch_size, total_entries)
            batch = dataset[i:batch_end]

            logging.info(f"Processing batch {i//batch_size + 1}: entries {i} to {batch_end-1}")

            for entry in batch:
                self.entries_processed += 1

                # Process entry
                processed_entry = self.process_entry(entry)
                if processed_entry:
                    # Store entry
                    self.store_entry(processed_entry)

                # Progress update
                if self.entries_processed % 500 == 0:
                    progress = (self.entries_processed / total_entries) * 100
                    logging.info(f"Progress: {self.entries_processed}/{total_entries} ({progress:.1f}%)")

        # Final summary
        logging.info("=" * 50)
        logging.info("INTEGRATION COMPLETE")
        logging.info(f"Total entries processed: {self.entries_processed}")
        logging.info(f"Entries successfully stored: {self.entries_stored}")
        logging.info(f"Errors encountered: {self.errors}")
        logging.info(f"Success rate: {(self.entries_stored/self.entries_processed)*100:.1f}%" if self.entries_processed > 0 else "0%")
        logging.info("=" * 50)

        return True

def main():
    """Main execution function"""
    integrator = WikiTextIntegrator()

    start_time = time.time()
    success = integrator.integrate_dataset()
    end_time = time.time()

    duration = end_time - start_time
    logging.info(f"Integration completed in {duration:.2f} seconds")

    if success:
        logging.info("WikiText dataset integration successful!")
        sys.exit(0)
    else:
        logging.error("WikiText dataset integration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()