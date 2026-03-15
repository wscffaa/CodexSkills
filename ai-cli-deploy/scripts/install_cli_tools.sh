#!/bin/bash
set -e

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

echo "Installing Claude Code..."
sudo npm i -g @anthropic-ai/claude-code@latest

echo "Installing Codex..."
sudo npm i -g @openai/codex@latest

echo "Installing Gemini CLI..."
sudo npm i -g @google/gemini-cli@latest

echo "AI CLI tools installed successfully."
