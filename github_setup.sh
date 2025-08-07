#!/bin/bash

# GitHub Repository Setup Script

echo "🚀 Geothermal Knowledge Base Assistant - GitHub Setup"
echo "===================================================="

# Check if git is installed
if ! command -v git &> /dev/null
then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "ℹ️  Git repository already exists"
fi

# Check if repository is already connected to remote
if git remote get-url origin &> /dev/null; then
    echo "ℹ️  Repository already connected to remote origin"
    echo "   Current remote: $(git remote get-url origin)"
else
    echo "🔗 Setting up GitHub repository connection"
    echo "Please enter your GitHub username:"
    read username
    echo "Please enter your repository name:"
    read repo_name
    
    echo "Connecting to https://github.com/$username/$repo_name.git"
    git remote add origin https://github.com/$username/$repo_name.git
    echo "✅ Remote repository connected"
fi

# Add all files
echo "📦 Adding files to repository..."
git add .

# Make initial commit
echo "📝 Making initial commit..."
git commit -m "Initial commit: Geothermal Knowledge Base Assistant with RAG implementation"

echo ""
echo "✅ GitHub setup completed!"
echo ""
echo "To push to GitHub, run:"
echo "   git push -u origin main"
echo ""
echo "If this is a new repository, you might need to create the main branch first:"
echo "   git branch -M main"
echo "   git push -u origin main"