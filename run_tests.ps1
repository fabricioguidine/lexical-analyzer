# Quick test runner with timeout
$ErrorActionPreference = "Continue"
Write-Host "Running tests..." -ForegroundColor Cyan

$testFiles = @(
    "test.test_regex_parser",
    "test.test_tag", 
    "test.test_lexer",
    "test.test_command_handler"
)

$totalPassed = 0
$totalFailed = 0

foreach ($test in $testFiles) {
    Write-Host "`nTesting: $test" -ForegroundColor Yellow
    try {
        $result = python -m unittest $test -v 2>&1
        $result | Write-Host
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ PASSED" -ForegroundColor Green
            $totalPassed++
        } else {
            Write-Host "✗ FAILED" -ForegroundColor Red
            $totalFailed++
        }
    } catch {
        Write-Host "Error running $test : $_" -ForegroundColor Red
        $totalFailed++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Total Passed: $totalPassed" -ForegroundColor Green
Write-Host "Total Failed: $totalFailed" -ForegroundColor $(if ($totalFailed -eq 0) { "Green" } else { "Red" })
Write-Host "========================================" -ForegroundColor Cyan

