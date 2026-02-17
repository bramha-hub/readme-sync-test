# 🚀 Quick Deployment Guide

## Choose Your Deployment Method

### Option A: Add to Existing Project ⭐ (Recommended)
**Use this if:** You want README-Sync to automatically update docs for a specific project

```powershell
# Run this command:
.\deploy-to-existing.ps1 -TargetRepo "C:\path\to\your\project"
```

**What it does:**
- Copies README-Sync to your project's `.readme-sync/` folder
- Adds GitHub Actions workflow
- Keeps your project clean and organized

---

### Option B: Create Standalone Repository
**Use this if:** You want to share README-Sync or use it as a template

```powershell
# Run this command:
.\deploy-standalone.ps1 -GithubUsername "YOUR_USERNAME" -RepoName "readme-sync"
```

**What it does:**
- Creates a new GitHub repository
- Pushes README-Sync as a standalone project
- You can then add it to other projects using Option A

---

## Quick Start Examples

### Example 1: Add to Your Existing "MyApp" Project

```powershell
# Navigate to README-Sync folder
cd C:\Users\Lenovo\OneDrive\Desktop\Readme-sync

# Deploy to your project
.\deploy-to-existing.ps1 -TargetRepo "C:\Users\Lenovo\Projects\MyApp"

# Then in your project:
cd C:\Users\Lenovo\Projects\MyApp
git add .
git commit -m "feat: add README-Sync"
git push
```

### Example 2: Create Your Own README-Sync Repository

```powershell
# Navigate to README-Sync folder
cd C:\Users\Lenovo\OneDrive\Desktop\Readme-sync

# First, create repo on GitHub: https://github.com/new
# Name it: readme-sync

# Then deploy:
.\deploy-standalone.ps1 -GithubUsername "YOUR_GITHUB_USERNAME" -RepoName "readme-sync"
```

---

## After Deployment: Add API Key

**For both options, you MUST add your API key to GitHub Secrets:**

1. Go to your repository on GitHub
2. Click: **Settings** → **Secrets and variables** → **Actions**
3. Click: **New repository secret**
4. Enter:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** `AIzaSyD-fg8EnsNPPoGeMcgqzjlZlPWbGCswL-s`
5. Click: **Add secret**

---

## Testing Your Deployment

After deployment and adding the API key:

```bash
# Make a code change
echo "def new_feature(): pass" >> your_file.py

# Commit and push
git add your_file.py
git commit -m "feat: add new feature"
git push
```

Then:
1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see "README Sync" workflow running
4. Wait for it to complete
5. Check **Pull Requests** for the auto-generated documentation update!

---

## Decision Tree

```
Do you have an existing project that needs auto-docs?
│
├─ YES → Use Option A (deploy-to-existing.ps1)
│         └─ Adds README-Sync to your project
│
└─ NO  → Do you want to share README-Sync with others?
          │
          ├─ YES → Use Option B (deploy-standalone.ps1)
          │         └─ Creates a public repository
          │
          └─ NO  → Start with Option B anyway
                    └─ You can always use it later with Option A
```

---

## Troubleshooting

### "Execution of scripts is disabled"
```powershell
# Run PowerShell as Administrator and execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Repository not found"
- Make sure you created the repository on GitHub first
- Check the repository name matches exactly

### "Permission denied"
- Make sure you're logged into GitHub
- Check your GitHub credentials
- Try using SSH instead of HTTPS

---

## What Happens Next?

Once deployed, every time you push code changes:

1. 🔍 GitHub Actions detects the push
2. 🤖 README-Sync analyzes your code changes
3. 🧠 Gemini AI generates documentation updates
4. 📝 A Pull Request is created automatically
5. 👀 You review and merge the PR
6. ✅ Your docs stay in sync!

---

## Need Help?

- 📖 Read: `DEPLOYMENT.md` for detailed instructions
- 🧪 Test: Run `python test_llm.py` to verify API connection
- 💬 Questions: Check the troubleshooting section above

---

**Ready to deploy?** Choose your option and run the script! 🚀
