# Gemini CLI 转发桥

## 目标

把本机已经登录可用的 Gemini CLI 当作一个可复用后端：

- 你发内容
- 本地脚本转给 Gemini CLI
- 拿到结果
- 后续可以继续接 TTS

---

## 最简单用法

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\gemini-forward.ps1 解释一下红黑树
```

或者直接：

```powershell
python .\scripts\gemini-forward.py --prompt "解释一下红黑树"
```

---

## 输出

- 控制台打印 Gemini 返回文本
- 同时保存到：
  - `output\gemini-latest.txt`

---

## Gemini + TTS 串联

如果你想本地直接走“Gemini 文本 -> GPT-SoVITS 音频”：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\gemini-tts.ps1 用中文简洁解释一下红黑树
```

这会：

1. 先调用 Gemini CLI
2. 把文本保存到 `output\gemini-latest.txt`
3. 再调用本地 GPT-SoVITS
4. 输出音频到 `output\gemini-tts-latest.wav`

---

## 后续可扩展

- 加对话历史/记忆注入
- 对不同任务自动切模型
- 真正接到 OpenClaw 的文本+音频回复流里
