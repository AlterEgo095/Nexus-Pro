#!/bin/bash

# 🚀 NEXUS Ultimate - One-Click GitHub Setup Script
# This script automates the entire GitHub deployment process

set -e  # Exit on error

echo "🧠 NEXUS Ultimate - GitHub Deployment Script"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install git first."
    exit 1
fi

if ! command -v gh &> /dev/null; then
    echo "⚠️  GitHub CLI (gh) not found. You'll need to create the repo manually."
    USE_GH=false
else
    USE_GH=true
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}\n"

# Get GitHub username
echo -e "${YELLOW}Enter your GitHub username:${NC}"
read -r GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username required"
    exit 1
fi

# Get repository name
echo -e "${YELLOW}Enter repository name (default: nexus-ultimate):${NC}"
read -r REPO_NAME
REPO_NAME=${REPO_NAME:-nexus-ultimate}

echo ""
echo "Configuration:"
echo "  Username: $GITHUB_USERNAME"
echo "  Repository: $REPO_NAME"
echo ""

# Initialize Git
echo -e "${BLUE}Step 1: Initializing Git repository...${NC}"
git init
git add .
git commit -m "🚀 Initial commit: NEXUS Ultimate v1.0.0

- Multi-level cognitive architecture
- 30+ tool orchestration
- Universal media processing
- Mobile-first optimization
- Complete test suite
- Docker support
- CI/CD configured"

echo -e "${GREEN}✅ Git initialized${NC}\n"

# Create GitHub repository
echo -e "${BLUE}Step 2: Creating GitHub repository...${NC}"

if [ "$USE_GH" = true ]; then
    # Using GitHub CLI
    gh repo create "$GITHUB_USERNAME/$REPO_NAME" \
        --public \
        --source=. \
        --remote=origin \
        --description="Elite cognitive AI agent framework with multi-level thinking, tool orchestration, and universal media processing" \
        --confirm || {
            echo "⚠️  Failed to create repo with gh. Try manually at https://github.com/new"
            exit 1
        }
    echo -e "${GREEN}✅ Repository created via GitHub CLI${NC}\n"
else
    # Manual instructions
    echo "Please create the repository manually:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: $REPO_NAME"
    echo "3. Description: Elite cognitive AI agent framework"
    echo "4. Public repository"
    echo "5. Do NOT initialize with README, .gitignore, or license"
    echo ""
    echo "Press Enter when done..."
    read -r
    
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo -e "${GREEN}✅ Remote added${NC}\n"
fi

# Push to GitHub
echo -e "${BLUE}Step 3: Pushing to GitHub...${NC}"
git branch -M main
git push -u origin main

echo -e "${GREEN}✅ Code pushed to GitHub${NC}\n"

# Configure repository settings
echo -e "${BLUE}Step 4: Configure repository settings${NC}"
echo ""
echo "⚙️  Manual configuration needed (visit your repo settings):"
echo ""
echo "1. Topics (About → Settings):"
echo "   ai, agent, cognitive-architecture, telegram-bot, python,"
echo "   nlp, automation, tree-of-thoughts, machine-learning"
echo ""
echo "2. Enable features (Settings → General → Features):"
echo "   ✓ Issues"
echo "   ✓ Projects"
echo "   ✓ Discussions"
echo ""
echo "3. Branch protection (Settings → Branches):"
echo "   ✓ Require pull request reviews"
echo "   ✓ Require status checks to pass"
echo ""
echo "4. Secrets (Settings → Secrets → Actions):"
echo "   • PYPI_API_TOKEN (for PyPI publication)"
echo "   • CODECOV_TOKEN (for code coverage)"
echo ""

# Create first release (optional)
echo -e "${YELLOW}Create initial release v1.0.0? (y/n)${NC}"
read -r CREATE_RELEASE

if [ "$CREATE_RELEASE" = "y" ] && [ "$USE_GH" = true ]; then
    echo -e "${BLUE}Creating release v1.0.0...${NC}"
    gh release create v1.0.0 \
        --title "NEXUS Ultimate v1.0.0 - Initial Release" \
        --notes "🎉 First public release of NEXUS Ultimate

## Features
- Multi-level cognitive architecture (4 levels)
- Tree of Thoughts & Chain of Thought reasoning
- 30+ tool orchestration with circuit breakers
- Universal media processing (images, audio, video, documents)
- Mobile-first output formatting
- Complete test suite (50+ benchmark cases)
- Docker support with docker-compose
- CI/CD via GitHub Actions

## Installation
\`\`\`bash
pip install nexus-ultimate
\`\`\`

## Quick Start
\`\`\`python
from nexus import NexusAgent
agent = NexusAgent(mode='auto')
response = agent.process_sync(query='Your query')
\`\`\`

See README.md for full documentation."
    
    echo -e "${GREEN}✅ Release created${NC}\n"
fi

# Final summary
echo ""
echo "=============================================="
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "=============================================="
echo ""
echo "📍 Repository URL:"
echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "📚 Next steps:"
echo "   1. Add badges to README.md (see README_BADGES.md)"
echo "   2. Configure repository settings (see above)"
echo "   3. Set up secrets for CI/CD"
echo "   4. Enable Discussions for community"
echo "   5. Star your own repo ⭐"
echo ""
echo "🚀 Your project is now live on GitHub!"
echo ""
