#!/bin/bash
# Script to clean Git history and remove API key

echo "🔧 Cleaning Git history to remove API key..."
echo ""

# Step 1: Reset to before the problematic commits
echo "Step 1: Resetting commits..."
git reset --soft 188bdc7b

# Step 2: Re-add all files with cleaned versions
echo "Step 2: Re-staging cleaned files..."
git add .

# Step 3: Create a new clean commit
echo "Step 3: Creating new commit..."
git commit -m "Add LLM integration and visualization scripts (API key removed)"

# Step 4: Force push to overwrite remote history
echo "Step 4: Force pushing to remote..."
echo "⚠️  This will rewrite history on GitHub"
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    git push --force origin main
    echo "✅ Done! History cleaned and pushed."
else
    echo "❌ Aborted. To push later, run: git push --force origin main"
fi
