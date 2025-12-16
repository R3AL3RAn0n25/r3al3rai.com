#!/usr/bin/env python3
"""
Test script to find good knowledge datasets on Hugging Face
"""

from datasets import load_dataset
import sys

datasets_to_try = [
    'openwebtext',
    'scientific_papers',
    'c4',
    'bookcorpus',
    'wikitext',
    'ag_news',
    'imdb',
]

for dataset_name in datasets_to_try:
    try:
        print(f'\nTrying {dataset_name}...')
        dataset = load_dataset(dataset_name, split='train', streaming=True, trust_remote_code=True)
        sample = next(iter(dataset))
        print(f'✓ {dataset_name}: {type(sample)}')
        if isinstance(sample, dict):
            print(f'  Keys: {list(sample.keys())}')
            for key, value in sample.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f'  {key}: {value[:200]}...')
                    break
                elif isinstance(value, str):
                    print(f'  {key}: {value}')
        else:
            print(f'  Content: {str(sample)[:200]}...')
    except Exception as e:
        print(f'✗ {dataset_name}: {str(e)[:150]}...')