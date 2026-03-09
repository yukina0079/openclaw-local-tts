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

## 本地最简入口：speak.ps1

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\speak.ps1 こんにちは 今日は テストです
```

输出文件：

- `output\speak-latest.wav`

这个脚本适合本地日常用，不用每次手写完整参数。

---

## 完整调用方式

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

## 现在补上的能力

- 基础配置化
- API 健康检查
- 本地一键 `speak.ps1`

如果 API 没启动，`tts-gptsovits.py` 会直接提示你先运行：

- `scripts/start-gptsovits-api.ps1`

---

## 备注

- 当前脚本默认直接打本地 GPT-SoVITS API，不走 OpenClaw 内置 tts。
- 现在已经比较适合本机自己日常使用。
- 如果之后要进一步公开化，还应该继续补更稳的进程管理和更通用的 Python 选择逻辑。
