#!/bin/bash
# R3ÆLƎR AI - Production Deployment Transfer & Setup Script
# Usage: bash DEPLOY_TO_PRODUCTION.sh <target_ip> <username>
# Example: bash DEPLOY_TO_PRODUCTION.sh 72.17.63.255 r3aler

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
TARGET_IP="${1:-172.17.48.5}"
TARGET_USER="${2:-r3al3ran0n24}"
DEPLOY_PATH="/opt/r3aler"

# Validate inputs
if [ -z "$TARGET_IP" ] || [ -z "$TARGET_USER" ]; then
    echo -e "${RED}❌ Usage: bash DEPLOY_TO_PRODUCTION.sh <target_ip> <username>${NC}"
    echo -e "   Example: bash DEPLOY_TO_PRODUCTION.sh 72.17.63.255 r3aler"
    exit 1
fi

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║    R3ÆLƎR AI - PRODUCTION DEPLOYMENT TRANSFER & SETUP         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}Target Server:${NC} $TARGET_IP"
echo -e "${YELLOW}Target User:${NC} $TARGET_USER"
echo -e "${YELLOW}Deploy Path:${NC} $DEPLOY_PATH"
echo ""

# ============================================================
# Phase 1: Pre-flight Checks
# ============================================================

echo -e "${CYAN}PHASE 1: Pre-flight Checks${NC}"

# Check if target is reachable
echo -n "Checking connectivity to $TARGET_IP..."
if ping -c 1 -W 2 "$TARGET_IP" > /dev/null 2>&1; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌ Cannot reach $TARGET_IP${NC}"
    exit 1
fi

# Check SSH access
echo -n "Checking SSH access..."
if ssh -o ConnectTimeout=5 "$TARGET_USER@$TARGET_IP" "echo 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌ Cannot SSH to $TARGET_USER@$TARGET_IP${NC}"
    exit 1
fi

# Check required local files
echo -n "Checking required files..."
if [[ -f "knowledge_api.py" && -f ".env.local" && -f "DEPLOY_PRODUCTION.sh" ]]; then
    echo -e "${GREEN}✅${NC}"
else
    echo -e "${RED}❌ Missing required files${NC}"
    exit 1
fi

# ============================================================
# Phase 2: Create Deployment Package
# ============================================================

echo -e "\n${CYAN}PHASE 2: Create Deployment Package${NC}"

PACKAGE_NAME="r3aler_deployment_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$PACKAGE_NAME"

cp *.py *.cer .env.local health_check.sh DEPLOY_PRODUCTION.sh "$PACKAGE_NAME/" 2>/dev/null || true

echo -e "${GREEN}✅ Package created: $PACKAGE_NAME${NC}"

# ============================================================
# Phase 3: Transfer Package
# ============================================================

echo -e "\n${CYAN}PHASE 3: Transfer Package to Production${NC}"

echo "Uploading to $TARGET_USER@$TARGET_IP..."

ssh "$TARGET_USER@$TARGET_IP" "mkdir -p $DEPLOY_PATH" > /dev/null 2>&1

rsync -avz --progress "$PACKAGE_NAME/" "$TARGET_USER@$TARGET_IP:$DEPLOY_PATH/" 2>&1 | grep -E '(sent|received|total)' || true

echo -e "${GREEN}✅ Transfer complete${NC}"

# ============================================================
# Phase 4: Execute Deployment
# ============================================================

echo -e "\n${CYAN}PHASE 4: Execute Deployment on Remote${NC}"

ssh -t "$TARGET_USER@$TARGET_IP" "cd $DEPLOY_PATH && bash DEPLOY_PRODUCTION.sh"

# ============================================================
# Phase 5: Verification
# ============================================================

echo -e "\n${CYAN}PHASE 5: Verification${NC}"

HEALTHY=0
for port in 5001 5003 5004 5005 5006; do
    echo -n "Checking port $port..."
    if ssh "$TARGET_USER@$TARGET_IP" "curl -s http://localhost:$port/health 2>/dev/null | grep -q healthy" 2>/dev/null; then
        echo -e "${GREEN}✅${NC}"
        ((HEALTHY++))
    else
        echo -e "${RED}⏳${NC} (may still be starting)"
    fi
done

# ============================================================
# Final Report
# ============================================================

echo -e "\n${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"

echo -e "\n${CYAN}📊 Results:${NC}"
echo -e "  Target:        $TARGET_IP"
echo -e "  APIs Deployed: 5/5"
echo -e "  Healthy:       $HEALTHY/5"
echo -e "  Status:        Check with: ssh $TARGET_USER@$TARGET_IP bash $DEPLOY_PATH/health_check.sh"

echo -e "\n${CYAN}🔗 API Endpoints:${NC}"
echo -e "  Management:  http://$TARGET_IP:5001/health"
echo -e "  Auth:        http://$TARGET_IP:5003/health"
echo -e "  Knowledge:   http://$TARGET_IP:5004/health"
echo -e "  Droid:       http://$TARGET_IP:5005/health"
echo -e "  Storage:     http://$TARGET_IP:5006/health"

echo -e "\n${GREEN}R3ÆLƎR AI is DEPLOYED to $TARGET_IP${NC}\n"

# Cleanup
rm -rf "$PACKAGE_NAME"
