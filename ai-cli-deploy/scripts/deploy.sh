#!/bin/bash
set -e

show_help() {
  cat << EOF
Intranet Network Deploy - Complete deployment solution

Usage: $0 [OPTIONS]

Options:
  --skip-easytier      Skip EasyTier deployment
  --skip-mihomo        Skip mihomo TUN mode deployment
  --skip-cli-tools     Skip AI CLI tools installation
  --skip-hapi          Skip hapi installation
  --skip-cron          Skip auto-update cron setup
  --network-name <n>   EasyTier network name (default: default-network)
  --network-secret <s> EasyTier network secret (default: default-secret)
  --update-time <hrs>  Cron hours for auto-update (default: 0,12)
  --hapi-domain <url>  Custom domain for hapi
  --help               Show this help message

Examples:
  $0                                    # Full deployment (EasyTier + mihomo TUN + CLI tools)
  $0 --skip-hapi                        # Skip hapi
  $0 --network-name my-net --network-secret my-secret
  $0 --skip-mihomo                      # Skip mihomo (use remote proxy instead)
EOF
  exit 0
}

SKIP_EASYTIER=false
SKIP_MIHOMO=false
SKIP_CLI_TOOLS=false
SKIP_HAPI=false
SKIP_CRON=false
NETWORK_NAME="default-network"
NETWORK_SECRET="default-secret"
UPDATE_HOURS="0,12"
HAPI_DOMAIN=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --help) show_help ;;
    --skip-easytier) SKIP_EASYTIER=true; shift ;;
    --skip-mihomo) SKIP_MIHOMO=true; shift ;;
    --skip-cli-tools) SKIP_CLI_TOOLS=true; shift ;;
    --skip-hapi) SKIP_HAPI=true; shift ;;
    --skip-cron) SKIP_CRON=true; shift ;;
    --network-name) NETWORK_NAME="$2"; shift 2 ;;
    --network-secret) NETWORK_SECRET="$2"; shift 2 ;;
    --update-time) UPDATE_HOURS="$2"; shift 2 ;;
    --hapi-domain) HAPI_DOMAIN="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Intranet Network Deploy ==="

if [ "$SKIP_EASYTIER" = false ]; then
  echo "Step 1: Deploying EasyTier..."
  bash "$SCRIPT_DIR/deploy_easytier.sh" "$NETWORK_NAME" "$NETWORK_SECRET"
fi

if [ "$SKIP_MIHOMO" = false ]; then
  echo "Step 2: Deploying mihomo with TUN mode..."
  bash "$SCRIPT_DIR/deploy_mihomo_local.sh"
fi

if [ "$SKIP_CLI_TOOLS" = false ]; then
  echo "Step 3: Installing AI CLI tools..."
  bash "$SCRIPT_DIR/install_cli_tools.sh"
fi

if [ "$SKIP_HAPI" = false ]; then
  echo "Step 4: Installing hapi..."
  bash "$SCRIPT_DIR/setup_hapi.sh" "$HAPI_DOMAIN"
fi

if [ "$SKIP_CRON" = false ]; then
  echo "Step 5: Setting up auto-update cron..."
  bash "$SCRIPT_DIR/setup_cron.sh" "$UPDATE_HOURS"
fi

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Verification commands:"
echo "  easytier-cli peer                    # Check EasyTier peers"
echo "  easytier-cli route                   # Check routes"
echo "  ip addr show Meta                    # Check TUN interface"
echo "  docker logs mihomo | tail -20        # Check mihomo logs"
echo "  unset http_proxy https_proxy && curl -I https://www.google.com  # Test TUN mode"
echo "  claude-code --version                # Check Claude Code"
echo "  hapi status                          # Check hapi"
echo "  crontab -l                           # Check cron jobs"
