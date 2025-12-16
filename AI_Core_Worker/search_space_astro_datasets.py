#!/usr/bin/env python3
"""
Search for ALL astrophysics and space engineering datasets on HuggingFace
"""

import requests
import json

def search_space_datasets():
    """Search HuggingFace for comprehensive astrophysics and space datasets"""
    
    print("\n" + "="*80)
    print("🔍 SEARCHING FOR ASTROPHYSICS & SPACE ENGINEERING DATASETS")
    print("="*80 + "\n")
    
    # Search queries for space-related topics
    search_terms = [
        "astrophysics",
        "astronomy",
        "cosmology",
        "space engineering",
        "aerospace",
        "planetary science",
        "solar system",
        "galaxies",
        "stars",
        "black holes",
        "exoplanets",
        "satellite",
        "spacecraft",
        "orbital mechanics",
        "rocket science"
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
                    
                    # Filter for relevant space/astro datasets
                    keywords = ['space', 'astro', 'planet', 'star', 'galaxy', 'cosmic', 
                               'satellite', 'orbit', 'rocket', 'aerospace', 'celestial',
                               'astronomy', 'cosmology', 'universe', 'solar']
                    
                    if any(keyword in dataset_id.lower() for keyword in keywords):
                        if dataset_id not in all_datasets:
                            all_datasets[dataset_id] = {
                                'downloads': downloads,
                                'likes': likes,
                                'tags': ds.get('tags', [])
                            }
                
                relevant_count = len([d for d in datasets if any(k in d.get('id', '').lower() 
                                     for k in keywords)])
                print(f"   Found {relevant_count} space-related datasets")
        
        except Exception as e:
            print(f"   ⚠️  Error searching '{term}': {e}")
            continue
    
    # Sort by downloads
    sorted_datasets = sorted(all_datasets.items(), key=lambda x: x[1]['downloads'], reverse=True)
    
    print("\n" + "="*80)
    print(f"📚 FOUND {len(sorted_datasets)} UNIQUE SPACE/ASTRO DATASETS")
    print("="*80)
    
    print("\n🏆 TOP 30 DATASETS BY POPULARITY:\n")
    for i, (dataset_id, info) in enumerate(sorted_datasets[:30], 1):
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
    
    with open('space_astro_datasets_catalog.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print("="*80)
    print(f"💾 Complete catalog saved to: space_astro_datasets_catalog.json")
    print("="*80 + "\n")
    
    return sorted_datasets

if __name__ == "__main__":
    datasets = search_space_datasets()
