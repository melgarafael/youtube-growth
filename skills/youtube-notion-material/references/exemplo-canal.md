# EXEMPLO-MODELO — Material Notion de um vídeo (caso genérico)

> Exemplo fictício e neutro que mostra os 8 princípios na prática. Substitua o app, a oferta
> e os links pelos dados reais do canal (voz/oferta vêm do onboarding/vault). Note como cada
> um dos 8 princípios aparece no texto — é a referência de QUALIDADE e TOM da skill
> `youtube-notion-material`.

---

# Como subir o seu [App self-hosted] no seu servidor (passo a passo, sem enrolação)

Este guia leva você do zero — sem servidor, sem nada — até o seu app no ar, funcionando de
ponta a ponta. **Não precisa saber programar.** Se travar em algum passo, o assistente do
Claude Code faz por você (veja o Caminho fácil).

> ⏱️ Tempo estimado: **20 a 40 minutos**, a maior parte esperando o domínio "propagar".
> 💰 Custo: o software é **grátis**. Você paga só a hospedagem (VPS) e, se quiser, a IA por uso.

## Visão geral (o que vamos montar)
```
Seu domínio  →  Servidor VPS ([Provedor da oferta])  →  [Seu App] rodando
                        │
                        ├─ o app (site + painel)
                        ├─ as integrações do app
                        └─ os robôs de IA (opcional)
Banco de dados: [provedor grátis]   ·   IA: [provedor de IA] (paga por uso)
```

## Antes de começar, você vai precisar de 3 contas
| O quê | Onde | Custo |
| --- | --- | --- |
| **Servidor VPS** | [Provedor da oferta] (links abaixo) | pago (mensal) |
| **Banco de dados** | [provedor de banco] | grátis |
| **IA** (opcional) | [provedor de IA] | pago por uso |

Crie a conta do banco e da IA agora (leva 2 min cada). O VPS a gente contrata no passo 1.

## Passo 1 — Contrate o servidor (VPS) na [oferta do canal]
O app roda num **VPS com Docker**. A opção mais fácil é um VPS que **já vem com Docker**:
- 👉 **VPS com Docker pronto** — recomendado
- 👉 **VPS padrão** — funciona também (a gente instala o Docker)
- 👉 **Servidor Dedicado** — só se você atende MUITO volume

**Plano recomendado:** a partir de **2 GB de RAM** já roda. Ao contratar, o provedor te
envia o **IP**, um **usuário** (`root`) e uma **senha**. Guarde isso.

## Passo 2 — Entre no servidor
Abra o Terminal (Windows: "PowerShell"; Mac: "Terminal") e digite, trocando pelo seu IP:
```bash
ssh -p PORT root@SEU-IP-AQUI
```
Libere as portas do site:
```bash
ufw allow 22,80,443/tcp && ufw --force enable
```
> ⚠️ **Antes de ativar o firewall, confira em que porta você está por SSH.** Se for diferente
> da 22, troque o `22` pela sua porta — senão o firewall te **tranca pra fora**. Se o provedor
> tiver firewall no painel, libere **80** e **443** lá também (motivo nº1 de o site não abrir).

## Passo 3 — Crie o banco de dados (grátis)
New project → região mais próxima → senha forte. Guarde as chaves de conexão (URL, chave
pública, chave de serviço). Se o provedor oferecer um "pooler" de conexão, use-o.
> **Por que o pooler, e não a conexão direta?** Muitos bancos gerenciados expõem a conexão
> direta **só por IPv6** — e quase todo VPS é IPv4, então ela não conecta e a instalação
> trava. O pooler aceita IPv4 e costuma ser **grátis**.

## Passo 4 — Aponte seu domínio para o servidor
> ⏳ **Faça primeiro, de preferência 1 dia antes** — o domínio leva minutos a horas pra propagar.
Crie um registro **A**: Nome `app` (ou `@`) → aponta pro **IP do servidor**.

## Passo 5 — Instale o app (escolha um caminho)
### Caminho fácil: o Claude Code faz por você
```bash
curl -fsSL https://claude.ai/install.sh | bash
```
Conecte por SSH, abra o Claude Code na VPS e peça:
> *"Clone [URL do repo do projeto] e me instale seguindo o script de setup. Me pergunte as
> chaves uma por uma e resolva os erros."*

### Caminho manual: um comando
```bash
git clone [URL do repo do projeto]
cd [pasta-do-projeto] && bash setup/install.sh
```

## Passo 6-8 — Primeiro acesso · Integrações · IA (chave opcional)
Abra `https://app.seudominio.com.br` (SSL leva ~1 min), configure MFA, conecte as
integrações do app, e cole a chave de IA na área correspondente (se usar).

## Deu certo? Cuide do seu app
| Quero… | Comando |
| --- | --- |
| Ver se está no ar | `bash setup/healthcheck.sh` |
| Atualizar | `bash setup/update.sh` |
| Backup (sempre!) | `bash setup/backup.sh` |
| Esqueci a senha | `bash setup/reset-password.sh seu@email.com` |
> **Backup é sério:** muitos planos grátis de banco não fazem backup sozinhos.

## Travou? Problemas comuns
| Sintoma | O que fazer |
| --- | --- |
| Site não abre / erro de segurança | Domínio não propagou, ou faltou liberar portas. `ufw allow 80,443,22/tcp`. |
| Página recarregando/erro | Faltou uma chave. `docker compose -f docker-compose.prod.yml logs app`. |
| Integração não conecta | `... logs <serviço>`. Confirme que a credencial não está em uso em outro lugar. |

## Por que [a oferta do canal]
O app foi desenhado pra rodar redondo na [oferta]. Além do VPS, você centraliza aí o
registro de domínio e o Servidor Dedicado quando o volume crescer. Todos os links são oficiais.
