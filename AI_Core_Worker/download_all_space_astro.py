#!/usr/bin/env python3
"""
Download ALL astrophysics and space engineering datasets
Total: 1,602,748 entries!
"""

from datasets import load_dataset
import json
import os

def download_aerospace_corpus():
    """Download BAAI aerospace industry corpus - 1.6M entries!"""
    
    print("\n" + "="*80)
    print("📥 DOWNLOADING BAAI AEROSPACE CORPUS (1.6M+ entries)")
    print("="*80 + "\n")
    
    try:
        print("   Loading dataset (this may take several minutes)...")
        dataset = load_dataset("BAAI/IndustryCorpus2_aerospace", split="train", trust_remote_code=True)
        
        print(f"   ✅ Loaded {len(dataset):,} entries")
        
        # Sample first to see structure
        print("\n   Checking data structure...")
        sample = dataset[0]
        print(f"   Fields: {list(sample.keys())}")
        
        # Convert to list - process in batches to save memory
        print("\n   Processing entries...")
        data_list = []
        
        batch_size = 10000
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:min(i+batch_size, len(dataset))]
            for item in batch:
                data_list.append(dict(item))
            
            if (i + batch_size) % 100000 == 0:
                print(f"      Progress: {len(data_list):,}/{len(dataset):,}")
        
        print(f"\n   ✅ Processed {len(data_list):,} entries")
        
        # Save to JSON
        output_file = "aerospace_BAAI_corpus_raw.json"
        
        output_data = {
            "dataset_name": "BAAI/IndustryCorpus2_aerospace",
            "total_entries": len(data_list),
            "data": data_list
        }
        
        print(f"\n   💾 Saving to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"   ✅ Saved: {file_size_mb:.2f} MB")
        
        return len(data_list)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 0

def download_astronomy_textbook():
    """Download astronomy textbook Q&A - 678 entries"""
    
    print("\n" + "="*80)
    print("📥 DOWNLOADING ASTRONOMY TEXTBOOK Q&A")
    print("="*80 + "\n")
    
    try:
        print("   Loading dataset...")
        dataset = load_dataset("jeff-vincent/astronomy-textbook-qa-context", split="train", trust_remote_code=True)
        
        print(f"   ✅ Loaded {len(dataset):,} entries")
        
        # Convert to list
        data_list = []
        for i, item in enumerate(dataset):
            data_list.append(dict(item))
            if (i + 1) % 100 == 0:
                print(f"      Processing: {i + 1}/{len(dataset)}")
        
        # Save to JSON
        output_file = "astronomy_textbook_qa_raw.json"
        
        output_data = {
            "dataset_name": "jeff-vincent/astronomy-textbook-qa-context",
            "total_entries": len(data_list),
            "data": data_list
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"   💾 Saved: {output_file} ({file_size_mb:.2f} MB)")
        
        return len(data_list)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 0

def download_exoplanets():
    """Download exoplanets dataset - 50 entries"""
    
    print("\n" + "="*80)
    print("📥 DOWNLOADING EXOPLANETS DATA")
    print("="*80 + "\n")
    
    try:
        print("   Loading dataset...")
        dataset = load_dataset("dpv/exoplanets-sql", split="train", trust_remote_code=True)
        
        print(f"   ✅ Loaded {len(dataset):,} entries")
        
        # Convert to list
        data_list = [dict(item) for item in dataset]
        
        # Save to JSON
        output_file = "exoplanets_raw.json"
        
        output_data = {
            "dataset_name": "dpv/exoplanets-sql",
            "total_entries": len(data_list),
            "data": data_list
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"   💾 Saved: {output_file} ({file_size_mb:.2f} MB)")
        
        return len(data_list)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return 0

def main():
    print("\n" + "="*80)
    print("🚀 DOWNLOADING ALL ASTROPHYSICS & SPACE DATASETS")
    print("="*80)
    
    total_downloaded = 0
    
    # Download astronomy textbook first (smaller)
    count = download_astronomy_textbook()
    total_downloaded += count
    
    # Download exoplanets
    count = download_exoplanets()
    total_downloaded += count
    
    # Download massive aerospace corpus
    count = download_aerospace_corpus()
    total_downloaded += count
    
    print("\n" + "="*80)
    print("✅ DOWNLOAD COMPLETE!")
    print("="*80)
    print(f"\n🎉 TOTAL SPACE/ASTRO KNOWLEDGE: {total_downloaded:,} entries!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
