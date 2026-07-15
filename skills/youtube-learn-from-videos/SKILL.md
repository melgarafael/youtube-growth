---
name: youtube-learn-from-videos
description: Aprende o modus operandi de RETENÇÃO de um vídeo de referência (viral do nicho ou concorrente) e destila o que é replicável no canal do usuário. Use quando o usuário quiser entender por que um vídeo prende/segura audiência, extrair a fórmula de um vídeo que bombou, dissecar o hook/gancho/pacing/CTA de um vídeo, aprender com um concorrente, fazer engenharia reversa de um viral, ou descobrir como aumentar retenção. Dado um videoId ou URL, extrai a transcrição, mede de forma determinística a densidade de ganchos, o hook (0-45s), o pacing e onde a audiência escapa, cruza com o que o canal já performa (Analytics API) e escreve um relatório ACIONÁVEL de como aplicar o padrão no próximo vídeo — na voz/ângulo do canal do usuário (onboarding/vault), anti-slop, extraindo o padrão sem copiar. Não confundir com youtube-benchmark (que acha TEMAS/thumbs quentes do nicho) nem com youtube-geo-growth (que EDITA os metadados de um vídeo).
---

# YouTube — Aprender com Vídeos que Performam

Faz engenharia reversa do **modus operandi de retenção** de um vídeo de referência e traz
o padrão replicável para o canal do usuário. Foco num gargalo comum: a retenção. O
algoritmo decide alcance pela retenção, então destilar como um viral **re-prende a
audiência** é o que move o crescimento do canal.

Parte **determinística** (dado duro: hook, densidade de ganchos, pacing, CTA) via
`retention_scan.py`; o **julgamento** (o padrão, como aplicar, o que não copiar) fica com o
agente — como no `youtube-benchmark`.

## Quando usar
- "por que esse vídeo prende tanto? o que dá pra roubar?"
- "disseca o hook / o pacing / a estrutura desse vídeo que bombou"
- "engenharia reversa desse viral de [tema do nicho]"
- "como aumentar a retenção do meu próximo vídeo?"

Não use para achar TEMA quente ou padrão de thumbnail (isso é `youtube-benchmark`) nem para
editar metadados de um vídeo (isso é `youtube-geo-growth`).

## Pré-requisito
Canal conectado pela skill `connect` (token OAuth vivo). Confirme com `bin/yt whoami`; se
falhar, rode a skill `connect` para reautorizar.

A transcrição precisa estar acessível. Vídeo público → `transcript.py` usa yt-dlp (sem
auth). Vídeo do próprio usuário privado/agendado → cai para a API do dono, usando a MESMA
credencial OAuth do canal (skill `connect`). O cruzamento com o canal usa
`bin/yt analytics` (Analytics API ligada no `connect`).

> As invocações abaixo usam `$YTG_CONFIG_DIR` (setado pela skill `connect`) e
> `<plugin>` = a raiz onde o plugin `youtube-growth` foi instalado. Se
> `$YTG_CONFIG_DIR` não estiver no shell, rode primeiro `connect` ou exporte-a
> apontando para o config dir do canal.

## Fluxo

1. **Pegar o videoId** do vídeo de referência (da URL: `youtu.be/<ID>` ou `watch?v=<ID>`).

2. **Medir (o script faz o dado duro):**
   ```bash
   "$YTG_CONFIG_DIR/.venv/bin/python" \
     <plugin>/skills/youtube-learn-from-videos/scripts/retention_scan.py <videoId>
   ```
   Ele roda a transcrição (janela fina de 20s), mede e escreve um scaffold em
   `drafts/aprendizado-<videoId>.md` com o **DADO já preenchido**: hook (0-45s), **a cada
   quantos segundos re-prende** (avg_gap), ganchos/min, pacing (palavras/min), stakes
   (dinheiro/cliente/erro), a **zona de risco** (maior trecho sem gancho) e os CTAs com
   timestamp. O JSON também sai no stdout; a transcrição completa fica em `/tmp/tr_<id>.txt`.
   - Vídeo do próprio usuário privado/agendado: acrescentar `--owner`.

3. **Ler a transcrição INTEIRA** (`/tmp/tr_<id>.txt`) — o dado aponta ONDE olhar; o
   padrão narrativo só aparece lendo. Não pule esta etapa.

4. **Cruzar com o canal (dado > achismo):** rodar `bin/yt analytics <videoId>` num
   **top performer do canal** (`bin/yt recent` para achar os IDs) e comparar a retenção — o
   padrão do vídeo de referência bate com o que já segura audiência no canal do usuário, ou
   contradiz? Registrar a conclusão.

5. **Escrever o relatório acionável:** preencher as seções 2–5 do
   `drafts/aprendizado-<videoId>.md`. Precisa ser **acionável, não resumo do vídeo**: o
   padrão replicável, o hook reescrito no molde certo, a meta de densidade de ganchos, o
   CTA amarrado à oferta, e o que NÃO copiar.

## Como destilar (o julgamento — leia antes de escrever)

- **Hook (0-45s):** que dor/promessa abre? Tem que aterrar no eixo de valor do canal
  (dinheiro / controle / reputação, conforme o onboarding/vault) — nunca uma promessa
  genérica e vazia. Se o hook do vídeo é curioso mas vazio, o valor é a MECÂNICA
  (contraste, pergunta, stakes), não o conteúdo.
- **Densidade de ganchos:** `avg_gap` diz a cada quantos segundos re-prende. Meta pro
  roteiro do canal: cobrir todo trecho >45s sem gancho com um open loop. A **zona de
  risco** que o script marca é exatamente onde a audiência do canal escaparia.
- **Estrutura:** o padrão comum é **problema → diagnóstico → caminho** (ver o perfil do
  canal no vault). Ver se o vídeo de referência segue isso e onde o encadeamento é mais forte.
- **CTA:** posição e forma que o criador usou; amarrar a **UMA** oferta clara do canal
  (ver o mapa vídeo→oferta no vault/onboarding).

## Anti-slop (inviolável)
- **Extrair o PADRÃO, não copiar** a fala. O resultado tem que sair na voz/ângulo do canal
  do usuário (definidos no onboarding/vault).
- Nada de hook clickbait vazio que quebra reputação — o público compra confiança.
- Se a recomendação serve pra qualquer canal, está genérica demais: refaça amarrando ao
  nicho do canal e a um dado (o número do scan ou do `analytics`).

## Arquivos
- `scripts/retention_scan.py` — transcreve (reusa `transcript.py`) + mede retenção +
  escreve o scaffold do relatório. O julgamento (seções 2–5) é do agente.
- Saída: `drafts/aprendizado-<videoId>.md`. Transcrição bruta: `/tmp/tr_<id>.txt`.
