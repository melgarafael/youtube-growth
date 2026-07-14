#!/usr/bin/env python3
"""Verifica o grafo de wikilinks de um vault: links quebrados, orfaos, sem-entrada."""
import os, re, sys

LINK = re.compile(r"\[\[([^\]]+)\]\]")
FENCE = re.compile(r"```.*?```", re.DOTALL)
CODE = re.compile(r"`[^`]*`")
HARNESS = {"CLAUDE.md", "AGENTS.md", "GEMINI.md", "README.md"}
NO_SCAN = {"CLAUDE.md", "AGENTS.md", "GEMINI.md"}

def verify_links(root, exclude_dirs=("node_modules", ".git", ".venv")):
    md = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in exclude_dirs]
        md += [os.path.join(dp, f) for f in fns if f.endswith(".md")]
    by_rel, by_base = {}, {}
    for f in md:
        rel = os.path.relpath(f, root)[:-3]
        by_rel[rel] = f
        by_base.setdefault(os.path.basename(rel), []).append(rel)

    def resolve(t):
        t = t.strip().lstrip("./")
        return t in by_rel or t in by_base

    broken, orphans, incoming = [], [], {os.path.relpath(f, root): 0 for f in md}
    for f in md:
        rel = os.path.relpath(f, root)
        if os.path.basename(f) in NO_SCAN:
            continue
        txt = CODE.sub("", FENCE.sub("", open(f, encoding="utf-8").read()))
        targets = [m.replace("\\|", "|").split("|")[0].split("#")[0].rstrip("\\").strip()
                   for m in LINK.findall(txt)]
        targets = [t for t in targets if t]
        for t in targets:
            if not resolve(t):
                broken.append((rel, t))
            else:
                key = t.lstrip("./")
                if key in by_rel:
                    incoming[os.path.relpath(by_rel[key], root)] += 1
                else:
                    for cand in by_base.get(key, []):
                        incoming[os.path.relpath(by_rel[cand], root)] += 1
        if not targets:
            base = os.path.basename(f)
            is_raw = "/benchmark/" in f and base in ("RELATORIO.md", "RECOMENDACOES.md")
            if base not in HARNESS and not is_raw:
                orphans.append(rel)
    unreachable = [r for r, n in incoming.items() if n == 0
                   and os.path.basename(r) not in HARNESS
                   and os.path.basename(r) != "_INDEX.md"]
    return {"broken": broken, "orphans": orphans, "unreachable": unreachable}

if __name__ == "__main__":
    r = verify_links(sys.argv[1])
    for k in ("broken", "orphans", "unreachable"):
        print(f"{k}: {r[k] or 'ok'}")
    sys.exit(1 if any(r.values()) else 0)
