# GitHub Authentication Guide

## Quick Solution: Use Personal Access Token

GitHub no longer accepts passwords for HTTPS. You need a **Personal Access Token (PAT)**.

### Step 1: Create a Personal Access Token

1. **Go to GitHub Token Settings:**
   - Open: https://github.com/settings/tokens/new
   - Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

2. **Configure the Token:**
   - **Note**: `Lexical Analyzer Project` (or any name you prefer)
   - **Expiration**: Choose your preference (90 days, 1 year, or no expiration)
   - **Scopes**: Check ✅ **`repo`** (Full control of private repositories)
   - Click **"Generate token"**

3. **Copy the Token:**
   - ⚠️ **IMPORTANT**: Copy it immediately! You won't see it again.
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 2: Push Using the Token

**Option A: Interactive Push (Recommended)**
```powershell
git push origin main
```
When prompted:
- **Username**: `fabricioguidine`
- **Password**: Paste your **Personal Access Token** (not your GitHub password)

Windows Credential Manager will save it for future use.

**Option B: Use the Script**
```powershell
.\push_to_github.ps1
```

**Option C: Set Token in URL (Temporary)**
```powershell
git remote set-url origin https://fabricioguidine:YOUR_TOKEN@github.com/fabricioguidine/trabalho_do_gleiph.git
git push origin main
```
⚠️ **Warning**: This stores the token in git config. Remove it after:
```powershell
git remote set-url origin https://github.com/fabricioguidine/trabalho_do_gleiph.git
```

## Alternative: Switch to SSH (Recommended for Long-term)

SSH doesn't require tokens and is more secure:

### Step 1: Check for Existing SSH Key
```powershell
ls ~/.ssh/id_rsa.pub
# or
ls ~/.ssh/id_ed25519.pub
```

### Step 2: Generate SSH Key (if needed)
```powershell
ssh-keygen -t ed25519 -C "fabricioguidine@gmail.com"
# Press Enter to accept default location
# Optionally set a passphrase (recommended)
```

### Step 3: Add SSH Key to GitHub
1. Copy your public key:
   ```powershell
   cat ~/.ssh/id_ed25519.pub
   # or
   cat ~/.ssh/id_rsa.pub
   ```

2. Go to: https://github.com/settings/keys
3. Click **"New SSH key"**
4. **Title**: `My Computer` (or any name)
5. **Key**: Paste the public key content
6. Click **"Add SSH key"**

### Step 4: Change Remote to SSH
```powershell
git remote set-url origin git@github.com:fabricioguidine/trabalho_do_gleiph.git
git push origin main
```

## Verify Authentication

After setting up, test with:
```powershell
git push origin main
```

If successful, you should see:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
...
To https://github.com/fabricioguidine/trabalho_do_gleiph.git
   [old-commit]..[new-commit]  main -> main
```

## Troubleshooting

**Error: "Authentication failed"**
- Make sure you're using a Personal Access Token, not your password
- Check that the token has `repo` scope
- Verify the token hasn't expired

**Error: "Permission denied"**
- Ensure you have push access to the repository
- Check that the repository exists and you're a collaborator

**Credential Manager Issues**
- Clear stored credentials:
  ```powershell
  git credential-manager-core erase
  # Then try pushing again
  ```

