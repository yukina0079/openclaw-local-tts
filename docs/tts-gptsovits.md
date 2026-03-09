# GPT-SoVITS 本地 TTS 用法

## 配置文件

脚本会按以下优先级读取配置：

1. `config.local.json`
2. `config.json`
3. `config.example.json`

建议第一次先复制：

```powershell
copy .\config.example.json .\config.local.json
```

然后改你自己的本地路径。

---

## 当前需要关注的配置项

```json
{
  "api": {
    "baseUrl": "http://127.0.0.1:9880",
    "host": "127.0.0.1",
    "port": 9880,
    "ttsPath": "/tts"
  },
  "paths": {
    "gptSovitsRoot": "C:\\your-path\\GPT-SoVITS",
    "downloadBase": "C:\\your-path",
    "runtimePython": "runtime\\python.exe",
    "apiScript": "api_v2.py",
    "ttsConfig": "GPT_SoVITS/configs/tts_infer.yaml",
    "outputDir": "output"
  },
  "defaults": {
    "model": "mzk(v2pp)",
    "textLang": "ja",
    "promptText": "こんにちは。これはテストです。",
    "promptLang": "ja"
  }
}
```

---

## 前台启动 API

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-gptsovits-api.ps1
```

这会新开一个可见窗口运行 GPT-SoVITS API。

## 停止 API

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop-gptsovits-api.ps1
```

---

## 快速调用 TTS

```powershell
python .\scripts\tts-gptsovits.py --text "こんにちは。テスト音声です。"
```

或者：

```powershell
python .\scripts\tts-gptsovits.py `
  --model "mzk(v2pp)" `
  --text "こんにちは。テスト音声です。" `
  --text-lang ja `
  --prompt-text "こんにちは。これはテストです。" `
  --prompt-lang ja `
  --out ".\output\tts-output.wav"
```

---

## 备注

- 当前脚本默认直接打本地 GPT-SoVITS API，不走 OpenClaw 内置 tts。
- 现在已经做了基础配置化，但仍然主要面向 Windows 本地环境。
- 如果你准备公开给别人用，下一步应该继续补健康检查、日志和更稳的进程管理。
