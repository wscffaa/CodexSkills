#!/bin/bash
set -e

echo "Deploying mihomo with TUN mode (transparent proxying)..."

# Check if config exists
if [ ! -f ~/.config/mihomo/config.yaml ]; then
  echo "✗ Config file not found at ~/.config/mihomo/config.yaml"
  echo "Creating config directory and copying template..."
  mkdir -p ~/.config/mihomo

  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  TEMPLATE_PATH="$SCRIPT_DIR/../assets/mihomo/config.yaml.template"

  if [ -f "$TEMPLATE_PATH" ]; then
    cp "$TEMPLATE_PATH" ~/.config/mihomo/config.yaml
    echo "✓ Template copied to ~/.config/mihomo/config.yaml"
    echo "⚠ IMPORTANT: Edit ~/.config/mihomo/config.yaml and replace YOUR_SUBSCRIPTION_URL_HERE with your actual proxy subscription"
    exit 1
  else
    echo "✗ Template not found at $TEMPLATE_PATH"
    exit 1
  fi
fi

# Stop existing container if running
if docker ps -a --format '{{.Names}}' | grep -q '^mihomo$'; then
  echo "Stopping existing mihomo container..."
  docker stop mihomo 2>/dev/null || true
  docker rm mihomo 2>/dev/null || true
fi

# Deploy mihomo container with TUN mode capabilities
docker run -d \
  --name mihomo \
  --restart unless-stopped \
  --cap-add=NET_ADMIN \
  --device=/dev/net/tun \
  --network host \
  -v ~/.config/mihomo:/root/.config/mihomo \
  metacubex/mihomo:latest

echo ""
echo "✓ Mihomo deployed with TUN mode"
echo ""
echo "Verifying TUN interface..."
sleep 3

if ip addr show Meta &>/dev/null; then
  echo "✓ TUN interface 'Meta' is up"
  ip addr show Meta | grep -E "inet |UP"
else
  echo "✗ TUN interface not found. Check Docker logs:"
  echo "  docker logs mihomo"
fi

echo ""
echo "Services:"
echo "  - HTTP Proxy: http://127.0.0.1:7890"
echo "  - SOCKS5 Proxy: socks5://127.0.0.1:7891"
echo "  - Dashboard: http://127.0.0.1:9090"
echo "  - DNS: 127.0.0.1:1053"
echo ""
echo "Test transparent proxying (no proxy env vars needed):"
echo "  unset http_proxy https_proxy"
echo "  curl -I https://www.google.com"
echo ""
echo "Monitor traffic:"
echo "  docker logs -f mihomo"
