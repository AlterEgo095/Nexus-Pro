#!/bin/bash

# 🚀 NEXUS Ultimate - Deploy to Existing GitHub Repo
# Usage: ./deploy-to-existing-repo.sh

set -e

echo "🧠 NEXUS Ultimate - Deploy to AlterEgo095/Nexus-Pro"
echo "===================================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Repository URL
REPO_URL="https://github.com/AlterEgo095/Nexus-Pro.git"

echo -e "${YELLOW}⚠️  SECURITY CHECK${NC}"
echo "This script will push code to: $REPO_URL"
echo ""
echo -e "${RED}NEVER share your GitHub token publicly!${NC}"
echo "Make sure you have revoked any exposed tokens."
echo ""
echo "Press Enter to continue or Ctrl+C to cancel..."
read -r

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git not found. Please install git first.${NC}"
    exit 1
fi

# Initialize Git
echo -e "${BLUE}Step 1: Initializing Git repository...${NC}"
git init
git add .
git commit -m "🚀 Initial commit: NEXUS Ultimate v1.0.0

Elite Cognitive AI Agent Framework

✨ Features:
- Multi-level cognitive architecture (4 levels)
- Tree of Thoughts & Chain of Thought reasoning
- 30+ tool orchestration with circuit breakers
- Universal media processing (images, audio, video, documents)
- Mobile-first Telegram optimization
- Complete test suite (50+ benchmark cases)
- Docker support with docker-compose
- Full CI/CD via GitHub Actions

📚 Documentation:
- Comprehensive README with examples
- Quick Start Guide (5min to productivity)
- Complete API documentation
- Contributing guidelines
- Security policy

🔧 DevOps:
- Automated testing (pytest)
- Code quality checks (black, flake8, mypy)
- Docker containerization
- GitHub Actions workflows

🌟 Ready for production deployment and community contributions!

Repository: https://github.com/AlterEgo095/Nexus-Pro"

echo -e "${GREEN}✅ Git initialized and committed${NC}\n"

# Add remote
echo -e "${BLUE}Step 2: Adding GitHub remote...${NC}"
if git remote | grep -q origin; then
    git remote remove origin
fi
git remote add origin "$REPO_URL"
echo -e "${GREEN}✅ Remote added${NC}\n"

# Rename branch to main
echo -e "${BLUE}Step 3: Setting up main branch...${NC}"
git branch -M main
echo -e "${GREEN}✅ Branch renamed to main${NC}\n"

# Push to GitHub
echo -e "${BLUE}Step 4: Pushing to GitHub...${NC}"
echo ""
echo -e "${YELLOW}You will be prompted for credentials:${NC}"
echo "  Username: AlterEgo095"
echo "  Password: [Your NEW GitHub Token]"
echo ""
echo -e "${RED}DO NOT use the old exposed token!${NC}"
echo ""

git push -u origin main --force

echo ""
echo -e "${GREEN}✅ Code successfully pushed to GitHub!${NC}\n"

# Success summary
echo "=============================================="
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "=============================================="
echo ""
echo "📍 Repository URL:"
echo "   https://github.com/AlterEgo095/Nexus-Pro"
echo ""
echo "📚 Next steps:"
echo "   1. Visit your repository on GitHub"
echo "   2. Follow GITHUB_SETUP_CHECKLIST.md"
echo "   3. Configure repository settings"
echo "   4. Add badges to README.md"
echo "   5. Enable GitHub Actions"
echo "   6. Create your first release (v1.0.0)"
echo ""
echo "🔒 Security reminder:"
echo "   - Never share GitHub tokens"
echo "   - Use environment variables for secrets"
echo "   - Enable 2FA on your GitHub account"
echo ""
echo "🚀 Your NEXUS Ultimate project is now live!"
echo ""
