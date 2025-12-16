#!/bin/bash
# Install all BlackArch tools

echo -e "\033[36mInstalling all BlackArch tools...\033[0m"

# Get list of all tools
tools_json=$(curl -s http://localhost:8081/api/tools)
tool_names=$(echo "$tools_json" | python3 -c "import sys, json; data=json.load(sys.stdin); print('\n'.join([t['name'] for t in data['tools']]))")

installed=0
failed=0
total=0

while IFS= read -r tool_name; do
    ((total++))
    echo -n "  Installing $tool_name..."
    
    result=$(curl -s -X POST "http://localhost:8081/api/install/$tool_name")
    status=$(echo "$result" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'error'))")
    
    if [ "$status" = "success" ]; then
        echo -e " \033[32m✓\033[0m"
        ((installed++))
    else
        message=$(echo "$result" | python3 -c "import sys, json; print(json.load(sys.stdin).get('message', 'Unknown error'))")
        echo -e " \033[31m✗ $message\033[0m"
        ((failed++))
    fi
    
    # Small delay to avoid overwhelming the server
    sleep 0.1
done <<< "$tool_names"

echo ""
echo -e "\033[36mInstallation Summary:\033[0m"
echo -e "  Total tools: $total"
echo -e "  \033[32mInstalled: $installed\033[0m"
echo -e "  \033[31mFailed: $failed\033[0m"
echo ""
echo -e "\033[32mAll tools are now ready for use!\033[0m"
