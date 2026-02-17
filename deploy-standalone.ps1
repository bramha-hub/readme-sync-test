# README-Sync Standalone Deployment Script
# Usage: .\deploy-standalone.ps1 -GithubUsername "yourusername" -RepoName "readme-sync"

param(
    [Parameter(Mandatory=$true)]
    [string]$GithubUsername,
    
    [Parameter(Mandatory=$true)]
    [string]$RepoName = "readme-sync"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  README-Sync Standalone Deployment" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "👤 GitHub Username: $GithubUsername" -ForegroundColor Yellow
Write-Host "📦 Repository Name: $RepoName`n" -ForegroundColor Yellow

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📝 Initializing Git repository..." -ForegroundColor Green
    git init
    
    Write-Host "📋 Adding files..." -ForegroundColor Green
    git add .
    
    Write-Host "💾 Creating initial commit..." -ForegroundColor Green
    git commit -m "Initial commit: README-Sync tool"
} else {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
}

# Check if remote exists
$remoteExists = git remote | Select-String -Pattern "origin"
if ($remoteExists) {
    Write-Host "⚠️  Remote 'origin' already exists. Removing..." -ForegroundColor Yellow
    git remote remove origin
}

# Add remote
Write-Host "🔗 Adding GitHub remote..." -ForegroundColor Green
$repoUrl = "https://github.com/$GithubUsername/$RepoName.git"
git remote add origin $repoUrl

# Set main branch
Write-Host "🌿 Setting main branch..." -ForegroundColor Green
git branch -M main

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Ready to Push!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "⚠️  Before pushing, make sure you:" -ForegroundColor Yellow
Write-Host "   1. Created the repository on GitHub: https://github.com/new"
Write-Host "   2. Named it: $RepoName"
Write-Host "   3. Did NOT initialize with README`n"

$confirm = Read-Host "Have you created the GitHub repository? (y/n)"

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Green
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Successfully deployed to GitHub!" -ForegroundColor Green
        
        Write-Host "`n========================================" -ForegroundColor Cyan
        Write-Host "  Next Steps" -ForegroundColor Cyan
        Write-Host "========================================`n" -ForegroundColor Cyan
        
        Write-Host "1. Add GitHub Secret:" -ForegroundColor Yellow
        Write-Host "   - Go to: https://github.com/$GithubUsername/$RepoName/settings/secrets/actions"
        Write-Host "   - Click 'New repository secret'"
        Write-Host "   - Name: GEMINI_API_KEY"
        Write-Host "   - Value: AIzaSyD-fg8EnsNPPoGeMcgqzjlZlPWbGCswL-s`n"
        
        Write-Host "2. View Your Repository:" -ForegroundColor Yellow
        Write-Host "   https://github.com/$GithubUsername/$RepoName`n"
        
        Write-Host "3. Use in Other Projects:" -ForegroundColor Yellow
        Write-Host "   Run: .\deploy-to-existing.ps1 -TargetRepo 'C:\path\to\project'`n"
        
        Write-Host "🎉 Deployment Complete!" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Push failed. Common issues:" -ForegroundColor Red
        Write-Host "   - Repository doesn't exist on GitHub"
        Write-Host "   - Authentication failed (check credentials)"
        Write-Host "   - Repository already has content`n"
    }
} else {
    Write-Host "`n⏸️  Deployment paused." -ForegroundColor Yellow
    Write-Host "   Create the repository on GitHub, then run:" -ForegroundColor Yellow
    Write-Host "   git push -u origin main`n"
}
