# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please send an email to the project maintainer. All security vulnerabilities will be promptly addressed.

## Secure Usage Guidelines

### 1. Protect Your Credentials

**Never commit:**
- Notion API tokens
- Database IDs
- Personal information
- API keys or secrets
- Passwords or credentials

### 2. Use Environment Variables

Store sensitive data in environment variables:

```bash
export NOTION_TOKEN="your_token_here"
export NOTION_DATABASE_ID="your_database_id"
```

### 3. Private Configuration

All personal data should be stored in `config/private/` which is:
- Ignored by git (see `.gitignore`)
- Never committed to the repository
- Your responsibility to backup separately

### 4. What's Safe to Share

Public parts of this repository contain only:
- Generic templates
- Documentation
- Reusable utilities
- Example configurations with placeholders

### 5. Before Committing

Always run the security check script:

```bash
./scripts/commit-and-push.sh "your commit message"
```

This script automatically:
- Checks for Notion tokens
- Verifies no real credentials are present
- Blocks commits with sensitive data

### 6. Manual Verification

Before any commit, check:

```bash
# Search for tokens
git diff | grep -E "ntn_[0-9]{10,}[a-zA-Z0-9]{20,}"

# Search for API keys
git diff | grep -iE "(api_key|secret|password)" | grep -v "placeholder"

# Search for UUIDs (potential database IDs)
git diff | grep -E "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
```

## Protected Directories

The following directories are **automatically excluded** from git:

```
config/private/          # All private configurations
config/backups/          # Backup files
config/credentials.json  # Credentials file
config/config.json       # Personal config
*.env                    # Environment files
secrets/                 # Secrets directory
tokens/                  # Tokens directory
```

## GitHub Security Features

This repository has **Push Protection** enabled which blocks:
- Known token patterns
- API keys
- Common secret formats

However, this is not 100% reliable. Always verify manually.

## Best Practices

1. **Never hardcode secrets**: Use environment variables or config files
2. **Audit regularly**: Check what's in your git history
3. **Use placeholders**: In documentation and examples
4. **Review before push**: Always run `git diff` before committing
5. **Update .gitignore**: Add new sensitive patterns as needed

## Example: Safe Configuration

### ❌ Wrong (Hardcoded)
```python
TOKEN = 'ntn_EXAMPLE123_NEVER_COMMIT_REAL_TOKENS_HERE'
DATABASE_ID = '00000000-0000-0000-0000-000000000000'
```

### ✅ Correct (Environment Variables)
```python
import os
TOKEN = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
```

### ✅ Correct (Private Config File)
```python
from config.private.credentials import TOKEN, DATABASE_ID
```

## Incident Response

If you accidentally commit sensitive data:

1. **Don't panic** - It can be fixed
2. **Rotate credentials immediately** - Get new tokens/keys
3. **Rewrite git history** - Remove the sensitive data
4. **Force push** - Update the remote repository
5. **Notify maintainers** - If it's a fork or shared repo

### Remove Sensitive Data

```bash
# Remove from specific files
git filter-branch --tree-filter 'find . -name "*.md" -exec sed -i "s/SENSITIVE_DATA/PLACEHOLDER/g" {} \;' -- --all

# Remove file completely from history
git filter-branch --index-filter 'git rm --cached --ignore-unmatch path/to/file' -- --all

# Clean up
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push --force origin main
```

## Security Checklist

Before making repository public or sharing:

- [ ] No real tokens in code or documentation
- [ ] No database IDs in public files
- [ ] No personal information exposed
- [ ] `.gitignore` properly configured
- [ ] Private configs excluded from git
- [ ] All examples use placeholders
- [ ] Security script in place
- [ ] Push protection enabled (if on GitHub)

## Contact

For security concerns, contact the maintainer through GitHub.

---

**Last Updated:** 2025-10-31  
**Repository:** https://github.com/LucasBiason/cursor-multiagent-system

