import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "output"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def resolve_gemini() -> str:
    candidates = [
        shutil.which("gemini"),
        shutil.which("gemini.cmd"),
        str(Path.home() / "AppData" / "Roaming" / "npm" / "gemini.cmd"),
        str(Path.home() / "AppData" / "Roaming" / "npm" / "gemini"),
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    raise FileNotFoundError("gemini CLI not found")


def run_gemini(prompt: str, model: str | None = None) -> str:
    gemini = resolve_gemini()
    cmd = [gemini]
    if model:
        cmd += ["--model", model]
    cmd += ["-p", prompt]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(REPO_ROOT), shell=False)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or f"gemini exited with code {proc.returncode}").strip())
    return proc.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description="Forward a prompt to local Gemini CLI")
    ap.add_argument("--prompt", required=True, help="Prompt text for Gemini CLI")
    ap.add_argument("--model", default=None, help="Optional Gemini model")
    ap.add_argument("--save", default=str(OUT_DIR / "gemini-latest.txt"), help="Optional output file path")
    args = ap.parse_args()

    text = run_gemini(args.prompt, args.model)
    out = Path(args.save)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n[SAVED] {out}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
