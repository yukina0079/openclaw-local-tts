$procs = Get-CimInstance Win32_Process | Where-Object {
  $_.Name -eq 'python.exe' -and $_.CommandLine -match 'api_v2.py' -and $_.CommandLine -match 'GPT-SoVITS-v2pro-20250604-nvidia50'
}

if (-not $procs) {
  Write-Host 'No GPT-SoVITS api_v2.py process found.'
  exit 0
}

$procs | ForEach-Object {
  Write-Host ("Stopping PID {0}" -f $_.ProcessId)
  Stop-Process -Id $_.ProcessId -Force
}
