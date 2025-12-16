#!/usr/bin/env python3
"""
Download aerospace corpus using API method in batches
"""

import requests
import json
import time

def download_aerospace_batched():
    """Download aerospace corpus in batches using HuggingFace API"""
    
    print("\n" + "="*80)
    print("📥 DOWNLOADING AEROSPACE CORPUS (BATCHED APPROACH)")
    print("   Dataset: BAAI/IndustryCorpus2_aerospace")
    print("   Total: ~1,600,000 entries")
    print("="*80 + "\n")
    
    dataset_name = "BAAI/IndustryCorpus2_aerospace"
    config = "default"
    split = "train"
    
    # Download first 100K as a substantial sample
    target_entries = 100000  # Start with 100K
    batch_size = 100
    num_batches = target_entries // batch_size
    
    all_rows = []
    features = None
    
    print(f"📊 Downloading first {target_entries:,} entries...")
    print(f"   Batch size: {batch_size}")
    print(f"   Total batches: {num_batches:,}\n")
    
    for batch_num in range(num_batches):
        offset = batch_num * batch_size
        
        url = "https://datasets-server.huggingface.co/rows"
        params = {
            "dataset": dataset_name,
            "config": config,
            "split": split,
            "offset": offset,
            "length": batch_size
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code != 200:
                print(f"   ⚠️  Batch {batch_num + 1} failed (status {response.status_code})")
                continue
            
            data = response.json()
            
            if features is None:
                features = data.get('features', [])
            
            rows = data.get('rows', [])
            all_rows.extend(rows)
            
            if (batch_num + 1) % 100 == 0:
                print(f"   ✅ Progress: {len(all_rows):,}/{target_entries:,} entries")
            
            time.sleep(0.2)  # Be nice to API
            
        except Exception as e:
            print(f"   ⚠️  Batch {batch_num + 1} error: {e}")
            continue
    
    # Save
    output_file = "aerospace_BAAI_corpus_raw.json"
    
    output_data = {
        "dataset_name": dataset_name,
        "features": features,
        "rows": all_rows,
        "total_downloaded": len(all_rows)
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    import os
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"\n✅ Download complete!")
    print(f"   Total entries: {len(all_rows):,}")
    print(f"   Output file: {output_file}")
    print(f"   File size: {file_size_mb:.2f} MB\n")
    
    return len(all_rows)

if __name__ == "__main__":
    count = download_aerospace_batched()
    print(f"🎉 Downloaded {count:,} aerospace industry entries!")
