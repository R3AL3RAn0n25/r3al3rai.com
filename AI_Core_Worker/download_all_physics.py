#!/usr/bin/env python3
"""
Download ALL physics datasets for R3ALER AI
Total: 43,727 physics entries!
"""

import requests
import json
import time

def download_dataset(dataset_name, config, split, total_entries):
    """Download complete dataset in batches"""
    
    print(f"\n{'='*80}")
    print(f"📥 DOWNLOADING: {dataset_name}")
    print(f"   Total entries: {total_entries:,}")
    print(f"{'='*80}\n")
    
    all_rows = []
    features = None
    batch_size = 100
    num_batches = (total_entries + batch_size - 1) // batch_size
    
    for batch_num in range(num_batches):
        offset = batch_num * batch_size
        length = min(batch_size, total_entries - offset)
        
        url = "https://datasets-server.huggingface.co/rows"
        params = {
            "dataset": dataset_name,
            "config": config,
            "split": split,
            "offset": offset,
            "length": length
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code != 200:
                print(f"   ❌ Batch {batch_num + 1}/{num_batches} failed")
                continue
            
            data = response.json()
            
            if features is None:
                features = data.get('features', [])
            
            rows = data.get('rows', [])
            all_rows.extend(rows)
            
            if (batch_num + 1) % 10 == 0 or batch_num == num_batches - 1:
                print(f"   ✅ Progress: {len(all_rows):,}/{total_entries:,} entries")
            
            time.sleep(0.3)  # Be nice to API
            
        except Exception as e:
            print(f"   ⚠️  Batch {batch_num + 1} error: {e}")
            continue
    
    return {
        "dataset_name": dataset_name,
        "features": features,
        "rows": all_rows,
        "total_downloaded": len(all_rows)
    }

def main():
    print("\n" + "="*80)
    print("🚀 DOWNLOADING ALL PHYSICS DATASETS FOR R3ALER AI")
    print("="*80)
    
    # Load dataset info
    with open('physics_datasets_available.json', 'r') as f:
        datasets = json.load(f)
    
    print(f"\n📊 Total datasets to download: {len(datasets)}")
    total_entries = sum(ds['total_entries'] for ds in datasets)
    print(f"📚 Total physics entries: {total_entries:,}\n")
    
    all_datasets = []
    
    for ds_info in datasets:
        result = download_dataset(
            ds_info['dataset'],
            ds_info['config'],
            ds_info['split'],
            ds_info['total_entries']
        )
        
        all_datasets.append(result)
        
        # Save individual dataset
        safe_name = ds_info['dataset'].replace('/', '_').replace('-', '_')
        output_file = f"physics_{safe_name}_raw.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        file_size_mb = len(json.dumps(result)) / (1024 * 1024)
        print(f"   💾 Saved: {output_file} ({file_size_mb:.2f} MB)")
    
    # Summary
    print("\n" + "="*80)
    print("✅ DOWNLOAD COMPLETE!")
    print("="*80)
    
    total_downloaded = sum(ds['total_downloaded'] for ds in all_datasets)
    
    print(f"\n📊 SUMMARY:")
    for ds in all_datasets:
        print(f"   ✅ {ds['dataset_name']}: {ds['total_downloaded']:,} entries")
    
    print(f"\n🎉 TOTAL PHYSICS KNOWLEDGE: {total_downloaded:,} entries!")
    print("="*80 + "\n")
    
    # Save summary
    summary = {
        'total_datasets': len(all_datasets),
        'total_entries': total_downloaded,
        'datasets': [
            {
                'name': ds['dataset_name'],
                'entries': ds['total_downloaded']
            }
            for ds in all_datasets
        ]
    }
    
    with open('physics_download_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
