#!/usr/bin/env python3
"""
Search for ALL available physics datasets on HuggingFace
Find the largest and best physics knowledge collections
"""

import requests
import json

def search_physics_datasets():
    """Search HuggingFace for comprehensive physics datasets"""
    
    print("\n" + "="*80)
    print("🔍 SEARCHING FOR ALL PHYSICS DATASETS ON HUGGINGFACE")
    print("="*80 + "\n")
    
    # Search queries for different physics topics
    search_terms = [
        "physics",
        "quantum physics",
        "theoretical physics",
        "particle physics",
        "astrophysics",
        "classical mechanics",
        "electromagnetism",
        "thermodynamics",
        "relativity",
        "nuclear physics"
    ]
    
    all_datasets = {}
    
    for term in search_terms:
        print(f"🔎 Searching for: {term}...")
        
        try:
            url = "https://huggingface.co/api/datasets"
            params = {
                "search": term,
                "limit": 50,
                "sort": "downloads",
                "direction": -1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                datasets = response.json()
                
                for ds in datasets:
                    dataset_id = ds.get('id', '')
                    downloads = ds.get('downloads', 0)
                    likes = ds.get('likes', 0)
                    
                    # Filter for relevant physics datasets
                    if any(keyword in dataset_id.lower() for keyword in ['physics', 'quantum', 'science', 'stem']):
                        if dataset_id not in all_datasets:
                            all_datasets[dataset_id] = {
                                'downloads': downloads,
                                'likes': likes,
                                'tags': ds.get('tags', [])
                            }
                
                print(f"   Found {len([d for d in datasets if any(k in d.get('id', '').lower() for k in ['physics', 'quantum', 'science'])])} physics-related datasets")
        
        except Exception as e:
            print(f"   ⚠️  Error searching '{term}': {e}")
            continue
    
    # Sort by downloads
    sorted_datasets = sorted(all_datasets.items(), key=lambda x: x[1]['downloads'], reverse=True)
    
    print("\n" + "="*80)
    print(f"📚 FOUND {len(sorted_datasets)} UNIQUE PHYSICS DATASETS")
    print("="*80)
    
    print("\n🏆 TOP 20 PHYSICS DATASETS BY POPULARITY:\n")
    for i, (dataset_id, info) in enumerate(sorted_datasets[:20], 1):
        print(f"{i:2}. {dataset_id}")
        print(f"    Downloads: {info['downloads']:,} | Likes: {info['likes']}")
        if info['tags']:
            print(f"    Tags: {', '.join(info['tags'][:5])}")
        print()
    
    # Save complete list
    output = {
        'total_found': len(sorted_datasets),
        'datasets': [
            {
                'id': ds_id,
                'downloads': info['downloads'],
                'likes': info['likes'],
                'tags': info['tags']
            }
            for ds_id, info in sorted_datasets
        ]
    }
    
    with open('physics_datasets_catalog.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print("="*80)
    print(f"💾 Complete catalog saved to: physics_datasets_catalog.json")
    print("="*80 + "\n")
    
    return sorted_datasets

if __name__ == "__main__":
    datasets = search_physics_datasets()
