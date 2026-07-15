---
name: youtube-video-oferta-map
description: O elo que liga cada video/tema de um canal a UMA oferta certa e gera o bloco de CTA + descricao na voz/angulo do proprio canal (definidos no onboarding/vault do usuario; anti-slop). Use quando for publicar/otimizar um video e precisar decidir "qual oferta esse video puxa?" e escrever o call-to-action — ou quando o pedido for monetizar um tema, ligar alcance a receita, ou montar a descricao de venda de um video. Roteia tema -> oferta usando a matriz-modelo do canal (references/matriz-oferta.md) e aplica a regra critica de UTM (so em dominio proprio, NUNCA em link de afiliado nem WhatsApp).
---

# Video -> Oferta Map — o elo entre alcance e receita

Cada video que estoura em alcance so vira dinheiro se puxar a oferta certa. Esta skill
faz o roteamento (tema -> UMA oferta) e escreve o CTA na voz do canal. A receita vem de
**venda** (as ofertas do proprio criador), nao de AdSense — este e o motor B.

> A voz, o angulo e o catalogo de ofertas deste canal saem do **onboarding/vault do
> usuario**. Antes de rotear, carregue esse contexto: quais ofertas existem, os dominios
> proprios, os links de afiliado, e o tom de escrita do canal. Se nao houver, monte a
> matriz junto com o usuario a partir do modelo em `references/matriz-oferta.md`.

## Quando usar
- "que oferta esse video puxa?" / "como monetizo esse tema?"
- Vou publicar/otimizar um video e preciso do bloco de CTA para a descricao.
- Ligar um video com traçao a receita (o alcance ja existe, falta a conversao).

## Doutrina inegociavel
- **Um video -> UMA oferta.** Nunca ofereça duas coisas no mesmo video (dilui, confunde).
- **Pensar MRR.** Na duvida entre duas ofertas, prefira a recorrente — MRR e a espinha de
  uma receita previsivel. So desvie se o resultado do video servir claramente outra oferta.
- **Nao precificar barato / nao "prostituir" o produto.** Zero "vitalicio", zero imagem de
  promocao/desconto relampago. Vender resultado, nao preço.
- **Cada CTA nomeia UM resultado concreto** e diz COMO o produto leva ate ele (padrao de
  pagina de vendas aplicado a descricao). Falar em dinheiro / controle / reputacao —
  nunca "aprenda X", nunca molde ("eleve seu negocio", "solucao completa").

## Fluxo

1. **Ler o tema do video.** Do que ele trata de verdade? (`bin/yt get <id>` ou a
   transcriçao). O que a pessoa que ACABOU de assistir precisa AGORA? Essa e a oferta.

2. **Rotear pela matriz** (`references/matriz-oferta.md`, tabela no topo — preenchida com as
   ofertas deste canal). Casou em duas? Aplique o tie-break: a oferta que e o **proximo
   passo natural** de quem assistiu vence; empate real -> a recorrente (MRR).

3. **Pegar o video_id** — `bin/yt recent` ou `bin/yt get <id>`. Ele entra no UTM.

4. **Montar o CTA** a partir do template da oferta escolhida (em `references/`). Trocar os
   `[...]` pelo resultado especifico ancorado NO tema do video — nao usar o template cru.

5. **Aplicar a regra de UTM** (critica, ver abaixo). Errar aqui quebra tracking ou o
   afiliado.

6. **Entregar para a skill que grava/publica.** Esta skill DECIDE a oferta e ESCREVE o
   CTA; quem grava a descriçao com backup e verificaçao e a skill de publicaçao do canal.
   O CTA entra na descriçao **depois** do bloco-resposta (nunca abrir a descriçao com link)
   e **aumenta**, nao substitui, os links/CTAs que ja convertem (preservar a voz e os
   destinos ja definidos do canal).

## Regra de UTM (critica — nao errar)
Padrao: `utm_source=youtube&utm_medium=<video_id>&utm_id=organico`
(`?` se o link nao tem query; `&` se ja tem).

| Destino | UTM? |
|---|---|
| Dominio proprio do canal (LPs, sites do criador) | **SIM** |
| Link de **afiliado** (produto de terceiro) | **NUNCA** — quebra o rastreio da comissao e nao mede nada |
| WhatsApp (`wa.me`, `chat.whatsapp...`) | **NUNCA** |

Onde ja existe UTM, **manter intacto** (nao quebrar historico). So adicionar onde falta.

## Arquivos
- `references/matriz-oferta.md` — a matriz-modelo tema->oferta (com resultado esperado e
  regra de UTM por oferta) + templates de CTA na voz do canal. Preencha os placeholders
  com as ofertas reais do usuario (onboarding/vault).
