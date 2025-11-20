# PowerShell script to push to GitHub with authentication
# Usage: .\push_to_github.ps1

Write-Host "GitHub Push Script" -ForegroundColor Green
Write-Host "===================" -ForegroundColor Green
Write-Host ""

# Check if we have commits to push
$commitsAhead = git rev-list --count origin/main..HEAD 2>$null
if ($commitsAhead -eq 0) {
    Write-Host "No commits to push." -ForegroundColor Yellow
    exit 0
}

Write-Host "You have $commitsAhead commit(s) ready to push." -ForegroundColor Cyan
Write-Host ""

# Option 1: Try with stored credentials
Write-Host "Attempting push with stored credentials..." -ForegroundColor Yellow
$result = git push origin main 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Push successful!" -ForegroundColor Green
    exit 0
}

# If it asks for credentials, provide instructions
Write-Host ""
Write-Host "Authentication Required" -ForegroundColor Yellow
Write-Host "======================" -ForegroundColor Yellow
Write-Host ""
Write-Host "GitHub requires a Personal Access Token (not your password)." -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick Steps:" -ForegroundColor White
Write-Host "1. Go to: https://github.com/settings/tokens/new" -ForegroundColor Cyan
Write-Host "2. Token name: 'Lexical Analyzer Project'" -ForegroundColor Cyan
Write-Host "3. Select scope: 'repo' (check the box)" -ForegroundColor Cyan
Write-Host "4. Click 'Generate token'" -ForegroundColor Cyan
Write-Host "5. Copy the token" -ForegroundColor Cyan
Write-Host ""
Write-Host "When prompted:" -ForegroundColor White
Write-Host "  Username: fabricioguidine" -ForegroundColor Green
Write-Host "  Password: [Paste your token here]" -ForegroundColor Green
Write-Host ""
Write-Host "Or run this command manually:" -ForegroundColor Yellow
Write-Host "  git push origin main" -ForegroundColor White
Write-Host ""

