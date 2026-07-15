#!/usr/bin/env python3
"""Transcreve um MP4 local com timestamps (SRT), rápido e privado (Apple Silicon).
Extrai o áudio e roda o mlx-whisper no Neural Engine — não sobe o vídeo pra lugar nenhum.

Uso:  transcribe.py <video.mp4> [saida.srt]
Requer: ffmpeg + mlx-whisper (uv pip install --python <venv> mlx-whisper).
Depois: leia o SRT e ache o SEGUNDO EXATO de cada fala-chave (grep pela palavra) —
é o `at` de cada cena no EDL. A cena reforça a fala NO MOMENTO em que ela é dita.
"""
import subprocess, sys, os, shutil

# ffmpeg pelo PATH (ou env), com fallback ao caminho homebrew do macOS
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"

def main():
    video = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(video)[0] + ".srt"
    wav = "/tmp/_transcribe_audio.wav"
    subprocess.run([FFMPEG,"-y","-i",video,"-ar","16000","-ac","1",
                    "-c:a","pcm_s16le",wav], check=True, capture_output=True)
    # large-v3-turbo: ótimo custo/qualidade em pt; ~1 min p/ 23 min de áudio no M-series.
    subprocess.run([sys.executable.replace("python","mlx_whisper"), wav,
                    "--model","mlx-community/whisper-large-v3-turbo","--language","pt",
                    "--output-dir", os.path.dirname(out) or ".",
                    "--output-name", os.path.splitext(os.path.basename(out))[0],
                    "--output-format","srt"], check=True)
    print(f"SRT: {out}")

if __name__ == "__main__":
    main()
