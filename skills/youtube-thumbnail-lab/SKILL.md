---
name: youtube-thumbnail-lab
description: Laboratório de thumbnails anti-slop para o canal do usuário. Use quando for criar, refinar ou testar a thumbnail de um vídeo — "que thumb usar?", "melhora essa capa", "monta um teste A/B de thumbnail", "por que meu CTR tá baixo?". Baixa as thumbs de referência dos concorrentes que performam e ESCREVE o prompt de geração de imagem por IA (estrutura por zonas + coordenadas), seguindo o padrão vencedor do nicho MAIS o ângulo/prova que só o canal do usuário tem. Define também o teste A/B — trocando a thumb SEM trocar o título de vídeo com tração. O entregável é o PROMPT que gera a imagem, não um briefing pra editor humano. Em muitos canais o gargalo nº1 é alcance/CTR: a thumb é onde se ataca.
---

# YouTube Thumbnail Lab — a capa que faz o clique acontecer

Em muitos canais o gargalo nº1 é **alcance/CTR**: inscritos existem, mas o vídeo
entrega poucas views = a porta não abre. Título + **thumbnail** é onde se ataca. Esta
skill sistematiza a criação de thumbs que fogem do slop e usam a vantagem/ângulo que o
nicho inteiro não tem — o diferencial do canal do usuário (definido no onboarding/vault).

Quando as thumbs do canal são **imagens geradas por IA** (uma IA que renderiza texto na
capa, elementos, iluminação — tudo por coordenada — e coloca o rosto do apresentador a
partir de uma foto-base), o **entregável desta skill é o PROMPT de geração**, não um
briefing pra editor humano. Ela baixa referências, aplica o padrão comprovado e escreve o
prompt pronto pra colar na IA de imagem.

## Pré-requisito
O `fetch_thumbs.py` baixa **imagens públicas** (`i.ytimg.com`) e **não precisa de OAuth**.
Já `bin/yt recent` (listar IDs do próprio canal) exige o **canal conectado pela skill
`connect`**. Confirme com `bin/yt whoami`; se falhar, rode a skill `connect` para
reautorizar.

> As invocações abaixo usam `$YTG_CONFIG_DIR` (setado pela skill `connect`) e `<plugin>` =
> a raiz onde o plugin `youtube-growth` foi instalado. Se `$YTG_CONFIG_DIR` não estiver no
> shell, rode primeiro `connect` ou exporte-a apontando para o config dir do canal.

## A tese (dado, não achismo)

O padrão vem do **benchmark do nicho** (skill `youtube-benchmark`, seção "Análise de
thumbnails" do `RELATORIO.md`). Um exemplo do tipo de leitura que ele produz:

- **Padrão dominante do nicho:** o que se repete nas thumbs que performam — ex.: rosto
  grande e expressivo (30–45% do quadro) + texto GIGANTE de 2–3 palavras com contorno
  sobre fundo escuro neutro + badge (tempo/preço). Extraia isso do benchmark, não do
  achismo.
- **A arma que só o canal tem:** o ângulo/prova que o nicho NÃO mostra e que só o canal do
  usuário pode mostrar (definido no onboarding/vault). O nicho geralmente prova *promessa*;
  a diferença que converte é provar *entrega/resultado* na própria thumb. Onde o benchmark
  mostra todo mundo fazendo a mesma coisa, o ângulo diferente do canal é a clareira.

**Direção estética = a identidade visual do canal** (fonte da verdade: o guia de identidade
do canal no onboarding/vault — seguir de lá). Os princípios abaixo são channel-agnostic;
os valores concretos (paleta, herói visual, fontes) vêm da identidade do canal:

- **Fundo:** coeso com a marca, com profundidade/atmosfera — não chapado genérico, não o
  clichê que qualquer IA cuspiria pro nicho.
- **Herói visual:** um objeto/elemento que DIFERENCIE do nicho (todos usam o mesmo clichê).
  **Elemento de marca entra como OBJETO FÍSICO 3D real** pousado na cena — **nunca** ícone
  plano flutuando. Mantém reconhecimento e foge do padrão.
- **Texto:** poucas palavras (3–4), tipografia **limpa e legível** conforme a identidade,
  com **uma palavra-âncora destacada** (marca-texto/realce), não só contorno. Acento à mão
  (seta/anotação manuscrita) quando ajuda. Evite a fonte-clichê do nicho.
- **A "prova" adapta-se à ESPINHA do vídeo** (não é sempre a mesma): se o vídeo é sobre
  resultado → prova de resultado (renderizada como objeto real, não como print genérico). Se
  é sobre um **mecanismo/método** → o mecanismo é a prova (ex.: a seta ligando causa a
  efeito). Se é jornada/decisão → o rosto do apresentador. Regra: a thumb promete o que o
  vídeo entrega — prova incoerente com a espinha mata retenção.
- **Badge (se usar):** valor/autoridade, nunca "GRÁTIS" de molde. Número concreto pra vídeo
  de resultado; selo de método/fonte pra vídeo de mecanismo.
- **Rosto:** do apresentador, via foto-base, ~28–35% do quadro num canto, iluminação com
  contraste (rim light quente de um lado + fill frio do outro). Expressão casa com a espinha
  (convicção / "sacou?" / calma).

Anti-slop inviolável: se parece o que qualquer IA cuspiria pro nicho (gradiente genérico,
fonte-clichê, ícone chapado flutuando, "GRÁTIS" de molde), refaça. A régua: **parece feito
com capricho editorial, ou parece template?**

> Exemplo de identidade bem-definida (de um canal real, como gabarito de granularidade — NÃO
> copie os valores, defina os do seu canal): look "Dossiê" — fundo índigo→azul-marinho com
> bokeh, herói = documento off-white skeuomórfico, elemento de marca como gema 3D real
> pousada nos documentos, texto sans humanista peso 700 caixa mista com uma palavra em
> marca-texto amarelo. Repare no NÍVEL de especificação — é isso que faz a thumb parecer
> marca e não template.

## Quando usar
- "que thumbnail uso no vídeo X?"
- "melhora/varia essa capa", "por que o CTR tá baixo?"
- "monta um teste A/B de thumbnail"

## Fluxo

### 1. Baixar as referências (o padrão vencedor na sua frente)
Pegue os videoIds dos top do benchmark mais próximo do tema (a coluna de URL do
`RELATORIO.md` da skill `youtube-benchmark`). Baixe as thumbs deles E as do próprio canal
para comparar lado a lado:

```bash
# referências dos concorrentes que performam
"$YTG_CONFIG_DIR/.venv/bin/python" \
  <plugin>/skills/youtube-thumbnail-lab/scripts/fetch_thumbs.py \
  --ids "<id1>,<id2>,<id3>" --out thumbnail-lab/ref --label ref

# suas próprias thumbs de referência (top performers do canal)
"$YTG_CONFIG_DIR/.venv/bin/python" \
  <plugin>/skills/youtube-thumbnail-lab/scripts/fetch_thumbs.py \
  --ids "<id4>,<id5>,<id6>" --out thumbnail-lab/canal --label canal
```

`bin/yt recent 8` lista os IDs recentes do canal se precisar. Depois **abra as imagens
com Read** e anote: onde está a prova/gancho, tamanho do texto, contraste, cor, rosto.

### 2. Escrever o PROMPT de geração (o entregável)
Escreva 1–3 conceitos como prompts prontos pra colar na IA de imagem. Grave em
`thumbnail-lab/<slug-do-video>/prompts-geracao.md`. Este é o produto da skill.

**A receita que funciona (seguir a ordem):**
1. **Abre com formato + estilo:** `Cinematic 16:9 YouTube thumbnail, premium editorial
   style, photorealistic.` (o estilo concreto vem da identidade do canal).
2. **Fundo:** descreva o fundo da identidade do canal com atmosfera/profundidade, e negue o
   clichê do nicho (`NO <clichê genérico do nicho>`).
3. **Uma ZONA por elemento, com coordenada** (x/y em %): descreva UM elemento por zona, da
   esquerda pra direita, criando **um caminho de leitura único** (ex.: herói → seta →
   elemento de marca). Ex.: `LEFT THIRD (x: 5–38%): <herói visual da marca>, <detalhe> …
   ONE word/line highlighted.`
4. **Elemento de marca como objeto físico:** `the <marca> as a REAL 3D physical object
   (…refractive/faceted…) resting on <o herói>` — nunca "ícone flutuando".
5. **Rosto por último entre os objetos:** `RIGHT (x: 68–98%): a person's face and shoulders
   (use provided reference photo for the face), ~30% of frame, warm rim light from one side,
   cool fill from the other, expression: <casa com a espinha>.`
6. **Texto como camada separada, com string EXATA e posição:** `TEXT OVERLAY, top (y: 5–28%,
   not covering the face): clean legible bold sans-serif (<fonte da identidade>), <cor>.
   Line 1: "<...>". Line 2: "<...>". The word "<âncora>" wrapped in a highlighter swipe.`
7. **Fecha com iluminação + cauda anti-slop:** `Cool cinematic lighting, shallow depth of
   field. Anti-slop: no generic gradient, no cliché font, no flat floating icon.`

**Regras do prompt:**
- Escreva a ESTRUTURA em inglês (o modelo obedece melhor), mas as **strings de texto na
  imagem no idioma do canal, exatas**. Modelos erram acento/grafia em frase longa → **máx
  3–4 palavras/linha, 1 palavra no highlight**; confira a grafia no render e
  regenere/corrija se escorregar.
- **Consistência de A/B:** mantenha fundo, elemento de marca, tratamento de rosto e de texto
  IDÊNTICOS entre os conceitos — muda só a ideia central. Look coeso = marca reconhecível no
  feed.
- A "prova" na imagem segue a **espinha do vídeo** (resultado / mecanismo / jornada — ver
  tese acima).

**Checklist anti-slop (rodar em cada prompt):**
- [ ] Caminho de leitura único e claro (um elemento por zona, coordenadas dadas)?
- [ ] Fundo coeso com a marca (não o clichê genérico do nicho)?
- [ ] Herói + marca como objeto físico 3D (não ícone chapado)?
- [ ] Texto 3–4 palavras, tipografia da identidade, 1 palavra no realce?
- [ ] Rosto via foto-base, expressão casa com a espinha, ~28–35% num canto?
- [ ] "Prova" coerente com a espinha do vídeo?
- [ ] Lê a 120px (visão de celular)?
- [ ] Cauda anti-slop no prompt (sem gradiente/fonte/ícone-clichê/"GRÁTIS")?

### 3. Teste A/B de thumbnail
Regra inviolável: **não trocar o TÍTULO de vídeo com tração** (reseta o algoritmo). O teste
é **só na thumb** — o título fica.

⚠️ **Limite honesto (dado real):** **CTR de impressões NÃO é exposto pela YouTube Analytics
API** — só existe no **YouTube Studio**. Logo, o A/B se **mede a mão no Studio**, não pela
API/`bin/yt`. Não prometa medir CTR por script.

**Como rodar e ler (manual, no Studio):**
1. **Escolha 1 vídeo com tração** (impressões/dia estáveis) — o A/B precisa de volume de
   impressões pra dar sinal; vídeo parado não conclui.
2. **Opção A — teste nativo do Studio:** YouTube Studio → vídeo → Detalhes → **"Testar e
   comparar"** (Test & Compare): sobe até 3 thumbs, o próprio YouTube divide as impressões e
   aponta a vencedora por **watch-time share**. É o caminho preferido — decisão do
   algoritmo, sem viés.
3. **Opção B — swap manual** (se o vídeo não tiver o teste nativo): anote a **baseline** no
   Studio → aba **Alcance** → **CTR de impressões** (janela de 7/28 dias) ANTES. Troque a
   thumb (backup da atual primeiro). Espere volume comparável de impressões (não dias fixos:
   **impressões**). Compare CTR do mesmo nº de impressões.
4. **Uma variável por vez:** muda a thumb, o título fica. Se mudar os dois, não sabe o que
   mexeu o número.
5. **Registre** o resultado em `thumbnail-lab/<slug>/ab-resultado.md`: baseline CTR, thumb
   nova, CTR novo, veredito. Vira dado pro próximo vídeo (dado > achismo).

## Arquivos
- `scripts/fetch_thumbs.py` — baixa thumbs (maxres→hq) de uma lista de IDs. Sem OAuth
  (imagem pública). Self-check: `--check`.
- Saídas em `thumbnail-lab/` (referências, `prompts-geracao.md`, resultados de A/B).

## Onde puxar dado
- Padrões de thumb do nicho: skill `youtube-benchmark` → `benchmark/*/RELATORIO.md` (seção
  "Análise de thumbnails").
- Top performers do canal p/ referência: `bin/yt recent` + auditoria do canal (onboarding/vault).
- Voz/ângulo/audiência do canal: definidos no onboarding/vault.
