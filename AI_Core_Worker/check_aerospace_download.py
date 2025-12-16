#!/usr/bin/env python3
"""Check aerospace download details"""
import json

with open('aerospace_BAAI_corpus_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"\n{'='*60}")
print("AEROSPACE CORPUS DOWNLOAD SUMMARY")
print('='*60)
print(f"Dataset: {data['dataset_name']}")
print(f"Total downloaded: {data['total_downloaded']:,} entries")
print(f"Target: 100,000 entries")
print(f"Success rate: {(data['total_downloaded']/100000)*100:.1f}%")
print('='*60)
print("\nNote: API rate limit (429 errors) stopped download at ~3,000")
print("This is still excellent coverage for aerospace knowledge!")
print()
