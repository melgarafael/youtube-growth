# Método GEO — Otimização de vídeos do YouTube para citação por IA

Como transformar metadados de um vídeo para que ele seja (a) mostrado pelo algoritmo
do YouTube e (b) **citado** por ChatGPT, Perplexity e Google AI Overviews. Base:
pesquisa 2026 + resultados aplicados em canais reais.

## A tese central
**Quase nenhum motor de IA assiste ao vídeo.** ChatGPT/Claude leem só o texto ao redor
(transcrição, descrição, chapters, páginas que embutem o vídeo). Perplexity/Google AIO
extraem *segmentos* via chapters + schema. Logo: **a palavra é o produto, o vídeo é a
entrega.** Otimizar metadados de texto É otimizar para IA.

## Split de citação (onde focar) — dados 2026
| Motor | Share das citações de vídeo | Premia |
|---|---|---|
| Perplexity | 38,7% | Recência (<90 dias) + densidade de citações |
| Google AI Overviews | 36,6% | Engajamento + watch time |
| Google AI Mode | 19,6% | Match semântico da transcrição |
| ChatGPT | 4,4% | Long-form; cita a *página de texto* que embute o vídeo |
| Copilot / Gemini | <1% | Ignoram vídeo |

Perplexity + Google = ~95%. Citação por **segmento/timestamp é quase exclusiva do
Google** → chapters são arquitetura de conteúdo, não enfeite.

## As 5 alavancas (aplicar em cada vídeo)

### 1. Chapters reais (superfície de citação)
- **Sempre extrair a transcrição primeiro** (`transcript.py`) e cortar os capítulos
  nas **viradas reais de assunto** — nunca inventar timestamps.
- Formato: **5–7 chapters** para 12–15 min; **8–10** para 25–60 min. Cada ~1,5–3 min.
- **Título do chapter = a pergunta que alguém digita, respondida.** É o rótulo que a
  IA exibe como fonte. Ruim: `02:15 Configuração`. Bom: `02:15 Como estruturar
  cobrança recorrente de um agente de IA`.
- Na descrição: mín. 3 timestamps, o 1º em `00:00`, ordem crescente. Isso ativa a
  barra de capítulos do YouTube (leva alguns minutos para processar).

### 2. Descrição = ativo de indexação (não rodapé)
- **1ª–2ª linha = bloco-resposta**: 2–3 frases que respondem sozinhas à intenção de
  busca do vídeo, com a keyword primária natural. É o que ChatGPT/Google leem como
  meta-description. Nunca abrir com link.
- Depois: CTAs/links do usuário, seção "O que você vai ver" (expansão semântica com
  vocabulário natural, sem stuffing), depois os CAPÍTULOS.
- Campo aceita 5.000 caracteres — usar bem.

### 3. Título = clique + busca
- Keyword na frente, gancho no fim (YouTube corta ~60 chars na busca/mobile).
- `(Passo a passo)` no fim gasta caractere sem gerar clique — isso é trabalho do
  chapter. Preferir gancho de dor/benefício.
- **Não trocar título de vídeo com tração** (reseta o aprendizado do algoritmo). Para
  ganho de CTR sem risco, testar só a thumbnail (A/B no Studio).

### 4. Tags
- 15–20 tags, keyword primária + variações + entidades (nomes de ferramentas,
  produto). Limite prático ~500 caracteres somados.

### 5. Legenda corrigida (maior impacto de citação isolado)
- Auto-caption erra os termos técnicos (ex.: "HTTB request", "Super Base"). Quando a
  IA cita com o termo errado, perde autoridade. Subir legenda corrigida (`set-caption`)
  ou ao menos garantir os termos certos nos chapters/descrição.

## Regras de UTM (ao mexer em links)
- **Seguir o padrão que o usuário já usa.** Ex.:
  `?utm_source=youtube&utm_medium=<video_id>&utm_id=organico`.
- **Só ADICIONAR onde não existe.** Onde já há UTM, **manter intacto** (não quebrar
  histórico de tracking).
- **Só em domínios do próprio usuário.** Links de afiliado de terceiros e convites de
  WhatsApp: **não tocar** — UTM ali não mede nada e pode atrapalhar o afiliado.
- Preservar o destino (domínio + path). Se o link já tem `?`, usar `&`.

## Distribuição (multiplicador de citação)
Vídeo embutido em domínio de alta confiança entra no índice de citação mais rápido.
Por vídeo long-form: (1) página-companheira no domínio do usuário (embed + transcrição
+ schema VideoObject/Clip); (2) post insight-first no Reddit relevante (link só quando
pedirem nos comentários); (3) artigo no LinkedIn com deep-links de timestamp.

## Anti-slop (o que NÃO fazer)
- Chapters genéricos ("Passo 3", "Introdução") ou com timestamp estimado/errado.
- Descrição que abre com link.
- Título com keyword stuffing ou verbo fraco na frente.
- Copy de molde ("Eleve seu negócio", "Solução completa").
- Reescrever descrição de vídeo com tração jogando fora os CTAs que convertem —
  **aumentar, não substituir**: preservar links e voz do usuário.

## Fluxo de trabalho por vídeo (resumo operacional)
1. `yt.py get <id>` → backup em `~/.youtube-seo/backup/<id>.json`.
2. `transcript.py <id>` → ler a transcrição consolidada.
3. Cortar chapters nas viradas reais; escrever bloco-resposta + "o que você vai ver".
4. Aplicar UTM pela regra (só onde falta, domínio próprio).
5. Vídeo existente: `update-desc`. Vídeo novo/agendado: `set-snippet` (título+desc+tags).
6. `get` de volta para verificar (relembrar do cache de alguns segundos).
7. Opcional: `set-caption` com legenda corrigida.
