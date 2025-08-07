@echo off
REM GitHub Repository Setup Script (Windows)

echo 🚀 Geothermal Knowledge Base Assistant - GitHub Setup
echo ====================================================

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed. Please install Git first.
    exit /b 1
)

REM Initialize git repository if not already initialized
if not exist ".git" (
    echo 🔧 Initializing Git repository...
    git init
    echo ✅ Git repository initialized
) else (
    echo ℹ️  Git repository already exists
)

REM Check if repository is already connected to remote
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo ℹ️  Repository already connected to remote origin
    for /f %%i in ('git remote get-url origin') do set remote_url=%%i
    echo    Current remote: %remote_url%
) else (
    echo 🔗 Setting up GitHub repository connection
    set /p username="Please enter your GitHub username: "
    set /p repo_name="Please enter your repository name: "
    
    echo Connecting to https://github.com/%username%/%repo_name%.git
    git remote add origin https://github.com/%username%/%repo_name%.git
    echo ✅ Remote repository connected
)

REM Add all files
echo 📦 Adding files to repository...
git add .

REM Make initial commit
echo 📝 Making initial commit...
git commit -m "Initial commit: Geothermal Knowledge Base Assistant with RAG implementation"

echo.
echo ✅ GitHub setup completed!
echo.
echo To push to GitHub, run:
echo    git push -u origin main
echo.
echo If this is a new repository, you might need to create the main branch first:
echo    git branch -M main
echo    git push -u origin main