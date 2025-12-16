#!/bin/bash
echo "=== Checking for installed tools ==="
for tool in nmap wireshark nikto sqlmap hydra john hashcat aircrack-ng gobuster dirb masscan netdiscover theharvester curl wget netcat
do
    if which $tool &>/dev/null; then
        echo "✓ $tool - $(which $tool)"
    else
        echo "✗ $tool - not found"
    fi
done
