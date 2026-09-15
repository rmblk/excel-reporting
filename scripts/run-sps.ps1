$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repoRoot ".venv\Scripts\python.exe"
$command = Join-Path $repoRoot ".venv\Scripts\excel-reporting.exe"
$envFile = Join-Path $repoRoot ".env"

if (-not (Test-Path $python)) {
	throw "Python executable not found at $python. Create the .venv first."
}

Set-Location $repoRoot
& $python -m pip install --editable .
if ($LASTEXITCODE -ne 0) {
	throw "Failed to install excel-reporting into the .venv."
}

& $command -f ./build/sps-test.xlsx -e $envFile -r sps
if ($LASTEXITCODE -ne 0) {
	throw "The SPS report command failed."
}
