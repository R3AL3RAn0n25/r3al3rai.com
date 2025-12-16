#!/usr/bin/env python3
"""
Check dataset sizes and download the largest physics datasets
Priority: camel-ai/physics (10K-100K), marianna13/physics-stackexchange (10K-100K)
"""

import requests
import json
import time

def check_dataset_size(dataset_name, config="default", split="train"):
    """Check the actual size of a dataset"""
    url = "https://datasets-server.huggingface.co/size"
    params = {
        "dataset": dataset_name
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data
    except Exception as e:
        print(f"   ⚠️  Error checking size: {e}")
    
    return None

def download_large_dataset(dataset_name, max_entries=None):
    """Download a large dataset in batches"""
    
    print(f"\n📥 Checking dataset: {dataset_name}")
    
    # First, get dataset info
    url = "https://datasets-server.huggingface.co/info"
    params = {"dataset": dataset_name}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"   ❌ Cannot access dataset info")
            return None
        
        info = response.json()
        print(f"   ✅ Dataset accessible")
        
        # Get available configs and splits
        dataset_info = info.get('dataset_info', {})
        
        if not dataset_info:
            print(f"   ⚠️  No dataset info available")
            return None
        
        # Try to find the best config
        config_name = list(dataset_info.keys())[0] if dataset_info else "default"
        splits = dataset_info.get(config_name, {}).get('splits', {})
        
        print(f"   Config: {config_name}")
        print(f"   Available splits: {list(splits.keys())}")
        
        # Find the largest split
        largest_split = None
        largest_size = 0
        
        for split_name, split_info in splits.items():
            num_examples = split_info.get('num_examples', 0)
            if num_examples > largest_size:
                largest_size = num_examples
                largest_split = split_name
        
        if not largest_split:
            print(f"   ❌ No valid splits found")
            return None
        
        print(f"   Largest split: {largest_split} ({largest_size:,} entries)")
        
        # Download the data
        if max_entries and largest_size > max_entries:
            print(f"   📊 Limiting to {max_entries:,} entries")
            largest_size = max_entries
        
        return {
            'dataset': dataset_name,
            'config': config_name,
            'split': largest_split,
            'total_entries': largest_size
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    print("\n" + "="*80)
    print("🔍 CHECKING TOP PHYSICS DATASETS")
    print("="*80)
    
    # Priority datasets to check
    datasets_to_check = [
        "camel-ai/physics",  # 10K-100K entries
        "marianna13/physics-stackexchange",  # 10K-100K entries
        "enesxgrahovac/the-feynman-lectures-on-physics",  # Feynman lectures!
        "burgerbee/physics_wiki",  # 1K-10K
        "Vikhrmodels/physics_big",  # 1K-10K
        "Kratos-AI/physics-problems",  # <1K but high quality
        "introvoyz041/physics",  # 1K-10K
    ]
    
    valid_datasets = []
    
    for dataset in datasets_to_check:
        info = download_large_dataset(dataset)
        if info:
            valid_datasets.append(info)
        time.sleep(0.5)  # Be nice to the API
    
    print("\n" + "="*80)
    print(f"✅ FOUND {len(valid_datasets)} ACCESSIBLE DATASETS")
    print("="*80)
    
    for i, ds in enumerate(valid_datasets, 1):
        print(f"\n{i}. {ds['dataset']}")
        print(f"   Config: {ds['config']}")
        print(f"   Split: {ds['split']}")
        print(f"   Total entries: {ds['total_entries']:,}")
    
    # Save results
    with open('physics_datasets_available.json', 'w') as f:
        json.dump(valid_datasets, f, indent=2)
    
    print("\n" + "="*80)
    print("💾 Dataset info saved to: physics_datasets_available.json")
    print("="*80 + "\n")
    
    return valid_datasets

if __name__ == "__main__":
    datasets = main()
