#!/usr/bin/env python3
"""
Check and download text-based astrophysics and space engineering datasets
Focus on knowledge, not images
"""

import requests
import json
import time

def check_dataset_accessibility(dataset_name):
    """Check if dataset is accessible and get info"""
    
    print(f"\n📥 Checking: {dataset_name}")
    
    url = "https://datasets-server.huggingface.co/info"
    params = {"dataset": dataset_name}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"   ❌ Cannot access")
            return None
        
        info = response.json()
        dataset_info = info.get('dataset_info', {})
        
        if not dataset_info:
            print(f"   ⚠️  No dataset info")
            return None
        
        config_name = list(dataset_info.keys())[0] if dataset_info else "default"
        splits = dataset_info.get(config_name, {}).get('splits', {})
        
        # Find largest split
        largest_split = None
        largest_size = 0
        
        for split_name, split_info in splits.items():
            num_examples = split_info.get('num_examples', 0)
            if num_examples > largest_size:
                largest_size = num_examples
                largest_split = split_name
        
        if not largest_split:
            print(f"   ❌ No valid splits")
            return None
        
        print(f"   ✅ Accessible: {largest_size:,} entries in '{largest_split}' split")
        
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
    print("🔍 CHECKING ASTROPHYSICS & SPACE ENGINEERING DATASETS")
    print("="*80)
    
    # Priority text-based datasets
    datasets_to_check = [
        "BAAI/IndustryCorpus2_aerospace",  # 1M-10M entries - aerospace industry
        "dpv/exoplanets-sql",  # Exoplanets data
        # Add more as we find them
    ]
    
    # Also search for more specific ones
    print("\n🔎 Searching for astronomy/astrophysics Q&A datasets...")
    
    search_terms = ["astronomy qa", "astrophysics questions", "space science"]
    
    for term in search_terms:
        try:
            url = "https://huggingface.co/api/datasets"
            params = {
                "search": term,
                "limit": 20,
                "sort": "downloads",
                "direction": -1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                datasets = response.json()
                
                for ds in datasets:
                    dataset_id = ds.get('id', '')
                    # Look for Q&A or text datasets
                    if any(k in dataset_id.lower() for k in ['qa', 'question', 'answer', 'knowledge', 'text']):
                        if dataset_id not in datasets_to_check:
                            datasets_to_check.append(dataset_id)
                            print(f"   Found: {dataset_id}")
        
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n" + "="*80)
    print(f"📊 Checking {len(datasets_to_check)} datasets...")
    print("="*80)
    
    valid_datasets = []
    
    for dataset in datasets_to_check:
        info = check_dataset_accessibility(dataset)
        if info:
            valid_datasets.append(info)
        time.sleep(0.5)
    
    print("\n" + "="*80)
    print(f"✅ FOUND {len(valid_datasets)} ACCESSIBLE TEXT DATASETS")
    print("="*80)
    
    for i, ds in enumerate(valid_datasets, 1):
        print(f"\n{i}. {ds['dataset']}")
        print(f"   Config: {ds['config']}")
        print(f"   Split: {ds['split']}")
        print(f"   Total entries: {ds['total_entries']:,}")
    
    # Save results
    with open('space_astro_datasets_available.json', 'w') as f:
        json.dump(valid_datasets, f, indent=2)
    
    print("\n" + "="*80)
    print("💾 Dataset info saved to: space_astro_datasets_available.json")
    print("="*80 + "\n")
    
    return valid_datasets

if __name__ == "__main__":
    datasets = main()
