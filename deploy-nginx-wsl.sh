#!/bin/bash

# R3ÆL3R AI - Nginx Configuration Deployment for WSL
# Run this script with: sudo bash deploy-nginx-wsl.sh

echo ""
echo "========================================"
echo "R3ÆL3R AI - Nginx Configuration Setup"
echo "========================================"
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Step 1: Creating SSL directory..."
mkdir -p /etc/ssl/r3al3rai
echo "✓ SSL directory created"

echo ""
echo "Step 2: Copying SSL certificates..."
cp "$SCRIPT_DIR/R3AL3R Production/ssl/r3al3rai.com.crt" /etc/ssl/r3al3rai/
cp "$SCRIPT_DIR/R3AL3R Production/ssl/r3al3rai.com.key" /etc/ssl/r3al3rai/
cp "$SCRIPT_DIR/R3AL3R Production/ssl/r3al3rai.com.chain.pem" /etc/ssl/r3al3rai/
echo "✓ Certificates copied"

echo ""
echo "Step 3: Setting certificate permissions..."
chmod 600 /etc/ssl/r3al3rai/r3al3rai.com.key
chmod 644 /etc/ssl/r3al3rai/r3al3rai.com.crt
chmod 644 /etc/ssl/r3al3rai/r3al3rai.com.chain.pem
echo "✓ Permissions set"

echo ""
echo "Step 4: Installing Nginx (if needed)..."
apt-get update -qq
apt-get install -y nginx
echo "✓ Nginx installed"

echo ""
echo "Step 5: Deploying Nginx configuration..."
cp "$SCRIPT_DIR/R3AL3R Production/nginx/r3al3rai.com.conf" /etc/nginx/sites-available/r3al3rai.com.conf
echo "✓ Configuration copied"

echo ""
echo "Step 6: Updating certificate paths in config..."
sed -i 's|/etc/ssl/certs/r3al3rai.com.crt|/etc/ssl/r3al3rai/r3al3rai.com.crt|g' /etc/nginx/sites-available/r3al3rai.com.conf
sed -i 's|/etc/ssl/private/r3al3rai.com.key|/etc/ssl/r3al3rai/r3al3rai.com.key|g' /etc/nginx/sites-available/r3al3rai.com.conf
sed -i 's|/etc/ssl/certs/r3al3rai.com.chain.pem|/etc/ssl/r3al3rai/r3al3rai.com.chain.pem|g' /etc/nginx/sites-available/r3al3rai.com.conf
echo "✓ Certificate paths updated"

echo ""
echo "Step 7: Enabling site..."
ln -sf /etc/nginx/sites-available/r3al3rai.com.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
echo "✓ Site enabled"

echo ""
echo "Step 8: Testing Nginx configuration..."
if nginx -t; then
    echo "✓ Nginx configuration is valid"
else
    echo "✗ Nginx configuration test failed"
    exit 1
fi

echo ""
echo "Step 9: Starting Nginx..."
systemctl enable nginx
systemctl restart nginx
echo "✓ Nginx restarted"

echo ""
echo "========================================"
echo "Nginx Configuration Complete!"
echo "========================================"
echo ""
echo "SSL Certificates installed:"
ls -lh /etc/ssl/r3al3rai/
echo ""
echo "Nginx Status:"
systemctl status nginx --no-pager | head -n 15
echo ""
echo "✓ R3ÆL3R AI is now accessible via HTTPS at:"
echo "  https://r3al3rai.com"
echo "  https://r3al3rai.com/rvn"
echo "  https://r3al3rai.com/bitxtractor"
echo "  https://r3al3rai.com/blackarchtools"
echo "  https://r3al3rai.com/manage"
echo ""
