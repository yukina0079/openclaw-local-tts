# openclaw-local-tts

给 OpenClaw 接本地 GPT-SoVITS TTS 的一套最小可用工作流。

这套仓库现在主要解决三件事：

- 前台启动本地 GPT-SoVITS API
- 用脚本调用本地 `/tts` 生成音频
- 把原先写死在个人电脑上的路径抽到配置文件里

现在它依然是偏 Windows、本地使用的项目，但至少已经不是“换台电脑就全炸”的状态了。

---

## 仓库结构

- `config.example.json`：配置模板
- `scripts/start-gptsovits-api.ps1`：前台启动本地 API
- `scripts/stop-gptsovits-api.ps1`：停止本地 API
- `scripts/tts-gptsovits.py`：主 TTS wrapper
- `scripts/tts-gptsovits.ps1`：PowerShell 转发壳
- `docs/tts-gptsovits.md`：更详细的中文说明

---

## 先配置

第一次使用前，先复制一份配置：

```powershell
copy .\config.example.json .\config.local.json
```

然后按你自己的环境修改 `config.local.json`，重点看这些字段：

- `paths.gptSovitsRoot`
- `paths.downloadBase`
- `paths.runtimePython`
- `paths.apiScript`
- `paths.ttsConfig`
- `defaults.model`
- `defaults.textLang`
- `defaults.promptText`
- `defaults.promptLang`

默认情况下，脚本会按这个优先级找配置：

1. `config.local.json`
2. `config.json`
3. `config.example.json`

也就是说：
- 你自己本机用时，建议只改 `config.local.json`
- 模板就留在 `config.example.json`

---

## 启动 API

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-gptsovits-api.ps1
```

这会新开一个可见的 cmd 窗口，在前台运行 GPT-SoVITS 的 `api_v2.py`。

停止：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop-gptsovits-api.ps1
```

---

## 执行一次 TTS

```powershell
python .\scripts\tts-gptsovits.py --text "こんにちは。テスト音声です。"
```

如果你不想用系统 `python`，也可以直接用 GPT-SoVITS 自带的 runtime：

```powershell
C:\your\gpt-sovits\runtime\python.exe .\scripts\tts-gptsovits.py --text "こんにちは。テスト音声です。"
```

脚本会：

- 读取配置文件
- 根据 `defaults.model` 去 `downloadBase/<model>` 下找参考音频
- 调本地 API
- 输出 wav 到 `output/`

---

## 常用参数

- `--model`：参考音频目录名
- `--text`：要合成的文本
- `--text-lang`：合成文本语言，例如 `ja` / `zh` / `en`
- `--prompt-text`：参考音频里实际说的话
- `--prompt-lang`：参考音频语言
- `--ref-audio`：显式指定参考音频路径
- `--out`：输出 wav 路径
- `--speed`：语速

---

## 这个项目现在适合什么场景

适合：

- 你本地已经有 GPT-SoVITS
- 你主要在 Windows 上用
- 你想快速给 OpenClaw / 本地 agent 接一层本地 TTS
- 你接受“先能跑，再慢慢工程化”

不适合：

- 想 clone 完零配置直接运行
- 想直接跨平台通吃
- 想要完整的服务治理、日志、守护进程、GUI 配置面板

---

## 目前相比第一版改了什么

- 不再把核心路径硬编码死在脚本里
- 增加 `config.example.json`
- 启动/停止/TTS wrapper 都改成优先读配置
- README 改成配置驱动的写法

---

## 下一步还能继续做

- 增加 `config.local.json` 自动忽略（gitignore）
- TTS 前先做 API 健康检查
- 更稳的进程管理（例如 PID 文件）
- 更智能的参考音频选择策略
- 直接和 OpenClaw 回复流绑定成“文本 + 音频”

如果你现在点进这个仓库，它已经不只是“我电脑上的一坨脚本”，而是一个勉强像样一点的本地 TTS 接线层了。