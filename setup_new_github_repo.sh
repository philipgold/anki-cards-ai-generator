#!/bin/bash

# Script to set up your own GitHub repository
# Usage: ./setup_new_github_repo.sh YOUR_GITHUB_USERNAME YOUR_REPO_NAME

if [ $# -ne 2 ]; then
    echo "Usage: $0 YOUR_GITHUB_USERNAME YOUR_REPO_NAME"
    echo "Example: $0 myusername anki-cards-ai-generator"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME=$2

echo "Setting up GitHub repository: $GITHUB_USERNAME/$REPO_NAME"
echo ""

# Remove old remote
echo "Removing old remote..."
git remote remove origin

# Add new remote
echo "Adding new remote..."
git remote add origin "git@github.com:$GITHUB_USERNAME/$REPO_NAME.git"

# Show current status
echo ""
echo "Current git status:"
git status

echo ""
echo "Next steps:"
echo "1. Review the changes above"
echo "2. Commit your changes: git add . && git commit -m 'Initial commit: fork of anki-cards-ai-generator'"
echo "3. Push to your new repository: git push -u origin main"
echo ""
echo "Or run these commands:"
echo "  git add ."
echo "  git commit -m 'Initial commit: fork of anki-cards-ai-generator'"
echo "  git push -u origin main"

