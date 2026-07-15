---
name: geo
description: >
  Ferramenta de análise GEO-first (Generative Engine Optimization) para a presença
  web PRÓPRIA do canal (site, landing pages, link-in-bio, blog) — otimiza para ser
  citado por motores de busca com IA (ChatGPT, Claude, Perplexity, Gemini, Google AI
  Overviews) sem abandonar o SEO tradicional. Faz auditoria de página, score de
  citabilidade, análise de acesso de crawlers de IA, geração/validação de llms.txt,
  varredura de menções à marca/criador e schema markup (JSON-LD). Use quando o usuário
  falar "geo", "seo", "auditar site", "visibilidade em IA", "citabilidade", "llms.txt",
  "schema", "menções da marca", ou passar uma URL para analisar. NÃO confundir com a
  skill youtube-geo-growth (que otimiza os metadados dos VÍDEOS do canal).
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write
---

# GEO — otimização da presença web do canal para citação por IA

> **Filosofia:** GEO-first, SEO-supported. A busca com IA está comendo a busca
> tradicional. Esta skill otimiza o que o **canal possui na web** (site, blog,
> link-in-bio) para que o conteúdo — e as entidades por trás dele — seja **citado**
> pelos motores de resposta com IA. Complementa a `youtube-geo-growth` (que cuida dos
> vídeos): aqui o alvo são as páginas próprias que sustentam a autoridade do canal.

> As invocações abaixo usam `$YTG_CONFIG_DIR` (o config dir por-canal criado pela skill
> `connect`) e `<plugin>` = a raiz onde o plugin `youtube-growth` foi instalado.
> Substitua `<plugin>` pelo caminho real de instalação.

## Setup (uma vez)

Esta skill tem dependências Python próprias (BeautifulSoup, requests, lxml, rich).
Instale no venv do canal:

```bash
"$YTG_CONFIG_DIR/.venv/bin/pip" install -r <plugin>/skills/geo/requirements.txt
```

## Scripts (o que embarca de fato)

Rode cada script pelo venv do canal para as deps resolverem:

| Script | Para quê | Invocação |
|--------|----------|-----------|
| `scripts/fetch_page.py` | Baixa/parseia uma página; modos: `page`, `robots`, `llms`, `sitemap`, `blocks`, `full` | `"$YTG_CONFIG_DIR/.venv/bin/python" <plugin>/skills/geo/scripts/fetch_page.py <url> [modo]` |
| `scripts/citability_scorer.py` | Pontua as passagens de uma página para prontidão de citação por IA (0-100) | `"$YTG_CONFIG_DIR/.venv/bin/python" <plugin>/skills/geo/scripts/citability_scorer.py <url>` |
| `scripts/brand_scanner.py` | Varre menções à marca/criador nas plataformas que a IA cita | `"$YTG_CONFIG_DIR/.venv/bin/python" <plugin>/skills/geo/scripts/brand_scanner.py "<marca>" [dominio]` |
| `scripts/llmstxt_generator.py` | Valida ou gera `llms.txt`; modos: `validate`, `generate` | `"$YTG_CONFIG_DIR/.venv/bin/python" <plugin>/skills/geo/scripts/llmstxt_generator.py <url> [modo]` |

Templates de schema JSON-LD ficam em `<plugin>/skills/geo/schema/` (organization,
local-business, article-author, product-ecommerce, software-saas,
website-searchaction) — copie e preencha para o site do canal.

## Fluxo de auditoria (o agente conduz)

**1. Descoberta.** Buscar o HTML da home (script `fetch_page.py <url> full`, ou WebFetch).
Detectar o tipo de negócio/página e extrair as páginas-chave do `sitemap.xml` ou dos
links internos (foco nas ~10-20 mais importantes; teto de 50).

**2. Análise.** Para cada página relevante:
- **Citabilidade**: `citability_scorer.py <url>` — passagens diretas, respondíveis, com
  dado/entidade explícita pontuam mais.
- **Crawlers de IA**: `fetch_page.py <url> robots` — confirmar que GPTBot,
  ClaudeBot, PerplexityBot, Google-Extended não estão bloqueados sem querer.
- **llms.txt**: `llmstxt_generator.py <url> validate` (ou `generate` para criar um).
- **Menções da marca**: `brand_scanner.py "<marca do canal>" <dominio>` — presença em
  plataformas que a IA cita (fóruns, YouTube, wiki, etc.).
- **Schema**: detectar o JSON-LD existente e propor o que falta a partir de `schema/`.

**3. Síntese.** Consolidar num relatório com GEO Score (0-100) e um plano de ação
priorizado. Gravar via Write (ex.: `GEO-AUDIT.md`) no diretório do canal.

## Detecção de tipo de página (ajusta as recomendações)

| Tipo | Sinais | Ênfase |
|------|--------|--------|
| **SaaS** | pricing, "sign up", "free trial", `/app`, API docs | SoftwareApplication schema, páginas de comparação |
| **Local** | telefone, endereço, "perto de mim", mapa | LocalBusiness schema, Google Business Profile |
| **E-commerce** | páginas de produto, carrinho, preço | Product schema, agregação de reviews |
| **Publisher/Blog** | artigos, autoria, datas | Article schema, E-E-A-T, autoria |
| **Outro** | — | boas práticas GEO gerais |

## Metodologia de score

| Categoria | Peso | Medido por |
|-----------|------|-----------|
| Citabilidade & visibilidade em IA | 25% | score de passagens, qualidade de "answer blocks", acesso de crawlers |
| Sinais de autoridade da marca | 20% | menções em plataformas citadas por IA; presença de entidade |
| Qualidade de conteúdo & E-E-A-T | 20% | sinais de expertise, dado original, credenciais de autor |
| Fundamentos técnicos | 15% | SSR, Core Web Vitals, crawlability, mobile, segurança |
| Dados estruturados | 10% | completude de schema, JSON-LD válido |
| Otimização por plataforma | 10% | prontidão p/ Google AIO, ChatGPT, Perplexity |

## Regras de qualidade
- **Limite de crawl:** máx. 50 páginas por auditoria (qualidade > quantidade).
- **Timeout:** 30s por página.
- **Rate limit:** ~1s entre requisições; respeitar sempre o `robots.txt`.
- **Dedup:** pular páginas com >80% de similaridade de conteúdo.

## Contexto de mercado (por que GEO importa)
A busca com IA cresce rápido (Google AI Overviews, ChatGPT, Perplexity com centenas de
milhões de usuários); tráfego referido por IA converte melhor que orgânico tradicional; e
**menções à marca** correlacionam mais forte com citação por IA do que backlinks. Otimizar
a presença web do canal agora é chegar onde o tráfego está indo.
