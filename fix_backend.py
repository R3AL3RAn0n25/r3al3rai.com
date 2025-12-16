#!/usr/bin/env python3
import re

# Read the original file
with open('/tmp/app_3001.py', 'r') as f:
    content = f.read()

# Fix the _tools_dir function
fixed_content = content.replace(
    'def _tools_dir() -> Path:\n    return (Path(__file__).resolve().parents[2] / \'Tools\' / \'tools\').resolve()',
    'def _tools_dir() -> Path:\n    return Path(\"/mnt/c/Users/work8/OneDrive/Desktop/r3al3rai/New Folder 1/R3al3r-AI Main Working/R3aler-ai/R3aler-ai/Tools/tools\").resolve()'
)

# Write the fixed file
with open('/tmp/app_3001_fixed.py', 'w') as f:
    f.write(fixed_content)

print("Backend path fixed!")