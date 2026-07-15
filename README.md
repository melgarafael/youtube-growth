<div align="center">

# 🎬 youtube-growth

### Uma agência de crescimento de YouTube que roda no seu terminal — e conhece o **seu** canal.

[![License: MIT](https://img.shields.io/badge/license-MIT-black.svg)](./LICENSE)
[![Feito para Claude Code](https://img.shields.io/badge/feito%20para-Claude%20Code-d97757.svg)](https://claude.com/claude-code)
[![Status](https://img.shields.io/badge/status-v0.2%20%C2%B7%2014%20skills-blue.svg)](#-status--roadmap)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-contribuindo)
[![pt-br](https://img.shields.io/badge/idioma-pt--br-009c3b.svg)](#)

</div>

---

A maioria das ferramentas de IA pra YouTube cospe o mesmo conselho genérico pra todo mundo — porque **não fazem ideia** de qual é o seu nicho, quais são os seus números, ou o que já deu certo no seu canal.

Essa faz.

`youtube-growth` conecta no seu canal **de verdade** (pela API oficial do YouTube), lê seus dados reais e monta um **segundo cérebro** sobre ele. Esse cérebro vira a base de tudo o que vem depois: achar tema, roteirizar, editar o vídeo, escrever o SEO — e otimizar pra você ser **citado por IA** (ChatGPT, Perplexity, Google AI). Open source, qualquer nicho, rodando dentro do [Claude Code](https://claude.com/claude-code).

Você não configura uma ferramenta. Você contrata um time.

---

## 😮‍💨 O problema

Você abre mais um app de IA pra YouTube e ele te pergunta... nada. Já sai cuspindo "10 ideias de título virais" que servem pra qualquer canal do planeta — ou seja, pra nenhum.

- Ele não sabe que **seu** público responde a tutorial e ignora vídeo conceitual.
- Ele não viu que **seu** vídeo de 6 minutos bateu o de 40.
- Ele não amarra o vídeo a uma **oferta** — porque não sabe que você tem uma.
- E ele com certeza não otimizou nada pra ChatGPT te citar como fonte.

Resultado: você faz no olhômetro, posta na esperança, e o canal anda de lado.

## ✨ Como funciona

Um comando (`/youtube-growth:start`) e a IA conduz o resto:

```
  ┌─────────────┐   ┌─────────────┐   ┌──────────────┐   ┌─────────────┐
  │  BRIEFING   │ → │  CONEXÃO    │ → │ ENRIQUECER   │ → │   VAULT     │
  │  5 perguntas│   │  seu YouTube│   │ lê seu canal │   │  segundo    │
  │  do canal   │   │  (guiado)   │   │  real (API)  │   │  cérebro    │
  └─────────────┘   └─────────────┘   └──────────────┘   └─────────────┘
        ↓                                                       ↓
   sem assumir                                          e daqui pra frente:
   nicho nenhum                              pauta → roteiro → edição → SEO/GEO → agendar
```

1. **Briefing leve** — 5 perguntas sobre o canal. Sem formulário gigante, sem assumir seu nicho.
2. **Conexão guiada** — te leva pelo Google Cloud passo a passo até seu YouTube estar conectado. (Sim, aquela parte chata — a IA segura sua mão nela, inclusive matando a expiração de token que todo mundo esquece.)
3. **Enriquecimento** — a IA lê seus vídeos reais e completa seu perfil com **dado, não achismo**: "seus tops são X e Y, seu público parece responder a Z — confere?"
4. **Vault** — monta seu segundo cérebro (perfil, metas, áreas), pronto pra virar a base da máquina de conteúdo.

## 🧠 Por que é diferente

**→ Conhece o seu canal, não "canais em geral."**
Trabalha a partir dos seus números reais, puxados pela API. Nada de conselho de molde.

**→ Constrói um segundo cérebro, não respostas descartáveis.**
Cada insight vira uma nota interligada no [método Karpathy](https://karpathy.bearblog.dev/) (matéria-prima → conhecimento compilado → produção). É **seu**, fica no seu diretório, e você edita à vontade. A IA mantém; você manda.

**→ Otimiza pra ser citado por IA (GEO), não só pra rankear (SEO).**
ChatGPT e Perplexity quase nunca *assistem* ao vídeo — eles leem o **texto** (transcrição, chapters, descrição). Aqui a palavra é o produto e o vídeo é a entrega. Quase nenhuma ferramenta de YouTube pensa nisso ainda.

**→ Qualquer nicho. Culinária, fitness, código, o que for.**
O motor é genérico. Nenhuma doutrina é imposta — o briefing preenche o que é seu.

**→ Roda no seu terminal e é aberto.**
Sem SaaS, sem mandar a credencial do seu canal pra servidor de terceiro. O token fica na sua máquina. O código é seu pra ler e mudar.

## 🚀 Começando

**Requisitos:** [Claude Code](https://claude.com/claude-code) **ou** [OpenClaw](https://openclaw.ai) · um canal no YouTube · uma conta Google (pra criar o projeto no Google Cloud — a IA te guia).

### No Claude Code

```bash
# 1. Adicione o marketplace e instale o plugin
/plugin marketplace add melgarafael/youtube-growth
/plugin install youtube-growth@youtube-growth
```

### No OpenClaw — um comando

```bash
openclaw plugins install youtube-growth --marketplace melgarafael/youtube-growth
```

> 💡 **Zero restart:** instale o plugin **antes** de começar a usar (a primeira sessão já
> carrega tudo). Se o seu gateway já estava rodando, recarregue com `openclaw gateway restart`
> — ou rode em uma linha só:
> ```bash
> openclaw plugins install youtube-growth --marketplace melgarafael/youtube-growth && openclaw gateway restart
> ```
> `--marketplace` aceita `melgarafael/youtube-growth` ou a URL completa do repo. O prefixo
> `github:` **não** funciona, e passar a URL sem `--marketplace` dá `URLs are not allowed`.

### Depois (em qualquer um dos dois)

```bash
# Vá até a pasta do seu canal (ou crie uma) e comece
/youtube-growth:start
```

É isso. A IA conduz o briefing, te leva pela conexão e monta seu vault. Da primeira vez, separe ~10 min pra parte do Google Cloud (é uma vez só).

## 📦 O que tem dentro

```
youtube-growth/
├── skills/
│   ├── onboarding/     → o maestro: briefing → conexão → enriquecer → vault
│   └── connect/        → conecta seu YouTube (Google Cloud + OAuth, guiado)
├── scripts/
│   ├── yt.py           → fala com a YouTube Data + Analytics API
│   ├── gen_vault.py    → gera seu segundo cérebro (com verificação de links)
│   ├── verify_links.py → garante que o vault nunca tem link quebrado ou nota órfã
│   └── init_channel.py → isola credenciais por canal, fora do repo
├── templates/          → o molde do vault que o onboarding preenche
└── commands/start.md   → /youtube-growth:start
```

Seus segredos (client_secret, token) **nunca** entram no repo — ficam em `~/.config/youtube-growth/`, fora de tudo.

## 🗺️ Status & Roadmap

Este projeto está sendo construído em fatias, cada uma testada de verdade antes de entrar. Honestidade acima de hype:

- [x] **Fase 1 — Onboarding + Conexão** *(v0.1, live)* — briefing, conexão guiada do YouTube, enriquecimento do canal real, geração do vault.
- [ ] **Fase 2 — O Motor** — benchmark de concorrentes, pipeline de pautas, thumbnails anti-slop, edição de metadados (SEO/GEO) e edição de vídeo (cenas Remotion).
- [ ] **Fase 3 — O Ciclo de Vídeo** — o conductor que te leva ponta a ponta: tema → gravar → editar → agendar → publicar.
- [ ] Instalação em um clique · internacionalização (i18n).

> As skills da Fase 2 já existem como protótipos; estão sendo de-generalizadas (tirando o que é específico de um canal) pra entrarem no plugin. Acompanhe as issues.

## 🧭 O método (a opinião por trás)

Ferramenta sem opinião gera conteúdo sem alma. As regras da casa:

- **Segundo cérebro, não caixa-preta.** Método Karpathy: você coleta, a IA compila e interliga, tudo fica auditável e seu.
- **A palavra é o produto (GEO).** Otimizar o texto ao redor do vídeo é otimizar pra IA te citar. Chapters são arquitetura, não enfeite.
- **Anti-slop, sempre.** Nada de título, thumb ou copy que qualquer IA cuspiria sem pensar. Se parece genérico, refaz.
- **Dado antes de achismo.** Toda recomendação se apoia em número — views, retenção, benchmark — não em opinião solta.

## 🤝 Contribuindo

PRs são bem-vindos. Achou um bug, quer uma skill nova, quer traduzir? Abra uma issue ou um PR. Cada mudança vem com teste — a suíte roda com `python3 -m pytest`.

## 📄 Licença

[MIT](./LICENSE) — use, forke, venda em cima. Só não finja que escreveu do zero. 😉

---

<div align="center">
<sub>Feito por <a href="https://github.com/melgarafael">Rafael Melgaço</a> · porque seu canal merece um time, não mais um app genérico.</sub>
</div>
