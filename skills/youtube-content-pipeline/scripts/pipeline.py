#!/usr/bin/env python3
"""
Pipeline de pautas — consolida os relatórios de benchmark numa FILA de pautas
priorizada por OPORTUNIDADE, para virar calendário editorial.

Não consulta a API: lê os `dados.json` que o youtube-benchmark já gerou (o trabalho
caro foi feito lá). Agrupa por tema/keyword, classifica o eixo (negócio / ferramenta /
construção) e ranqueia — pondo no TOPO a lacuna do canal: tema de NEGÓCIO com busca mas
sem vídeo forte (clareira), depois casos concretos quentes. O julgamento fino (ângulo na
voz e no ângulo do canal, título, oferta, meta de retenção) fica no processo da skill
(SKILL.md) — aqui é só o dado. Consolidador determinístico, não re-processa a rede.

Uso:
  pipeline.py --benchmarks ../../../benchmark --out ../../../drafts/fila-pautas.md
"""
import os, sys, json, glob, re, argparse, datetime, collections

# heurística de eixo (ordem importa: o eixo de negócio casa primeiro). As listas de
# termos abaixo estão calibradas para um nicho de exemplo (negócio/ferramenta/
# construção em PT-BR); ajuste-as ao vocabulário do canal se o nicho for outro.
_EIXOS = [
    ("negócio", ["cobrar", "vender", "venda", "cliente", "agência", "agencia", "dinheiro",
                 "ganhar", "freelancer", "mrr", "recorr", "r$", "preç", "prec", "faturar",
                 "revend", "lucr", "monetiz"]),
    ("ferramenta/caso", ["clínica", "clinica", "crm", "sdr", "whatsapp", "atendimento",
                          "e-commerce", "ecommerce", "follow", "disparo", "agendamento",
                          "lead", "barbearia", "salão", "salao"]),
    ("construção", ["zero", "iniciante", "primeiro", "criar", "instalar", "self-host",
                    "self host", "vps", "tutorial", "curso", "montar", "n8n", "rag", "dify"]),
]

def eixo_de(texto):
    t = texto.lower()
    for nome, termos in _EIXOS:
        if any(k in t for k in termos):
            return nome
    return "outro"

def carregar(benchdir):
    """Junta todos os vídeos de todos os dados.json, dedup por videoId (mantém maior vpd)."""
    vids = {}
    files = glob.glob(os.path.join(benchdir, "*", "dados.json"))
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        for r in d.get("top", []):
            vid = r["videoId"]
            if vid not in vids or r["views_per_day"] > vids[vid]["views_per_day"]:
                vids[vid] = r
    return list(vids.values()), files

def agrupar_por_tema(vids):
    """Uma pauta candidata por keyword: nº de vídeos, teto de views/dia, melhor vídeo."""
    por_kw = collections.defaultdict(list)
    for r in vids:
        por_kw[r.get("keyword", "?")].append(r)
    pautas = []
    for kw, rs in por_kw.items():
        rs.sort(key=lambda x: x["views_per_day"], reverse=True)
        teto = rs[0]["views_per_day"]
        pautas.append({
            "tema": kw,
            "eixo": eixo_de(kw),
            "n_videos": len(rs),
            "teto_vpd": teto,
            "melhor": rs[0],
            # LACUNA: eixo negócio com teto baixo = busca existe, ninguém domina.
            # Marcamos pela combinação eixo + teto relativo (calibrado após ordenar).
        })
    return pautas

def priorizar(pautas):
    """Ordena: lacuna de negócio primeiro; depois casos quentes; construção por último."""
    if not pautas:
        return []
    tetos = sorted(p["teto_vpd"] for p in pautas)
    mediana = tetos[len(tetos) // 2]
    def score(p):
        # lacuna = eixo negócio com teto abaixo da mediana (demanda sem oferta forte)
        lacuna = p["eixo"] == "negócio" and p["teto_vpd"] <= mediana
        p["sinal"] = ("LACUNA (negócio sub-servido)" if lacuna
                      else "quente (negócio)" if p["eixo"] == "negócio"
                      else "caso concreto" if p["eixo"] == "ferramenta/caso"
                      else "competido (construção)" if p["eixo"] == "construção"
                      else "revisar")
        # ranking: lacuna(3) > caso concreto(2) > negócio quente(1.5) > construção(1)
        peso = {"negócio": 1.5, "ferramenta/caso": 2, "construção": 1, "outro": 0.5}[p["eixo"]]
        if lacuna:
            peso = 3
        return (peso, -p["teto_vpd"] if p["eixo"] == "negócio" else p["teto_vpd"])
    return sorted(pautas, key=score, reverse=True)

def escrever(pautas, files, out):
    hoje = datetime.date.today().isoformat()
    L, A = [], None
    lines = []
    lines.append(f"# Fila de pautas — consolidado de benchmark  ·  {hoje}")
    lines.append(f"\n_Fonte: {len(files)} relatório(s) de benchmark. Priorizada por OPORTUNIDADE: "
                 "lacuna de negócio no topo (busca sem oferta forte), depois casos concretos, "
                 "construção por último (competido)._\n")
    lines.append("> A skill `youtube-content-pipeline` transforma cada pauta em vídeo: ângulo na "
                 "voz e no ângulo do canal (definidos no onboarding/vault), título, **oferta "
                 "amarrada** (skill `youtube-video-oferta-map`) e meta de retenção. Preencha os "
                 "slots [ ].\n")
    lines.append("| # | prioridade | tema | eixo | vídeos | teto views/dia | ref (melhor do nicho) |")
    lines.append("|---|---|---|---|---:|---:|---|")
    for i, p in enumerate(pautas, 1):
        m = p["melhor"]
        lines.append(f"| {i} | {p['sinal']} | {p['tema']} | {p['eixo']} | {p['n_videos']} | "
                     f"{p['teto_vpd']:,} | [{m['title'][:45]}]({m['url']}) |")
    lines.append("\n## Pautas a desenvolver (topo da fila)\n")
    for i, p in enumerate(pautas[:8], 1):
        lines.append(f"### {i}. {p['tema']}  ·  _{p['sinal']}_")
        lines.append(f"- **Dado:** {p['n_videos']} vídeo(s) no nicho, teto {p['teto_vpd']:,} views/dia. "
                     f"Ref: {p['melhor']['channel']}.")
        lines.append("- **Ângulo (voz e ângulo do canal — onboarding/vault):** [ virar o eixo de 'aprender' para o resultado que o canal promete ]")
        lines.append("- **Título candidato:** [ número + tempo + resultado concreto ]")
        lines.append("- **Oferta amarrada:** [ a oferta do canal ligada a este vídeo — skill `youtube-video-oferta-map` ]")
        lines.append("- **Formato/retenção:** [ curto e denso; meta de retenção > mediana do canal ]\n")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmarks", default="benchmark", help="pasta com os <tema>/dados.json")
    ap.add_argument("--out", default="drafts/fila-pautas.md")
    a = ap.parse_args()
    vids, files = carregar(a.benchmarks)
    if not vids:
        sys.exit(f"nenhum dados.json em {a.benchmarks} — rode o youtube-benchmark antes.")
    pautas = priorizar(agrupar_por_tema(vids))
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    escrever(pautas, files, a.out)

if __name__ == "__main__":
    main()
