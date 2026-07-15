---
name: youtube-benchmark
description: Benchmark de concorrentes no YouTube para o canal do usuário. Use quando quiser descobrir o que está funcionando no nicho do canal — quais temas estão subindo agora, que fórmulas de título e padrões de thumbnail se repetem, e onde há lacuna de tema (oportunidade). Dado antes de achismo: ranqueia por views/dia (velocidade), baixa as thumbs dos top para análise visual e extrai padrões de SEO. Gera um relatório acionável com 3 recomendações na voz do canal.
---

# YouTube Benchmark — o que está funcionando no nicho

Descobre padrões acionáveis dos concorrentes e traz para o canal do usuário.
Parte determinística (dado) via API + julgamento (thumbs, recomendações) via agente.

## Quando usar
- "o que está bombando no meu nicho agora?"
- "que título/thumbnail usar no próximo vídeo?"
- "tem tema quente sem bom vídeo? (lacuna = oportunidade)"

## Pré-requisito
Canal conectado pela skill `connect` (token OAuth vivo). A MESMA credencial —
`search.list`/`videos.list` leem dados públicos de qualquer canal com ela. **Não
precisa de API key separada.** Confirme com `bin/yt whoami`; se falhar, rode a
skill `connect` para reautorizar.

> As invocações abaixo usam `$YTG_CONFIG_DIR` (setado pela skill `connect`) e
> `<plugin>` = a raiz onde o plugin `youtube-growth` foi instalado. Se
> `$YTG_CONFIG_DIR` não estiver no shell, rode primeiro `connect` ou exporte-a
> apontando para o config dir do canal.

⚠️ Quota: 10.000 unid/dia no projeto. `search.list` custa ~100 por keyword. O
script tem `--max-keywords` (default 12) e `--per-keyword` para conter. Espace
rodadas grandes.

## Fluxo

1. **Keywords** — pegue do briefing do canal (onboarding/vault) ou dos temas que o
   usuário quer explorar. Concreto vence abstrato.

2. **Coletar** (o script faz o dado duro):
   ```bash
   "$YTG_CONFIG_DIR/.venv/bin/python" \
     <plugin>/skills/youtube-benchmark/scripts/benchmark.py collect \
     --keywords "keyword A,keyword B,keyword C" \
     --per-keyword 12 --top 20 --out benchmark
   ```
   Saída em `benchmark/<slug>-<data>/`: `dados.json`, `thumbs/*.jpg`,
   `RELATORIO.md`. Ranqueia por **views/dia** (acha o que sobe agora, não o hit
   antigo). Shorts são excluídos (outro jogo). O stdout imprime o caminho.
   Passe `--own-handle @docanal` para rotular o canal de referência no relatório.

   Para analisar **canais específicos** (não por keyword), use o `channel_scan.py`:
   ```bash
   "$YTG_CONFIG_DIR/.venv/bin/python" \
     <plugin>/skills/youtube-benchmark/scripts/channel_scan.py \
     --handles "@canalA,@canalB" --per-channel 15 --out benchmark/ref.json
   ```

3. **Julgar as thumbs** (o agente faz) — abrir as imagens de `thumbs/` (Read) e
   anotar: rosto/sem rosto, texto grande, cor dominante, contraste, número.
   Comparar com as thumbs atuais do canal (`bin/yt recent`).

4. **Escrever as 3 recomendações** — preencher a seção final do `RELATORIO.md`.
   Cada rec ancorada num DADO da tabela (tema-lacuna, fórmula de título, padrão de
   thumb). Na **voz e no ângulo do canal do usuário** (definidos no onboarding/vault).
   Anti-slop.

## Onde procurar a LACUNA
O ouro não está em imitar o top — está no que o top NÃO cobre. Se todos os top de
um tema atacam o mesmo ângulo, o ângulo diferente do canal do usuário é uma
clareira. Dado > achismo.

## Arquivos
- `scripts/benchmark.py` — coletor + ranqueador + downloader de thumbs + relatório (por keyword).
- `scripts/channel_scan.py` — top vídeos de canais específicos (por @handle).
- Saídas em `benchmark/<slug>-<data>/`.
