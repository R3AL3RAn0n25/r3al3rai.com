#!/usr/bin/env python3
"""
explore_math_datasets.py - Explore and download math datasets from Hugging Face
for integration into R3ÆLƎR AI knowledge base
"""

import requests
import json
import os
from datasets import load_dataset
import pandas as pd
from typing import List, Dict, Any

class MathDatasetExplorer:
    """Explore and integrate math datasets from Hugging Face"""

    def __init__(self):
        self.math_datasets = [
            "gsm8k",  # Grade School Math 8K
            "aqua_rat",  # AQuA-RAT (Algebra Question Answering with Rationales)
            "openai/gsm8k",  # Alternative GSM8K
            "EleutherAI/mathqa",  # MathQA alternative
            "allenai/ai2_arc",  # AI2 Reasoning Challenge (has math)
            "lukaemon/bbh",  # Big Bench Hard (has math reasoning)
            "microsoft/orca-math-word-problems-200k",  # Math word problems
            "math-ai/AutoMathText",  # AutoMathText
            "hendrycks/competition_math",  # Competition Math
            "lighteval/MATH",  # MATH dataset
        ]

    def explore_datasets(self) -> List[Dict]:
        """Explore available math datasets"""
        print("🔍 Exploring Math Datasets from Hugging Face...")
        print("=" * 60)

        available_datasets = []

        for dataset_name in self.math_datasets:
            try:
                print(f"📚 Checking {dataset_name}...")

                # Try to load a small sample
                try:
                    dataset = load_dataset(dataset_name, split='train[:5]')
                    sample = dataset[0] if len(dataset) > 0 else {}

                    info = {
                        'name': dataset_name,
                        'available': True,
                        'size': len(dataset) if hasattr(dataset, '__len__') else 'unknown',
                        'sample_keys': list(sample.keys()) if sample else [],
                        'sample_data': sample
                    }

                    print(f"  ✅ Available - Size: {info['size']}, Keys: {info['sample_keys']}")
                    available_datasets.append(info)

                except Exception as e:
                    print(f"  ❌ Error loading: {str(e)[:100]}...")
                    available_datasets.append({
                        'name': dataset_name,
                        'available': False,
                        'error': str(e)
                    })

            except Exception as e:
                print(f"  ❌ Failed to check: {str(e)[:100]}...")
                available_datasets.append({
                    'name': dataset_name,
                    'available': False,
                    'error': str(e)
                })

        return available_datasets

    def download_and_format_dataset(self, dataset_name: str, limit: int = 1000) -> List[Dict]:
        """Download and format a math dataset for storage facility integration"""
        print(f"📥 Downloading {dataset_name} (limit: {limit})...")

        try:
            # Load dataset with proper config handling
            if dataset_name == "gsm8k":
                dataset = load_dataset(dataset_name, 'main', split=f'train[:{limit}]')
            else:
                dataset = load_dataset(dataset_name, split=f'train[:{limit}]')

            formatted_entries = []

            for i, item in enumerate(dataset):
                try:
                    # Format based on common math dataset structures
                    if dataset_name == "gsm8k":
                        entry = {
                            'id': f"gsm8k_{i}",
                            'topic': 'Grade School Mathematics',
                            'content': item.get('question', ''),
                            'answer': item.get('answer', ''),
                            'explanation': item.get('explanation', ''),
                            'category': 'arithmetic',
                            'subcategory': 'word_problems',
                            'level': 'elementary',
                            'source': 'GSM8K'
                        }

                    elif dataset_name == "aqua_rat":
                        # Get the correct answer from options
                        options = item.get('options', [])
                        correct_idx = item.get('correct', 0)
                        correct_answer = options[correct_idx] if isinstance(correct_idx, int) and correct_idx < len(options) else str(correct_idx)

                        entry = {
                            'id': f"aqua_rat_{i}",
                            'topic': 'Algebra and Reasoning',
                            'content': item.get('question', ''),
                            'answer': correct_answer,
                            'explanation': item.get('rationale', ''),
                            'category': 'algebra',
                            'subcategory': 'equation_solving',
                            'level': 'advanced',
                            'source': 'AQuA-RAT'
                        }

                    else:
                        # Generic format for other datasets
                        entry = {
                            'id': f"{dataset_name}_{i}",
                            'topic': 'Mathematics',
                            'content': str(item.get('question', item.get('problem', item))),
                            'answer': str(item.get('answer', item.get('solution', ''))),
                            'explanation': str(item.get('explanation', item.get('rationale', ''))),
                            'category': 'mathematics',
                            'subcategory': 'general',
                            'level': 'intermediate',
                            'source': dataset_name.upper()
                        }

                    formatted_entries.append(entry)

                except Exception as e:
                    print(f"  ⚠️ Error formatting entry {i}: {e}")
                    continue

            print(f"  ✅ Downloaded and formatted {len(formatted_entries)} entries")
            return formatted_entries

        except Exception as e:
            print(f"  ❌ Failed to download {dataset_name}: {e}")
            return []
            for i, item in enumerate(dataset):
                try:
                    # Format based on common math dataset structures
                    if dataset_name == "gsm8k":
                        entry = {
                            'id': f"gsm8k_{i}",
                            'topic': 'Grade School Mathematics',
                            'content': item.get('question', ''),
                            'answer': item.get('answer', ''),
                            'explanation': item.get('explanation', ''),
                            'category': 'arithmetic',
                            'subcategory': 'word_problems',
                            'level': 'elementary',
                            'source': 'GSM8K'
                        }

                    elif dataset_name == "math_qa":
                        entry = {
                            'id': f"math_qa_{i}",
                            'topic': item.get('Problem', ''),
                            'content': item.get('Problem', ''),
                            'answer': item.get('correct', ''),
                            'explanation': item.get('Rationale', ''),
                            'category': 'mathematics',
                            'subcategory': item.get('category', 'general'),
                            'level': 'intermediate',
                            'source': 'MathQA'
                        }

                    elif dataset_name == "aqua_rat":
                        entry = {
                            'id': f"aqua_rat_{i}",
                            'topic': 'Algebra and Reasoning',
                            'content': item.get('question', ''),
                            'answer': item.get('answer', ''),
                            'explanation': item.get('rationale', ''),
                            'category': 'algebra',
                            'subcategory': 'equation_solving',
                            'level': 'advanced',
                            'source': 'AQuA-RAT'
                        }

                    else:
                        # Generic format for other datasets
                        entry = {
                            'id': f"{dataset_name}_{i}",
                            'topic': 'Mathematics',
                            'content': str(item.get('question', item.get('problem', item))),
                            'answer': str(item.get('answer', item.get('solution', ''))),
                            'explanation': str(item.get('explanation', item.get('rationale', ''))),
                            'category': 'mathematics',
                            'subcategory': 'general',
                            'level': 'intermediate',
                            'source': dataset_name.upper()
                        }

                    formatted_entries.append(entry)

                except Exception as e:
                    print(f"  ⚠️ Error formatting entry {i}: {e}")
                    continue

            print(f"  ✅ Downloaded and formatted {len(formatted_entries)} entries")
            return formatted_entries

        except Exception as e:
            print(f"  ❌ Failed to download {dataset_name}: {e}")
            return []

def main():
    """Main function to explore and download math datasets"""
    print("🧮 R3ÆLƎR AI - Math Dataset Integration")
    print("=" * 50)

    explorer = MathDatasetExplorer()

    # Explore available datasets
    datasets = explorer.explore_datasets()

    print(f"\n📊 Summary: {len([d for d in datasets if d['available']])}/{len(datasets)} datasets available")

    # Download and format key datasets
    selected_datasets = ['gsm8k', 'aqua_rat', 'allenai/ai2_arc', 'microsoft/orca-math-word-problems-200k']

    all_math_data = []
    for dataset_name in selected_datasets:
        data = explorer.download_and_format_dataset(dataset_name, limit=500)
        all_math_data.extend(data)

    # Save to JSON for integration
    output_file = 'math_datasets_integrated.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_math_data, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Saved {len(all_math_data)} math entries to {output_file}")
    print("Ready for integration into storage facility!")

if __name__ == "__main__":
    main()