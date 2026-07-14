# Aceite manual — onboarding + conexão

Rodar uma vez com um canal real (seu ou de teste):
1. Num diretório novo, rodar `/youtube-growth:start`.
2. Responder o briefing (5 perguntas).
3. Seguir o fluxo de conexão até `bin/yt whoami` imprimir o canal certo.
4. Confirmar o enriquecimento (a IA resume seus vídeos reais).
5. Verificar o vault gerado: `_INDEX.md`, `perfil-canal.md`, `metas.md`, os 3 `_MOC.md`.
6. Rodar `python3 <plugin>/scripts/verify_links.py .` → 0 problemas.
7. Re-rodar `/youtube-growth:start` → deve retomar/dizer que já está pronto, sem duplicar.
