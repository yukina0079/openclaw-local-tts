param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$PromptParts
)

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$prompt = ($PromptParts -join ' ').Trim()
if (-not $prompt) {
  throw 'Prompt is required.'
}

$geminiPy = Join-Path $repoRoot 'scripts\gemini-forward.py'
$ttsPy = Join-Path $repoRoot 'scripts\tts-gptsovits.py'
$outText = Join-Path $repoRoot 'output\gemini-latest.txt'
$outAudio = Join-Path $repoRoot 'output\gemini-tts-latest.wav'

python $geminiPy --prompt $prompt --save $outText
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$text = Get-Content $outText -Raw
if (-not $text -or $text.Trim() -eq '') {
  throw 'Gemini returned empty text.'
}

$ttsPython = 'C:\baidunetdiskdownload\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\python.exe'
& $ttsPython $ttsPy --text $text --out $outAudio
exit $LASTEXITCODE
