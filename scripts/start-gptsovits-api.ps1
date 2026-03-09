$root = 'C:\baidunetdiskdownload\GPT-SoVITS-v2pro-20250604-nvidia50'
$py = Join-Path $root 'runtime\python.exe'
$api = Join-Path $root 'api_v2.py'
$config = 'GPT_SoVITS/configs/tts_infer.yaml'

$cmd = "title GPT-SoVITS API && cd /d `"$root`" && `"$py`" `"$api`" -a 127.0.0.1 -p 9880 -c `"$config`""
Start-Process -FilePath 'cmd.exe' -ArgumentList '/k', $cmd -WorkingDirectory $root
Write-Host 'Started GPT-SoVITS API in a new visible cmd window.'
