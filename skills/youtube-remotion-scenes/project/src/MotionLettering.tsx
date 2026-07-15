// Motion UTILITÁRIO — frase-soco kinetic. A frase entra com PUNCH (scale overshoot) + flash +
// shake no impactFrame; um trecho ganha MARCA-TEXTO que pinta (wipe). Serve pros letterings do
// mapa (tese, pergunta, CTA). Full = tela cheia; transparent+anchor = overlay no canto.
// AJUSTES: impactFrame (palavra-soco), title, highlight (trecho a marcar), color, anchor.
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { loadFont } from "@remotion/google-fonts/Inter";
import { clamp, Flash, KIN, OUT, Ricochet, useImpact, Vignette } from "./fx";

const SANS = loadFont("normal", { weights: ["600", "800"], subsets: ["latin"] }).fontFamily;

export const letterSchema = z.object({
  title: z.string(),
  highlight: z.string().default(""),
  impactFrame: z.number().default(16),
  color: z.string().default(KIN.gold),
  transparent: z.boolean().optional(),
  anchor: z.enum(["center", "top"]).default("center"),
});
type Props = z.infer<typeof letterSchema>;

const split = (p: string, h: string) => {
  if (!h) return [p, "", ""] as const;
  const i = p.toLowerCase().indexOf(h.toLowerCase());
  return i < 0 ? [p, "", ""] as const : [p.slice(0, i), p.slice(i, i + h.length), p.slice(i + h.length)] as const;
};

export const MotionLettering: React.FC<Props> = ({ title, highlight, impactFrame, color, transparent, anchor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const atTop = transparent && anchor === "top";
  const { flash, shakeX, shakeY } = useImpact(frame, fps, impactFrame, { shake: atTop ? 1.5 : 3.2, pulse: 0 });

  // punch de entrada no impactFrame
  const pop = spring({ frame: frame - impactFrame + 6, fps, config: { damping: 11, mass: 0.5, stiffness: 200 } });
  const scale = interpolate(pop, [0, 0.5, 1], [0.7, 1.08, 1], clamp);
  const op = interpolate(pop, [0, 0.4], [0, 1], clamp);
  // marca-texto pinta (wipe) logo após o punch
  const paint = interpolate(frame - impactFrame, [4, 16], [0, 1], { ...clamp, easing: OUT });
  const [before, hit, after] = split(title, highlight);

  const fontSize = atTop ? 54 : 82;
  const halo = transparent
    ? "0 0 4px #000, 0 0 10px rgba(0,0,0,0.8), 0 6px 16px rgba(0,0,0,0.9)"
    : "0 6px 24px rgba(0,0,0,0.85)";

  return (
    <AbsoluteFill style={{ background: transparent ? "transparent" : KIN.bg, overflow: "hidden",
      justifyContent: atTop ? "flex-start" : "center", alignItems: atTop ? "flex-start" : "center",
      paddingTop: atTop ? 70 : 0, paddingLeft: atTop ? 90 : 0 }}>
      {!transparent && <Vignette color={color} />}
      <div style={{ transform: `translate(${shakeX}px, ${shakeY}px) scale(${scale})`, transformOrigin: atTop ? "top left" : "center", opacity: op }}>
        <div style={{ position: "relative", fontFamily: SANS, fontWeight: 800, fontSize, lineHeight: 1.08,
          color: "#fff", textAlign: atTop ? "left" : "center", maxWidth: atTop ? 900 : 1400, textShadow: halo }}>
          {before}
          <span style={{ position: "relative", display: "inline-block", whiteSpace: "pre-wrap" }}>
            <span style={{ position: "absolute", left: -6, right: -6, top: "16%", bottom: "10%", background: color,
              width: `calc(${paint * 100}% + 12px)`, borderRadius: 4, transform: "rotate(-0.6deg)", opacity: 0.9, zIndex: 0 }} />
            <span style={{ position: "relative", zIndex: 1, color: paint > 0.5 ? "#0B0D12" : "#fff" }}>{hit}</span>
          </span>
          {after}
        </div>
      </div>
      {!atTop && <div style={{ position: "absolute", left: "50%", top: "50%" }}>
        <Ricochet frame={frame} fps={fps} impactFrame={impactFrame} colors={[color, "#fff"]} spread={140} count={10} />
      </div>}
      <Flash opacity={flash} color={color} />
    </AbsoluteFill>
  );
};

export const letterDefaults: Props = {
  title: "não vendemos IA, vendemos GOVERNANÇA",
  highlight: "GOVERNANÇA",
  impactFrame: 16,
  color: KIN.gold,
  anchor: "center",
};
