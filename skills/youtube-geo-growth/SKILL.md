---
name: youtube-geo-growth
description: "Otimiza vídeos do YouTube para SEO e para citação por IA (GEO), operando direto no canal via YouTube Data API v3. Use quando o usuário quiser crescer um canal do YouTube, otimizar ou editar vídeos, escrever ou melhorar título/descrição/tags, adicionar capítulos (chapters), subir legendas corrigidas, fazer retrofit de vídeos antigos, ou preparar um vídeo novo/agendado antes de publicar. Cobre extrair a transcrição real (pública via yt-dlp ou privada/agendada via API do dono), cortar capítulos nas viradas de assunto, escrever a primeira linha como resposta indexável, aplicar UTMs com segurança e gravar via API com backup e verificação. Específica para YouTube — não confundir com a skill geo (auditoria de sites) nem com edição de vídeo/imagem."
---

# YouTube GEO Growth

Transforma metadados de vídeos do YouTube para dois objetivos ao mesmo tempo: ser
mostrado pelo algoritmo (SEO — retenção, título, CTR) e ser **citado** por ChatGPT,
Perplexity e Google AI Overviews (GEO — transcrição, chapters, descrição). Opera
direto no canal do usuário via YouTube Data API v3, de forma reversível.

## Tese que guia tudo
Quase nenhum motor de IA assiste ao vídeo — eles leem o **texto** (transcrição,
descrição, chapters). **A palavra é o produto, o vídeo é a entrega.** Detalhes,
split de citação por motor e as 5 alavancas em `references/geo-method.md`.

## Pré-requisitos (verificar antes de operar)
1. **Canal conectado.** Esta skill usa a mesma conexão OAuth da skill `connect`.
   Confirme com `bin/yt whoami` — deve imprimir o canal do usuário. Se falhar (ou se
   `bin/yt` não existir), rode primeiro a skill `connect` (ela cria o config dir do
   canal, o venv e o wrapper `bin/yt`). Setup manual/detalhes da API em
   `references/youtube-data-api-setup.md`.
2. **yt-dlp** instalado (para transcrição de vídeos públicos). `<plugin>/scripts/setup_env.sh`
   avisa se faltar.

> `bin/yt` é o wrapper gerado pela skill `connect` (aponta para o venv e o `yt.py` do
> plugin, com o config dir do canal embutido). Todas as chamadas `yt.py <cmd>` abaixo
> são feitas via `bin/yt <cmd>`.

## Fluxo de trabalho por vídeo

Ler `references/geo-method.md` para as regras de conteúdo (chapters, descrição, título,
UTM, anti-slop) e `references/youtube-data-api-setup.md` para os comandos e as regras
de segurança da API.

1. **Localizar o vídeo**. Público: pegar o ID pela URL. Agendado/privado/rascunho:
   `bin/yt recent 8` lista uploads incluindo os não-públicos (com `privacyStatus` e
   `publishAt`).
2. **Backup**: `bin/yt get <id>` salvo em `$YTG_CONFIG_DIR/backup/<id>.json` ANTES de
   gravar. `videos.update` sobrescreve — o backup é o undo.
3. **Transcrição real**: `"$YTG_CONFIG_DIR/.venv/bin/python" <plugin>/scripts/transcript.py <id>`
   — usa yt-dlp (público) e cai automaticamente para a API de captions do dono em vídeo
   privado/agendado. Ler a saída consolidada em janelas de tempo.
4. **Montar o conteúdo** (do método): cortar 5–10 chapters nas **viradas reais** de
   assunto (título de chapter = pergunta buscável); escrever a **1ª linha como
   resposta indexável**; "o que você vai ver"; preservar CTAs/links do usuário.
5. **UTMs com segurança**: só adicionar onde falta, só em domínio próprio do usuário,
   nunca em afiliado/WhatsApp, seguindo o padrão de UTM que o usuário já usa.
6. **Gravar**:
   - Vídeo existente (mexer só na descrição/chapters): escrever a nova descrição num
     `.txt` → `bin/yt update-desc <id> <arquivo.txt>`.
   - Vídeo novo/agendado (título + descrição + tags): montar um `.json` (mesmo formato
     de um backup) → `bin/yt set-snippet <id> <arquivo.json>`.
   - Legenda corrigida (opcional, alto impacto): `bin/yt set-caption <id> <arquivo.srt>`.
7. **Verificar**: `bin/yt get <id>` de volta e confirmar. A leitura pode pegar cache por
   alguns segundos — reler antes de concluir que uma gravação falhou.

## Regras invioláveis
- **Nunca gravar sem backup.** Toda edição é reversível a partir de `$YTG_CONFIG_DIR/backup/`.
- **Aumentar, não substituir**: preservar os links e a voz do usuário na descrição.
- **Não trocar título de vídeo com tração** (reseta o algoritmo) — sugerir A/B de
  thumbnail em vez disso.
- **Chapters só com timestamps reais** da transcrição — nunca estimar.
- Para lote grande (dezenas de vídeos), processar por prioridade (mais views primeiro)
  e vigiar a quota da API (`references/youtube-data-api-setup.md`).

## Contexto do dono do canal
As decisões de copy (título, ângulo, CTA) devem refletir quem o usuário é e com quem
ele fala. Buscar esse contexto no vault/perfil do usuário (onboarding) antes de escrever
copy — público, oferta, jargões, tom. Comunicar no nível de dor/benefício da audiência
dele, não em termos técnicos genéricos.
