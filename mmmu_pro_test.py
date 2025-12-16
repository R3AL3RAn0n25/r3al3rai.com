#!/usr/bin/env python3
"""
MMMU Pro Benchmark Test for R3ÆLƎR AI
Tests the multimodal understanding capabilities using MMMU Pro dataset
"""

import sys
import os
from datasets import load_dataset

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from ai_benchmarks import AIBenchmarks

def run_mmmu_pro_benchmarks():
    """Run all MMMU Pro benchmarks"""
    print("🎯 Running MMMU Pro Benchmarks for R3ÆLƎR AI")
    print("=" * 60)

    benchmarks = AIBenchmarks()

    # Run only MMMU Pro benchmarks
    mmmu_benchmarks = [
        ("MMMU_Pro_Vision", benchmarks.mmmu_pro_vision_benchmark),
        ("MMMU_Pro_Standard_4", benchmarks.mmmu_pro_standard_4_benchmark),
        ("MMMU_Pro_Standard_10", benchmarks.mmmu_pro_standard_10_benchmark)
    ]

    results = {}
    for benchmark_name, benchmark_func in mmmu_benchmarks:
        print(f"\n🧪 Running {benchmark_name}...")
        try:
            result = benchmark_func()
            results[benchmark_name] = result
            if "error" not in result:
                print(f"✅ {benchmark_name}: {result['score']:.1f}% ({result['correct']}/{result['total']})")
            else:
                print(f"❌ {benchmark_name} failed: {result['error']}")
        except Exception as e:
            print(f"❌ {benchmark_name} failed: {e}")
            results[benchmark_name] = {"error": str(e)}

    # Print summary
    print("\n🏆 MMMU PRO BENCHMARK RESULTS:")
    print("-" * 40)
    for name, result in results.items():
        if "error" not in result:
            print(f"{name:25} {result['score']:5.1f}% ({result['correct']}/{result['total']})")
        else:
            print(f"{name:25} ERROR: {result['error']}")

    return results

def test_dataset_loading():
    """Test loading the MMMU Pro datasets"""
    print("🔍 Testing MMMU Pro Dataset Loading...")
    print("-" * 40)

    datasets_to_test = [
        ("vision", "MMMU/MMMU_Pro"),
        ("standard (4 options)", "MMMU/MMMU_Pro"),
        ("standard (10 options)", "MMMU/MMMU_Pro")
    ]

    for config, dataset_name in datasets_to_test:
        try:
            print(f"Loading {dataset_name} - {config}...")
            dataset = load_dataset(dataset_name, config, split="test")
            print(f"✅ Successfully loaded {len(dataset)} samples")
            # Show a sample
            if len(dataset) > 0:
                sample = dataset[0]
                print(f"   Sample question: {sample['question'][:100]}...")
                print(f"   Options: {len(sample.get('options', []))} options")
        except Exception as e:
            print(f"❌ Failed to load {config}: {e}")

if __name__ == "__main__":
    # Test dataset loading first
    test_dataset_loading()
    print()

    # Run the benchmarks
    run_mmmu_pro_benchmarks()