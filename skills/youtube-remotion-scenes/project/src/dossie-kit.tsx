// Kit compartilhado das cenas v2 "Dossiê" NOVAS (docs/identidade-visual.md).
// Arquivo NOVO e isolado — não toca em Root/index/DossieCena (editados por outro agente).
// Reúne os tokens v2, as fontes (Inter/Caveat) e o fundo bokeh, iguais aos da DossieCena.
import { useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadCaveat } from "@remotion/google-fonts/Caveat";

export const SANS = loadInter("normal", {
  weights: ["400", "700", "800"],
  subsets: ["latin"],
}).fontFamily;
export const HAND = loadCaveat("normal", { weights: ["400", "700"], subsets: ["latin"] })
  .fontFamily;

// Tokens v2 "Dossiê". Sem roxo.
export const V2 = {
  bgDeep: "#0A0E24",
  bgMid: "#141B3C",
  bokehA: "#2A3A7A",
  bokehB: "#4257B0",
  paper: "#F6F5F1",
  ink: "#1A1A1A",
  inkSoft: "#333333",
  highlight: "#EEEA5A",
} as const;

// prefers-reduced-motion: prop tem prioridade; senão consulta o SO.
export const shouldReduceMotion = (propOverride?: boolean): boolean => {
  if (propOverride !== undefined) return propOverride;
  if (typeof window === "undefined" || !window.matchMedia) return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
};

// R$ inteiro pt-BR (o dinheiro subindo).
export const brl = (v: number) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    maximumFractionDigits: 0,
  }).format(Math.round(v));

// Bokeh: luzes grandes desfocadas em deriva lenta (parallax). Estáticas p/ reduced.
const BOKEH = [
  { x: 18, y: 24, r: 520, color: V2.bokehB, op: 0.32, ax: 40, ay: 24, ph: 0 },
  { x: 74, y: 30, r: 620, color: V2.bokehA, op: 0.28, ax: 34, ay: 30, ph: 1.7 },
  { x: 60, y: 78, r: 480, color: V2.bokehB, op: 0.24, ax: 46, ay: 22, ph: 3.1 },
  { x: 30, y: 82, r: 560, color: V2.bokehA, op: 0.26, ax: 30, ay: 34, ph: 4.6 },
  { x: 88, y: 66, r: 400, color: V2.bokehB, op: 0.2, ax: 28, ay: 26, ph: 2.2 },
] as const;

export const Bokeh: React.FC<{ reduced: boolean }> = ({ reduced }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <>
      {BOKEH.map((b, i) => {
        const t = reduced ? 0 : frame / fps;
        const dx = reduced ? 0 : Math.sin(t * 0.35 + b.ph) * b.ax;
        const dy = reduced ? 0 : Math.cos(t * 0.28 + b.ph) * b.ay;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `${b.x}%`,
              top: `${b.y}%`,
              width: b.r,
              height: b.r,
              marginLeft: -b.r / 2,
              marginTop: -b.r / 2,
              borderRadius: "50%",
              background: b.color,
              opacity: b.op,
              filter: "blur(110px)",
              transform: `translate(${dx}px, ${dy}px)`,
            }}
          />
        );
      })}
    </>
  );
};

export const indigoBg = `linear-gradient(160deg, ${V2.bgDeep} 0%, ${V2.bgMid} 100%)`;
