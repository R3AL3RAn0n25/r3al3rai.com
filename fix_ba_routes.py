#!/usr/bin/env python3
"""Fix BlackArch route references in backendserver.js"""

import re

# Read the file
with open('application/Backend/backendserver.js', 'r') as f:
    content = f.read()

# Define the replacements for BlackArch routes
replacements = [
    # Status, tools, workflows, info endpoints
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/status', '${BLACKARCH_SERVICE_URL}/api/status'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/tools\}', '${BLACKARCH_SERVICE_URL}/api/tools}'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/tools/\$\{tool\}', '${BLACKARCH_SERVICE_URL}/api/tools/${tool}'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/tools/\$\{tool_name\}', '${BLACKARCH_SERVICE_URL}/api/tools/${tool_name}'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/workflows', '${BLACKARCH_SERVICE_URL}/api/workflows'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/workflows/run', '${BLACKARCH_SERVICE_URL}/api/workflows/run'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/info', '${BLACKARCH_SERVICE_URL}/api/info'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/categories', '${BLACKARCH_SERVICE_URL}/api/categories'),
    
    # Install and execute endpoints
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/install/\$\{tool\}', '${BLACKARCH_SERVICE_URL}/api/install/${tool}'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/install/\$\{tool_name\}', '${BLACKARCH_SERVICE_URL}/api/install/${tool_name}'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/execute/\$\{tool\}', '${BLACKARCH_SERVICE_URL}/api/execute/${tool}'),
    (r'\$\{PYTHON_BACKEND_URL\}/api/blackarch/execute/\$\{tool_name\}', '${BLACKARCH_SERVICE_URL}/api/execute/${tool_name}'),
]

# Apply replacements
original_content = content
for old_pattern, new_pattern in replacements:
    content = re.sub(old_pattern, new_pattern, content)

# Show what changed
if content != original_content:
    changes = sum(1 for old, new in replacements if old in original_content)
    print(f"✓ Made {changes} route corrections")
    
    # Write back
    with open('application/Backend/backendserver.js', 'w') as f:
        f.write(content)
    print("✓ Updated backendserver.js")
else:
    print("No changes needed - routes already correct")
