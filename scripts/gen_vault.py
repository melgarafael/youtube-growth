#!/usr/bin/env python3
"""Gera o vault do usuario a partir de um briefing, e valida com verify_links."""
import os, sys, json, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(os.path.dirname(HERE), "templates")
sys.path.insert(0, HERE)
from verify_links import verify_links

def _render(text, briefing):
    for k, v in briefing.items():
        text = text.replace("{{" + k + "}}", str(v).strip() or "_(a definir)_")
    return text

def gen_vault(briefing, dest, overwrite=True):
    os.makedirs(dest, exist_ok=True)
    for dp, _, fns in os.walk(TEMPLATES):
        for fn in fns:
            src = os.path.join(dp, fn)
            rel = os.path.relpath(src, TEMPLATES)
            out = os.path.join(dest, rel)
            if not overwrite and os.path.exists(out):
                continue  # preserva edição do usuário num re-run
            os.makedirs(os.path.dirname(out), exist_ok=True)
            content = _render(open(src, encoding="utf-8").read(), briefing)
            with open(out, "w", encoding="utf-8") as f:
                f.write(content)
    r = verify_links(dest)
    if any(r.values()):
        raise ValueError(f"vault gerado tem problemas de link: {r}")

if __name__ == "__main__":
    briefing = json.load(open(sys.argv[1], encoding="utf-8"))
    gen_vault(briefing, sys.argv[2])
    print(f"Vault gerado em {sys.argv[2]}")
