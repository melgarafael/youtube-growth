// Tokens da identidade "Sala de Máquinas" — fonte da verdade: docs/identidade-visual.md.
// Alterou lá? Alterar aqui. Não inventar cor/tipo fora deste conjunto.

export const COLOR = {
  bg: "#0B0B10", // fundo dominante — só quando NÃO-alpha
  surface: "#15151F", // cards, painéis
  roxo: "#7C3AED", // acento elétrico de marca (borda, glow) — NUNCA gradiente de fundo
  roxoHi: "#A78BFA",
  amarelo: "#FFCC00", // ação / palavra-soco
  verde: "#22C55E", // prova de dinheiro
  texto: "#F4F4F8",
  textoMute: "#8B8B9A",
} as const;

// Glow roxo sutil para o elemento ativo (não decorar tudo).
export const glowRoxo = `0 0 24px ${COLOR.roxo}66, 0 0 2px ${COLOR.roxo}`;

// Formata número inteiro em R$ pt-BR (o dinheiro subindo).
export const brl = (v: number) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    maximumFractionDigits: 0,
  }).format(Math.round(v));
