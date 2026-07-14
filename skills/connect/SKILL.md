---
name: connect
description: Conecta o canal de YouTube do usuário via YouTube Data API v3 + OAuth. Use no onboarding, quando o usuário pede "conecta meu canal", ou quando o token expira e precisa reautorizar ("conserta minha conexão").
---

# connect — conectar o YouTube do usuário

Guia o usuário (leigo) a conectar o canal DELE. A IA NÃO clica no Google Cloud — narra
cada passo, o usuário executa, a IA verifica.

## Passo 1 — Google Cloud (guiado)
Peça ao usuário para abrir console.cloud.google.com logado na conta DONA do canal.
Oriente, um passo por vez:
1. Criar um projeto (nome livre).
2. Ativar **YouTube Data API v3** E **YouTube Analytics API** (busque cada uma → Ativar).
3. Tela de consentimento OAuth → tipo **External** → em **Test users** adicionar o
   e-mail do próprio usuário. ⚠️ Avise: este é o passo MAIS esquecido; sem ele o auth falha.
4. Credenciais → Criar → ID do cliente OAuth → **App para computador (Desktop)** → baixar JSON.

## Passo 2 — Instalar as credenciais
- Peça o **caminho** do JSON baixado (NUNCA peça pra colar o conteúdo — vai pro histórico).
- Rode `init_channel.py <channel_id_ou_placeholder> <dir_do_usuario>` para criar o config dir
  e o wrapper `bin/yt`. (No 1º run o channel_id ainda é desconhecido; use um slug temporário
  do handle e renomeie depois do whoami se quiser.)
- Copie o JSON para `$YTG_CONFIG_DIR/client_secret.json` com `chmod 600`.
- Valide o tipo: deve ser `"installed"` (Desktop). Se for `"web"`, o usuário criou o tipo
  errado — mande refazer o Passo 1.4.

## Passo 3 — Ambiente + autorização
- Rode `setup_env.sh` (cria o venv + libs Google no config dir). Uma vez por canal.
- Rode `yt_auth.py`. Abre o navegador. Oriente: escolher a conta do canal; no aviso "Google
  não verificou este app", **Avançado → Acessar (não seguro)** — é o app do próprio usuário.

## Passo 4 — Matar a expiração de 7 dias (padrão)
Com a app em "Testing", o token expira a cada ~7 dias. Oriente o usuário a publicar:
Tela de consentimento OAuth → **Publishing status → Publish app → confirmar**. O Google
mostra "app não verificada" (esperado, é o app dele) — seguir. Isso torna a conexão permanente.

## Passo 5 — Verificar
Rode `bin/yt whoami`. Deve imprimir o canal do usuário com inscritos e nº de vídeos.
- Canal ERRADO no output → a pessoa autorizou com a conta errada (canais de marca pertencem
  a uma conta específica). Mande refazer o `yt_auth.py` escolhendo a conta dona.
- Falhou → releia o erro: sem test user (Passo 1.3) ou client_secret errado (Passo 2).

Ao final, confirme para o conductor (onboarding) que a conexão está viva.
