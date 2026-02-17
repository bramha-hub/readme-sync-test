# 🚀 Quick Start Guide

Get README-Sync running in 5 minutes!

## Prerequisites

- ✅ Python 3.10+ installed
- ✅ Git repository
- ✅ Google Gemini API key ([Get free key](https://makersuite.google.com/app/apikey))

## Step 1: Clone or Copy Files

If you're integrating into an existing project, copy these files:

```bash
# Essential files
.github/workflows/readme-sync.yml
src/
config.yml
requirements.txt
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed google-generativeai-0.3.0 PyGithub-2.1.1 GitPython-3.1.40 PyYAML-6.0.1
```

## Step 3: Test Locally (Optional)

Run the demo to verify everything works:

```bash
python demo.py
```

You should see output showing Python and JavaScript parsing examples.

## Step 4: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your API key from Google AI Studio

## Step 5: Customize Config (Optional)

Edit `config.yml` to match your needs:

```yaml
# Monitor these file types
monitored_extensions:
  - .py
  - .js
  - .ts

# Update these documentation files
documentation_files:
  - README.md
```

## Step 6: Initialize Git (If New Project)

```bash
git init
git add .
git commit -m "Initial commit with README-Sync"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Step 7: Test the Workflow

Make a code change to trigger the workflow:

```bash
# Edit a Python file
echo "def new_function(): pass" >> examples/example_module.py

# Commit and push
git add .
git commit -m "feat: add new function"
git push
```

## Step 8: Check the Results

1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. You should see a workflow run called "README Sync"
4. Wait for it to complete
5. Check the **"Pull Requests"** tab for the AI-generated documentation update

## 🎉 Success!

You should now have a pull request with updated documentation. Review it and merge if it looks good!

## Troubleshooting

### "No relevant code changes detected"

**Cause**: You modified files that aren't in `monitored_extensions`

**Fix**: Check `config.yml` and ensure your file types are listed

### "GEMINI_API_KEY environment variable not set"

**Cause**: Secret not configured in GitHub

**Fix**: Follow Step 4 above to add the secret

### Workflow doesn't run

**Cause**: Workflow file not on main branch or wrong trigger

**Fix**: 
```bash
git checkout main
git pull
ls .github/workflows/readme-sync.yml  # Should exist
```

### "Failed to generate documentation"

**Cause**: API quota exceeded or invalid key

**Fix**: 
1. Check your API key is valid
2. Verify you haven't exceeded Gemini's free tier limits
3. Check the Actions log for specific error messages

## Next Steps

- ✅ Review the [full README](README.md) for advanced features
- ✅ Check out [SETUP.md](SETUP.md) for detailed configuration
- ✅ Customize `config.yml` for your project
- ✅ Add more documentation files to `documentation_files`

## Example Workflow

Here's a typical development workflow with README-Sync:

```bash
# 1. Create a feature branch
git checkout -b feature/new-api

# 2. Add your code
cat > api.py << EOF
def create_user(name: str, email: str) -> dict:
    """Create a new user account."""
    return {"name": name, "email": email}
EOF

# 3. Commit and push
git add api.py
git commit -m "feat: add user creation API"
git push origin feature/new-api

# 4. Create PR on GitHub
# 5. README-Sync runs automatically
# 6. Review both your code PR and the docs PR
# 7. Merge both!
```

## Tips for Best Results

1. **Write good docstrings**: The AI uses them to understand your code
2. **Use type hints**: Helps generate accurate documentation
3. **Review AI changes**: Always review before merging
4. **Iterate on config**: Adjust `temperature` if updates are too creative or too conservative
5. **Start small**: Test on a small project first

---

**Need help?** Check the [main README](README.md) or open an issue!
