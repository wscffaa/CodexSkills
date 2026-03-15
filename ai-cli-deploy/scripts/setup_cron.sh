#!/bin/bash
set -e

UPDATE_HOURS="${1:-0,12}"

CRON_CMD="sudo npm i -g @anthropic-ai/claude-code@latest && sudo npm i -g @openai/codex@latest && sudo npm i -g @google/gemini-cli@latest >> /tmp/cli-update.log 2>&1"

(crontab -l 2>/dev/null | grep -v 'claude-code@latest\|codex@latest\|gemini-cli@latest' || true; echo "0 $UPDATE_HOURS * * * $CRON_CMD") | crontab -

echo "Cron job configured for hours: $UPDATE_HOURS"
crontab -l | grep -E 'claude-code|codex|gemini'
