param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$TextParts
)

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$configLocal = Join-Path $repoRoot 'config.local.json'
$configExample = Join-Path $repoRoot 'config.example.json'
$configPath = if (Test-Path $configLocal) { $configLocal } else { $configExample }

$pyCandidates = @(
  'C:\baidunetdiskdownload\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\python.exe',
  'python'
)
$py = $pyCandidates | Select-Object -First 1
$script = Join-Path $repoRoot 'scripts\tts-gptsovits.py'
$text = ($TextParts -join ' ').Trim()
$out = Join-Path $repoRoot 'output\speak-latest.wav'

$args = @($script, '--out', $out)
if ($text) {
  $args += @('--text', $text)
}

& $py @args
exit $LASTEXITCODE
