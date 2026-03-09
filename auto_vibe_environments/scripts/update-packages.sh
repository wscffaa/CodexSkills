#!/bin/bash
# Auto NPM Update Script
# Checks for outdated npm packages and updates them if newer versions are available

# Default packages
npm outdated -g @anthropic-ai/claude-code 2>/dev/null | grep -q '@anthropic-ai/claude-code' && npm install -g @anthropic-ai/claude-code@latest --force
npm outdated -g @openai/codex 2>/dev/null | grep -q '@openai/codex' && npm install -g @openai/codex@latest --force
