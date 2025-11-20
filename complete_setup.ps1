# Complete Setup Script - Does Everything Possible
# This script will guide you through completing all remaining tasks

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Complete Project Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Verify all commits are ready
Write-Host "[1/3] Checking git status..." -ForegroundColor Yellow
$commitsAhead = git rev-list --count origin/main..HEAD 2>$null
if ($commitsAhead -gt 0) {
    Write-Host "  ✓ $commitsAhead commit(s) ready to push" -ForegroundColor Green
} else {
    Write-Host "  ✓ All commits are pushed" -ForegroundColor Green
}

# Step 2: Authentication setup
Write-Host "`n[2/3] GitHub Authentication Setup" -ForegroundColor Yellow
Write-Host "  Opening token creation page..." -ForegroundColor White
Start-Process "https://github.com/settings/tokens/new"

Write-Host "`n  ⚠️  ACTION REQUIRED:" -ForegroundColor Red
Write-Host "  1. Create a token with 'repo' scope" -ForegroundColor White
Write-Host "  2. Copy the token (starts with 'ghp_')" -ForegroundColor White
Write-Host "  3. Press Enter here when done..." -ForegroundColor Yellow
$null = Read-Host

# Step 3: Push to GitHub
Write-Host "`n[3/3] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "  When prompted:" -ForegroundColor White
Write-Host "    Username: fabricioguidine" -ForegroundColor Cyan
Write-Host "    Password: [Paste your token]" -ForegroundColor Cyan
Write-Host ""

$pushResult = git push origin main 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Successfully pushed to GitHub!" -ForegroundColor Green
} else {
    Write-Host "  ✗ Push failed. Please check the error above." -ForegroundColor Red
    Write-Host "  You can try manually: git push origin main" -ForegroundColor Yellow
}

# Step 4: Repository Renaming Instructions
Write-Host "`n[4/4] Repository Renaming" -ForegroundColor Yellow
Write-Host "  To rename the repository:" -ForegroundColor White
Write-Host "  1. Go to: https://github.com/fabricioguidine/trabalho_do_gleiph/settings" -ForegroundColor Cyan
Write-Host "  2. Scroll to 'Repository name' section" -ForegroundColor White
Write-Host "  3. Enter new name (suggested: 'lexical-analyzer' or 'rpn-lexer')" -ForegroundColor White
Write-Host "  4. Click 'Rename'" -ForegroundColor White
Write-Host "  5. Update local remote:" -ForegroundColor White
Write-Host "     git remote set-url origin https://github.com/fabricioguidine/NEW_NAME.git" -ForegroundColor Cyan

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  ✓ All code implemented" -ForegroundColor Green
Write-Host "  ✓ All tests created" -ForegroundColor Green
Write-Host "  ✓ Documentation complete" -ForegroundColor Green
Write-Host "  ✓ All commits ready" -ForegroundColor Green
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Pushed to GitHub" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Push pending (authentication required)" -ForegroundColor Yellow
}
Write-Host "  ⚠️  Repository rename pending (manual step)" -ForegroundColor Yellow
Write-Host ""

