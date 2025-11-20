# Repository Renaming Instructions

## Suggested Repository Name

Based on the project theme (lexical analyzer), here are some suggested names:

1. **lexical-analyzer** - Clear and descriptive
2. **rpn-lexer** - Emphasizes reverse Polish notation
3. **automata-lexer** - Emphasizes finite automata
4. **tag-based-lexer** - Emphasizes tag-based tokenization
5. **dcc146-lexical-analyzer** - Includes course code

## How to Rename on GitHub

### Option 1: Via GitHub Web Interface (Recommended)

1. Go to your repository on GitHub: `https://github.com/fabricioguidine/trabalho_do_gleiph`
2. Click on **Settings** (top right of the repository page)
3. Scroll down to the **Repository name** section
4. Enter the new repository name (e.g., `lexical-analyzer`)
5. Click **Rename**
6. GitHub will automatically redirect and update the remote URL

### Option 2: Update Local Remote URL

After renaming on GitHub, update your local repository:

```bash
git remote set-url origin https://github.com/fabricioguidine/NEW_REPO_NAME.git
```

### Option 3: Using GitHub CLI (if installed)

```bash
gh repo rename NEW_REPO_NAME
```

## Current Remote

Current repository: `trabalho_do_gleiph`

After renaming, remember to update any documentation or links that reference the old repository name.

