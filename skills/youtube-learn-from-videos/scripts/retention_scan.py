#!/usr/bin/env python3
"""Extrai o MODUS OPERANDI de retenção de um vídeo de referência (viral/concorrente).

Um gargalo comum de canais no YouTube é a RETENÇÃO. Este script mede, de forma
DETERMINÍSTICA, os mecanismos de retenção da transcrição de um vídeo que performa, para
o agente destilar o padrão replicável na voz/ângulo do canal do usuário (definidos no
onboarding/vault), anti-slop.

O que ele mede (dado, não achismo):
  - HOOK (0-45s): o texto que abre — que dor/promessa o criador usa para prender.
  - DENSIDADE DE GANCHOS: a cada quantos segundos, em média, o criador re-prende
    (open loop, pergunta, curiosidade). Retenção alta = ganchos frequentes.
  - ZONA DE RISCO: o maior trecho SEM nenhum gancho (onde a audiência escapa).
  - PACING: palavras por minuto (fala densa vs. arrastada).
  - CTA: onde e como o criador amarra a chamada (timestamps + trechos).

O JULGAMENTO fica com o agente (como no benchmark.py): ler a transcrição inteira, cruzar
com o que o canal já performa (bin/yt analytics) e escrever o padrão + como aplicar. Aqui
não inferimos "estrutura narrativa" por heurística — seria frágil e genérico. A análise
de padrão é delegada ao modelo; o script só entrega os números crus.

Config: resolve o dir de credencial/venv por $YTG_CONFIG_DIR (setado pela skill
`connect`/`bin/yt`), caindo no legado ~/.youtube-seo se a var não estiver setada.

Uso (via o venv do canal):
  retention_scan.py <videoId>          # público (yt-dlp) ou dono (API)
  retention_scan.py <videoId> --owner  # força a via da API do dono (privado/agendado)

Saída: JSON no stdout + scaffold do relatório em
drafts/aprendizado-<videoId>.md (seções de DADO preenchidas; ACIONÁVEL p/ o agente).
"""
import os, re, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
# Resolve o dir de config/credencial igual ao yt.py do plugin: prioriza
# $YTG_CONFIG_DIR (por-canal, setado pela skill connect) e cai no legado.
BASE = os.environ.get("YTG_CONFIG_DIR") or os.path.expanduser("~/.youtube-seo")
# reusa o transcript.py compartilhado do plugin (fonte única de transcrição),
# resolvido relativo a este arquivo — script em skills/<nome>/scripts/, sobe 3 níveis
# até a raiz do plugin, depois scripts/.
TRANSCRIPT = os.path.join(HERE, "..", "..", "..", "scripts", "transcript.py")
PYTHON = os.path.join(BASE, ".venv", "bin", "python")
# drafts fica na pasta de trabalho do usuário (vault), igual à saída do benchmark.
DRAFTS = os.path.join(os.getcwd(), "drafts")

# Marcadores de GANCHO de retenção em PT-BR (open loops, curiosidade, promessa).
# São os sinais que re-prendem a audiência a cada poucos segundos.
HOOK_MARKERS = [
    "mas ", "só que", "porém", "o problema", "o segredo", "o pulo do gato",
    "presta atenção", "olha ", "olha só", "repara", "veja ", "vou te mostrar",
    "vou mostrar", "daqui a pouco", "no final", "spoiler", "adivinha",
    "sabe por que", "sabe qual", "o detalhe", "e aqui", "acontece que",
    "não é bem assim", "calma que", "guarda isso", "presta bem atenção",
    "e o melhor", "pior que", "acredita que", "olha que loucura",
]
# Sinais de CTA / conversão.
CTA_MARKERS = [
    "link na descri", "na descri", "inscreve", "inscreva", "se inscrev",
    "comunidade", "comentário", "comenta", "clica no", "clique no", "cadastr",
    "grupo do", "whatsapp", "deixa o like", "curte o vídeo", "sino ",
    "primeiro vídeo", "próximo vídeo", "aqui em cima", "card ",
]
# Sinais de "stakes": dinheiro / controle / reputação.
STAKES_MARKERS = [
    "cliente", "r$", "reais", "cobrar", "cobra ", "vender", "vend", "receita",
    "mrr", "recorrên", "perder", "perde ", "erro", "trava", "gambiarra",
    "escala", "faturar", "faturamento", "prejuízo", "reputação", "confiança",
]


def load_windows(vid, force_owner, window=20):
    """Roda o transcript.py (janela fina) e lê [MM:SS] texto de /tmp/tr_<id>.txt."""
    cmd = [PYTHON, TRANSCRIPT, vid, str(window)]
    if force_owner:
        cmd.append("--owner")
    r = subprocess.run(cmd, capture_output=True, text=True)
    path = f"/tmp/tr_{vid}.txt"
    if not os.path.exists(path):
        sys.stderr.write(r.stderr or "sem transcrição\n")
        sys.exit(1)
    wins = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\[(\d\d):(\d\d)\]\s*(.*)", line)
        if m:
            sec = int(m.group(1)) * 60 + int(m.group(2))
            wins.append((sec, m.group(3).strip()))
    return wins


def count_markers(text, markers):
    t = text.lower()
    return sum(t.count(m) for m in markers)


def analyze(wins):
    if not wins:
        return None
    duration = wins[-1][0] + 20
    full = " ".join(t for _, t in wins).lower()

    hook_wins = [(s, t) for s, t in wins if s < 45]
    # janelas que contêm >=1 gancho
    hooked = [(s, t) for s, t in wins if count_markers(t, HOOK_MARKERS) >= 1]
    n_hooks = len(hooked)
    avg_gap = round(duration / n_hooks, 1) if n_hooks else None

    # maior trecho sem gancho (zona de risco de escape)
    marks = [s for s, _ in hooked]
    edges = [0] + marks + [duration]
    gaps = [(edges[i + 1] - edges[i], edges[i], edges[i + 1])
            for i in range(len(edges) - 1)]
    worst = max(gaps, key=lambda g: g[0]) if gaps else (0, 0, 0)

    words = sum(len(t.split()) for _, t in wins)
    wpm = round(words / (duration / 60), 1) if duration else 0

    cta = [(s, t) for s, t in wins if count_markers(t, CTA_MARKERS) >= 1]

    return {
        "duration_s": duration,
        "duration_mmss": f"{duration // 60:02d}:{duration % 60:02d}",
        "hook_text": " ".join(t for _, t in hook_wins),
        "hook_stakes_hits": count_markers(
            " ".join(t for _, t in hook_wins), STAKES_MARKERS),
        "n_hooks": n_hooks,
        "avg_gap_s": avg_gap,
        "hooks_per_min": round(n_hooks / (duration / 60), 1) if duration else 0,
        "worst_dry_gap_s": worst[0],
        "worst_dry_gap_window": f"{worst[1] // 60:02d}:{worst[1] % 60:02d}"
                                f"–{worst[2] // 60:02d}:{worst[2] % 60:02d}",
        "wpm": wpm,
        "stakes_hits_total": count_markers(full, STAKES_MARKERS),
        "cta": [{"t": f"{s // 60:02d}:{s % 60:02d}", "text": t} for s, t in cta],
    }


def scaffold(vid, a):
    cta_lines = "\n".join(f"- `{c['t']}` — {c['text']}" for c in a["cta"]) or \
        "- (nenhum CTA verbal detectado na fala — pode estar só na tela/descrição)"
    gap_alert = ("⚠️ **Zona de risco**" if a["worst_dry_gap_s"] >= 60
                 else "OK") + f" — maior trecho sem gancho: **{a['worst_dry_gap_s']}s** " \
        f"({a['worst_dry_gap_window']})."
    return f"""# Aprendizado — vídeo `{vid}`

> Modus operandi de RETENÇÃO extraído de um vídeo que performa, para replicar o
> PADRÃO (não copiar) no canal do usuário. Um gargalo comum é a retenção. Dado bruto
> pelo `retention_scan.py`; destilação pelo agente na voz/ângulo do canal (onboarding/vault).

## 1. Dado bruto (medido, não achismo)

| Métrica | Valor | Leitura |
|---|---|---|
| Duração | {a['duration_mmss']} | — |
| Ganchos de retenção | {a['n_hooks']} | quantas vezes re-prende |
| **Re-prende a cada** | **~{a['avg_gap_s']}s** | <20s = muito denso; >45s = solta a audiência |
| Ganchos por minuto | {a['hooks_per_min']} | ritmo de curiosidade |
| Pacing (palavras/min) | {a['wpm']} | ~130-160 conversacional; <110 arrastado |
| Stakes no hook (dinheiro/cliente/erro) | {a['hook_stakes_hits']} hits | promessa aterrada em dor real? |
| Stakes no vídeo todo | {a['stakes_hits_total']} hits | o tema fala de RESULTADO o tempo todo? |

{gap_alert}

### O HOOK (0-45s) — o que abre a porta
> {a['hook_text']}

### CTA — como amarra a chamada
{cta_lines}

---

## 2. O padrão replicável _(agente preenche — ler a transcrição inteira antes)_

- **Que dor/promessa o hook abre?** (uma frase, no nível de dinheiro/controle/reputação)
- **Estrutura narrativa:** como ele encadeia problema → diagnóstico → caminho?
- **Mecânica de gancho:** que tipo de open loop ele usa para re-prender (pergunta,
  "só que", contraste antes/depois, stakes)? Qual é o de maior recorrência?
- **Pacing:** a fala é densa ou tem gordura? Onde ele acelera/respira?

## 3. Como aplicar no PRÓXIMO vídeo do canal _(agente — acionável, não resumo)_

- **Reescreva o hook** do próximo vídeo no molde acima, mas na voz/ângulo do canal do
  usuário (definidos no onboarding/vault).
- **Meta de densidade:** um gancho a cada ~`{a['avg_gap_s']}`s. Onde o roteiro do canal
  fica >45s sem gancho, injetar um open loop.
- **CTA:** posição e forma que funcionaram aqui, amarrado à oferta certa do canal
  (ver o mapa vídeo→oferta no vault/onboarding).

## 4. O que NÃO copiar (anti-slop) _(agente)_
- Tiques do criador que não são a voz do canal; ganchos clickbait vazios que quebram
  reputação; qualquer coisa que soe genérica de IA.

## 5. Cruzamento com o canal _(agente — dado > achismo)_
Rodar `bin/yt analytics <videoId-de-um-top-do-canal>` e comparar: o padrão daqui bate
com o que já segura retenção no canal do usuário, ou contradiz? Registrar a conclusão.
"""


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: retention_scan.py <videoId> [--owner]")
    vid = sys.argv[1]
    force_owner = "--owner" in sys.argv
    wins = load_windows(vid, force_owner)
    a = analyze(wins)
    if not a:
        sys.exit("transcrição vazia")
    os.makedirs(DRAFTS, exist_ok=True)
    out = os.path.join(DRAFTS, f"aprendizado-{vid}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(scaffold(vid, a))
    print(json.dumps(a, ensure_ascii=False, indent=2))
    print(f"\n# scaffold do relatório: {out}", file=sys.stderr)
    print(f"# transcrição completa: /tmp/tr_{vid}.txt", file=sys.stderr)


if __name__ == "__main__":
    main()
