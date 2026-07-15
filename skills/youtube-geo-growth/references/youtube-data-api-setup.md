# YouTube Data API v3 — Setup e Operação

Guia para conectar-se ao canal do usuário e editar metadados de vídeos (título,
descrição, chapters, tags, legendas) de forma programática e reversível.

## Por que a API (e não cookies / MCP / navegador)

- **Cookies do navegador (`yt-dlp --cookies-from-browser`)**: falham em vídeos
  privados/agendados, especialmente em **canais de marca (brand accounts)** — os
  cookies de conta pessoal não "assumem" o brand channel. Não confiar nisso.
- **MCP de terceiro**: exigiria entregar credencial do canal a um servidor externo.
- **API Data v3 + OAuth**: a via limpa. O token fica local, o usuário autoriza uma
  vez na tela do Google, e a credencial do dono acessa até vídeos privados e baixa
  legendas ASR. É o caminho canônico desta skill.

## Setup único (o usuário faz no Google Cloud, ~10 min)

O passo de autorização só o dono do canal pode fazer. Guiar o usuário:

1. **console.cloud.google.com**, logado na conta Google **dona do canal** (se houver
   múltiplas contas, confirmar a certa — canais de marca pertencem a uma conta).
2. Criar um projeto (nome livre, ex.: `youtube-seo`).
3. Buscar **"YouTube Data API v3"** → **Ativar**.
4. **APIs e serviços → Tela de permissão OAuth**: tipo **External** → preencher nome
   e e-mail → em **Usuários de teste (Test users)** adicionar o próprio e-mail do
   dono. **Este passo é o mais esquecido — sem ele a autorização falha.**
5. **Credenciais → Criar credenciais → ID do cliente OAuth → App para computador
   (Desktop app)** → baixar o JSON.
6. Pedir ao usuário o **caminho** do JSON (não colar o conteúdo no chat — fica no
   histórico). Copiá-lo para `~/.youtube-seo/client_secret.json` com `chmod 600`.

### Validar o client_secret
Deve ser tipo `"installed"` (Desktop app), com `client_secret` e
`redirect_uris: ["http://localhost"]`. Se vier `"web"`, foi criado o tipo errado.

## Autorização (gera o token)

```bash
bash scripts/setup_env.sh                 # cria venv + libs (uma vez)
~/.youtube-seo/.venv/bin/python scripts/yt_auth.py
```

`yt_auth.py` abre o navegador do usuário na tela de consentimento. Orientar:
- Escolher a conta do canal.
- No aviso **"O Google não verificou este app"** (esperado — o app é do próprio
  usuário): **Avançado → Acessar <app> (não seguro)**.
- Marcar a permissão do YouTube → **Continuar** → "fluxo concluído".

O token é salvo em `~/.youtube-seo/token.json` (chmod 600).

### Escopo
`https://www.googleapis.com/auth/youtube.force-ssl` — cobre `videos.update`
(título/descrição/tags) e `captions` (listar/baixar/subir legendas).

### Gotcha do token de 7 dias
Com a tela OAuth em modo **"Testing"**, o refresh token **expira em ~7 dias**. Ao
expirar, é só rodar `yt_auth.py` de novo (1 clique). Para acabar com isso:
publicar o app (OAuth consent → **Publishing status → In production**); como usa
escopo sensível, o Google mostra "app não verificado", mas o dono pode prosseguir
(é o app dele). Não requer verificação para uso próprio.

## Comandos (scripts/yt.py)

Sempre via o interpretador do venv: `~/.youtube-seo/.venv/bin/python scripts/yt.py <cmd>`

| Comando | O que faz |
|---|---|
| `whoami` | Confirma o canal conectado (título, inscritos, nº de vídeos) |
| `get <videoId>` | Imprime título, categoryId, idioma, tags e descrição atuais (JSON) |
| `recent [n]` | Lista uploads recentes **incluindo privados/agendados** (id, privacyStatus, publishAt) — usar para achar um vídeo agendado |
| `update-desc <videoId> <arquivo.txt>` | Atualiza **só a descrição**, preservando título/categoria/tags/idioma |
| `set-snippet <videoId> <arquivo.json>` | Atualiza título+descrição+tags+categoria+idioma de uma vez (para vídeos novos/agendados) |
| `set-caption <videoId> <arquivo.srt>` | Sobe uma legenda corrigida |

### Regras de segurança ao gravar
- **Backup antes**: salvar `get <id>` de cada vídeo em `~/.youtube-seo/backup/<id>.json`
  ANTES de qualquer `update`. `videos.update` sobrescreve — o backup é o undo.
- **`videos.update` exige o snippet com `title` e `categoryId`** senão apaga esses
  campos. `yt.py` já lê o estado atual e preserva o que não muda.
- **Verificar lendo de volta** após cada gravação (`get`), confirmando a mudança.
  Cuidado: a leitura pode pegar cache por alguns segundos — se algo vier "vazio",
  reler antes de concluir que falhou.

## Transcrição (scripts/transcript.py)

```bash
~/.youtube-seo/.venv/bin/python scripts/transcript.py <videoId> [janela_seg]
```
- Vídeo **público**: usa `yt-dlp` (sem auth).
- Vídeo **privado/agendado**: cai automaticamente para a API `captions().download`
  do dono — que baixa até a legenda automática (ASR). Este é o truque que destrava
  chapters de vídeos ainda não publicados.
- Saída: linhas `[MM:SS] texto` em janelas (~40s) — a base para cortar os chapters.

## Quotas
Quota diária padrão: 10.000 unidades. `videos.update` custa ~50; `captions.download`
~200; `search.list` ~100. Suficiente para dezenas de vídeos/dia. Retrofit em lote
grande: espaçar por dias ou pedir aumento de quota no Cloud Console.
