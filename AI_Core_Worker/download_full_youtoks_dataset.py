#!/usr/bin/env python3
"""
Download COMPLETE YouToks Quantum Physics II Dataset from HuggingFace
All 1,042 entries for maximum quantum physics knowledge!
"""

import requests
import json
import time

DATASET_NAME = "jilp00/YouToks-Instruct-Quantum-Physics-II"
CONFIG = "default"
SPLIT = "train"
BATCH_SIZE = 100
TOTAL_ENTRIES = 1042

def download_batch(offset, length):
    """Download a batch of entries from HuggingFace"""
    url = f"https://datasets-server.huggingface.co/rows"
    params = {
        "dataset": DATASET_NAME,
        "config": CONFIG,
        "split": SPLIT,
        "offset": offset,
        "length": length
    }
    
    print(f"📥 Downloading entries {offset} to {offset + length}...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def main():
    print("\n" + "="*70)
    print("📚 DOWNLOADING COMPLETE YOUTOKS QUANTUM PHYSICS II DATASET")
    print("="*70)
    print(f"Dataset: {DATASET_NAME}")
    print(f"Total entries to download: {TOTAL_ENTRIES}")
    print(f"Batch size: {BATCH_SIZE}")
    print("="*70 + "\n")
    
    all_rows = []
    features = None
    
    # Calculate number of batches needed
    num_batches = (TOTAL_ENTRIES + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_num in range(num_batches):
        offset = batch_num * BATCH_SIZE
        # Last batch might be smaller
        length = min(BATCH_SIZE, TOTAL_ENTRIES - offset)
        
        try:
            data = download_batch(offset, length)
            
            # Store features from first batch
            if features is None:
                features = data.get('features', [])
            
            # Add rows
            rows = data.get('rows', [])
            all_rows.extend(rows)
            
            print(f"   ✅ Batch {batch_num + 1}/{num_batches} complete ({len(rows)} entries)")
            print(f"   📊 Total downloaded so far: {len(all_rows)} entries\n")
            
            # Be nice to the API
            if batch_num < num_batches - 1:
                time.sleep(0.5)
                
        except Exception as e:
            print(f"   ❌ Error downloading batch {batch_num + 1}: {e}")
            print(f"   Continuing with {len(all_rows)} entries downloaded so far...\n")
            continue
    
    # Save complete dataset
    output_data = {
        "features": features,
        "rows": all_rows
    }
    
    output_file = "quantum_physics_youtoks_FULL_raw.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print("✅ DOWNLOAD COMPLETE!")
    print("="*70)
    print(f"Total entries downloaded: {len(all_rows)}")
    print(f"Output file: {output_file}")
    file_size_mb = len(json.dumps(output_data)) / (1024 * 1024)
    print(f"File size: {file_size_mb:.2f} MB")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
