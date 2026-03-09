import argparse
import json
import sys
from pathlib import Path
from urllib import request, error
from typing import Optional


REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_CANDIDATES = [
    REPO_ROOT / "config.local.json",
    REPO_ROOT / "config.json",
    REPO_ROOT / "config.example.json",
]


def load_config():
    for path in CONFIG_CANDIDATES:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return json.load(f), path
    raise FileNotFoundError("No config file found. Please create config.local.json or config.json from config.example.json")


def resolve_path(base: Path, value: str) -> Path:
    p = Path(value)
    return p if p.is_absolute() else (base / p).resolve()


def check_api_health(base_url: str) -> bool:
    candidates = [base_url.rstrip("/"), base_url.rstrip("/") + "/docs"]
    for url in candidates:
        try:
            with request.urlopen(url, timeout=3) as resp:
                if 200 <= getattr(resp, "status", 200) < 500:
                    return True
        except Exception:
            pass
    return False


def pick_ref(download_base: Path, model_name: str, explicit_ref: Optional[str]) -> Path:
    if explicit_ref:
        p = Path(explicit_ref)
        if not p.exists():
            raise FileNotFoundError(f"ref audio not found: {p}")
        return p
    voice_dir = download_base / model_name
    if not voice_dir.exists():
        raise FileNotFoundError(f"voice dir not found: {voice_dir}")
    wavs = sorted([p for p in voice_dir.iterdir() if p.is_file() and p.suffix.lower() in {'.wav', '.mp3', '.flac'}])
    if not wavs:
        raise FileNotFoundError(f"no audio samples found in: {voice_dir}")
    return wavs[0]


def synthesize(api_url, text, text_lang, prompt_text, prompt_lang, ref_audio, out_path, speed):
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
    req = request.Request(api_url, data=data, headers={"Content-Type": "application/json"}, method="POST")
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


if __name__ == "__main__":
    try:
        cfg, cfg_path = load_config()
        api = cfg["api"]
        paths = cfg["paths"]
        defaults = cfg["defaults"]

        ap = argparse.ArgumentParser(description="GPT-SoVITS local TTS wrapper")
        ap.add_argument("--model", default=defaults.get("model", "mzk(v2pp)"))
        ap.add_argument("--text", default=defaults.get("text", "こんにちは。テストです。"))
        ap.add_argument("--text-lang", default=defaults.get("textLang", "ja"))
        ap.add_argument("--prompt-text", default=defaults.get("promptText", "こんにちは。これはテストです。"))
        ap.add_argument("--prompt-lang", default=defaults.get("promptLang", "ja"))
        ap.add_argument("--ref-audio", default=None)
        ap.add_argument("--out", default=str((REPO_ROOT / paths.get("outputDir", "output") / "tts-output.wav").resolve()))
        ap.add_argument("--speed", type=float, default=float(defaults.get("speed", 1.0)))
        ap.add_argument("--skip-health-check", action="store_true")
        args = ap.parse_args()

        download_base = resolve_path(REPO_ROOT, paths["downloadBase"])
        api_base = api["baseUrl"].rstrip("/")
        api_url = api_base + api.get("ttsPath", "/tts")

        if not args.skip_health_check and not check_api_health(api_base):
            raise RuntimeError("GPT-SoVITS API is not reachable. Please start it first with scripts/start-gptsovits-api.ps1")

        ref = pick_ref(download_base, args.model, args.ref_audio)
        out = Path(args.out)
        synthesize(api_url, args.text, args.text_lang, args.prompt_text, args.prompt_lang, ref, out, args.speed)
        print(f"CONFIG={cfg_path}")
        print(f"REF={ref}")
        print(f"OUT={out}")
        print(f"SIZE={out.stat().st_size}")
    except Exception as e:
        print(f"ERROR={e}", file=sys.stderr)
        sys.exit(1)
