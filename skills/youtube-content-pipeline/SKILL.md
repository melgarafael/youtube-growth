---
name: youtube-content-pipeline
description: Pipeline de pautas e calendário editorial para o canal do usuário. Use quando precisar decidir O QUE gravar e QUANDO — transformar os benchmarks de concorrentes numa fila de pautas priorizada por oportunidade (lacuna de negócio no topo), amarrar cada pauta a uma oferta e a uma meta de retenção, e distribuir num calendário com cadência fixa. Consistência é a alavanca: sai do "gravo o que der na cabeça" para um sistema. Consome as saídas do youtube-benchmark; alimenta o youtube-video-oferta-map.
---

# Pipeline de pautas — o sistema de "o que gravar e quando"

Consistência é palavra-chave. Esta skill tira a decisão de pauta do achismo:
benchmark → fila priorizada → pauta desenvolvida (ângulo + título + oferta) → calendário.

## Quando usar
- "o que eu gravo essa semana / esse mês?"
- "monta o calendário editorial"
- "qual a próxima pauta de maior alavanca?"

## Pré-requisito
Ter ao menos um relatório do `youtube-benchmark` em `benchmark/<tema>-<data>/`. Sem dado de
nicho, não há fila. Quanto mais benchmarks (temas variados), mais rica a consolidação.

> A invocação abaixo usa `$YTG_CONFIG_DIR` (setado pela skill `connect`) e `<plugin>` = a
> raiz onde o plugin `youtube-growth` foi instalado. Se `$YTG_CONFIG_DIR` não estiver no
> shell, rode primeiro `connect` ou exporte-a apontando para o config dir do canal.

## Fluxo

1. **Consolidar em fila** (parte determinística):
   ```bash
   "$YTG_CONFIG_DIR/.venv/bin/python" \
     <plugin>/skills/youtube-content-pipeline/scripts/pipeline.py \
     --benchmarks benchmark --out drafts/fila-pautas.md
   ```
   Lê todos os `dados.json` dos benchmarks, agrupa por tema e **prioriza por oportunidade**:
   lacuna de negócio no topo (busca sem oferta forte) → casos concretos verticais →
   construção por último (competido). Gera `drafts/fila-pautas.md`.

2. **Desenvolver as pautas do topo** (julgamento — a parte que vale). Para cada pauta,
   preencher os slots:
   - **Ângulo (voz e ângulo do canal):** virar o eixo de _aprender_ para o resultado que o
     canal promete (definido no onboarding/vault). Do "como fazer X" → "como transformar X
     no resultado que interessa ao público do canal". Concreto vence abstrato.
   - **Título:** roubar a mecânica que vence no nicho (número + tempo + especificidade) e
     trocar o objeto. Usar a `youtube-benchmark` para as fórmulas reais.
   - **Oferta amarrada:** chamar a skill `youtube-video-oferta-map` — cada vídeo → UMA
     oferta do canal com resultado explícito.
   - **Meta de retenção:** o gargalo real do canal (ver a meta de retenção definida no
     briefing/onboarding do canal). Definir formato **curto e denso** com meta acima da
     mediana do canal; evitar o vídeo/live muito longo como peça de descoberta (clipar em
     cortes verticais específicos).

3. **Distribuir no calendário** (`drafts/calendario-editorial.md`): cadência FIXA (a
   consistência importa mais que o volume). Sugestão de arranque: **1 vídeo de descoberta
   por semana** (pauta do topo da fila) + cortes/lives conforme a rotina. Balancear os
   eixos: a maioria em caso concreto (a fórmula que traz tração) + 1 de negócio puro por
   mês (constrói a autoridade da clareira).

4. **Ao publicar cada pauta:** seguir o playbook de publicação do canal (se o briefing/
   onboarding tiver um) — o ritual de subir: não-listado 30-60min, configs do upload,
   distribuição multi-formato (Comunidade + Shorts), o que nunca fazer no lançamento. A fila
   decide O QUE gravar; o playbook, COMO publicar.

## A régua de priorização (por que a fila é essa ordem)
Ligada às metas do canal (definidas no onboarding/vault): alcance vem de **descoberta**
(tema que estoura), receita vem de **amarrar oferta**. Por isso: caso concreto vertical
(tração comprovada) e lacuna de negócio (clareira) ganham da construção genérica ("curso do
zero"), que é onde o nicho já se mata. Cada pauta escolhida move Alcance **e** Monetização —
nunca só uma.

## Arquivos
- `scripts/pipeline.py` — consolida benchmarks → `drafts/fila-pautas.md`.
- `drafts/fila-pautas.md` — a fila viva (regerar quando houver benchmark novo).
- `drafts/calendario-editorial.md` — o calendário com cadência (manter à mão).
