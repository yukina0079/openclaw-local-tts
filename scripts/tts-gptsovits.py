import argparse
import json
import sys
from pathlib import Path
from urllib import request, error
from typing import Optional

DOWNLOAD_BASE = Path(r"C:\baidunetdiskdownload")
API_URL = "http://127.0.0.1:9880/tts"
DEFAULT_TEXT = "こんにちは。テスト音声です。今日はいい感じに話せています。"


def pick_ref(model_name: str, explicit_ref: Optional[str]) -> Path:
    if explicit_ref:
        p = Path(explicit_ref)
        if not p.exists():
            raise FileNotFoundError(f"ref audio not found: {p}")
        return p
    voice_dir = DOWNLOAD_BASE / model_name
    if not voice_dir.exists():
        raise FileNotFoundError(f"voice dir not found: {voice_dir}")
    wavs = sorted([p for p in voice_dir.iterdir() if p.is_file() and p.suffix.lower() in {'.wav', '.mp3', '.flac'}])
    if not wavs:
        raise FileNotFoundError(f"no audio samples found in: {voice_dir}")
    return wavs[0]


def synthesize(text, text_lang, prompt_text, prompt_lang, ref_audio, out_path, speed):
    payload = {
        "text": text,
        "text_lang": text_lang,
        "ref_audio_path": str(ref_audio),
        "prompt_lang": prompt_lang,
        "prompt_text": prompt_text,
        "text_split_method": "cut5",
        "batch_size": 1,
        "media_type": "wav",
        "streaming_mode": False,
        "speed_factor": speed,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(API_URL, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=300) as resp:
            audio = resp.read()
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")
    except Exception as e:
        raise RuntimeError(f"request failed: {e}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(audio)


def main():
    ap = argparse.ArgumentParser(description="GPT-SoVITS local TTS wrapper")
    ap.add_argument("--model", default="mzk(v2pp)", help="voice/model folder name under C:\\baidunetdiskdownload")
    ap.add_argument("--text", default=DEFAULT_TEXT, help="text to synthesize")
    ap.add_argument("--text-lang", default="ja", help="target text language, e.g. ja/zh/en")
    ap.add_argument("--prompt-text", default="こんにちは。これはテストです。", help="transcript for reference audio")
    ap.add_argument("--prompt-lang", default="ja", help="reference prompt language")
    ap.add_argument("--ref-audio", default=None, help="explicit reference audio path")
    ap.add_argument("--out", default=str(Path.cwd() / "output" / "tts-output.wav"), help="output wav path")
    ap.add_argument("--speed", type=float, default=1.0, help="speed factor")
    args = ap.parse_args()

    ref = pick_ref(args.model, args.ref_audio)
    out = Path(args.out)
    synthesize(args.text, args.text_lang, args.prompt_text, args.prompt_lang, ref, out, args.speed)
    print(f"REF={ref}")
    print(f"OUT={out}")
    print(f"SIZE={out.stat().st_size}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR={e}", file=sys.stderr)
        sys.exit(1)
