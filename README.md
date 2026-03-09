# openclaw-local-tts

给 OpenClaw 接本地 GPT-SoVITS TTS 的一套最小可用工作流。

这套仓库现在主要解决五件事：

- 前台启动本地 GPT-SoVITS API
- 用脚本调用本地 `/tts` 生成音频
- 把原先写死在个人电脑上的路径抽到配置文件里
- 给本地使用补一个更顺手的一键 speak 脚本
- 提供 Gemini CLI -> GPT-SoVITS 的本地串联桥

现在它依然是偏 Windows、本地使用的项目，但已经从“只能我自己临时调通”进化到“能持续复用”。

---

## 仓库结构

- `config.example.json`：配置模板
- `scripts/start-gptsovits-api.ps1`：前台启动本地 API
- `scripts/stop-gptsovits-api.ps1`：停止本地 API
- `scripts/tts-gptsovits.py`：主 TTS wrapper
- `scripts/tts-gptsovits.ps1`：PowerShell 转发壳
- `scripts/speak.ps1`：本地一键说话脚本
- `scripts/gemini-forward.py`：Gemini CLI 转发桥
- `scripts/gemini-forward.ps1`：Gemini CLI PowerShell 入口
- `scripts/gemini-tts.ps1`：Gemini -> TTS 串联脚本
- `docs/tts-gptsovits.md`：本地 TTS 说明
- `docs/gemini-forward.md`：Gemini 转发桥说明

---

## 先配置

第一次使用前，先复制一份配置：

```powershell
copy .\config.example.json .\config.local.json
```

然后按你自己的环境修改 `config.local.json`。

---

## 启动 GPT-SoVITS API

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-gptsovits-api.ps1
```

停止：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\stop-gptsovits-api.ps1
```

---

## 本地最简 TTS

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\speak.ps1 こんにちは 今日は テストです
```

输出：

- `output\speak-latest.wav`

---

## Gemini CLI 转发

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\gemini-forward.ps1 解释一下红黑树
```

输出：

- 控制台文本
- `output\gemini-latest.txt`

---

## Gemini -> TTS 串联

如果你想直接走：

**你输入问题 -> Gemini CLI 生成文本 -> GPT-SoVITS 生成音频**

可以用：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\gemini-tts.ps1 用中文简洁解释一下红黑树
```

输出：

- 文本：`output\gemini-latest.txt`
- 音频：`output\gemini-tts-latest.wav`

这个就是当前最实用的本地“文本 + 音频”桥。

---

## 当前状态总结

### 已经可用
- 本地 GPT-SoVITS TTS
- 配置化路径管理
- 本地一键 speak
- Gemini CLI 转发桥
- Gemini -> TTS 串联

### 还没完全打通
- OpenClaw 当前聊天界面里自动把本地 wav 作为附件一起回传
- ACP + Gemini 作为正式 runtime 的完整闭环

所以现在这仓库的定位很明确：

**先把本地可用链打通，再慢慢做更深的 OpenClaw 集成。**
