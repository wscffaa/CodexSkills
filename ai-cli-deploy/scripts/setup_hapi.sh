#!/bin/bash
set -e

CUSTOM_DOMAIN="$1"

if ! command -v npm &> /dev/null; then
  echo "Error: npm not found. Install Node.js first."
  exit 1
fi

# Check sudo access
if ! sudo -n true 2>/dev/null; then
  echo "Configuring passwordless sudo for npm..."
  echo "$USER ALL=(ALL) NOPASSWD: $(which npm)" | sudo tee /etc/sudoers.d/npm-nopasswd > /dev/null
  sudo chmod 440 /etc/sudoers.d/npm-nopasswd
fi

echo "Installing hapi..."
sudo npm i -g @twsxtd/hapi@latest

echo "Starting hapi..."
hapi runner start

if [ -n "$CUSTOM_DOMAIN" ]; then
  echo "Configuring custom domain: $CUSTOM_DOMAIN"
  echo "Run: cloudflared tunnel route dns hapi $CUSTOM_DOMAIN"
fi

echo "Hapi installed. Check status: hapi status"
