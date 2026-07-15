---
name: youtube-remotion-scenes
description: Editor/diretor visual de motion do canal do usuário — cria cenas animadas de reforço (estilo MrBeast/Mark Tilbury) e as monta no vídeo. Use quando pedir uma inserção/overlay de vídeo, reforço de uma frase, destaque de número/estatística, "faz um motion disso", transição, ou editar as cenas ao longo de um vídeo gravado. PADRÃO = kinetic senior (fx.tsx): pico de impacto (flash+shake+pulso+ricochete), sucção, count-up, wireframe/glow — cada frase ganha uma COREOGRAFIA escolhida pela EMOÇÃO que precisa cravar. Paleta de exemplo escuro + dourado #FFC24B + ciano #4DD0E1 + verde #3BD07A + vermelho-YT; personalizável por props (impactFrame sincroniza com a fala, cores, textos, densidade) e adaptável à identidade do seu canal. Renderiza MP4 e monta como overlay no footage sem cortar o áudio (scripts/build_video.py). Templates "Dossiê" v2 são legacy — migrar pro kinetic.
---

# YouTube Remotion Scenes — motion kinetic senior

Você é o **editor de motion** do canal. Cria as cenas de reforço que quebram o padrão
visual nos pontos-chave (o gargalo é retenção) e as monta no vídeo. A meta é o vídeo virar
**30% motion** — uma animação viva junto do conteúdo — pra segurar a atenção quando a câmera
está parada. Isso costuma ser um diferencial forte do canal; **não entregue motion morno.**

## Dependências PESADAS (opcionais — só para quem renderiza vídeo)

Esta skill embute um projeto Remotion completo em `project/`. Renderizar/montar exige um
setup por-máquina que é **pesado e opcional** — só instale se você for de fato produzir vídeo:

- **Node.js + npm**, e um `npm install` dentro de `project/` (baixa Remotion, React, Chromium
  headless — centenas de MB). `node_modules/` NÃO acompanha o plugin; rode o install localmente.
- **ffmpeg / ffprobe** no PATH (montagem/overlay/extração de frame). Os scripts resolvem o
  binário pelo PATH (ou pelas envs `FFMPEG`/`FFPROBE`), caindo no caminho homebrew do macOS.
- **(opcional) mlx-whisper** para transcrição local no modo "vídeo inteiro" (Apple Silicon).

Se você só quer o restante do plugin `youtube-growth` (benchmark, SEO, etc.), pode ignorar
esta skill inteira — nada mais depende dela.

> As invocações Python abaixo usam `$YTG_CONFIG_DIR` (setado pela skill `connect`) e
> `<plugin>` = a raiz onde o plugin `youtube-growth` foi instalado. Se `$YTG_CONFIG_DIR`
> não estiver no shell, rode a skill `connect` primeiro (ou exporte a var manualmente).
> As invocações Node/Remotion (`npm run studio`, `npx remotion render`) rodam a partir de
> `<plugin>/skills/youtube-remotion-scenes/project` e usam o Node da máquina, não o venv.

## A doutrina-mãe: EMOÇÃO primeiro, coreografia depois

Um motion senior não ilustra a palavra literal — ele **encarna a sensação** que a frase
precisa cravar. Antes de escolher a cena, decida a emoção:

| Sensação que a frase carrega | Coreografia (física que a encarna) | Composição |
|---|---|---|
| **Consolidação / alívio** ("a IA lembra de tudo") | fragmentos são SUGADOS e engolidos por um núcleo | `MotionCerebroAbsorve` |
| **Orquestração / controle** ("rege minha vida e meu negócio") | núcleo irradia feixes que ATIVAM constelações em cascata | `MotionRegencia` |
| **Momentum / subida** ("fiz o canal crescer") | contador sobe + gráfico desenha e DISPARA pra cima | `MotionCanalCresce` |
| **Prova / autoridade de dado** (o print do Studio, métricas) | dashboard GANHA VIDA: tiles com count-up, gráfico, barras vivas | `MotionPainelVivo` |
| **Competência / montagem** ("instalei ferramentas na VPS") | chips ENCAIXAM no rack (snap) + progresso + check | `MotionVpsInstala` |
| **Construção / completude** ("construí um negócio inteiro") | blocos CONVERGEM e travam numa malha; conectores desenham | `MotionNegocioConstroi` |

Não achou a emoção nessa lista? **Crie uma coreografia nova** a partir do kit (abaixo) —
o catálogo cresce. O erro é recolorir a sucção do cérebro e chamar de cena nova.

> **Importante:** a tabela acima ensina o **método** (emoção→coreografia) — os nomes de
> cena (`MotionCerebroAbsorve`, `MotionRegencia`, …) são exemplos ilustrativos e **não
> embarcam** no plugin. O kit vem com **3 cenas-semente** prontas: `DossieCena` (cena base
> com fundo), `MotionLettering` (texto kinetic) e `MotionNumero` (número count-up). Use-as
> como ponto de partida e **crie as demais coreografias a partir do `fx.tsx`** conforme a
> emoção que cada frase precisa cravar.

## O KIT (`project/src/fx.tsx`) — a assinatura de movimento

**Toda cena nova nasce do `fx.tsx`.** É ele que garante que cenas diferentes tenham o MESMO
"peso" — e peso consistente = identidade. As **8 regras** (não são opções — a régua que separou
5/10 de estado-da-arte):

1. **Stagger** — nada entra junto; delays escalonados (3-4 frames) dão ritmo.
2. **Easing de sucção/gravidade** — `SUCK = bezier(0.55,0,1,0.45)`: começa lento, é puxado, acelera. Nunca linha reta.
3. **Estados de vida** — o elemento nasce (scale 0.6, op 0), voa, e é engolido/encaixado (scale→0.12 + fade), não só some.
4. **Motion blur** proporcional à velocidade (cresce no meio-fim da trajetória).
5. **Pico de impacto num frame** — `useImpact()`: flash (`mix-blend screen`) + screen-shake + pulso (spring overshoot), TODOS no frame da palavra-chave. É o "snap" que registra na retina. **Isto substitui o "travamento" seco do Dossiê em toda cena.**
6. **Vida residual** — `<Ricochet>`: partículas de ricochete pós-impacto. Nada engole e acaba seco.
7. **Wireframe/glow > fill chapado** — nós/sinapses que acendem, `GlowDefs`, núcleo de luz radial.
8. **Props de ajuste** — `impactFrame` (sincronizar com a fala), cores, densidade. A cena é reutilizável.

Primitivas prontas em `fx.tsx`: `useImpact`, `Flash`, `Ricochet`, `countUp`, `GlowDefs`,
`Vignette`, `SUCK`/`SNAP`/`OUT`, e a paleta `KIN`.

## Personalizar pro momento (é isto que faz parecer feito à mão, não template)

- **`impactFrame`** — crave o pico no SEGUNDO EXATO da palavra de impacto da fala (ache no SRT). Cena sem sync = cena genérica.
- **Cor pela emoção** (paleta `KIN`): verde `#3BD07A` = dinheiro/subida · ciano `#4DD0E1` = IA/neural · dourado `#FFC24B` = conhecimento/valor · vermelho `#E4574C` = YouTube/urgência. A cor conta parte da história. (É a paleta de exemplo — troque pelos acentos do seu canal.)
- **Textos na voz do canal** — use a voz e o ângulo definidos no onboarding/perfil do canal. Título curto, palavra-soco. Evite genérico ("aprenda X").
- **Densidade pela grandeza da afirmação** — `iconCount`/`tools`/`blocks`: afirmação forte = mais elementos convergindo; frase contida = menos.
- **`transparent: true`** — vira overlay alpha (card no canto) pra não tampar screencast (ver regras de overlay abaixo).

## Fluxo

1. **Editar no visual:** `cd <plugin>/skills/youtube-remotion-scenes/project && npm run studio` — escolha a composição, ajuste props (schema Zod) com preview ao vivo. (Requer o `npm install` do projeto — ver Dependências.)
2. **Renderizar** (MP4 com fundo):
   ```bash
   cd <plugin>/skills/youtube-remotion-scenes/project
   npx remotion render src/index.ts <Composição> \
     "$YTG_RENDERS_DIR/<nome>.mp4" --codec=h264 --pixel-format=yuv420p --log=error
   ```
   (Sem `$YTG_RENDERS_DIR` setada, os scripts caem em `./drafts/renders`. `--props='{"title":"...","impactFrame":62}'` sobrescreve; `--scale=2` p/ 4K.)
3. **Verificar SEMPRE antes de "pronto":** extraia o frame do impacto (`ffmpeg -ss <t> -i out.mp4 -frames:v 1 f.png`) e OLHE. Render ≠ bom.
4. **Reel de portfólio:** `ffmpeg -f concat` dos renders.

## Modo "vídeo inteiro" — cenas sincronizadas com a fala, em lote

Pra cravar cenas ao longo de um vídeo gravado. Pipeline em `scripts/`:

1. **Transcrever:**
   ```bash
   "$YTG_CONFIG_DIR/.venv/bin/python" \
     <plugin>/skills/youtube-remotion-scenes/scripts/transcribe.py <video.mp4>
   ```
   (mlx-whisper, local/rápido, com word-timestamps.)
2. **Sugerir rascunho:**
   ```bash
   "$YTG_CONFIG_DIR/.venv/bin/python" \
     <plugin>/skills/youtube-remotion-scenes/scripts/suggest_edl.py <words.json> <footage.mp4>
   ```
   Mapeia frases → a coreografia certa por emoção (número→count-up, crescer→CanalCresce,
   instalar/VPS→VpsInstala, negócio→NegocioConstroi, reger→Regencia, lembrar→CerebroAbsorve).
   Devolve candidatos com o segundo exato + a fala; o humano refina os `REESCREVER` e o `impactFrame`.
   (Os gatilhos de frase são de exemplo — cure o mapa para o vocabulário do seu canal.)
3. **Montar:**
   ```bash
   "$YTG_CONFIG_DIR/.venv/bin/python" \
     <plugin>/skills/youtube-remotion-scenes/scripts/build_video.py <edl.json> all
   ```
   (Render lote → overlay no footage. Requer o `npm install` do projeto + ffmpeg.)

### Regras firmes do modo vídeo (aprendidas em produção real — não são opções)
1. **Reforço-no-momento-da-fala, não transição.** A cena dá impacto à frase dita NAQUELE segundo. Se não casa com fala de impacto, não entra.
2. **NADA corta o áudio.** Tudo é OVERLAY por cima do footage; áudio/vídeo seguem por baixo, duração = footage.
3. **Não sobrepor o que a tela já mostra.** Em screencast, quando o footage já exibe o dado (Excalidraw/terminal), use `transparent:true` num canto VAZIO (topo-esquerda), nunca no centro. Evite o canto inferior-direito (PIP da câmera).
4. **Contraste garantido.** Fundo branco de screencast → overlay leva halo/sombra forte.
5. **Cena já nos primeiros ~5–25s** e densidade ao longo de todo o vídeo — retém desde o arranque. Ritmo de inserção tela-cheia: ~1 a cada 60–120s (senão vira videoclipe); overlays podem ser mais densos.

## Identidade kinetic (a paleta de exemplo)
Fundo escuro `#0B0D12` + dourado `#FFC24B` + ciano `#4DD0E1` + verde `#3BD07A` + vermelho-YT `#E4574C`.
Movimento rápido/extravagante mas elegante (springs com overshoot). Inter 600/800. **Sem roxo neon,
sem fonte condensada, sem orbe/robô genérico.** Esta é a assinatura de um canal de exemplo — **adapte
as cores, a fonte e a voz à identidade visual do seu canal** (o *método* kinetic é o que se reaproveita).

> **Dossiê v2 é legacy.** Os `Dossie*.tsx` (índigo/documento/caderno) ainda rodam, mas o padrão
> passou a ser o kinetic. Ao mexer numa cena Dossiê, migre o fechamento pro pico de impacto do
> `fx.tsx` (`useImpact` + `Ricochet`) no lugar do settle seco.

## Cenas de exemplo (adapte à sua marca)
As 3 cenas-semente em `project/src/` (`DossieCena`, `MotionLettering`, `MotionNumero`) são
**gabaritos genéricos** de partida — os defaultProps (textos/cores) são só exemplos. Use-as
como **referência de craft** (o *como* do movimento), reescreva textos/cores/temas para o seu
nicho, ou crie novas cenas a partir do `fx.tsx`. O valor reutilizável é o kit (`fx.tsx`) + as
8 regras + a doutrina emoção-primeiro (`references/doutrina-cenas.md`, que descreve várias
coreografias como referência, mesmo as que não vêm prontas).

## Arquivos
- `project/src/fx.tsx` — **o KIT** (impacto, ricochete, count-up, sucção, glow, paleta `KIN`). Base de toda cena.
- `project/src/DossieCena.tsx` · `MotionLettering.tsx` · `MotionNumero.tsx` — as 3 cenas-semente de exemplo, cada uma auto-contida com schema Zod. `Root.tsx` registra as três.
- `project/src/{motion,tokens,fonts}.ts` · `dossie-kit.tsx` — utilitários do kit.
- `scripts/transcribe.py` · `scripts/suggest_edl.py` · `scripts/build_video.py` · `scripts/gen_captions.py` — pipeline vídeo-inteiro.
- `references/doutrina-cenas.md` — log do lab + a doutrina kinetic (RODADA 4). `references/edl-exemplo.json` — modelo de EDL.
- Saídas em `$YTG_RENDERS_DIR` (default `./drafts/renders`).
