# Helper script to set up GitHub authentication
# This will open the token creation page in your browser

Write-Host "`n=== GitHub Authentication Setup Helper ===" -ForegroundColor Cyan
Write-Host ""

# Open token creation page
Write-Host "Opening GitHub token creation page in your browser..." -ForegroundColor Yellow
Start-Process "https://github.com/settings/tokens/new"

Write-Host ""
Write-Host "Instructions:" -ForegroundColor Green
Write-Host "1. Token name: 'Lexical Analyzer Project'" -ForegroundColor White
Write-Host "2. Expiration: Choose your preference" -ForegroundColor White
Write-Host "3. Scopes: Check 'repo' (Full control of private repositories)" -ForegroundColor White
Write-Host "4. Click 'Generate token'" -ForegroundColor White
Write-Host "5. Copy the token (starts with 'ghp_')" -ForegroundColor White
Write-Host ""
Write-Host "After creating the token, run:" -ForegroundColor Yellow
Write-Host "  git push origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "When prompted:" -ForegroundColor Yellow
Write-Host "  Username: fabricioguidine" -ForegroundColor White
Write-Host "  Password: [Paste your token here]" -ForegroundColor White
Write-Host ""

# Wait a moment
Start-Sleep -Seconds 2

Write-Host "Press any key to continue or close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

