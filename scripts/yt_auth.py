#!/usr/bin/env python3
"""Autoriza o acesso ao YouTube (OAuth). Salva token.json local. Roda uma vez."""
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

BASE = os.environ.get("YTG_CONFIG_DIR") or os.path.expanduser("~/.youtube-seo")
CLIENT = os.path.join(BASE, "client_secret.json")
TOKEN = os.path.join(BASE, "token.json")
# force-ssl = editar metadados/legendas; yt-analytics = CTR/retenção/inscritos;
# monetary = receita/RPM. Precisa bater com SCOPES do yt.py, senão analytics falha
# por escopo insuficiente. Refresh NÃO amplia escopo: se faltar, força novo consent.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/yt-analytics.readonly",
          "https://www.googleapis.com/auth/yt-analytics-monetary.readonly"]

def main():
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN)  # scopes vêm do token
    have_scopes = creds is not None and creds.has_scopes(SCOPES)
    if creds and creds.valid and have_scopes:
        print("Já autorizado (token válido, escopos completos).")
        return
    if creds and creds.expired and creds.refresh_token and have_scopes:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES)
        # abre o navegador; se não abrir, imprime a URL pra colar manualmente
        creds = flow.run_local_server(port=0, open_browser=True,
                                      authorization_prompt_message="Abrindo o navegador para autorizar...\nSe não abrir, acesse: {url}")
    with open(TOKEN, "w") as f:
        f.write(creds.to_json())
    os.chmod(TOKEN, 0o600)
    print(f"AUTORIZADO. Token salvo em {TOKEN}")

if __name__ == "__main__":
    main()
