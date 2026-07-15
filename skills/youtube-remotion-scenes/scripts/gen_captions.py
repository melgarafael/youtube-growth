#!/usr/bin/env python3
"""Legendas animadas word-by-word (estilo Hormozi) a partir do JSON word-timestamps
do mlx-whisper. Gera um .ass leve (queimado com ffmpeg, sem Remotion — 23 min é
impraticável frame-a-frame). Identidade Dossiê: sans bold, branco + contorno preto
grosso, palavra ATIVA em amarelo, embaixo-centro (não tampa o PIP no canto direito).

Uso:  gen_captions.py <words.json> <saida.ass>
Queimar:  ffmpeg -i video.mp4 -vf "subtitles=saida.ass" -c:a copy out.mp4
"""
import json, sys

AMAR = "&H0027E5EE&"   # amarelo #EEE527 em BGR (marca-texto Dossiê)
BRANCO = "&H00FFFFFF&"
MAXW = 3               # palavras visíveis por vez
GAP = 0.6             # pausa (s) que fecha o grupo

def ts(s):
    h=int(s//3600); m=int((s%3600)//60); sec=s%60
    return f"{h:d}:{m:02d}:{sec:05.2f}"

def esc(t):
    return t.strip().replace("{","(").replace("}",")").replace("\\","")

def group(words):
    """agrupa palavras em blocos de até MAXW, quebrando em pausas."""
    groups, cur = [], []
    for w in words:
        if cur and (len(cur) >= MAXW or w["start"] - cur[-1]["end"] > GAP):
            groups.append(cur); cur = []
        cur.append(w)
    if cur: groups.append(cur)
    return groups

def main():
    src, out = sys.argv[1], sys.argv[2]
    d = json.load(open(src))
    words = [w for s in d.get("segments", []) for w in s.get("words", []) if w.get("word", "").strip()]
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap, Arial, 74, {BRANCO}, &H00000000&, &H64000000&, 1, 5, 2, 2, 200, 200, 150, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for g in group(words):
        for i, w in enumerate(g):
            start = w["start"]
            end = g[i+1]["start"] if i+1 < len(g) else w["end"]
            # monta o texto do grupo com a palavra ativa em amarelo
            parts = []
            for j, ww in enumerate(g):
                txt = esc(ww["word"])
                parts.append(f"{{\\c{AMAR}}}{txt}{{\\c{BRANCO}}}" if j == i else txt)
            text = " ".join(parts)
            lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Cap,,0,0,0,,{text}")
    open(out, "w", encoding="utf-8").write(header + "\n".join(lines) + "\n")
    print(f"{len(words)} palavras -> {out}")

if __name__ == "__main__":
    main()
