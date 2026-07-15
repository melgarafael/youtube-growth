---
name: youtube-community-opensource
description: Formato "Open Code / construir em público" — o motor de co-criação, a audiência que CO-CRIA open source com o canal. Use ao planejar, roteirizar ou fechar um vídeo de construir junto (série Open Code, "criei um SaaS ao vivo", "montei X open source"), ao definir o CTA que leva espectador → GitHub → comunidade do canal, ou ao medir quanta co-criação o canal gerou. Entrega a estrutura replicável do episódio (ignição → primeiro resultado → expandir), a trilha de conversão em 3 degraus (star → issue → membro), os templates de convite/issue/descrição na voz do canal, e a métrica-âncora do motor (co-criadores por projeto). Mecânica concreta de co-criação, nunca "engaje com a comunidade".
---

# Open Code — a audiência que constrói junto

O motor de co-criação do canal: transformar espectador passivo em **co-criador** de
projetos open source do canal, e desse trilho alimentar a **comunidade paga do canal**
(o motor de recorrência/MRR). Se o canal já pratica o formato ("Open Code #04/#06",
"criei um SaaS ao vivo até a primeira venda"), esta skill sistematiza o formato para
repetir e o loop composto funcionar sozinho.

Princípio: co-criação não nasce de "comenta aí". Nasce de dar uma **peça funcionando**,
apontar uma **tarefa nomeada** e creditar quem pega. A fórmula aplicada:
**ignição** (mostra que dá pra fazer) → **primeiro resultado** (a peça roda na tela) →
**expandir** (o repo vira base pro caso de uso de cada espectador).

## Quando usar
- Planejar/roteirizar um episódio Open Code ou qualquer vídeo de "construir em público".
- Definir o CTA e a descrição que convertem espectador em contribuidor/membro.
- Fechar o loop: creditar contribuições e medir o motor (quanto o canal co-criou).
- Escolher QUAL projeto vira série (fit com a dor da audiência + com uma oferta).

## Pré-requisitos (o que tem que existir ANTES de gravar)
1. **Um repo público pronto pra receber gente.** Ex.: `github.com/<seu-usuario>/<REPO>`.
   README com "como rodar em 5 min", `LICENSE`, e — crucial — **issues reais abertas e
   rotuladas** `good first issue` / `help wanted`, cada uma com resultado concreto no
   título (não "refatorar util", e sim uma feature que o espectador reconhece que precisa,
   ex.: "adicionar export de dados (#12)").
2. **Issue template** com o campo de atribuição (`.github/ISSUE_TEMPLATE`): uma linha
   "Cheguei pelo vídeo: \_\_\_". É assim que a co-criação vira dado sem chute.
3. **Link da comunidade com UTM** pronto (ver Trilha, degrau 3).

Sem os 3, o vídeo gera view e não gera contribuidor. Monte isso primeiro (ou peça a quem
cuida do setup do repo).

## A estrutura replicável do episódio (o roteiro Open Code)

Cinco blocos. Os tempos são âncora, não camisa de força — o que não pode faltar é a
ordem (dor → peça rodando → convite nomeado → horizonte → ponte).

1. **Abertura pela DOR, não pelo projeto (0–45s).** Nunca "hoje vou construir um SaaS".
   Sempre a dor concreta da audiência (o que ela ganha ou evita perder): *"Todo mundo no
   seu nicho perde X porque não tem Y. Vou construir a peça que resolve isso, aberta, e no
   fim do vídeo você pega ela pro seu caso."* Isso é a **ignição**: promete um resultado
   que o espectador leva.

2. **Primeiro resultado AO VIVO (o menor que funciona).** Constrói na tela a menor fatia
   que roda ponta-a-ponta — do commit ao "olha funcionando". O espectador vê a peça
   entregando valor, não slides. Esse é o **primeiro resultado** da fórmula: a prova de
   que dá, e que ele conseguiria refazer.

3. **O CONVITE CONCRETO (o coração da co-criação).** Repo na tela. Aponte **2–3 issues
   REAIS** já abertas, cada uma dita pelo número e pelo ganho: *"a #12 é adicionar tal
   feature — coisa que a galera do nicho vive pedindo; quem pegar tem o nome no projeto."*
   Banido: "deixa nos comentários o que fazer". O convite é uma **tarefa com dono em
   aberto**, não uma caixa de sugestão. Ponha os números das issues na descrição.

4. **Expandir possibilidades (o horizonte + prova social).** Mostre o roadmap do repo
   ("com essa base você pluga isto, aquilo, tal integração") e **feche o loop do episódio
   anterior**: mostre 1 contribuição que já chegou, credite a pessoa na tela (Muro dos
   Co-Criadores). Isso prova que co-criar ali acontece de verdade — o que converte o
   próximo.

5. **Ponte em camadas (fechamento).** Não um CTA, três degraus de compromisso crescente
   (ver Trilha). Star agora → pega uma issue essa semana → constrói junto toda semana na
   comunidade.

**O loop composto entre episódios:** todo episódio ABRE creditando quem contribuiu no
anterior e FECHA convidando pro próximo. Contribuir passa a dar palco no canal — esse é o
incentivo que faz a audiência voltar como co-criadora, não como plateia.

## A trilha YouTube → GitHub → Comunidade (a ponte de co-criação)

Escada de compromisso: cada degrau pede um pouco mais e filtra pra frente. Os três
aparecem no vídeo (fala + tela) e na descrição, sempre nesta ordem.

| Degrau | Ação | Atrito | Onde leva | Papel |
|---|---|---|---|---|
| 1 · Star | "deixa a estrela — é o combustível do projeto" | baixo | link direto do repo | leading indicator, marca intenção |
| 2 · Issue | "pega a #12, é uma feature que a galera pede" | médio | lista filtrada `label:"good first issue"` | **co-criação de verdade** |
| 3 · Comunidade | "a gente constrói isso junto toda semana, com suporte" | alto | link da comunidade do canal | **MRR — alimenta a recorrência** |

Link do degrau 3 SEMPRE com UTM (padrão do canal, `utm_medium` = id do vídeo):
```
https://<link-da-sua-comunidade>/?utm_source=youtube&utm_medium=<VIDEO_ID>&utm_id=opencode
```
Assim a venda/entrada na comunidade vinda do trilho open-code fica atribuível. O degrau 3
é o que liga comunidade a dinheiro: a comunidade é recorrência.

### Templates na voz do canal (copiar e ajustar à voz e ao ângulo definidos no onboarding/vault)

**Descrição do vídeo (bloco Open Code — soma ao CTA existente, não substitui):**
```
🛠️ CONSTRUÍMOS JUNTO — este projeto é aberto e seu:
→ Repo (deixa a ⭐, é o que move): https://github.com/<seu-usuario>/<REPO>
→ Pega uma tarefa e coloca teu nome no projeto (issues "good first issue"):
   https://github.com/<seu-usuario>/<REPO>/issues?q=is:open+label:"good first issue"
   Nesse vídeo citei a #<N1>, #<N2>, #<N3> — abre uma delas.
→ Construir junto toda semana, com suporte, dentro da comunidade:
   https://<link-da-sua-comunidade>/?utm_source=youtube&utm_medium=<VIDEO_ID>&utm_id=opencode

Abriu uma issue ou mandou PR? Marca "vim pelo YouTube" — teu nome entra no Muro dos
Co-Criadores no próximo vídeo.
```

**Comentário fixado (pinned):**
```
Quem for pegar a #<N1> comenta aqui "peguei" pra ninguém colidir. Dúvida de setup? Manda
que respondo. O nome de quem mandar PR mergeado esse mês vai pro vídeo. 🚀
```

**Issue "good first issue" (título + corpo curto):**
```
Título:  <Feature com ganho claro pro usuário>  (bom primeiro PR)
Corpo:   Resultado pra quem usa: <o benefício concreto, em uma frase>.
         Por onde começar: <arquivo/função>. Escopo fechado, ~1h.
         Chegou por um vídeo? Diz qual aqui: ___  (pra creditar você)
```

Anti-slop: título de issue com **ganho concreto**, escopo fechado e "por onde começar" —
não um TODO vago. Uma issue nomeada e pequena é o que faz o iniciante virar contribuidor.

## A métrica-âncora do motor de co-criação

Este motor mede **co-criação**, não vaidade. North-star por projeto:

> **Co-Criadores por projeto (CC)** = nº de pessoas distintas, atribuíveis ao canal, que
> deram um passo verificável de co-criação: **issue acionável aberta** ou **PR mergeado**.

Star é leading indicator (intenção), não co-criação — entra como KPI de apoio, não como a
âncora. PR mergeado é o sinal mais forte; issue acionável conta porque também move o
projeto. "Atribuível ao canal" = a pessoa marcou o campo de origem, ou a issue/PR chegou
na janela de 7 dias após um episódio com o repo em pauta.

**KPIs de apoio (o funil que puxa a âncora):**
- ⭐ **Stars ganhas por episódio** (delta 72h pós-publicação) — abertura do funil.
- 🔀 **Contribuidores novos / episódio** — quantos passaram de star pra issue/PR.
- 💰 **Membros da comunidade via trilho open-code** (UTM `utm_id=opencode`) — o elo com o
  MRR/recorrência. É o número que liga comunidade a receita.

**Alvo sugerido pra 1ª rodada** (a cravar no briefing/metas do canal): fechar um período de
~6 meses com **≥ 1 projeto ativo, ≥ 25 co-criadores e ≥ 10 membros da comunidade vindos do
open-code**. Régua de plantio — sobe quando bater.

### Como medir (dado, não achismo)
- **Stars / contribuidores / issues abertas** do repo — GitHub API, uma linha:
  ```bash
  gh api repos/<seu-usuario>/<REPO> --jq '{stars: .stargazers_count, forks: .forks_count, open_issues: .open_issues_count}'
  gh api 'repos/<seu-usuario>/<REPO>/contributors?per_page=100' --jq 'length'
  ```
  (Sem `gh`, trocar por `curl -s https://api.github.com/repos/<seu-usuario>/<REPO>`.)
  Registrar o número ANTES de publicar e 72h/7d DEPOIS → o delta é o efeito do episódio.
- **Membros via open-code**: contagem por `utm_id=opencode` no destino da comunidade
  (mesmo tracking do trilho de recorrência do canal).
- **Atribuição limpa**: o campo "vim pelo vídeo" na issue/PR + a janela de 7 dias. Sem
  campo e fora da janela, não conte como do canal — a âncora não mente.

Atualizar o briefing/metas do canal (linha do motor de co-criação) a cada episódio da série.

## Escolher o projeto certo pra série
Vira Open Code o projeto que cruza **dor da audiência** × **fit com uma oferta**:
- Resolve uma dor concreta do público (o que ele ganha ou evita perder), não é brinquedo
  técnico.
- Tem base pequena que roda em minutos (primeiro resultado viável ao vivo).
- Puxa uma oferta: a construção semanal mora na comunidade (MRR). Ex.: um projeto open
  source que resolve a dor central do nicho → dor real + trilho natural pra comunidade do
  canal.
Se o projeto não amarra numa oferta, ele gera comunidade sem receita — pensar em camadas do
mesmo ecossistema, não projeto solto.

## Não faça (anti-slop do motor de co-criação)
- ❌ "Comenta aí o que construir" → ✅ issue nomeada, numerada, com ganho concreto.
- ❌ CTA único "entra na comunidade" → ✅ escada star → issue → membro.
- ❌ Contar star como co-criação → ✅ âncora = issue acionável/PR; star é apoio.
- ❌ Prometer projeto e sumir → ✅ loop: creditar o episódio anterior abre o próximo.
- ❌ Projeto sem oferta amarrada → ✅ toda série puxa a comunidade (MRR).

## Onde as coisas estão
- Briefing/onboarding/vault do canal: voz e ângulo, métricas-âncora, metas e roadmap do
  motor de co-criação, e o padrão de UTM/atribuição.
- Repo-exemplo e link da comunidade: definidos no vault do canal
  (`github.com/<seu-usuario>/<REPO>` e `<link-da-sua-comunidade>`).
