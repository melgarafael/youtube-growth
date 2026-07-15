---
name: youtube-notion-material
description: Cria o MATERIAL NOTION (guia passo a passo) que acompanha cada vídeo/aula de um canal do YouTube. Use quando for gerar o material de apoio de um vídeo — "monta o Notion desse vídeo", "cria o guia do projeto", "o passo a passo pra descrição", "material de apoio da aula". Produz um guia leigo-first (não precisa programar / a IA faz por você), sem enrolação, com expectativa de tempo+custo no topo, visão geral visual, pré-requisitos em tabela, passos acionáveis com comandos copiáveis e callouts de aviso nos pontos que travam, caminho fácil (IA) + manual, manutenção e troubleshooting em tabela, e o fecho amarrando a monetização do canal (a oferta/afiliado). Saída em Markdown pronto pra colar/importar no Notion. É a "LP/guia" do funil de vídeo.
---

# Material Notion — o guia que acompanha cada vídeo

Todo vídeo do canal pode liberar um **material Notion** (peça do funil de vídeo). Ele não é
"documentação" — é **peça do funil**: transforma o espectador em alguém que EXECUTA o
resultado, e amarra a monetização do canal (a oferta principal, ex.: um afiliado ou produto)
no caminho. Use `references/exemplo-canal.md` como modelo de qualidade e tom.

## Voz e oferta do canal
Antes de escrever, puxe a **voz/ângulo do canal do usuário** e a **oferta principal** do
onboarding/vault do canal (quem é o público, qual o tom, qual o produto/afiliado que
monetiza). Todo o guia é escrito nessa voz e amarra ESSA oferta — os exemplos abaixo usam
placeholders genéricos que você substitui pelos dados reais do canal.

## Quando usar
- "monta o Notion desse vídeo" · "cria o guia do projeto" · "material de apoio da aula"
- sempre que um vídeo entra em produção (todo vídeo → um Notion).

## Os 8 princípios (o que faz o guia funcionar)

1. **Leigo-first, fricção zero.** Abre com "**não precisa saber programar**" e o **Caminho
   fácil: o Claude Code/IA faz por você**. O público quer o resultado, não a técnica.
2. **Expectativa no topo.** Um callout com **⏱️ tempo estimado** e **💰 custo** (o que é
   grátis vs. pago). O leitor decide entrar sabendo no que se mete.
3. **Visão geral visual.** Um diagrama (ASCII/texto) do que vai ser montado, ANTES dos
   passos — o mapa mental do sistema.
4. **Pré-requisitos em tabela.** "Antes de começar, você vai precisar de N contas" →
   tabela `O quê | Onde | Custo`. Manda criar as contas agora.
5. **Passos numerados e acionáveis.** Cada passo = uma ação com resultado. **Comandos
   copiáveis exatos** em code block. Título de ação ("Contrate o servidor", não "Servidor").
6. **Callout de aviso no ponto que TRAVA.** Marque com ⚠️ o "motivo nº1" de dar errado
   (portas do firewall, domínio não propagou, etc.). E o **"por quê" só quando muda a
   decisão** (ex.: Session pooler porque o VPS é IPv4) — senão, corta.
7. **Dois caminhos.** "**Caminho fácil (a IA faz)**" + "**Caminho manual**". Sempre dá a
   saída pro leigo destravar sozinho com o Claude Code.
8. **Fecho de monetização.** Manutenção (tabela `Quero… | Comando`) + Troubleshooting
   (tabela `Sintoma | O que fazer`) + **"Por que [a oferta do canal]"** com os links
   oficiais. A oferta principal aparece onde é natural (ex.: contratar o servidor) e no fecho.

## Fluxo

1. **Leia o contexto** do vídeo: o pacote de produção (artifact), o projeto/repo, e qual a
   oferta amarrada (do onboarding/vault do canal). Confirme o **resultado** que o guia
   entrega (o mesmo do vídeo).
2. **Preencha o template** (`references/template-notion.md`) seção por seção, seguindo os 8
   princípios. Tom: **sem enrolação**, 2ª pessoa ("você"), na voz do canal. Nada de jargão
   solto.
3. **Amarre a monetização** onde é natural (o passo em que o projeto precisa da oferta) e
   no fecho "Por que [a oferta]" — links oficiais de afiliado/produto.
4. **Entregue em Markdown** (Notion importa markdown: headings, tabelas, code blocks,
   callouts com `>`). O criador cola/importa no Notion.
5. **Registre o link** onde o canal controla o cronograma/publicação, depois que o criador
   publicar e mandar a URL.

## Anti-slop (o guia NÃO pode)
- Ser uma "documentação técnica" fria — é guia de leigo com resultado.
- Explicar o "por quê" de tudo (só o que muda a decisão).
- Esconder o custo ou a oferta — transparência (grátis vs pago) É o que gera confiança.
- Passo sem comando copiável, ou comando que "mais ou menos" funciona.
- Esquecer o caminho fácil (IA faz) — é o diferencial pro público não-técnico.

## Arquivos
- `references/template-notion.md` — o esqueleto reutilizável (preencher).
- `references/exemplo-canal.md` — um guia-modelo (referência de qualidade/tom).
