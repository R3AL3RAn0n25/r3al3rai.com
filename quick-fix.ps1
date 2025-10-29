param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    [Parameter(Mandatory=$true)]
    [string]$KeyPath
)

ssh -i $KeyPath ubuntu@$ServerIP @"
# Copy templates to correct location
sudo mkdir -p /opt/r3aler-ai/application/Backend/templates
sudo cp -r /opt/r3aler-ai/application/Frontend/templates/* /opt/r3aler-ai/application/Backend/templates/
sudo cp -r /opt/r3aler-ai/application/Frontend/static /opt/r3aler-ai/application/Backend/
sudo chown -R ubuntu:ubuntu /opt/r3aler-ai/application/Backend/

# Restart service
sudo systemctl restart r3aler-ai
sleep 3
sudo systemctl status r3aler-ai --no-pager -l

echo "Fixed! Try http://3.144.216.245 now"
"@