#!/usr/bin/env bash
# Cria o ambiente isolado da skill em ~/.youtube-seo/.venv com as libs do Google.
# Idempotente: pode rodar de novo sem problema. Requer python3 e (uv OU pip).
set -euo pipefail
BASE="${YTG_CONFIG_DIR:-$HOME/.youtube-seo}"
mkdir -p "$BASE" && chmod 700 "$BASE"
VENV="$BASE/.venv"

if command -v uv >/dev/null 2>&1; then
  uv venv "$VENV" --python python3 --quiet
  uv pip install --python "$VENV/bin/python" -q \
    google-api-python-client google-auth-oauthlib google-auth-httplib2
else
  python3 -m venv "$VENV"
  "$VENV/bin/python" -m pip install -q --upgrade pip
  "$VENV/bin/python" -m pip install -q \
    google-api-python-client google-auth-oauthlib google-auth-httplib2
fi
echo "OK: ambiente pronto em $VENV"
echo "Interpreter: $VENV/bin/python"
echo ""
echo "yt-dlp (para transcrição de vídeos públicos):"
command -v yt-dlp >/dev/null 2>&1 && echo "  já instalado: $(command -v yt-dlp)" \
  || echo "  NÃO instalado — instale com: uv tool install yt-dlp  (ou pipx install yt-dlp)"
