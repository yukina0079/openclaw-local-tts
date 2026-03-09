$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$configCandidates = @(
  (Join-Path $repoRoot 'config.local.json'),
  (Join-Path $repoRoot 'config.json'),
  (Join-Path $repoRoot 'config.example.json')
)
$configPath = $configCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $configPath) { throw 'No config file found.' }
$config = Get-Content $configPath -Raw | ConvertFrom-Json
$root = $config.paths.gptSovitsRoot

$procs = Get-CimInstance Win32_Process | Where-Object {
  $_.Name -eq 'python.exe' -and $_.CommandLine -match 'api_v2.py' -and $_.CommandLine -match [regex]::Escape($root)
}

if (-not $procs) {
  Write-Host 'No GPT-SoVITS api_v2.py process found.'
  exit 0
}

$procs | ForEach-Object {
  Write-Host ("Stopping PID {0}" -f $_.ProcessId)
  Stop-Process -Id $_.ProcessId -Force
}
