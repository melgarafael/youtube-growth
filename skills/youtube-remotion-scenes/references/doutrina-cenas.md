# Doutrina de cenas/motion — laboratório (base da futura skill)

Log de aprendizado do 1º vídeo real (open source/VPS, 22:55). Objetivo: destilar QUANDO
inserir, O QUE inserir e COMO, a partir da estratégia dos grandes produtores + os templates
"Dossiê" que já temos. Cada rodada alimenta a skill.

## Princípio-raiz (dado dos grandes produtores)
Pacing é a decisão editorial que mais define retenção — conteúdo mediano com bom pacing
segura mais que conteúdo ótimo com pacing arrastado. Regras observadas:
- **Mudar algo visual a cada 5–7s** (mais denso no arranque). ← isso é CORTE/zoom/b-roll (editor).
- **Pattern interrupt aos ~25–35s** (mini-despertar antes da audiência dispersar).
- **Texto/gráfico cedo pra ancorar** ("3 regras", "o erro") — substitui repetição verbal.
- **Callout de dado no meio de fala longa reseta a atenção visual.**

## A distinção que a skill precisa aprender: 2 MODOS de cena
1. **INSERÇÃO (tela cheia, corta o footage)** — o que a skill já faz. Para: transição de
   bloco, número-prova gigante, tese que merece pausa. Ritmo: ~1 a cada 60–120s (marca
   pontos-chave; não é a cada 5s, senão vira videoclipe).
2. **OVERLAY (sobre o footage, fundo transparente/alpha)** — o que FALTA construir. Para:
   destacar uma palavra/frase enquanto você fala, lower-third, callout de número sem cortar
   o fluxo. Precisa render `.mov` ProRes 4444 com alpha (o roadmap já previa).

**As cenas Remotion NÃO substituem o corte fino** (zoom, b-roll, remover "éé") — isso é do
editor. Elas marcam os picos.

## Mapa: gatilho na fala → tipo de cena (nos 7 templates atuais)
| O que está sendo falado | Cena | Modo |
|---|---|---|
| Número / preço / dado / estatística ("R$1.500/mês", "2.000 apps") | `DossieNumero` (count-up) | inserção OU overlay |
| Frase-soco / tese / insight ("você não é dono") | `DossieCenaFast` (marca-texto) | overlay (ideal) |
| Virada de bloco / novo capítulo | `DossieSecao` (card + título) | inserção |
| Lista de 3 (setup · mensalidade · white-label) | `DossiePilha` (leque) | inserção |
| Abertura de tópico novo ("agora o segredo: Coolify") | `DossiePasta` (pasta abre) | inserção |
| Tese única, forte, que merece drama | `DossiePerspectiva` (3D) | inserção (com parcimônia) |
| Fala mais longa com um destaque | `DossieCena` (lento) | inserção/overlay |

## Regra anti-slop (a que vai pra skill)
Cada cena precisa servir a UM de três: **retenção** (quebra a monotonia num ponto de risco),
**compreensão** (ancora uma ideia difícil) ou **prova** (dá peso a um número). Se não serve a
nenhum, não entra — poluir com motion é tão ruim quanto não ter nenhum.

## Pipeline técnico (o que a skill vai automatizar) — validado nesta rodada
1. **Extrair áudio:** `ffmpeg -i <video.mp4> -ar 16000 -ac 1 -c:a pcm_s16le audio.wav`
2. **Transcrever LOCAL e rápido** (Apple Silicon, privado — não sobe o vídeo pra ninguém):
   `mlx_whisper audio.wav --model mlx-community/whisper-large-v3-turbo --language pt --output-format srt`
   (23 min transcritos em ~1 min no Neural Engine. Instala via `uv pip install mlx-whisper`.)
3. SRT → mapa de cenas (julgamento) → render Remotion → montagem com ffmpeg no timestamp.

## RODADA 1 — resultados e aprendizados (pipeline provado end-to-end)
Provado no vídeo real: transcrição (mlx) → cena Remotion → **overlay alpha (ProRes 4444)** →
ffmpeg monta no footage no timestamp certo. Funciona. Renderizados: `drafts/renders/ov_conta.mov`
(overlay), `ins_passo1.mp4` (inserção), `trecho_overlay.mp4` (montado).

Descobertas (do frame real):
1. **O vídeo é SCREENCAST + cam PIP no canto inferior direito.** Muda tudo:
   - O rosto está no PIP → overlays no resto da tela **não tampam o rosto** (confirmado: o "R$1.000"
     à esquerda não cobriu a cam). Regra: **evitar o canto inferior direito** (é o PIP).
   - A área ativa é a TELA (Excalidraw/terminal/navegador) → overlay **compete com o conteúdo**.
2. **Regra nova — complementar, não repetir.** O footage já mostrava a conta escrita à mão (R$197,
   R$100, n8n…). O overlay "R$1.000 + conta" ficou redundante. Quando a tela já mostra o dado, o
   overlay dá só o **carimbo/total** ("R$1.000", "não são suas") ou é dispensável.
3. **Em screencast, favorecer INSERÇÃO** (tela cheia, corta) — sempre limpa, não compete. A inserção
   "PASSO 1 · CONTRATAR A VPS" ficou perfeita. Overlay fica pra quando a tela NÃO mostra o dado
   (ele falando em pé, ou terminal rodando).
4. **Overlay precisa de âncora configurável** (topo / faixa lateral) — implementado prop `anchor`.

## RODADA 2 — vídeo inteiro montado (18 cenas) + aprendizado do overlay
Entregue: `drafts/renders/vps_montado.mp4` (23:54, 1080p) — 16 inserções + 2 overlays, todas nos
timestamps certos (verificado: PASSO 1 @06:14, pico "A IA SOZINHA" @16:06). Pipeline `build.py`
(render lote + montagem 2 fases) funciona end-to-end.

Aprendizado decisivo (do frame real):
- **Inserções e o pico ficaram ótimos** — card preto de PASSO, DossiePerspectiva do clímax. Cortam
  o footage, não competem. **Em screencast, inserção é a regra.**
- **Os 2 overlays sobre a conta AINDA competem.** Mesmo no topo, o "R$1.000" sobrepôs a conta que
  o criador já desenhou no Excalidraw. Confirma em definitivo: **quando a tela JÁ mostra o dado, não
  sobrepor** — ou remover o overlay, ou usar só um canto vazio pequeno (o topo-esquerda estava livre).
  Regra pra skill: overlay só quando o footage NÃO mostra o dado (ele falando, terminal rodando).
- **Ajuste de texto:** highlight sem espaço ("trabalhaSOZINHA") — o split do marca-texto comeu o
  espaço; corrigir no template (padding no span do highlight).
- **1080p nesta rodada** (rápido); versão final é `--scale=2` (4K nativo).

## RODADA 3 — feedback do dono do canal (regras firmes pra skill)
1. **NENHUMA cena corta o áudio.** Cenas de tela cheia "param o vídeo" (áudio para) — errado.
   TUDO é **overlay POR CIMA** do footage; o áudio/vídeo seguem por baixo. Montagem = só overlay
   (setpts+enable por cena), sem concat, duração = footage. (build.py reescrito.)
2. **Overlay some no fundo branco do screencast** (Excalidraw) → precisa **sombra/halo forte**
   (texto: halo preto multicamada; card: sombra + borda) e **reposição pro canto** (topo-esquerda,
   onde a tela costuma estar vazia), menor. Nunca no centro sobre o conteúdo.
3. **Cena já nos primeiros ~5s** e densidade ao longo de todo o vídeo — retém desde o início.
4. Fix: `whiteSpace: pre-wrap` no highlight (letterSpacing negativo comia o espaço → "trabalhaSOZINHA").

Estas 4 viram REGRAS da skill (não "opções"): overlay-sempre, contraste-garantido, densidade-desde-o-início.

## RODADA 4 — kinetic senior vira o PADRÃO (aprovado pelo dono do canal)
Depois que os 3 primeiros motions ilustrativos ("Segundo Cérebro") ficaram 5/10, um senior de
motion reescreveu o padrão e provamos em **5 cenas kinetic distintas** (Regência, Canal Cresce,
Painel Vivo, VPS Instala, Negócio Constrói). O dono do canal avaliou como **excelente** e mandou tornar
esse o padrão — **substituindo o "travamento" seco do Dossiê pelo pico de impacto kinetic em
TODAS as cenas**, com a IA editando sempre com esse instinto senior, emoção-primeiro.

**O que virou lei da skill:**
1. **`fx.tsx` é o kit canônico.** Impacto (flash+shake+pulso via `useImpact`), `Ricochet`, `countUp`,
   sucção `SUCK`, `GlowDefs`, paleta `KIN`. Toda cena nova nasce dele → "snap" consistente = identidade.
2. **As 8 regras** (stagger · sucção · estados-de-vida · motion blur · pico-de-impacto-num-frame ·
   ricochete · wireframe/glow · props de ajuste) são **obrigatórias**. Ver SKILL.md.
3. **Emoção primeiro.** Decidir a SENSAÇÃO (consolidação · orquestração · momentum · prova · montagem ·
   construção) e escolher a coreografia cuja física a encarna — não ilustrar a palavra literal.
4. **Catálogo de coreografias** (mapa emoção→cena) mora na SKILL.md; cresce quando surge emoção nova.
5. **Personalização pro momento:** `impactFrame` no segundo da palavra-chave; cor pela emoção
   (verde=dinheiro/subida, ciano=IA, dourado=valor, vermelho=YT); densidade (`iconCount`/`tools`/`blocks`)
   pela grandeza da afirmação.
6. **Estilo próprio** escuro + dourado + ciano + verde + vermelho-YT. Dossiê v2 = legacy (migrar o
   fechamento pro impacto kinetic).
7. **Verificar olhando o frame do impacto** antes de dar "pronto" (render ≠ bom).

Renderes de referência: `drafts/renders/amostra_m_{regencia,canal,painel,vps,negocio}.mp4` + `reel_motions_v3.mp4`.
Memórias do lab: feedback-motion-kinetic-padrao, feedback-motion-estado-da-arte.

---

## CRAFT KINETIC — as receitas concretas que fizeram as melhores cenas (RODADA 4, detalhado)
Não é teoria: são os números e truques exatos que produziram o lote aprovado. Reproduza estes
para bater o mesmo nível. Tudo vive em `project/src/fx.tsx` + as `Motion*.tsx`.

### Por que ESTE lote virou o melhor de todos (as 3 causas-raiz)
1. **Extração do kit deu consistência.** Antes, cada cena reimplementava (mal) o impacto. Ao
   extrair `useImpact`/`Ricochet`/`countUp` pro `fx.tsx`, TODAS as cenas passaram a ter o MESMO
   "snap" e o mesmo peso — e peso repetido é o que o olho lê como "identidade/marca", não "clipes soltos".
2. **Emoção-primeiro deu distinção.** Cada cena ganhou um VERBO de movimento diferente (sugar,
   irradiar, disparar, revelar, encaixar, convergir). É a diversidade de física que impede o vídeo
   de cansar quando 30% dele é motion.
3. **Sync no `impactFrame` deu intenção.** O pico caindo na palavra-chave é o que separa "decoração"
   de "reforço". Sem sync, a melhor animação parece genérica.

### A receita EXATA do pico de impacto (`useImpact`, o "snap")
Tudo sincronizado a UM frame (`impactFrame`), sobreposto na mesma keyframe:
- **Flash:** `interpolate(frame-impact, [0,3,8], [0,0.42,0])` num radial `mix-blend-mode: screen`. Sobe em 3 frames, some em 8. Curto = soco, não clarão.
- **Screen-shake (move a CÂMERA, não os elementos):** amplitude `interpolate(frame-impact,[0,7],[3.2,0])`; deslocamento `x=sin(frame*3.1)*amt, y=cos(frame*2.7)*amt`. Frequências diferentes em x/y = trepidação orgânica, não vibração robótica. Aplicar no wrapper que engloba o palco inteiro.
- **Pulso:** `spring({damping:8, mass:0.5, stiffness:200})` → `interpolate(sp,[0,0.45,1],[0,0.16,0])`. Overshoot que incha ~16% e volta. Somar ao scale do núcleo.
- **Ricochete (vida residual):** `spring({damping:15,mass:0.4,stiffness:120})`; 14 partículas em 360°, distância `spread+(i%3)*40`, opacidade `[0,0.2,1]→[0,1,0]`, delay `i%4`. Sem isso, "engole e acaba seco".

### A receita da sucção / engolir (o oposto do impacto)
- **Ease de gravidade:** `SUCK = Easing.bezier(0.55,0,1,0.45)` — ease-out no começo (flutua), puxado e acelerando no fim (sugado). NUNCA linha reta a velocidade constante.
- **Engolir, não sumir:** `scale interpolate(t,[0,0.78,1],[0.85,0.85,0.12])` + `opacity [0,0.12,0.8,1]→[0,1,1,0]`. O elemento vive, voa e É consumido nos últimos ~10 frames.
- **Motion blur ~ velocidade:** `blur interpolate(t,[0.25,0.7,0.93,1],[0,3,7,2])` — cresce no trecho rápido, alivia no impacto.
- **Stagger:** `startF = START + i*STAGGER` (3-4 frames). Ritmo, nunca enxurrada simultânea.

### As 6 coreografias — o VERBO e o truque técnico de cada (o que as torna distintas)
- **CerebroAbsorve — SUGAR.** Ícones em anel são puxados ao núcleo (SUCK) e engolidos; sinapses acendem conforme `absorbFrac`; núcleo de luz radial cresce e "come" os que chegam. Emoção: consolidação/alívio.
- **Regência — IRRADIAR.** Core central desenha FEIXES até nós pré-posicionados, ativando em cascata (o oposto de sugar: energia SAI). Uníssono no impacto (todos os feixes pulsam juntos). Emoção: orquestração/controle.
- **CanalCresce — DISPARAR.** Count-up + `clipPath` revelando o gráfico L→R que bate o pico EXATO no `impactFrame`; foguete/seta sobe com blur no impacto. Momentum vertical. Emoção: subida.
- **PainelVivo — REVELAR (UI ganha vida).** Rebuild FIEL de um dashboard real (números reais do canal de exemplo) em estilo kinetic; 4 tiles com snap + count-up, área desenhando o pico, barras "em tempo real" ondulando (`sin(frame)`), inscritos subindo. Técnica de maior impacto: **dado como movimento**. Emoção: prova/autoridade.
- **VpsInstala — ENCAIXAR.** Chips voam e docam no rack com snap (overshoot `interpolate(snap,[0,0.5,1],[1.18,0.92,1])`); barra de progresso enche; check spring-pop. **Stagger < duração-de-install** → vários instalam ao mesmo tempo (67%, 7%) = montagem viva, não fila. Emoção: competência.
- **NegocioConstrói — CONVERGIR.** Blocos vêm de scatter determinístico e travam numa malha 3×2; conector desenha SÓ depois dos DOIS vizinhos no lugar (`max(arrivalA,arrivalB)`); nó dourado no meio de cada aresta = a "camada de IA" amarrando. Contorno fecha a "máquina" no impacto. Emoção: construção/completude.

### Técnicas transversais (valem pra qualquer cena nova)
- **Determinismo obrigatório** (render não pode variar): scatter via seed de índice (`(i*47)%360`), nunca `Math.random`/`Date.now`.
- **Cor conta história:** acento por emoção — verde `#3BD07A` subida/dinheiro · ciano `#4DD0E1` IA/neural · dourado `#FFC24B` valor/conhecimento · vermelho `#E4574C` YouTube/urgência.
- **Título entra DEPOIS do soco** (`impact+6`), nunca competindo com o pico.
- **`clipPath` com `<rect width={clipW}>` crescendo** é o jeito robusto de "desenhar" gráfico/linha L→R (mais confiável que stroke-dashoffset pra áreas).
- **Count-up desacelera** (`OUT`) e termina no impacto + punch de escala (`1+pulse*k`).
- **Gotcha de montagem:** `ffmpeg -f concat` resolve `file '...'` RELATIVO ao arquivo de lista — usar caminhos ABSOLUTOS na lista.
- **Overlay em screencast:** `transparent:true` + halo/sombra forte + canto vazio (topo-esq), nunca sobre o que a tela já mostra; evitar canto inf-direito (PIP).

## Perguntas em aberto pra este lab (a validar com o vídeo real + o dono do canal)
- Densidade certa: quantas cenas em 23 min? (hipótese: 12–18 inserções + N overlays)
- Duração de cada inserção (o portfólio tem 5s "Fast" e mais lentas) — qual segura sem arrastar?
- A identidade "Dossiê" (índigo/documento/caderno) combina com o conteúdo tech (VPS/terminal)?
- Overlay é obrigatório ou dá pra entregar valor só com inserção nesta 1ª rodada?
