# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Local TTS

- Engine: GPT-SoVITS local API
- API root: `http://127.0.0.1:9880`
- Project root: `C:\baidunetdiskdownload\GPT-SoVITS-v2pro-20250604-nvidia50`
- Runtime Python: `C:\baidunetdiskdownload\GPT-SoVITS-v2pro-20250604-nvidia50\runtime\python.exe`
- Start API (foreground): `C:\Users\35252\.openclaw\workspace\scripts\start-gptsovits-api.ps1`
- Stop API: `C:\Users\35252\.openclaw\workspace\scripts\stop-gptsovits-api.ps1`
- Main wrapper: `C:\Users\35252\.openclaw\workspace\scripts\tts-gptsovits.py`
- Preferred voice folder: `mzk(v2pp)`
- Default TTS language for this flow: `ja`
- For model-folder based voice selection, pick the matching folder under `C:\baidunetdiskdownload\<model>` and auto-select the first sample if no explicit ref audio is given.
- User wants: text + audio, not audio-only.
