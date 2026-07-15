#!/usr/bin/env python3
"""
Analisa CANAIS específicos (por @handle): top vídeos por views/dia. Complementa o
benchmark.py (que é por keyword). Usa a Data API (dado público) — só force-ssl basta.

Uso (via o venv do canal):
  "$YTG_CONFIG_DIR/.venv/bin/python" <plugin>/skills/youtube-benchmark/scripts/channel_scan.py \
      --handles "@canalA,@canalB" --per-channel 15 --out benchmark/ref.json
"""
import os, sys, json, re, datetime, argparse
# Importa o yt.py do plugin (scripts/ na raiz do plugin), resolvido relativo a
# este arquivo — nao depende de onde o plugin foi instalado.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from yt import svc  # reusa auth OAuth existente

def parse_dur(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s

def scan(handles, per_channel, out):
    y = svc()
    now = datetime.datetime.now(datetime.timezone.utc)
    rows = []
    for h in handles:
        h = h.strip().lstrip("@")
        ch = y.channels().list(part="contentDetails,snippet,statistics", forHandle=h).execute()
        items = ch.get("items", [])
        if not items:
            print(f"! canal não encontrado: @{h}", file=sys.stderr)
            continue
        c = items[0]
        uploads = c["contentDetails"]["relatedPlaylists"]["uploads"]
        subs = c["statistics"].get("subscriberCount")
        pl = y.playlistItems().list(part="contentDetails", playlistId=uploads,
                                    maxResults=min(per_channel, 50)).execute()
        vids = [it["contentDetails"]["videoId"] for it in pl.get("items", [])]
        for i in range(0, len(vids), 50):
            vr = y.videos().list(part="statistics,snippet,contentDetails",
                                 id=",".join(vids[i:i + 50])).execute()
            for it in vr.get("items", []):
                st, sn, cd = it.get("statistics", {}), it["snippet"], it.get("contentDetails", {})
                dur = parse_dur(cd.get("duration"))
                if dur and dur < 60:  # exclui Shorts
                    continue
                pub = datetime.datetime.fromisoformat(sn["publishedAt"].replace("Z", "+00:00"))
                days = max((now - pub).total_seconds() / 86400.0, 0.5)
                views = int(st.get("viewCount", 0))
                rows.append({
                    "channel": c["snippet"]["title"], "handle": "@" + h, "subs": subs,
                    "videoId": it["id"], "title": sn["title"], "published": sn["publishedAt"][:10],
                    "days": round(days, 1), "views": views, "views_per_day": round(views / days),
                    "likes": int(st.get("likeCount", 0)), "dur_min": round(dur / 60, 1),
                    "url": f"https://youtu.be/{it['id']}",
                })
    rows.sort(key=lambda r: r["views_per_day"], reverse=True)
    json.dump({"generated": now.isoformat(), "channels": handles, "videos": rows},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--handles", required=True)
    ap.add_argument("--per-channel", type=int, default=15)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    scan(a.handles.split(","), a.per_channel, a.out)
