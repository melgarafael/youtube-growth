#!/usr/bin/env python3
"""
Conductor do ciclo de vídeo — estado leve (kanban) de cada vídeo do canal ao longo de
tema → roteiro → gravado → editado → agendado → publicado.

NÃO chama a API do YouTube (isso é do yt.py / das skills-irmãs). Só mantém o estado do
pipeline num JSON no vault do canal, pra o agente saber ONDE cada vídeo está e o que
falta. Fonte da verdade do progresso; as skills fazem o trabalho de cada etapa.

Estado: ./pipeline/videos.json (relativo ao diretório do canal — o cwd/vault).

Uso:
  cycle.py add "Título de trabalho" [--theme "tema"] [--offer "oferta"] [--note "..."]
  cycle.py list [--stage <stage>]
  cycle.py show <slug>
  cycle.py advance <slug> [--to <stage>] [--video-id <ytid>] [--note "..."]
  cycle.py set <slug> <campo> <valor>        # campos: title, theme, offer, video_id, publish_at, note

Stages (em ordem):
  idea → roteiro → gravado → editado → agendado → publicado
"""
import os, sys, json, re, argparse, datetime

STAGES = ["idea", "roteiro", "gravado", "editado", "agendado", "publicado"]
STORE = os.path.join(os.getcwd(), "pipeline", "videos.json")


def _now():
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def _load():
    if not os.path.exists(STORE):
        return {"videos": []}
    with open(STORE, encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    os.makedirs(os.path.dirname(STORE), exist_ok=True)
    tmp = STORE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STORE)


def _slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40]
    return s or "video"


def _find(data, slug):
    for v in data["videos"]:
        if v["slug"] == slug:
            return v
    sys.exit(f"erro: vídeo '{slug}' não encontrado (veja `cycle.py list`)")


def _uniq_slug(data, base):
    slugs = {v["slug"] for v in data["videos"]}
    if base not in slugs:
        return base
    i = 2
    while f"{base}-{i}" in slugs:
        i += 1
    return f"{base}-{i}"


def add(a):
    data = _load()
    slug = _uniq_slug(data, _slugify(a.title))
    v = {"slug": slug, "title": a.title, "stage": "idea",
         "theme": a.theme or "", "offer": a.offer or "", "video_id": "",
         "publish_at": "", "notes": [], "created": _now(), "updated": _now()}
    if a.note:
        v["notes"].append(f"{_now()}  {a.note}")
    data["videos"].append(v)
    _save(data)
    print(slug)  # stdout = slug (p/ encadear)


def _line(v):
    yt = f" · yt={v['video_id']}" if v["video_id"] else ""
    when = f" · publishAt={v['publish_at']}" if v["publish_at"] else ""
    theme = f" · tema: {v['theme']}" if v["theme"] else ""
    return f"[{v['stage']:<10}] {v['slug']}  — {v['title'][:60]}{theme}{yt}{when}"


def list_(a):
    data = _load()
    vids = data["videos"]
    if a.stage:
        vids = [v for v in vids if v["stage"] == a.stage]
    if not vids:
        print("(pipeline vazio — use `cycle.py add`)"); return
    order = {s: i for i, s in enumerate(STAGES)}
    for v in sorted(vids, key=lambda v: (order.get(v["stage"], 99), v["updated"])):
        print(_line(v))


def show(a):
    v = _find(_load(), a.slug)
    print(json.dumps(v, ensure_ascii=False, indent=2))


def advance(a):
    data = _load()
    v = _find(data, a.slug)
    if a.to:
        if a.to not in STAGES:
            sys.exit(f"erro: stage inválido '{a.to}'. Válidos: {', '.join(STAGES)}")
        v["stage"] = a.to
    else:
        i = STAGES.index(v["stage"])
        if i >= len(STAGES) - 1:
            print(f"'{v['slug']}' já está em '{v['stage']}' (última etapa).")
        else:
            v["stage"] = STAGES[i + 1]
    if a.video_id:
        v["video_id"] = a.video_id
    if a.note:
        v["notes"].append(f"{_now()}  {a.note}")
    v["updated"] = _now()
    _save(data)
    print(_line(v))


def set_(a):
    data = _load()
    v = _find(data, a.slug)
    field = a.field
    if field == "note":
        v["notes"].append(f"{_now()}  {a.value}")
    elif field in ("title", "theme", "offer", "video_id", "publish_at"):
        v[field] = a.value
    else:
        sys.exit(f"erro: campo '{field}' inválido. Use: title, theme, offer, video_id, publish_at, note")
    v["updated"] = _now()
    _save(data)
    print(_line(v))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add"); p.add_argument("title")
    p.add_argument("--theme"); p.add_argument("--offer"); p.add_argument("--note")
    p.set_defaults(func=add)

    p = sub.add_parser("list"); p.add_argument("--stage"); p.set_defaults(func=list_)

    p = sub.add_parser("show"); p.add_argument("slug"); p.set_defaults(func=show)

    p = sub.add_parser("advance"); p.add_argument("slug")
    p.add_argument("--to"); p.add_argument("--video-id", dest="video_id"); p.add_argument("--note")
    p.set_defaults(func=advance)

    p = sub.add_parser("set"); p.add_argument("slug"); p.add_argument("field"); p.add_argument("value")
    p.set_defaults(func=set_)

    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
