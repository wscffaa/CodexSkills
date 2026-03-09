#!/bin/bash
# Install skill-creator from GitHub
git clone https://github.com/anthropics/skills.git /tmp/skills-repo
cp -r /tmp/skills-repo/skills/skill-creator ~/.claude/skills/
rm -rf /tmp/skills-repo
