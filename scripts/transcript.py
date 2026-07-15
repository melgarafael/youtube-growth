#!/usr/bin/env python3
"""Extrai a transcrição de um vídeo do YouTube e consolida em janelas de tempo.

Estratégia em dois níveis (a lição central da skill):
  1. yt-dlp com auto-subs  -> funciona para vídeos PÚBLICOS, sem autenticação.
  2. API captions().download do DONO -> funciona para vídeos PRIVADOS/AGENDADOS,
     onde cookies de navegador falham (canal de marca). Requer token OAuth
     (ver yt_auth.py). Baixa até a legenda automática (ASR).

Uso:
  transcript.py <videoId> [janela_seg]      # tenta público, cai pro dono
  transcript.py <videoId> --owner           # força a via da API do dono

Saída: imprime linhas "[MM:SS] texto" (janelas ~40s) e salva em /tmp/tr_<id>.txt
"""
import os, re, sys, subprocess, tempfile

def consolidate(srt_text, window=40):
    blocks = re.split(r"\n\n+", srt_text.strip())
    last, out = "", []
    for b in blocks:
        L = b.strip().split("\n")
        if len(L) < 2:
            continue
        m = re.search(r"(\d\d):(\d\d):(\d\d)", L[1])
        if not m:
            continue
        s = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        t = re.sub(r"<[^>]+>", "", " ".join(L[2:])).strip()
        if t and t != last:
            out.append((s, t)); last = t
    buf, ws, res = [], 0, []
    for s, t in out:
        if not buf:
            ws = s
        buf.append(t)
        if s - ws >= window:
            res.append((ws, " ".join(buf))); buf = []
    if buf:
        res.append((ws, " ".join(buf)))
    return res

def via_ytdlp(vid):
    """Público: baixa auto-sub pt via yt-dlp. Retorna srt text ou None."""
    tmp = tempfile.mktemp()
    subprocess.run(["yt-dlp", "--no-warnings", "--skip-download", "--write-auto-subs",
                    "--sub-langs", "pt-orig,pt", "--sub-format", "srt", "--convert-subs", "srt",
                    "-o", tmp + ".%(ext)s", f"https://youtu.be/{vid}"],
                   capture_output=True)
    for ext in ("pt-orig", "pt"):
        p = f"{tmp}.{ext}.srt"
        if os.path.exists(p):
            return open(p, encoding="utf-8").read()
    return None

def via_owner_api(vid):
    """Privado/agendado: baixa via API captions do dono (inclui ASR)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from yt import svc
    y = svc()
    tracks = y.captions().list(part="snippet", videoId=vid).execute().get("items", [])
    if not tracks:
        return None
    # prefere pt; senão a primeira
    track = next((t for t in tracks if t["snippet"].get("language", "").startswith("pt")), tracks[0])
    data = y.captions().download(id=track["id"], tfmt="srt").execute()
    return data.decode("utf-8") if isinstance(data, bytes) else data

def main():
    vid = sys.argv[1]
    force_owner = "--owner" in sys.argv
    window = next((int(a) for a in sys.argv[2:] if a.isdigit()), 40)
    srt = None
    if not force_owner:
        srt = via_ytdlp(vid)
        if srt:
            print("# fonte: yt-dlp (público)", file=sys.stderr)
    if srt is None:
        srt = via_owner_api(vid)
        if srt:
            print("# fonte: API captions do dono (privado/agendado OK)", file=sys.stderr)
    if not srt:
        print("ERRO: sem legenda disponível (nem pública nem via API do dono).", file=sys.stderr)
        sys.exit(1)
    res = consolidate(srt, window)
    out_path = f"/tmp/tr_{vid}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        for s, t in res:
            line = f"[{s//60:02d}:{s%60:02d}] {t}"
            print(line[:200])          # preview no terminal (truncado p/ não poluir)
            f.write(line + "\n")        # arquivo é a fonte de verdade: texto COMPLETO
    print(f"\n# {len(res)} janelas salvas em {out_path}", file=sys.stderr)

if __name__ == "__main__":
    main()
