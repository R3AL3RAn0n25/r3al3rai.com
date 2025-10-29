# R3ÆLƎR AI - Add SSL (HTTPS) Script
param(
    [Parameter(Mandatory=$true)]
    [string]$PublicIP,

    [Parameter(Mandatory=$true)]
    [string]$KeyPath,

    [Parameter(Mandatory=$true)]
    [string]$DomainName,

    [Parameter(Mandatory=$true)]
    [string]$Email
)

Write-Host "--- Adding SSL Certificate for $DomainName ---"

$RemoteSSLScript = @"
#!/bin/bash
set -e

echo "--- Installing Certbot for Let's Encrypt ---"
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx

echo "--- Stopping Nginx temporarily to obtain certificate ---"
sudo systemctl stop nginx

echo "--- Requesting SSL Certificate ---"
sudo certbot certonly --standalone -d $DomainName --non-interactive --agree-tos -m $Email

echo "--- Reconfiguring and Restarting Nginx for SSL ---"
sudo systemctl restart nginx

echo "--- SSL Setup Complete! Your site should be available at https://$DomainName ---"
"@

$CleanRemoteSSLScript = $RemoteSSLScript -replace "`r`n", "`n"

ssh -i $KeyPath ubuntu@$PublicIP $CleanRemoteSSLScript

Write-Host "SSL configuration finished."