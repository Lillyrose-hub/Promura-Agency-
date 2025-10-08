#!/bin/bash
# Quick commit and push script for PROMURA
# Usage: ./quick-commit.sh "Your commit message"

cd /opt/promura

# Check if commit message was provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide a commit message"
    echo "Usage: ./quick-commit.sh \"Your commit message\""
    exit 1
fi

echo "📝 Adding all changes..."
git add .

echo "💾 Committing changes..."
git commit -m "$1

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Done! Changes pushed to GitHub"
