---
name: onboarding
description: Onboarding de um canal de YouTube novo no youtube-growth. Use quando o usuário roda /youtube-growth:start, diz "quero começar", "configurar meu canal", ou está num diretório sem vault ainda. Conduz briefing → conexão → enriquecimento → geração do vault.
---

# onboarding — a porta de entrada

Você é o conductor. Fluxo idempotente: consulte `state.py` (`state_get(user_dir)`) e RETOME
da fase não concluída. Marque cada fase com `state_set` ao terminar. NUNCA recomece do zero.
Fale simples (o usuário é leigo), uma pergunta por vez.

## Fase 0 — Estado
Rode `state_get`. Se `vault_done`, diga que já está pronto e ofereça o próximo passo (vídeo).
Senão, pule para a 1ª fase não concluída.

## Fase 1 — Briefing leve (se não `briefing_done`)
Pergunte, uma de cada vez, sem assumir nicho nem monetização:
1. Qual é o seu canal? (URL ou @handle)
2. Sobre o que ele é, em uma frase?
3. Qual seu objetivo com ele? (alcance / autoridade / vender / comunidade)
4. O que te torna diferente?
5. Você monetiza ou quer monetizar? Como? (se não, deixe vazio)
Guarde as respostas num dict `briefing` e grave em `<user_dir>/.youtube-growth/briefing.json`.
`state_set(user_dir, briefing_done=True)`.

## Fase 2 — Conexão (se não `connected`)
Invoque a skill `connect`. Ao final, confirme com `bin/yt whoami`.
`state_set(user_dir, connected=True)`.

## Fase 3 — Enriquecimento (se não `enriched`)
Rode `bin/yt whoami` e `bin/yt recent 15` para ler o canal real. Se houver vídeos,
resuma para o usuário o que observou (tops por views, durações, temas recorrentes) e
pergunte: "confere? ajusto algo do perfil?". Incorpore as correções ao `briefing`.
Canal SEM vídeos: diga que vai pular esta parte e seguir. `state_set(user_dir, enriched=True)`.

## Fase 4 — Gerar o vault (se não `vault_done`)
Rode `gen_vault.py <briefing.json> <user_dir>`. Ele valida os links sozinho (falha se houver
problema). `state_set(user_dir, vault_done=True)`. Feche: "Vault montado e canal conectado.
Bora pro seu primeiro vídeo?" (handoff pra fase seguinte do produto).
