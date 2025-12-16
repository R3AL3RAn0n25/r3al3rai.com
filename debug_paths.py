from pathlib import Path
import sys

backend_path = Path("/tmp/app_3001.py").resolve()
print("Backend location:", backend_path)
print("Parent 1:", backend_path.parent)
print("Parent 2:", backend_path.parents[1] if len(backend_path.parents) > 1 else "N/A")
print("Parent 3:", backend_path.parents[2] if len(backend_path.parents) > 2 else "N/A")

tools_dir = backend_path.parents[2] / "Tools" / "tools" if len(backend_path.parents) > 2 else Path("/tmp/Tools/tools")
print("Tools dir would be:", tools_dir)
print("Tools dir exists:", tools_dir.exists())

wallet_path = tools_dir / "wallet_extractor.py"
print("Wallet extractor path:", wallet_path)
print("Wallet extractor exists:", wallet_path.exists())

# Check the actual workspace location
workspace_tools = Path("/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai/Tools/tools/wallet_extractor.py")
print("Actual wallet extractor exists:", workspace_tools.exists())