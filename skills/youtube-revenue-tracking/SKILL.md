---
name: youtube-revenue-tracking
description: Rastreamento de receita do canal do usuário (monetização). Use quando quiser saber quanto o canal está faturando de verdade, montar/atualizar o painel de receita, atribuir uma venda a um vídeo, ou decidir que afiliado citar. Cobre a atribuição UTM->venda e a esteira de parceiros/afiliados. Honesto sobre o dado: a API do YouTube só vê AdSense (costuma ser pouco); a maior parte da meta vem de VENDAS (produtos próprios, recorrência, afiliados) que a API NÃO enxerga — essas entram à mão hoje. É o lado de LEITURA da monetização; escrever o CTA/UTM é da skill youtube-video-oferta-map.
---

# YouTube Revenue Tracking — quanto o canal fatura de verdade

Consolida a receita real do canal contra a meta de receita mensal (definida no
onboarding/vault do canal). Parte automatica (AdSense, via API) + parte manual
(vendas das LPs, sem API ainda).

## A verdade dura (por que este painel existe)
A Analytics do YouTube **so ve AdSense** (costuma ser pouco). O grosso da meta
vem de **vendas** — produtos proprios, recorrencia/assinatura (MRR), afiliados —
que vivem nas plataformas de venda do canal e a API do YouTube **nao enxerga**. Logo o
painel de receita PRECISA somar `AdSense (auto) + vendas atribuidas (manual)`. Fingir que a
API da o faturamento total e mentira; este painel e honesto sobre o que e real vs. estimado.

## Quando usar
- "quanto o canal ta faturando esse mes?" -> gerar/atualizar o painel.
- "que video gerou essa venda?" -> metodo de atribuicao (UTM->venda).
- "que afiliado cito nesse video?" -> esteira de parceiros.

## Pre-requisito
Canal conectado pela skill `connect` (token OAuth vivo) — a mesma credencial da
`youtube-geo-growth`/`benchmark`. Confirme com `bin/yt whoami`; se falhar, rode a
skill `connect` para reautorizar.

> As invocacoes abaixo usam `$YTG_CONFIG_DIR` (setado pela skill `connect`) e
> `<plugin>` = a raiz onde o plugin `youtube-growth` foi instalado. Se
> `$YTG_CONFIG_DIR` nao estiver no shell, rode primeiro `connect`. A meta mensal
> e channel-agnostic: exporte `YTG_META_MENSAL` (em R$) ou ajuste o default no script.

## Painel de receita (AdSense auto + vendas manual)

O script `scripts/painel.py` puxa o AdSense da API (via `bin/yt channel`) e monta o
esqueleto do painel em `drafts/painel-receita.md`. Ele **so preenche o que e real**
(AdSense) e deixa as vendas como campo `____` pra preencher — nao inventa numero de
venda que nao tem.

```bash
P="$YTG_CONFIG_DIR/.venv/bin/python"
SK="<plugin>/skills/youtube-revenue-tracking/scripts/painel.py"

"$P" "$SK" init --dias 30      # gera drafts/painel-receita.md com AdSense preenchido
"$P" "$SK" adsense 30          # so imprime a receita AdSense (read-only, pra refresh mensal)
```

- `init` **nao sobrescreve** um painel existente sem `--force` — protege as vendas
  preenchidas a mao. Pra refresh mensal, use `adsense` e atualize a linha na mao.
- Fluxo de atualizacao mensal: (1) `adsense 30` -> atualiza a linha AdSense; (2) puxar as
  vendas do mes de cada plataforma -> preencher as celulas `____`; (3) somar TOTAL vs. meta.

### Atribuicao: qual video gerou a venda
- **Ofertas de dominio proprio** (produtos/LPs do canal): o CTA carrega
  `utm_source=youtube&utm_medium=<video_id>&utm_id=organico` (a `youtube-video-oferta-map`
  escreve isso). No GA4/plataforma da LP, `utm_medium` = o `<video_id>` que originou o lead.
  Cruzar com `bin/yt recent` pro titulo. **A atribuicao so existe se o UTM foi posto no CTA** —
  as duas skills sao os dois lados da mesma moeda.
- **Afiliados e WhatsApp:** sem UTM (link de afiliado/WhatsApp nunca levam UTM). Atribuicao por
  proxy — qual video citou a oferta na janela em que a comissao caiu. Manual.
- **AdSense por video** (opcional): `bin/yt analytics <videoId> <dias>` da a receita AdSense
  de um video, pra ranquear quais videos monetizam melhor.

> Integracao futura: quando GA4/plataforma expuser API, as celulas manuais viram
> automaticas lendo o `utm_medium`. O painel ja reserva o lugar (bloco machine-readable).
> Hoje **nao existe** essa integracao — nao prometer ao canal o que ainda e manual.

## Esteira de parceiros (afiliados)
Qual afiliado citar, mecanica de cada comissao, e como maximizar sem virar promocional:
ver `references/esteira-parceiros.md`. Regra-mae: so entra o que o canal usa de verdade;
o afiliado e a ferramenta DENTRO do tutorial, nao o motivo dele. Preencha a tabela de
parceiros com os programas reais do canal (comissao, link, tipo de video).

## Doutrina
- **Pensar MRR.** A recorrencia (assinatura/comunidade + afiliado recorrente) e a espinha
  da receita composta — uma venda avulsa paga uma vez; uma assinatura paga todo mes. Priorizar recorrencia.
- **Dado antes de achismo.** Toda leitura de receita se apoia no numero (AdSense da API,
  vendas da plataforma) — nunca "acho que vendeu bem".
- **Honestidade > numero bonito.** Sem dado de venda, a celula fica vazia, nao vira zero
  nem estimativa fabricada. O gap real pra meta so fecha com as vendas preenchidas.

## Arquivos
- `scripts/painel.py` — puxa AdSense (via `bin/yt channel`) e monta/atualiza o painel.
  Subcomandos: `init`, `adsense`, `selfcheck`. Valida com `selfcheck`.
- `references/esteira-parceiros.md` — a esteira de afiliados (template a preencher).
- Saida: `drafts/painel-receita.md` (o painel vivo).
