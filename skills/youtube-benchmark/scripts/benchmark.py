#!/usr/bin/env python3
"""
Benchmark de concorrentes no YouTube para o canal do usuario.

Coleta a parte DETERMINISTICA (dado duro): dado um conjunto de keywords do nicho,
acha os videos que estao subindo AGORA (ranqueados por views/dia desde a
publicacao), baixa as thumbnails dos top e extrai os padroes de SEO (frequencia
de palavras em titulos, tags recorrentes).

O JULGAMENTO fica com o agente: ler as thumbs baixadas (visualmente, via Read),
comparar com as do canal e escrever as 3 recomendacoes na voz do canal (definida
no onboarding). Nao fazemos visao computacional aqui — heuristica de cor/rosto em
v1 seria fragil e generica; analise visual delegada ao modelo multimodal.

Usa a MESMA credencial OAuth do dono (token da skill `connect`, scope force-ssl).
search.list/videos.list leem dados publicos de qualquer canal com essa credencial
— nao precisa de API key separada. Quota: search.list ~100 unid/chamada; o projeto
tem 10k/dia. Por isso ha --max-keywords e cache.

Config: resolve o dir de credenciais por $YTG_CONFIG_DIR (setado pela skill
`connect`/`bin/yt`), caindo no legado ~/.youtube-seo se a var nao estiver setada.

Uso (via o venv do canal):
  "$YTG_CONFIG_DIR/.venv/bin/python" <plugin>/skills/youtube-benchmark/scripts/benchmark.py collect \
      --keywords "keyword A,keyword B,keyword C" --per-keyword 15 --top 20 --out benchmark

Saida:
  benchmark/<slug>-<data>/dados.json     dados brutos ranqueados
  benchmark/<slug>-<data>/thumbs/*.jpg   thumbs dos top N
  benchmark/<slug>-<data>/RELATORIO.md   relatorio com dados + secao de recs p/ o agente preencher
"""
import os, sys, json, re, argparse, urllib.request, datetime, collections

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Resolve o dir de config/credencial igual ao yt.py do plugin: prioriza
# $YTG_CONFIG_DIR (por-canal, setado pela skill connect) e cai no legado.
BASE = os.environ.get("YTG_CONFIG_DIR") or os.path.expanduser("~/.youtube-seo")
TOKEN = os.path.join(BASE, "token.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# stopwords PT/EN para nao poluir a frequencia de palavras dos titulos
STOP = set("""a o e de da do das dos em no na nos nas um uma para por com que se sua seu
seus suas como qual quais mais menos ja nao sim the a an of to in on for and or with your you
how what why is are my me eu voce vc pra pro ao aos das dos isso esse essa este esta""".split())


def svc():
    creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        open(TOKEN, "w").write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def parse_duration(iso):
    """PT#H#M#S -> segundos. Retorna 0 se nao parsear (live/sem duracao)."""
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def days_since(published_iso, now):
    dt = datetime.datetime.fromisoformat(published_iso.replace("Z", "+00:00"))
    return max((now - dt).total_seconds() / 86400.0, 0.5)  # piso 0.5d evita div por ~0


def search_ids(y, keyword, n):
    """search.list por relevancia recente. Retorna videoIds (dedup)."""
    r = y.search().list(
        part="id", q=keyword, type="video", order="relevance",
        maxResults=min(int(n), 50), relevanceLanguage="pt", regionCode="BR",
    ).execute()
    return [it["id"]["videoId"] for it in r.get("items", []) if it["id"].get("videoId")]


def hydrate(y, ids):
    """videos.list em lotes de 50 -> statistics+snippet+contentDetails."""
    out = []
    for i in range(0, len(ids), 50):
        r = y.videos().list(
            part="statistics,snippet,contentDetails", id=",".join(ids[i:i + 50])
        ).execute()
        out.extend(r.get("items", []))
    return out


def collect(args):
    y = svc()
    now = datetime.datetime.now(datetime.timezone.utc)
    own_channel = args.own_handle or "seu canal"

    keywords = []
    if args.keywords_file:
        keywords = [l.strip() for l in open(args.keywords_file, encoding="utf-8") if l.strip()]
    if args.keywords:
        keywords += [k.strip() for k in args.keywords.split(",") if k.strip()]
    keywords = keywords[: args.max_keywords]
    if not keywords:
        sys.exit("erro: passe --keywords ou --keywords-file")

    # 1) coleta ids por keyword (dedup global, guardando de qual kw veio)
    id_to_kw, all_ids = {}, []
    for kw in keywords:
        for vid in search_ids(y, kw, args.per_keyword):
            if vid not in id_to_kw:
                id_to_kw[vid] = kw
                all_ids.append(vid)
    print(f"coletados {len(all_ids)} videos unicos de {len(keywords)} keywords", file=sys.stderr)

    # 2) hidrata e ranqueia por views/dia
    rows = []
    for it in hydrate(y, all_ids):
        st, sn, cd = it.get("statistics", {}), it["snippet"], it.get("contentDetails", {})
        views = int(st.get("viewCount", 0))
        dur = parse_duration(cd.get("duration"))
        if dur and dur < 60:  # descarta Shorts — outro jogo, distorce o benchmark
            continue
        d = days_since(sn["publishedAt"], now)
        rows.append({
            "videoId": it["id"],
            "title": sn["title"],
            "channel": sn["channelTitle"],
            "channelId": sn["channelId"],
            "published": sn["publishedAt"][:10],
            "days": round(d, 1),
            "views": views,
            "views_per_day": round(views / d),
            "likes": int(st.get("likeCount", 0)),
            "comments": int(st.get("commentCount", 0)),
            "duration_s": dur,
            "tags": sn.get("tags", []),
            "keyword": id_to_kw[it["id"]],
            "url": f"https://youtu.be/{it['id']}",
        })
    rows.sort(key=lambda r: r["views_per_day"], reverse=True)
    top = rows[: args.top]

    # 3) pasta de saida
    slug = re.sub(r"[^a-z0-9]+", "-", keywords[0].lower())[:30].strip("-")
    stamp = now.strftime("%Y-%m-%d")
    outdir = os.path.join(args.out, f"{slug}-{stamp}")
    thumbsdir = os.path.join(outdir, "thumbs")
    os.makedirs(thumbsdir, exist_ok=True)

    # 4) baixa thumbs dos top (maxres, cai p/ hqdefault se nao houver)
    for i, r in enumerate(top, 1):
        vid = r["videoId"]
        dest = os.path.join(thumbsdir, f"{i:02d}_{vid}.jpg")
        for q in ("maxresdefault", "hqdefault"):
            try:
                urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{vid}/{q}.jpg", dest)
                r["thumb"] = os.path.relpath(dest, outdir)
                break
            except Exception:
                continue

    # 5) padroes de SEO (dado duro)
    word_freq = collections.Counter()
    tag_freq = collections.Counter()
    for r in top:
        for w in re.findall(r"[\wÀ-ÿ]+", r["title"].lower()):
            if len(w) > 2 and w not in STOP:
                word_freq[w] += 1
        for t in r["tags"]:
            tag_freq[t.lower()] += 1

    json.dump({"generated": now.isoformat(), "keywords": keywords, "top": top,
               "title_words": word_freq.most_common(30), "tags": tag_freq.most_common(30)},
              open(os.path.join(outdir, "dados.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    write_report(outdir, keywords, top, word_freq, tag_freq, stamp, own_channel)
    print(outdir)  # stdout = caminho, para o agente saber onde ler


def write_report(outdir, keywords, top, word_freq, tag_freq, stamp, own_channel):
    L = []
    A = L.append
    A(f"# Benchmark — {keywords[0]}  ·  {stamp}")
    A(f"\n_Nicho: {', '.join(keywords)}_")
    A(f"\n_Canal de referencia: {own_channel}. Ranqueado por **views/dia** (velocidade, nao volume). Shorts excluidos._\n")

    A("## Top videos subindo agora\n")
    A("| # | views/dia | views | dias | canal | titulo |")
    A("|---|---:|---:|---:|---|---|")
    for i, r in enumerate(top, 1):
        A(f"| {i} | {r['views_per_day']:,} | {r['views']:,} | {r['days']} | {r['channel']} | [{r['title'][:70]}]({r['url']}) |")

    A("\n## Formulas de titulo (palavras mais frequentes nos top)\n")
    A(", ".join(f"`{w}`×{c}" for w, c in word_freq.most_common(20)))

    A("\n\n## Tags recorrentes no nicho\n")
    tags = tag_freq.most_common(20)
    A(", ".join(f"`{t}`×{c}" for t, c in tags) if tags else "_(os top nao expuseram tags publicamente)_")

    A("\n\n## Thumbnails dos top\n")
    A(f"Baixadas em `thumbs/` ({sum(1 for r in top if r.get('thumb'))} imagens). ")
    A("O agente deve ABRIR essas imagens (Read) e anotar padroes: rosto/sem rosto, texto grande, "
      "cor dominante, contraste, numero — e comparar com as thumbs do canal.\n")

    A("\n## 3 recomendacoes para o canal  _(a preencher pelo agente/Writer — voz do canal)_\n")
    A("> Regra: falar na voz e no angulo do canal do usuario (definidos no onboarding/vault), "
      "nao em generico. Anti-slop. Cada rec ancorada em um DADO da tabela acima "
      "(tema-lacuna, formula de titulo, padrao de thumb).\n")
    A("1. **Tema:** …\n2. **Titulo/formato:** …\n3. **Thumbnail:** …\n")

    open(os.path.join(outdir, "RELATORIO.md"), "w", encoding="utf-8").write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--keywords", help="lista separada por virgula")
    c.add_argument("--keywords-file", help="arquivo, uma keyword por linha")
    c.add_argument("--per-keyword", type=int, default=12, help="videos por keyword (max 50)")
    c.add_argument("--top", type=int, default=20, help="quantos entram no relatorio")
    c.add_argument("--max-keywords", type=int, default=12, help="teto de keywords (protege quota)")
    c.add_argument("--out", default="benchmark", help="pasta base de saida")
    c.add_argument("--own-handle", help="@handle do canal do usuario (rotulo no relatorio)")
    c.set_defaults(func=collect)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
