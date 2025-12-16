#!/usr/bin/env python3
"""
Download remaining physics datasets using HuggingFace datasets library
This bypasses API rate limits
"""

from datasets import load_dataset
import json

def download_with_datasets_library(dataset_name, split='train', skip_images=False):
    """Download dataset using datasets library"""
    
    print(f"\n{'='*80}")
    print(f"📥 DOWNLOADING: {dataset_name}")
    print(f"{'='*80}\n")
    
    try:
        # Load dataset
        print(f"   Loading dataset...")
        dataset = load_dataset(dataset_name, split=split, trust_remote_code=True)
        
        print(f"   ✅ Loaded {len(dataset):,} entries")
        
        # Convert to list of dicts
        data_list = []
        for i, item in enumerate(dataset):
            # Skip image fields if requested
            if skip_images:
                item_dict = {k: v for k, v in item.items() if not (hasattr(v, 'mode') or 'image' in k.lower())}
            else:
                item_dict = dict(item)
            data_list.append(item_dict)
            if (i + 1) % 100 == 0:
                print(f"   Processing: {i + 1:,}/{len(dataset):,}")
        
        # Save to JSON
        safe_name = dataset_name.replace('/', '_').replace('-', '_')
        output_file = f"physics_{safe_name}_raw.json"
        
        output_data = {
            "dataset_name": dataset_name,
            "total_entries": len(data_list),
            "data": data_list
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        file_size_mb = len(json.dumps(output_data)) / (1024 * 1024)
        print(f"   💾 Saved: {output_file} ({file_size_mb:.2f} MB)")
        
        return len(data_list)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 0

def main():
    print("\n" + "="*80)
    print("🚀 DOWNLOADING REMAINING PHYSICS DATASETS")
    print("="*80)
    
    # Datasets that failed with API method (skip Vikhrmodels - it's images)
    remaining_datasets = [
        ("enesxgrahovac/the-feynman-lectures-on-physics", "train", False),
        ("burgerbee/physics_wiki", "train", False),
        ("Kratos-AI/physics-problems", "train", False),
        ("introvoyz041/physics", "test", False),  # This one uses 'test' split
    ]
    
    total_downloaded = 0
    
    for dataset_name, split, skip_images in remaining_datasets:
        count = download_with_datasets_library(dataset_name, split, skip_images)
        total_downloaded += count
    
    print("\n" + "="*80)
    print("✅ ADDITIONAL DOWNLOADS COMPLETE!")
    print(f"🎉 Downloaded {total_downloaded:,} more physics entries!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
