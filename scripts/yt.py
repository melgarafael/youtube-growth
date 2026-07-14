#!/usr/bin/env python3
"""Utilitário YouTube Data API v3: whoami, get, update-desc, set-captions."""
import os, sys, json, datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE = os.environ.get("YTG_CONFIG_DIR") or os.path.expanduser("~/.youtube-seo")
TOKEN = os.path.join(BASE, "token.json")
# Escopos DESEJADOS (o yt_auth.py pede estes ao reautorizar). force-ssl = editar
# metadados/legendas; yt-analytics = CTR/retenção/inscritos; monetary = receita/RPM.
# _creds() NÃO força esta lista: usa os escopos que o token REALMENTE tem (do arquivo),
# senão o refresh quebra com invalid_scope enquanto o token ainda não foi ampliado.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/yt-analytics.readonly",
          "https://www.googleapis.com/auth/yt-analytics-monetary.readonly"]

def _creds():
    creds = Credentials.from_authorized_user_file(TOKEN)  # scopes vêm do token
    if creds.expired and creds.refresh_token:
        creds.refresh(Request()); open(TOKEN, "w").write(creds.to_json())
    return creds

def svc():
    return build("youtube", "v3", credentials=_creds())

def yta():
    """Serviço da YouTube Analytics API v2 (CTR/retenção/receita)."""
    return build("youtubeAnalytics", "v2", credentials=_creds())

def whoami():
    y = svc()
    r = y.channels().list(part="snippet,statistics", mine=True).execute()
    for c in r.get("items", []):
        s, st = c["snippet"], c["statistics"]
        print(f"CANAL: {s['title']}  (id {c['id']})")
        print(f"inscritos: {st.get('subscriberCount')} | videos: {st.get('videoCount')} | views totais: {st.get('viewCount')}")

def get(vid):
    y = svc()
    r = y.videos().list(part="snippet", id=vid).execute()
    it = r["items"][0]["snippet"]
    print(json.dumps({
        "title": it["title"], "categoryId": it.get("categoryId"),
        "defaultLanguage": it.get("defaultLanguage"),
        "defaultAudioLanguage": it.get("defaultAudioLanguage"),
        "tags": it.get("tags", []),
        "description": it["description"],
    }, ensure_ascii=False, indent=2))

def update_desc(vid, descfile):
    """Atualiza SÓ a descrição, preservando title/categoryId/tags/idioma."""
    y = svc()
    cur = y.videos().list(part="snippet", id=vid).execute()["items"][0]["snippet"]
    new_desc = open(descfile, encoding="utf-8").read()
    body = {"id": vid, "snippet": {
        "title": cur["title"],
        "categoryId": cur.get("categoryId", "22"),
        "description": new_desc,
    }}
    for k in ("tags", "defaultLanguage", "defaultAudioLanguage"):
        if cur.get(k): body["snippet"][k] = cur[k]
    y.videos().update(part="snippet", body=body).execute()
    print("DESCRICAO ATUALIZADA:", vid)

def recent(n=8):
    """Lista uploads recentes do dono, incluindo privados/agendados."""
    y = svc()
    r = y.search().list(part="id", forMine=True, type="video", order="date", maxResults=int(n)).execute()
    ids = [it["id"]["videoId"] for it in r.get("items", [])]
    if not ids:
        print("nenhum video"); return
    v = y.videos().list(part="snippet,status,contentDetails", id=",".join(ids)).execute()
    for it in v["items"]:
        s, st, cd = it["snippet"], it["status"], it["contentDetails"]
        print(f"{it['id']} | {st.get('privacyStatus')} | publishAt={st.get('publishAt')} | {cd.get('duration')} | {s['title'][:60]}")

def set_snippet(vid, jsonfile):
    """Atualiza titulo+descricao+tags+categoryId a partir de um JSON."""
    y = svc()
    cur = y.videos().list(part="snippet", id=vid).execute()["items"][0]["snippet"]
    new = json.load(open(jsonfile, encoding="utf-8"))
    sn = {"title": new.get("title", cur["title"]),
          "categoryId": new.get("categoryId", cur.get("categoryId", "22")),
          "description": new["description"],
          "tags": new.get("tags", cur.get("tags", []))}
    for k in ("defaultLanguage", "defaultAudioLanguage"):
        if new.get(k) or cur.get(k): sn[k] = new.get(k) or cur[k]
    y.videos().update(part="snippet", body={"id": vid, "snippet": sn}).execute()
    print("SNIPPET ATUALIZADO:", vid, "| titulo:", sn["title"][:50], "| tags:", len(sn["tags"]))

def set_caption(vid, srtfile, lang="pt", name="pt-corrigida"):
    y = svc()
    body = {"snippet": {"videoId": vid, "language": lang, "name": name, "isDraft": False}}
    media = MediaFileUpload(srtfile, mimetype="application/octet-stream", resumable=False)
    y.captions().insert(part="snippet", body=body, media_body=media).execute()
    print("LEGENDA ENVIADA:", vid, lang)

# ---------------------------------------------------------------------------
# Analytics API (CTR, retenção, inscritos, receita) — precisa dos escopos
# yt-analytics(.monetary).readonly no token. Se falhar por escopo, reautorizar
# rodando a skill `connect` (ou, manualmente, com YTG_CONFIG_DIR setado:
#   $YTG_CONFIG_DIR/.venv/bin/python <plugin>/scripts/yt_auth.py)
# ---------------------------------------------------------------------------

def _report(metrics, days, video=None):
    """Roda reports.query e devolve {coluna: valor}. Linha vazia -> zeros."""
    end = datetime.date.today()
    start = end - datetime.timedelta(days=int(days))
    kw = dict(ids="channel==MINE", startDate=start.isoformat(),
              endDate=end.isoformat(), metrics=",".join(metrics))
    if video:
        kw["filters"] = f"video=={video}"
    r = yta().reports().query(**kw).execute()
    headers = [h["name"] for h in r.get("columnHeaders", [])]
    rows = r.get("rows", [])
    return dict(zip(headers, rows[0])) if rows else {m: 0 for m in metrics}

# blocos separados: sem escopo monetário não há 'receita'. NOTA: impressions/CTR NÃO são
# expostas pela Analytics API (só no YouTube Studio) — por isso não entram aqui.
_BLOCKS = {
    "core": ["views", "estimatedMinutesWatched", "averageViewDuration",
             "averageViewPercentage", "subscribersGained", "subscribersLost", "likes"],
    "receita": ["estimatedRevenue", "playbackBasedCpm", "cpm"],
}

def _collect(days, video=None):
    """Junta os blocos; cada bloco falha isolado e o motivo é reportado, não engolido."""
    from googleapiclient.errors import HttpError
    out = {}
    for name, mets in _BLOCKS.items():
        try:
            out.update(_report(mets, days, video=video))
        except HttpError as e:
            reason = getattr(e, "reason", None) or str(e)
            print(f"  [bloco {name}] indisponível: {reason}")
    return out

def _fmt(v):
    g = lambda k: v.get(k, 0)
    avg = int(g("averageViewDuration") or 0)
    print(f"views: {g('views')} | minutos assistidos: {g('estimatedMinutesWatched')}")
    print(f"retenção média: {g('averageViewPercentage')}% | duração média assistida: {avg//60}:{avg%60:02d}")
    print(f"inscritos: +{g('subscribersGained')} / -{g('subscribersLost')} | likes: {g('likes')}")
    print("(CTR de impressões: só no YouTube Studio — a Analytics API não expõe)")
    if "estimatedRevenue" in v:
        print(f"receita estimada: {g('estimatedRevenue')} | RPM: {g('playbackBasedCpm')} | CPM: {g('cpm')}  (moeda da conta AdSense)")
    else:
        print("receita: sem dado (escopo monetário ausente ou canal sem monetização no período)")

def analytics(vid, days=28):
    print(f"== ANALYTICS · vídeo {vid} · últimos {days} dias ==")
    _fmt(_collect(days, video=vid))

def channel_analytics(days=28):
    print(f"== ANALYTICS · CANAL · últimos {days} dias ==")
    _fmt(_collect(days))

if __name__ == "__main__":
    cmd = sys.argv[1]
    {"whoami": lambda: whoami(),
     "get": lambda: get(sys.argv[2]),
     "recent": lambda: recent(sys.argv[2] if len(sys.argv) > 2 else 8),
     "update-desc": lambda: update_desc(sys.argv[2], sys.argv[3]),
     "set-snippet": lambda: set_snippet(sys.argv[2], sys.argv[3]),
     "set-caption": lambda: set_caption(sys.argv[2], sys.argv[3]),
     "analytics": lambda: analytics(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 28),
     "channel": lambda: channel_analytics(sys.argv[2] if len(sys.argv) > 2 else 28)}[cmd]()
