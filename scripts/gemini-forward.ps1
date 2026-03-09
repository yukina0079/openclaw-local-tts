param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$PromptParts
)

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$py = 'python'
$script = Join-Path $repoRoot 'scripts\gemini-forward.py'
$prompt = ($PromptParts -join ' ').Trim()
if (-not $prompt) {
  throw 'Prompt is required.'
}

& $py $script --prompt $prompt
exit $LASTEXITCODE
