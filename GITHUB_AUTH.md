# GitHub Authentication Setup

## Important: GitHub No Longer Accepts Passwords

GitHub requires a **Personal Access Token (PAT)** for HTTPS authentication instead of passwords.

## Steps to Create a Personal Access Token

1. Go to GitHub: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name (e.g., "Lexical Analyzer Project")
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (if you use GitHub Actions)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

## Using the Token

When you push, you'll be prompted for:
- **Username**: `fabricioguidine`
- **Password**: **Paste your Personal Access Token here** (not your GitHub password)

The credential manager will save it for future use.

## Alternative: Use SSH Instead

If you prefer SSH (no token needed each time):

```bash
# Check if you have SSH key
ls ~/.ssh/id_rsa.pub

# If not, generate one
ssh-keygen -t ed25519 -C "fabricioguidine@gmail.com"

# Add to GitHub: https://github.com/settings/keys
# Then change remote:
git remote set-url origin git@github.com:fabricioguidine/trabalho_do_gleiph.git
```

