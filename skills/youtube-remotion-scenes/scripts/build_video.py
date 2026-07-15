#!/usr/bin/env python3
"""Orquestrador do lab de cenas (embrião da skill). Lê o EDL, renderiza cada cena
(inserção h264 / overlay ProRes 4444 com alpha) e monta no footage via ffmpeg:
overlays primeiro (preservam a timeline), depois inserções (split+concat, alongam).

Uso:  build.py render   |   build.py assemble   |   build.py all
"""
import json, subprocess, os, sys, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
# projeto Remotion desta skill (resolvido relativo a este arquivo, não a um repo fixo)
PROJ = os.path.normpath(os.path.join(BASE, "..", "project"))
# dir de saída dos renders: configurável por env, senão ./drafts/renders (relativo ao cwd)
RENDERS = os.environ.get("YTG_RENDERS_DIR") or os.path.abspath("drafts/renders")
# ffmpeg/ffprobe: resolve pelo PATH (ou env), com fallback ao caminho homebrew do macOS
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = os.environ.get("FFPROBE") or shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
EDL_PATH = next((a for a in sys.argv if a.endswith(".json")), f"{BASE}/edl-vps.json")
EDL = json.load(open(EDL_PATH))
FOOTAGE = EDL["footage"]
FOURK = "4k" in sys.argv
W, H, FPS = (3840, 2160, 30) if FOURK else (1920, 1080, 30)  # 4k: cenas em --scale=2, nativo
PRESET = "veryfast" if FOURK else "medium"  # 4k: veryfast p/ não estourar tempo (YT re-encoda)
CRF = "20" if FOURK else "18"
os.makedirs(RENDERS, exist_ok=True)

def scene_path(i, sc):
    return f"{RENDERS}/scene_{i:02d}_{sc['comp']}.{'mov' if sc['mode']=='partial' else 'mp4'}"

def render():
    for i, sc in enumerate(EDL["scenes"]):
        out = scene_path(i, sc)
        props = json.dumps(sc["props"], ensure_ascii=False)
        cmd = ["npx","remotion","render","src/index.ts", sc["comp"], out]
        cmd += (["--codec=prores","--prores-profile=4444"] if sc["mode"]=="partial"
                else ["--codec=h264","--pixel-format=yuv420p"])
        if FOURK: cmd += ["--scale=2"]   # 1080p comp renderiza nativo em 2160p
        cmd += [f"--props={props}"]
        print(f"[{i:02d}] {sc['comp']} ({sc['mode']}) at {sc['at']}s")
        if subprocess.run(cmd, cwd=PROJ).returncode != 0:
            print(f"  !! FALHOU cena {i}"); sys.exit(1)
    print("== render OK ==")

def dur(path):
    r = subprocess.run([FFPROBE,"-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1", path], capture_output=True, text=True)
    return float(r.stdout.strip())

def assemble():
    # TUDO OVERLAY (nada corta o áudio). Montado em CHUNKS de overlays com intermediários:
    # 18 overlays num filter só estoura memória em 4K. Cada chunk sobrepõe poucos overlays
    # e passa o resultado adiante. Robusto em qualquer resolução.
    scenes = list(enumerate(EDL["scenes"]))
    CHUNK = 9 if not FOURK else 4
    chunks = [scenes[i:i+CHUNK] for i in range(0, len(scenes), CHUNK)]
    final = f"{RENDERS}/vps_montado.mp4"
    src, prev_tmp = FOOTAGE, None
    for ci, chunk in enumerate(chunks):
        last = ci == len(chunks) - 1
        out = final if last else f"{RENDERS}/_tmp_{ci}.mp4"
        inputs = ["-i", src]
        for i,sc in chunk: inputs += ["-i", scene_path(i,sc)]
        # 1ª passada escala o footage p/ WxH; depois o intermediário já está em WxH.
        fc = [f"[0:v]scale={W}:{H},fps={FPS},setsar=1[base]" if ci==0 else "[0:v]setsar=1[base]"]
        cur = "base"
        for k,(i,sc) in enumerate(chunk):
            at = sc["at"]; d = dur(scene_path(i,sc))
            fc.append(f"[{k+1}:v]setpts=PTS-STARTPTS+{at}/TB[o{k}]")
            fc.append(f"[{cur}][o{k}]overlay=0:0:enable='between(t,{at},{at+d:.2f})':eof_action=pass[t{k}]")
            cur = f"t{k}"
        cmd = [FFMPEG,"-y",*inputs,"-filter_complex",";".join(fc),"-map",f"[{cur}]","-map","0:a",
               "-c:v","libx264","-preset",PRESET,"-crf",CRF,"-pix_fmt","yuv420p","-c:a","aac", out]
        print(f"== chunk {ci+1}/{len(chunks)} ({len(chunk)} overlays) -> {out} ==")
        if subprocess.run(cmd).returncode != 0: print(f"!! falhou chunk {ci}"); sys.exit(1)
        if prev_tmp and os.path.exists(prev_tmp): os.remove(prev_tmp)
        src, prev_tmp = out, (None if last else out)
    print(f"== PRONTO: {final} ==")

if __name__ == "__main__":
    # aceita flags soltas ("4k", <edl>.json) em qualquer ordem; a ação é render/assemble/all.
    what = next((a for a in sys.argv[1:] if a in ("render","assemble","all")), "all")
    if what in ("render","all"): render()
    if what in ("assemble","all"): assemble()
