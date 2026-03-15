#!/bin/bash

echo "=== Testing Intranet Network Connectivity ==="
echo ""

# Test 1: EasyTier
echo "1. EasyTier Status:"
if command -v easytier-cli &> /dev/null; then
  echo "   Peers:"
  easytier-cli peer 2>/dev/null || echo "   ✗ EasyTier not running or no peers"
  echo "   Routes:"
  easytier-cli route 2>/dev/null || echo "   ✗ No routes configured"
else
  echo "   ✗ easytier-cli not found"
fi
echo ""

# Test 2: Mihomo TUN Mode
echo "2. Mihomo TUN Mode:"
if docker ps --format '{{.Names}}' | grep -q '^mihomo$'; then
  echo "   ✓ Mihomo container running"

  if ip addr show Meta &>/dev/null; then
    echo "   ✓ TUN interface 'Meta' is up"
    ip addr show Meta | grep -E "inet " | head -1
  else
    echo "   ✗ TUN interface 'Meta' not found"
  fi

  if ss -tulnp 2>/dev/null | grep -q ':1053'; then
    echo "   ✓ DNS hijacking active (port 1053)"
  else
    echo "   ✗ DNS hijacking not active"
  fi
else
  echo "   ✗ Mihomo container not running"
fi
echo ""

# Test 3: Transparent Proxying (without proxy env vars)
echo "3. Transparent Proxying Test:"
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY

if curl -s -I --connect-timeout 5 https://www.google.com | head -1 | grep -q "200"; then
  echo "   ✓ Google accessible (transparent proxying works)"
else
  echo "   ✗ Google not accessible"
fi

if curl -s -I --connect-timeout 5 https://github.com | head -1 | grep -q "200"; then
  echo "   ✓ GitHub accessible"
else
  echo "   ✗ GitHub not accessible"
fi
echo ""

# Test 4: AI CLI Tools
echo "4. AI CLI Tools:"
for tool in claude-code codex gemini-cli; do
  if command -v $tool &> /dev/null; then
    version=$($tool --version 2>/dev/null | head -1)
    echo "   ✓ $tool: $version"
  else
    echo "   ✗ $tool not installed"
  fi
done
echo ""

# Test 5: Hapi
echo "5. Hapi Status:"
if command -v hapi &> /dev/null; then
  hapi status 2>/dev/null || echo "   ✗ Hapi not running"
else
  echo "   ✗ Hapi not installed"
fi
echo ""

# Test 6: Auto-start Configuration
echo "6. Auto-start Configuration:"
if docker inspect easytier --format='{{.HostConfig.RestartPolicy.Name}}' 2>/dev/null | grep -q "unless-stopped"; then
  echo "   ✓ EasyTier restart policy: unless-stopped"
else
  echo "   ✗ EasyTier restart policy not configured"
fi

if docker inspect mihomo --format='{{.HostConfig.RestartPolicy.Name}}' 2>/dev/null | grep -q "unless-stopped"; then
  echo "   ✓ Mihomo restart policy: unless-stopped"
else
  echo "   ✗ Mihomo restart policy not configured"
fi

if crontab -l 2>/dev/null | grep -q "claude-code\|codex\|gemini"; then
  echo "   ✓ AI CLI tools auto-update cron configured"
else
  echo "   ✗ AI CLI tools auto-update cron not configured"
fi
echo ""

echo "=== Test Complete ==="
