"""
Test script for HuggingFace prompts integration
"""
import requests
import json

def test_hf_api():
    """Test HuggingFace datasets API access"""
    print("🔍 Testing HuggingFace Awesome ChatGPT Prompts API...\n")
    
    # Test 1: Get dataset rows
    print("1. Fetching dataset rows...")
    url = "https://datasets-server.huggingface.co/rows"
    params = {
        "dataset": "fka/awesome-chatgpt-prompts",
        "config": "default",
        "split": "train",
        "offset": 0,
        "length": 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "rows" in data:
            print(f"✅ Successfully fetched {len(data['rows'])} prompts\n")
            
            # Display first 3 prompts
            print("Sample prompts:")
            print("-" * 80)
            for i, row in enumerate(data["rows"][:3], 1):
                row_data = row.get("row", {})
                act = row_data.get("act", "Unknown")
                prompt = row_data.get("prompt", "")[:150]  # First 150 chars
                print(f"\n{i}. Role: {act}")
                print(f"   Prompt: {prompt}...")
            print("\n" + "-" * 80)
        else:
            print("❌ No rows found in response")
            
    except Exception as e:
        print(f"❌ Error fetching rows: {e}")
    
    # Test 2: Get splits info
    print("\n2. Fetching dataset splits info...")
    splits_url = "https://datasets-server.huggingface.co/splits"
    splits_params = {"dataset": "fka/awesome-chatgpt-prompts"}
    
    try:
        response = requests.get(splits_url, params=splits_params, timeout=10)
        response.raise_for_status()
        splits_data = response.json()
        
        print(f"✅ Dataset splits: {json.dumps(splits_data, indent=2)}\n")
        
    except Exception as e:
        print(f"❌ Error fetching splits: {e}")
    
    # Test 3: Get parquet files
    print("\n3. Checking parquet files...")
    parquet_url = "https://huggingface.co/api/datasets/fka/awesome-chatgpt-prompts/parquet/default/train"
    
    try:
        response = requests.get(parquet_url, timeout=10)
        response.raise_for_status()
        parquet_data = response.json()
        
        print(f"✅ Parquet files available: {len(parquet_data)} file(s)")
        if parquet_data:
            print(f"   First file: {parquet_data[0]}\n")
        
    except Exception as e:
        print(f"❌ Error fetching parquet info: {e}")

if __name__ == "__main__":
    test_hf_api()
    print("\n✨ HuggingFace API test complete!")
