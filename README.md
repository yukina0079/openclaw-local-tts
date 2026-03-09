# openclaw-local-tts

给 OpenClaw 接本地 GPT-SoVITS TTS 的一套最小可用工作流。现在这套仓库的目标很直接：

- 本地前台启动 GPT-SoVITS API
- 用固定脚本调用本地 API 合成语音
- 按模型名自动选择对应目录下的参考音频
- 为后续的“文本 + 音频”回复流程打基础

---

## 当前实现了什么

### 1. 前台启动 / 停止 GPT-SoVITS API
脚本：

- `scripts/start-gptsovits-api.ps1`
- `scripts/stop-gptsovits-api.ps1`

前台启动：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-gptsovits-api.ps1
```

停止：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop-gptsovits-api.ps1
```

默认 API 地址：

- `http://127.0.0.1:9880`

---

### 2. 本地 TTS wrapper
主脚本：

- `scripts/tts-gptsovits.py`

这个脚本会：

- 调用本地 GPT-SoVITS `/tts`
- 按模型文件夹自动选参考音频
- 输出 wav 到指定路径

PowerShell 壳：

- `scripts/tts-gptsovits.ps1`

---

## 使用方法

### 先启动 API

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-gptsovits-api.ps1
```

### 再执行一次 TTS

```powershell
C:\baidunetdiskdownload\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\python.exe `
  .\scripts\tts-gptsovits.py `
  --model "mzk(v2pp)" `
  --text "こんにちは。テスト音声です。" `
  --text-lang ja `
  --prompt-text "こんにちは。これはテストです。" `
  --prompt-lang ja `
  --out ".\output\tts-output.wav"
```

---

## 参数说明

- `--model`：参考音频目录名，对应 `C:\baidunetdiskdownload\<model>`
- `--text`：要合成的文本
- `--text-lang`：合成文本语言，例如 `ja` / `zh` / `en`
- `--prompt-text`：参考音频里实际说的话
- `--prompt-lang`：参考音频语言
- `--ref-audio`：可选，显式指定参考音频路径
- `--out`：输出 wav 路径
- `--speed`：语速

---

## 当前约定

这套仓库目前按以下本地环境写死 / 约定：

- GPT-SoVITS 根目录：
  - `C:\baidunetdiskdownload\GPT-SoVITS-v2pro-20250604-nvidia50`
- 默认参考音色目录：
  - `mzk(v2pp)`
- 当前主要测试语言：
  - `ja`

如果你本地路径不一样，改脚本里的常量即可。

---

## 适合谁

适合这些场景：

- 已经有本地 GPT-SoVITS 环境
- 想把 OpenClaw / 本地 agent 接到本地 TTS
- 不想先搞太复杂的服务编排，只想先跑通

---

## 下一步可以扩展什么

- 自动检测 API 是否存活，不在就自动拉起
- 更智能地选择参考音频
- 把“文本回复 + 音频生成”整合进 agent 回复流
- 增加不同模型/音色的配置文件
- 支持附件自动发送到聊天渠道

---

如果你是从 GitHub 点进来看，这个仓库现在就是一个**能跑的本地 TTS 接线层**，不是大而全的产品。先通路，再慢慢长肉。