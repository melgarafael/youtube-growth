#!/usr/bin/env python3
"""Painel de receita (monetizacao): consolida AdSense (AUTOMATICO via bin/yt) +
vendas atribuidas (MANUAL hoje) vs. a meta de receita mensal do canal.

Honestidade dura: a Analytics do YouTube so ve AdSense (costuma ser pouco). As vendas
(produtos proprios, recorrencia/assinatura, afiliados) vivem nas plataformas de venda/LP
do canal e NAO tem acesso programatico ainda -> entram a mao. Este script preenche
so o que e real (AdSense) e deixa o resto como campo pra preencher; nunca inventa.

A meta mensal e channel-agnostic: leia de $YTG_META_MENSAL (em R$) ou ajuste o
default abaixo; ela deve refletir a meta de receita do canal (onboarding/vault).

Uso:
  painel.py adsense [dias]                 # so imprime a receita AdSense da janela (read-only)
  painel.py init [--dias N] [--out PATH] [--force]   # gera o esqueleto do painel
  painel.py selfcheck                      # roda os asserts do parser
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

# Meta mensal de receita do canal, em R$. Channel-agnostic: prioriza
# $YTG_META_MENSAL e cai num default de exemplo. Ajuste ao canal (onboarding/vault).
META_MENSAL = int(os.environ.get("YTG_META_MENSAL") or 30000)


def find_repo(start: Path) -> Path:
    """Sobe a arvore ate achar bin/yt (raiz do plugin/repo). Falha explicita, nao engole."""
    p = start.resolve()
    for _ in range(8):
        if (p / "bin" / "yt").exists():
            return p
        p = p.parent
    raise RuntimeError("nao achei bin/yt subindo a arvore de diretorios")


def parse_adsense(texto: str):
    """Extrai (receita, rpm) em R$ do stdout de `bin/yt channel`.
    Retorna (None, None) se o bloco de receita nao veio (sem escopo/monetizacao) —
    honesto: sem dado nao vira zero fabricado."""
    m = re.search(r"receita estimada:\s*([\d.]+)\s*\|\s*RPM:\s*([\d.]+)", texto)
    if not m:
        return None, None
    return float(m.group(1)), float(m.group(2))


def fetch_adsense(repo: Path, dias: int):
    out = subprocess.run(
        [str(repo / "bin" / "yt"), "channel", str(dias)],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"bin/yt channel falhou: {out.stderr.strip() or out.stdout.strip()}")
    return parse_adsense(out.stdout)


def brl(v: float) -> str:
    """Formata em R$ pt-BR (1.234,56)."""
    s = f"{v:,.2f}"
    return "R$ " + s.replace(",", "X").replace(".", ",").replace("X", ".")


SKELETON = """# Painel de Receita do canal (monetizacao)

> Painel vivo. AdSense e AUTOMATICO (puxado da API pelo `painel.py`). As vendas sao
> MANUAIS hoje — nao ha acesso programatico as LPs/plataformas ainda. Preencha as
> celulas `____` com o numero real do mes; o metodo de atribuicao esta no rodape.
>
> _Gerado em {hoje} · Janela AdSense: ultimos {dias} dias · Meta: {meta}/mes._

## Consolidado do mes

| Fonte | Mecanica | Valor no mes | Como capturar |
|---|---|---:|---|
| **AdSense** | monetizacao de video (auto) | **{adsense}** | automatico via `painel.py adsense` |
| **Afiliado (one-shot)** | comissao por venda | `____` (nº vendas × comissao) | painel do programa de afiliado (manual) |
| **Produto low-ticket** | venda avulsa | `____` | plataforma de venda / GA4 por UTM (manual) |
| **Recorrencia / assinatura** | recorrencia / MRR | `____` | plataforma de assinatura (manual) |
| **Produto ticket alto** | ticket alto | `____` | plataforma de venda / GA4 por UTM (manual) |
| **TOTAL** | | **{adsense}** + vendas | somar apos preencher |

<!-- machine-readable (para integracao futura; nao apagar)
adsense_brl={adsense_raw}
adsense_rpm={rpm_raw}
janela_dias={dias}
gerado={hoje}
-->

**Falta pra meta:** {meta} − (AdSense {adsense} + vendas preenchidas). Hoje so o
AdSense esta contabilizado automaticamente — o gap real depende das vendas do mes.

## Metodo de atribuicao — qual video gerou a venda

1. **Ofertas de dominio proprio (produtos/LPs do canal):** o CTA leva UTM
   `utm_source=youtube&utm_medium=<video_id>&utm_id=organico` (padrao da skill
   `youtube-video-oferta-map`). No GA4 / plataforma de venda da LP, o `utm_medium`
   = o `<video_id>` que originou o lead/venda. Cruzar com `bin/yt recent` para o titulo.
2. **Afiliados e WhatsApp:** NAO levam UTM. Atribuicao so por proxy —
   qual video citou a oferta na janela em que a comissao caiu. Anotar manualmente.
3. **AdSense:** nao precisa de atribuicao por video pra receita — mas `bin/yt
   analytics <videoId> <dias>` da a receita AdSense por video, se quiser ranquear.

## Como atualizar (cadencia mensal)
- Rodar `painel.py adsense 30` -> atualizar a linha AdSense.
- Puxar as vendas do mes de cada plataforma -> preencher as celulas `____`.
- Somar o TOTAL e comparar com a meta. Registrar o marco no acompanhamento de
  metas do canal se bater etapa.

_Integracao futura: quando GA4/plataforma expuser API, as celulas manuais viram
automaticas lendo o `utm_medium`. O bloco machine-readable acima ja reserva o lugar._
"""


def cmd_adsense(repo, dias):
    receita, rpm = fetch_adsense(repo, dias)
    if receita is None:
        print(f"AdSense (ultimos {dias} dias): sem dado (escopo monetario ausente ou sem monetizacao no periodo)")
        return
    print(f"AdSense (ultimos {dias} dias): {brl(receita)} | RPM: {brl(rpm)}")


def cmd_init(repo, dias, out, force):
    out = Path(out) if out else repo / "drafts" / "painel-receita.md"
    if out.exists() and not force:
        print(f"Ja existe {out} — nao sobrescrevo pra nao apagar as vendas preenchidas a mao.")
        print("Use --force pra regerar do zero, ou 'painel.py adsense' pra so pegar o numero novo do AdSense.")
        return
    receita, rpm = fetch_adsense(repo, dias)
    adsense = brl(receita) if receita is not None else "sem dado"
    body = SKELETON.format(
        hoje=date.today().isoformat(),
        dias=dias,
        meta=brl(META_MENSAL),
        adsense=adsense,
        adsense_raw="" if receita is None else f"{receita:.2f}",
        rpm_raw="" if rpm is None else f"{rpm:.2f}",
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    print(f"Painel gerado: {out}  (AdSense: {adsense})")


def selfcheck():
    ok = "receita estimada: 22.861 | RPM: 14.868 | CPM: 9.054  (moeda da conta AdSense)"
    assert parse_adsense(ok) == (22.861, 14.868), parse_adsense(ok)
    assert parse_adsense("receita: sem dado (escopo monetario ausente)") == (None, None)
    assert brl(22.861) == "R$ 22,86", brl(22.861)
    assert brl(30000) == "R$ 30.000,00", brl(30000)
    print("selfcheck OK")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("adsense"); a.add_argument("dias", nargs="?", type=int, default=30)
    i = sub.add_parser("init")
    i.add_argument("--dias", type=int, default=30)
    i.add_argument("--out", default=None)
    i.add_argument("--force", action="store_true")
    sub.add_parser("selfcheck")
    args = ap.parse_args()

    if args.cmd == "selfcheck":
        selfcheck(); return
    repo = find_repo(Path(__file__).parent)
    if args.cmd == "adsense":
        cmd_adsense(repo, args.dias)
    elif args.cmd == "init":
        cmd_init(repo, args.dias, args.out, args.force)


if __name__ == "__main__":
    sys.exit(main())
