# README-Sync Setup Guide

## Prerequisites

- GitHub repository
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Python 3.11+ (for local testing)

## Installation Steps

### 1. Copy Files to Your Repository

Copy the following files to your repository:

```
your-repo/
├── .github/
│   └── workflows/
│       └── readme-sync.yml
├── src/
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── python_parser.py
│   │   └── javascript_parser.py
│   ├── sync_readme.py
│   ├── prompt_builder.py
│   └── llm_client.py
├── config.yml
└── requirements.txt
```

### 2. Configure GitHub Secrets

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: Your Gemini API key

### 3. Customize Configuration

Edit `config.yml` to match your project:

```yaml
# Which file types to monitor
monitored_extensions:
  - .py
  - .js
  - .ts

# Which documentation files to update
documentation_files:
  - README.md
  - docs/API.md  # Add more as needed

# Paths to ignore
exclude_patterns:
  - "**/test_*.py"
  - "**/tests/**"
  - "**/node_modules/**"
```

### 4. Test Locally (Optional but Recommended)

Before relying on the GitHub Action, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GEMINI_API_KEY="your-api-key"

# Make a code change and commit it
git add .
git commit -m "test: add new function"

# Run the sync
python src/sync_readme.py
```

### 5. Push and Watch It Work

```bash
git push origin main
```

Go to the **Actions** tab in your GitHub repository to see the workflow run.

## Troubleshooting

### "GEMINI_API_KEY environment variable not set"

**Solution**: Make sure you've added the secret in GitHub Settings → Secrets and variables → Actions.

### "No relevant code changes detected"

**Solution**: The tool only runs on files matching `monitored_extensions`. Check your `config.yml`.

### Workflow doesn't trigger

**Solution**: 
1. Check that `.github/workflows/readme-sync.yml` is on your main branch
2. Verify the `on:` trigger matches your branch name
3. Check Actions tab for any error messages

### LLM returns "NO_CHANGES_NEEDED" but changes are needed

**Solution**: 
1. The AI might think the docs are already accurate
2. Try lowering the `temperature` in `config.yml` (e.g., 0.1)
3. Check if your code changes are significant enough to warrant doc updates

## Advanced Configuration

### Using a Different Branch

Edit `.github/workflows/readme-sync.yml`:

```yaml
on:
  push:
    branches:
      - develop  # Change from 'main'
```

### Updating Multiple Documentation Files

Edit `config.yml`:

```yaml
documentation_files:
  - README.md
  - docs/API.md
  - docs/CONTRIBUTING.md
  - docs/ARCHITECTURE.md
```

### Using Gemini Flash (Faster, Cheaper)

Edit `config.yml`:

```yaml
llm:
  model: gemini-1.5-flash  # Faster alternative
  temperature: 0.3
  max_tokens: 4096
```

### Custom Exclude Patterns

Edit `config.yml`:

```yaml
exclude_patterns:
  - "**/test_*.py"
  - "**/*_test.py"
  - "**/tests/**"
  - "**/migrations/**"
  - "**/vendor/**"
  - "**/.venv/**"
```

## Next Steps

1. ✅ Set up the GitHub Action
2. ✅ Configure secrets
3. ✅ Customize config.yml
4. ✅ Test locally
5. ✅ Push and verify
6. 📚 Review the first AI-generated PR
7. 🎉 Enjoy always-updated docs!

## Getting Help

- Check the [main README](README.md) for architecture details
- Review the [example workflow runs](../../actions)
- Open an issue if you encounter problems
