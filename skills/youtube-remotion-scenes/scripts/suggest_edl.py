#!/usr/bin/env python3
"""Sugeridor de EDL (autonomia): lê a transcrição word-level e propõe candidatos a cena
com o SEGUNDO EXATO da fala. NÃO decide o texto final — gera um rascunho que o humano/agente
refina (reescreve os títulos curtos, ajusta o impactFrame, corta ruído).

Método (doutrina kinetic — ver SKILL.md): mapeia a fala pela EMOÇÃO que ela carrega e escolhe
a COREOGRAFIA cuja física a encarna — não ilustra a palavra literal.

Detecta:
  (1) valor em R$ → DossieNumero partial (canto, durante execução — não tampa o screencast);
  (2) frase temática → a Motion* kinetic da emoção certa (crescer→CanalCresce, instalar/VPS→
      VpsInstala, negócio/construir→NegocioConstroi, reger/vida e negócio→Regencia, lembrar→
      CerebroAbsorve, métricas/painel→PainelVivo);
  (3) afirmação de impacto genérica → DossieCenaFast (legacy full — até haver card kinetic genérico).

Cada candidato traz `_fala` (a fala original) e `_emocao` pra facilitar o refino.

Uso:  suggest_edl.py <words.json> <footage.mp4> [saida-rascunho.json]
Depois: revisar — reescrever `title` na voz do canal, alinhar `impactFrame` à palavra-chave da
fala, decidir full/partial pelo que está na tela, e rodar build_video.py.
"""
import json, re, sys

# frase temática → (coreografia kinetic, emoção, impactFrame-palpite). ORDEM importa: mais
# específico primeiro (Regência ganha de Negócio p/ "vida e negócio"). Curar por canal.
KINETIC = [
    (r"\breg(e|er|ência)\b|vida e neg[óo]cio|segundo c[ée]rebro|orquestr", "MotionRegencia", "orquestração/controle", 74),
    (r"lembr(a|ar)|tudo que (eu )?(já )?fiz|nunca esquece|mem[óo]ria", "MotionCerebroAbsorve", "consolidação/alívio", 58),
    (r"cresc(er|eu|endo|imento)|(mais|ganhei|bati).*inscrit|decol", "MotionCanalCresce", "momentum/subida", 62),
    (r"instal|ferramenta|\bvps\b|servidor|docker|\bn8n\b|subi.*(servidor|nuvem)", "MotionVpsInstala", "competência/montagem", 96),
    (r"neg[óo]cio inteiro|constru[íi]|empresa|opera[çc][ãa]o inteira|sistema inteiro", "MotionNegocioConstroi", "construção/completude", 88),
    (r"m[ée]tricas|painel|dashboard|estat[íi]stica|em tempo real|resultado do canal", "MotionPainelVivo", "prova/autoridade de dado", 70),
]

# afirmações de impacto SEM emoção temática → full genérico (legacy DossieCenaFast).
IMPACTO = ["insano", "insana", "bizarro", "absurdo", "de graça", "grátis", "sozinho",
           "sozinha", "nova era", "dono de nada", "revende", "revender", "nunca mais",
           "para sempre", "sistema operacional", "coisa insana"]

def words_of(d):
    return [w for s in d.get("segments", []) for w in s.get("words", []) if w.get("word", "").strip()]

def seg_text_at(d, t):
    for s in d.get("segments", []):
        if s.get("start", 0) <= t <= s.get("end", 0):
            return s.get("text", "").strip()
    return ""

def main():
    src, footage = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else "edl-rascunho.json"
    d = json.load(open(src))
    words = words_of(d)
    scenes, last_at = [], -99
    seen_seg = None  # dedup: uma cena temática por segmento de fala
    for i, w in enumerate(words):
        tok = w["word"].strip()
        at = round(w["start"], 1)
        fala = seg_text_at(d, w["start"])
        low = fala.lower()
        # (1) valor em R$ — o número costuma vir 1-2 tokens depois de "R$"
        m = re.search(r"R\$?\s?(\d[\d\.]*)", tok)
        joined = (tok + " " + (words[i+1]["word"] if i+1 < len(words) else "")).strip()
        m = m or re.search(r"R\$\s?(\d[\d\.]*)", joined)
        if m:
            val = int(m.group(1).replace(".", ""))
            scenes.append({"at": at, "comp": "DossieNumero", "mode": "partial",
                "props": {"target": val, "caption": "REESCREVER", "captionHighlight": "", "emoji": "💸",
                          "transparent": True, "anchor": "top"}, "_fala": fala, "_emocao": "prova/número"})
            continue
        # (2) frase temática → coreografia kinetic pela emoção (dedup por proximidade e segmento)
        if at - last_at > 8 and fala != seen_seg:
            hit = next(((comp, emo, imp) for rgx, comp, emo, imp in KINETIC if re.search(rgx, low)), None)
            if hit:
                comp, emo, imp = hit
                last_at, seen_seg = at, fala
                scenes.append({"at": at, "comp": comp, "mode": "full",
                    "props": {"title": "REESCREVER (voz do canal)", "impactFrame": imp},
                    "_fala": fala, "_emocao": emo,
                    "_dica": "alinhar impactFrame ao SEGUNDO da palavra-chave desta fala"})
                continue
        # (3) afirmação de impacto genérica → full legacy
        gen = next((k for k in IMPACTO if k in low), None)
        if gen and at - last_at > 8 and fala != seen_seg:
            last_at, seen_seg = at, fala
            scenes.append({"at": at, "comp": "DossieCenaFast", "mode": "full",
                "props": {"emoji": "✨", "title": "REESCREVER (frase de impacto)",
                          "annotation": "REESCREVER", "annotationHighlight": ""},
                "_fala": fala, "_emocao": "impacto genérico (legacy)"})
    edl = {"footage": footage, "fps": 30,
           "_doc": "RASCUNHO gerado por suggest_edl.py — revisar title (REESCREVER), alinhar impactFrame à palavra-chave, decidir full/partial e cortar ruído antes de build.",
           "scenes": sorted(scenes, key=lambda s: s["at"])}
    json.dump(edl, open(out, "w"), ensure_ascii=False, indent=2)
    print(f"{len(scenes)} candidatos -> {out} (revisar 'REESCREVER', 'impactFrame' e o _fala/_emocao)")

if __name__ == "__main__":
    main()
