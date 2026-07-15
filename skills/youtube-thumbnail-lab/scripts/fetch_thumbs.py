#!/usr/bin/env python3
"""
Baixa thumbnails do YouTube em alta resolucao a partir de uma lista de videoIds.

Uso no thumbnail-lab: puxar as thumbs de REFERENCIA (concorrentes que performam,
tirados do benchmark) e as do PROPRIO canal, lado a lado, para o agente abrir
(Read) e comparar antes de escrever o briefing da nova thumb.

Nao precisa de OAuth: a imagem em i.ytimg.com/vi/<id>/maxresdefault.jpg e publica.
Cai para hqdefault se o video nao tiver maxres (videos antigos/verticais).

Uso:
  fetch_thumbs.py --ids "UiK9pl8tKao,4LVALSXHDcg" --out thumbnail-lab/ref --label ref
  fetch_thumbs.py --ids-file ids.txt --out thumbnail-lab/canal --label meu
  fetch_thumbs.py --check          # self-check offline (nao baixa nada)

Saida: <out>/<label>_NN_<id>.jpg  +  stdout com o caminho da pasta.
"""
import os, sys, argparse, urllib.request

# maxres primeiro (1280x720, o que o YouTube serve na busca); hq (480x360) e o
# fallback garantido — todo video tem. sd/mq nao valem a chamada extra.
QUALITIES = ("maxresdefault", "hqdefault")


def thumb_urls(video_id):
    return [f"https://i.ytimg.com/vi/{video_id}/{q}.jpg" for q in QUALITIES]


def fetch_one(video_id, dest):
    """Tenta maxres, cai para hq. Retorna a qualidade baixada ou None se falhou."""
    for q, url in zip(QUALITIES, thumb_urls(video_id)):
        try:
            urllib.request.urlretrieve(url, dest)
            # maxresdefault as vezes existe como placeholder 120x90; se veio
            # minusculo, trata como ausente e tenta o proximo.
            if os.path.getsize(dest) > 2000:
                return q
        except Exception:
            continue
    return None


def parse_ids(args):
    ids = []
    if args.ids_file:
        ids += [l.strip() for l in open(args.ids_file, encoding="utf-8") if l.strip()]
    if args.ids:
        ids += [i.strip() for i in args.ids.split(",") if i.strip()]
    # dedup preservando ordem
    seen, out = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out


def run(args):
    ids = parse_ids(args)
    if not ids:
        sys.exit("erro: passe --ids ou --ids-file")
    os.makedirs(args.out, exist_ok=True)
    ok, fail = 0, []
    for n, vid in enumerate(ids, 1):
        dest = os.path.join(args.out, f"{args.label}_{n:02d}_{vid}.jpg")
        q = fetch_one(vid, dest)
        if q:
            ok += 1
            print(f"  [{n:02d}] {vid}  {q}", file=sys.stderr)
        else:
            fail.append(vid)
            print(f"  [{n:02d}] {vid}  FALHOU", file=sys.stderr)
    print(f"baixadas {ok}/{len(ids)} thumbs" + (f" (falhas: {', '.join(fail)})" if fail else ""),
          file=sys.stderr)
    print(os.path.abspath(args.out))  # stdout = caminho, para o agente abrir


def check():
    assert thumb_urls("abc123") == [
        "https://i.ytimg.com/vi/abc123/maxresdefault.jpg",
        "https://i.ytimg.com/vi/abc123/hqdefault.jpg",
    ]
    ns = argparse.Namespace(ids="a, b ,a,,c", ids_file=None)
    assert parse_ids(ns) == ["a", "b", "c"], parse_ids(ns)  # trim + dedup + ordem
    print("self-check OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", help="videoIds separados por virgula")
    ap.add_argument("--ids-file", help="arquivo, um videoId por linha")
    ap.add_argument("--out", default="thumbnail-lab/ref", help="pasta de saida")
    ap.add_argument("--label", default="ref", help="prefixo do arquivo (ex: ref, canal)")
    ap.add_argument("--check", action="store_true", help="self-check offline e sai")
    args = ap.parse_args()
    if args.check:
        check()
        return
    run(args)


if __name__ == "__main__":
    main()
