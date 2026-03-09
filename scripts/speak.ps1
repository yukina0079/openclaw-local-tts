param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$TextParts
)

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
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
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Add-Type -AssemblyName presentationCore
$player = New-Object System.Windows.Media.MediaPlayer
$player.Open([uri]$out)
$player.Volume = 1.0
$player.Play()
Start-Sleep -Seconds 5
