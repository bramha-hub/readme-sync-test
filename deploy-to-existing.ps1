# README-Sync Deployment Script for Existing Repository
# Usage: .\deploy-to-existing.ps1 -TargetRepo "C:\path\to\your\project"

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetRepo
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  README-Sync Deployment Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Validate target repository exists
if (-not (Test-Path $TargetRepo)) {
    Write-Host "❌ Error: Target repository not found: $TargetRepo" -ForegroundColor Red
    exit 1
}

Write-Host "🎯 Target Repository: $TargetRepo" -ForegroundColor Yellow
Write-Host "📦 Source: $PSScriptRoot`n" -ForegroundColor Yellow

# Create directories
Write-Host "📁 Creating directories..." -ForegroundColor Green
New-Item -Path "$TargetRepo\.github\workflows" -ItemType Directory -Force | Out-Null
New-Item -Path "$TargetRepo\.readme-sync\src\parsers" -ItemType Directory -Force | Out-Null

# Copy workflow file
Write-Host "📋 Copying workflow file..." -ForegroundColor Green
Copy-Item -Path "$PSScriptRoot\.github\workflows\readme-sync.yml" -Destination "$TargetRepo\.github\workflows\" -Force

# Update workflow to use .readme-sync directory
$workflowContent = Get-Content "$TargetRepo\.github\workflows\readme-sync.yml" -Raw
$workflowContent = $workflowContent -replace 'pip install -r requirements.txt', 'pip install -r .readme-sync/requirements.txt'
$workflowContent = $workflowContent -replace 'python src/sync_readme.py', 'cd .readme-sync && python src/sync_readme.py'
Set-Content -Path "$TargetRepo\.github\workflows\readme-sync.yml" -Value $workflowContent

# Copy source files
Write-Host "💻 Copying source code..." -ForegroundColor Green
Copy-Item -Path "$PSScriptRoot\src\*" -Destination "$TargetRepo\.readme-sync\src\" -Recurse -Force

# Copy configuration files
Write-Host "⚙️  Copying configuration..." -ForegroundColor Green
Copy-Item -Path "$PSScriptRoot\config.yml" -Destination "$TargetRepo\.readme-sync\" -Force
Copy-Item -Path "$PSScriptRoot\requirements.txt" -Destination "$TargetRepo\.readme-sync\" -Force

Write-Host "`n✅ Deployment Complete!" -ForegroundColor Green
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "1. Add GitHub Secret:" -ForegroundColor Yellow
Write-Host "   - Go to your repo → Settings → Secrets → Actions"
Write-Host "   - Add secret: GEMINI_API_KEY"
Write-Host "   - Value: AIzaSyD-fg8EnsNPPoGeMcgqzjlZlPWbGCswL-s`n"

Write-Host "2. Commit and Push:" -ForegroundColor Yellow
Write-Host "   cd $TargetRepo"
Write-Host "   git add .github/workflows/readme-sync.yml"
Write-Host "   git add .readme-sync/"
Write-Host "   git commit -m 'feat: add README-Sync automation'"
Write-Host "   git push`n"

Write-Host "3. Test It:" -ForegroundColor Yellow
Write-Host "   - Make a code change"
Write-Host "   - Push to GitHub"
Write-Host "   - Check Actions tab for README-Sync workflow`n"

Write-Host "📚 Documentation: See DEPLOYMENT.md for details`n" -ForegroundColor Cyan
