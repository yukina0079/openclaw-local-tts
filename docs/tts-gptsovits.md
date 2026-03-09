# GPT-SoVITS 本地 TTS 用法

## 当前状态
- 本地 API: `http://127.0.0.1:9880`
- 当前已验证可用模型目录: `C:\baidunetdiskdownload\mzk(v2pp)`
- 运行时 Python: `C:\baidunetdiskdownload\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\python.exe`

## 前台启动 API（推荐你现在用这个）
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\35252\.openclaw\workspace\scripts\start-gptsovits-api.ps1
```

这会弹出一个可见的 PowerShell 窗口，并在前台运行 `api_v2.py`。

如果想在当前窗口直接运行：
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\35252\.openclaw\workspace\scripts\start-gptsovits-api.ps1 -NoExit
```

## 停止 API
```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\35252\.openclaw\workspace\scripts\stop-gptsovits-api.ps1
```

## 快速调用 TTS
```powershell
C:\baidunetdiskdownload\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\python.exe `
  C:\Users\35252\.openclaw\workspace\scripts\tts-gptsovits.py `
  --model "mzk(v2pp)" `
  --text "こんにちは。テスト音声です。" `
  --text-lang ja `
  --prompt-text "こんにちは。これはテストです。" `
  --prompt-lang ja `
  --out "C:\Users\35252\.openclaw\workspace\output\tts-output.wav"
```

## 参数说明
- `Model`: 对应 `C:\baidunetdiskdownload\<Model>` 文件夹名
- `Text`: 要合成的文本
- `TextLang`: 合成文本语言，例如 `ja` / `zh` / `en`
- `PromptText`: 参考音频里实际说的话
- `PromptLang`: 参考音频语言
- `RefAudio`: 可选，显式指定参考音频；不填则自动从模型文件夹选第一条音频
- `Out`: 输出 wav 路径
- `Speed`: 语速

## 备注
- 当前脚本默认直接打本地 GPT-SoVITS API，不走 OpenClaw 内置 tts。
- 你现在偏好前台启动，所以以后建议先用 `start-gptsovits-api.ps1` 开一个可见窗口。
- 日文参考音频可以继续用对应模型名目录下的样本。
