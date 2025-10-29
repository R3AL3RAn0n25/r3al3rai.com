param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

Write-Host "Diagnosing EC2 instance: $ServerIP"

# Check current directory structure and file locations
ssh -i $KeyPath ubuntu@$ServerIP @"
echo "=== Current directory ==="
pwd
ls -la

echo "=== Home directory ==="
ls -la /home/ubuntu/

echo "=== Opt directory ==="
ls -la /opt/ 2>/dev/null || echo "No /opt directory"

echo "=== Looking for R3ALER files ==="
find /home/ubuntu -name "*.py" -o -name "app.py" -o -name "application" -type d 2>/dev/null

echo "=== Running processes ==="
ps aux | grep -E "(python|flask|gunicorn)" | grep -v grep

echo "=== System services ==="
sudo systemctl status r3aler-ai 2>/dev/null || echo "No r3aler-ai service"

echo "=== Nginx status ==="
sudo systemctl status nginx 2>/dev/null || echo "No nginx service"
"@