import os
import sys

if __name__ == "__main__":
    keyword = sys.argv[sys.argv.index("--keyword")+1] if "--keyword" in sys.argv else "r3al3erai"
    print(f"Training wake word → {keyword}")
    # In a real setup this would record 10 samples and retrain the CNN
    # For now just fake it
    open("current_wake.txt", "w").write(keyword)
    print("Wake word updated (simulated). Restart r3al3erai.py")