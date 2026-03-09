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
$pyRel = $config.paths.runtimePython
$apiRel = $config.paths.apiScript
$ttsConfig = $config.paths.ttsConfig
$host = $config.api.host
$port = [string]$config.api.port

$py = Join-Path $root $pyRel
$api = Join-Path $root $apiRel
$cmd = "title GPT-SoVITS API && cd /d `"$root`" && `"$py`" `"$api`" -a $host -p $port -c `"$ttsConfig`""
Start-Process -FilePath 'cmd.exe' -ArgumentList '/k', $cmd -WorkingDirectory $root
Write-Host "Started GPT-SoVITS API in a new visible cmd window using config: $configPath"
