# 🚀 README-Sync Deployment Guide

## Deployment Options

You have **two main options** for deploying README-Sync:

1. **Deploy to an Existing GitHub Repository** (Recommended for most users)
2. **Deploy as a Standalone Repository** (For sharing/reusing across projects)

---

## Option 1: Deploy to Your Existing Repository (Recommended)

This is the best option if you want README-Sync to automatically update documentation for a specific project.

### Step 1: Copy Files to Your Repository

Copy these essential files to your existing project:

```bash
# Navigate to your project
cd path/to/your/project

# Create necessary directories
mkdir -p .github/workflows
mkdir -p .readme-sync/src/parsers

# Copy the workflow file
cp C:/Users/Lenovo/OneDrive/Desktop/Readme-sync/.github/workflows/readme-sync.yml .github/workflows/

# Copy the source code
cp -r C:/Users/Lenovo/OneDrive/Desktop/Readme-sync/src/* .readme-sync/src/

# Copy configuration
cp C:/Users/Lenovo/OneDrive/Desktop/Readme-sync/config.yml .readme-sync/
cp C:/Users/Lenovo/OneDrive/Desktop/Readme-sync/requirements.txt .readme-sync/
```

**Or manually copy:**
```
your-project/
├── .github/
│   └── workflows/
│       └── readme-sync.yml
├── .readme-sync/
│   ├── src/
│   │   ├── parsers/
│   │   ├── sync_readme.py
│   │   ├── llm_client.py
│   │   └── prompt_builder.py
│   ├── config.yml
│   └── requirements.txt
└── [your existing project files]
```

### Step 2: Update the Workflow File

Edit `.github/workflows/readme-sync.yml` to point to the new location:

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r .readme-sync/requirements.txt

- name: Run README Sync
  env:
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITHUB_REPOSITORY: ${{ github.repository }}
  run: |
    cd .readme-sync
    python src/sync_readme.py
```

### Step 3: Add API Key to GitHub Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** `AIzaSyD-fg8EnsNPPoGeMcgqzjlZlPWbGCswL-s`
5. Click **Add secret**

### Step 4: Commit and Push

```bash
git add .github/workflows/readme-sync.yml
git add .readme-sync/
git commit -m "feat: add README-Sync automation"
git push origin main
```

### Step 5: Test It!

Make a code change to trigger the workflow:

```bash
# Edit a Python file
echo "def test_function(): pass" >> your_file.py

# Commit and push
git add your_file.py
git commit -m "feat: add test function"
git push
```

Go to **Actions** tab on GitHub to see README-Sync running!

---

## Option 2: Deploy as a Standalone Repository

This is useful if you want to:
- Share README-Sync with others
- Use it as a template
- Contribute to the project

### Step 1: Initialize Git Repository

```bash
cd C:/Users/Lenovo/OneDrive/Desktop/Readme-sync

# Initialize git
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: README-Sync tool"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository named `readme-sync`
3. **Don't** initialize with README (we already have one)
4. Click **Create repository**

### Step 3: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/readme-sync.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Add API Key to Secrets

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Add `GEMINI_API_KEY` secret with your API key

### Step 5: Test on a Sample Project

Create a test repository and add README-Sync to it using **Option 1** above.

---

## Quick Deployment Script

I can create an automated deployment script for you. Choose your option:

### For Option 1 (Deploy to Existing Repo):

```powershell
# Save this as deploy-to-existing.ps1

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetRepo
)

Write-Host "🚀 Deploying README-Sync to $TargetRepo..." -ForegroundColor Green

# Create directories
New-Item -Path "$TargetRepo/.github/workflows" -ItemType Directory -Force
New-Item -Path "$TargetRepo/.readme-sync/src/parsers" -ItemType Directory -Force

# Copy files
Copy-Item -Path ".github/workflows/readme-sync.yml" -Destination "$TargetRepo/.github/workflows/" -Force
Copy-Item -Path "src/*" -Destination "$TargetRepo/.readme-sync/src/" -Recurse -Force
Copy-Item -Path "config.yml" -Destination "$TargetRepo/.readme-sync/" -Force
Copy-Item -Path "requirements.txt" -Destination "$TargetRepo/.readme-sync/" -Force

Write-Host "✅ Files copied successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Add GEMINI_API_KEY to GitHub Secrets"
Write-Host "2. Commit and push the changes"
Write-Host "3. Make a code change to test"
```

### For Option 2 (Standalone Repo):

```powershell
# Save this as deploy-standalone.ps1

param(
    [Parameter(Mandatory=$true)]
    [string]$GithubUsername,
    [Parameter(Mandatory=$true)]
    [string]$RepoName
)

Write-Host "🚀 Deploying README-Sync as standalone repository..." -ForegroundColor Green

# Initialize git if not already
if (-not (Test-Path ".git")) {
    git init
    git add .
    git commit -m "Initial commit: README-Sync tool"
}

# Add remote and push
git remote add origin "https://github.com/$GithubUsername/$RepoName.git"
git branch -M main
git push -u origin main

Write-Host "✅ Pushed to GitHub!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com/$GithubUsername/$RepoName/settings/secrets/actions"
Write-Host "2. Add GEMINI_API_KEY secret"
Write-Host "3. Use this in other projects!"
```

---

## Verification Checklist

After deployment, verify everything works:

### ✅ Pre-Deployment
- [ ] API key ready: `AIzaSyD-fg8EnsNPPoGeMcgqzjlZlPWbGCswL-s`
- [ ] Files copied to correct location
- [ ] Workflow file updated (if Option 1)

### ✅ GitHub Setup
- [ ] Repository created/selected
- [ ] GEMINI_API_KEY added to Secrets
- [ ] Workflow file in `.github/workflows/`
- [ ] Source code accessible

### ✅ Testing
- [ ] Make a code change
- [ ] Push to GitHub
- [ ] Check Actions tab for workflow run
- [ ] Verify PR is created with documentation updates

---

## Troubleshooting

### Workflow doesn't trigger
**Fix:** Check that the workflow file is on the main branch:
```bash
git checkout main
ls .github/workflows/readme-sync.yml
```

### "GEMINI_API_KEY not set" error
**Fix:** Verify the secret is added:
1. Go to Settings → Secrets → Actions
2. Ensure `GEMINI_API_KEY` is listed
3. Re-run the workflow

### No PR created
**Fix:** Check the workflow logs:
1. Go to Actions tab
2. Click on the failed run
3. Check logs for errors

### Permission denied errors
**Fix:** Update workflow permissions:
1. Go to Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Save

---

## What Happens After Deployment?

Once deployed, README-Sync will:

1. **Monitor** your repository for code changes
2. **Analyze** changes using AST parsing
3. **Generate** documentation updates with Gemini AI
4. **Create** a pull request with the updates
5. **Wait** for your review and approval

### Example Workflow:

```
Developer pushes code
        ↓
GitHub Actions triggers
        ↓
README-Sync analyzes changes
        ↓
Gemini generates docs
        ↓
PR created: "Update README based on code changes"
        ↓
Developer reviews and merges
        ↓
Documentation stays in sync! 🎉
```

---

## Need Help?

Choose the deployment option that works best for you:

- **Option 1** if you want to add README-Sync to an existing project
- **Option 2** if you want to create a reusable template

Run the appropriate script or follow the manual steps above!

---

**Ready to deploy?** Let me know which option you prefer and I can help you execute it! 🚀
