#!/bin/bash
# Check and update skill-creator from GitHub

SKILL_PATH="$HOME/.claude/skills/skill-creator"
TEMP_REPO="/tmp/skills-repo-update"

# Clone the latest version
git clone --depth 1 https://github.com/anthropics/skills.git "$TEMP_REPO" 2>/dev/null

if [ -d "$TEMP_REPO/skills/skill-creator" ]; then
    # Check if there are differences
    if ! diff -r "$SKILL_PATH" "$TEMP_REPO/skills/skill-creator" > /dev/null 2>&1; then
        echo "Updating skill-creator..."
        rm -rf "$SKILL_PATH"
        cp -r "$TEMP_REPO/skills/skill-creator" "$SKILL_PATH"
        echo "skill-creator updated successfully"
    fi
fi

# Cleanup
rm -rf "$TEMP_REPO"
