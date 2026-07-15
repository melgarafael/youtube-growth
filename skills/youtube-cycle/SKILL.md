---
name: youtube-cycle
description: O conductor do ciclo de vídeo — leva um vídeo de ponta a ponta (tema → roteiro → gravar → editar → agendar → publicar), chamando a skill certa em cada etapa e rastreando onde cada vídeo está. Use quando o usuário disser "toca o próximo vídeo do começo ao fim", "me leva do tema até publicar", "o que falta nos meus vídeos?", "qual o próximo passo?", ou quiser um painel do pipeline do canal. NÃO faz o trabalho de cada etapa sozinha — orquestra as skills-irmãs (benchmark, content-pipeline, geo-growth, thumbnail-lab, remotion-scenes) e usa o yt.py p/ agendar/publicar.
---

# YouTube Cycle — o conductor do ciclo de vídeo

Tira o vídeo do "achismo → posta na esperança" e o leva por um trilho de 6 etapas, com
estado rastreado. **Esta skill não substitui as outras — ela as REGE**: em cada etapa,
decide o próximo passo, invoca a skill certa e avança o estado. O usuário sempre no
controle (aprova cada passo).

> Invocações usam `$YTG_CONFIG_DIR` (config do canal, criado pela skill `connect`),
> `bin/yt` (wrapper gerado) e `<plugin>` = raiz de instalação do plugin. Rode a partir do
> diretório do canal (o vault) — o estado do pipeline mora em `./pipeline/videos.json`.

## O quadro (estado do pipeline)

Rastreado por `scripts/cycle.py` — um kanban leve, uma fonte de verdade do progresso:

```bash
PY="$YTG_CONFIG_DIR/.venv/bin/python"; CY="<plugin>/skills/youtube-cycle/scripts/cycle.py"
"$PY" "$CY" list                      # o quadro inteiro (por etapa)
"$PY" "$CY" add "Título de trabalho"  # cria um vídeo em 'idea' (imprime o slug)
"$PY" "$CY" show <slug>               # detalhes de um vídeo
"$PY" "$CY" advance <slug> [--to <etapa>] [--video-id <ytid>] [--note "..."]
"$PY" "$CY" set <slug> <campo> <valor>   # title|theme|offer|video_id|publish_at|note
```

Etapas, em ordem: **idea → roteiro → gravado → editado → agendado → publicado**.

## Como reger (fluxo)

Ao começar, rode `cycle.py list`. Escolha o vídeo mais adiantado que ainda não terminou
(ou crie um com `add`). Faça UMA etapa por vez, sempre confirmando com o usuário, e
**avance o estado** ao concluir.

### 1. `idea` — o tema (dado, não achismo)
- Se não há vídeo, ache o tema com as skills: **`youtube-benchmark`** (o que sobe no
  nicho agora) → **`youtube-content-pipeline`** (fila de pautas priorizada) →
  **`youtube-video-oferta-map`** (amarra o vídeo a UMA oferta do canal).
- Registre: `cycle.py add "<título de trabalho>" --theme "<tema>" --offer "<oferta>"`.
- Avance quando tema + ângulo + oferta estiverem decididos: `advance <slug> --to roteiro`.

### 2. `roteiro` — o script pra gravar
- Escreva o roteiro na **voz do canal** (puxe do vault/onboarding): gancho nos primeiros
  segundos, promessa, entrega, CTA amarrado na oferta (etapa 1). Consulte
  `youtube-geo-growth` p/ já pensar em chapters/1ª linha indexável.
- Salve o roteiro no vault (ex.: `drafts/roteiro-<slug>.md`) e `advance <slug> --to gravado`
  quando o usuário confirmar que **gravou** (esta etapa é humana — a IA prepara, o
  usuário grava).

### 3. `gravado` → `editado` — edição
- **Motion/cenas**: `youtube-remotion-scenes` (inserções kinetic sincronizadas com a fala)
  + `remotion-best-practices`. **Thumbnail**: `youtube-thumbnail-lab`.
- **Metadados** (prepare agora, aplique ao publicar): `youtube-geo-growth` monta
  título/descrição/chapters/tags (SEO + citação por IA) num `.json` (formato do backup).
- `advance <slug> --to editado --note "cenas X, thumb Y, metadados prontos"`.

### 4. `editado` → `agendado` — subir e agendar
Duas formas (o usuário escolhe):
- **Upload manual** (Studio): o usuário sobe o arquivo como *privado/agendado*. Depois
  `bin/yt recent` mostra o vídeo (com `privacyStatus`/`publishAt`); pegue o `videoId`.
- **Upload via API**: monte um `meta.json` `{title, description, tags, categoryId,
  privacyStatus:"private", publishAt:"2026-08-01T13:00:00Z"}` e rode
  `bin/yt upload <arquivo.mp4> <meta.json>` — imprime o `videoId`.
- Aplique/ajuste o agendamento: `bin/yt set-status <videoId> private <publishAt-ISO-UTC>`
  (YouTube exige `private` + `publishAt` p/ agendar). Aplique os metadados otimizados:
  `bin/yt set-snippet <videoId> <meta.json>`.
- Registre: `cycle.py advance <slug> --to agendado --video-id <videoId>` e
  `cycle.py set <slug> publish_at "<ISO>"`.

### 5. `agendado` → `publicado`
- Se agendado, o YouTube publica sozinho no `publishAt`. Para publicar **agora**:
  `bin/yt set-status <videoId> public`.
- Confirme no ar e `advance <slug> --to publicado`.
- **Pós**: dias depois, `bin/yt analytics <videoId>` + `youtube-learn-from-videos`
  fecham o loop (o que a retenção ensina pro próximo tema) e `youtube-revenue-tracking`
  contabiliza a oferta. O ciclo recomeça na etapa 1, agora com dado do próprio canal.

## Regras
- **Uma etapa por vez, com aprovação.** O conductor propõe e executa; o usuário decide.
- **O estado é a verdade.** Sempre `advance`/`set` ao concluir, pra retomar de onde parou.
- **Nunca invente timestamp/publishAt** — use datas reais combinadas com o usuário.
- **Gravar é humano.** A IA entrega roteiro e direção; não simula gravação.
- Datas de agendamento em **ISO 8601 UTC** (ex.: `2026-08-01T13:00:00Z`).

## Arquivos
- `scripts/cycle.py` — estado do pipeline (kanban) em `./pipeline/videos.json`.
- Comandos de API novos (no `yt.py` do plugin, via `bin/yt`): `upload`, `set-status`.
