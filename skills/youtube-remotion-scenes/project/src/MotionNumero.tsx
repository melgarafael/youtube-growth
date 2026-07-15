// Motion UTILITÁRIO — número/dado kinetic. Um número CONTA rápido (count-up) e dá PUNCH no
// fim (impactFrame) + flash + ricochete; abaixo, um card com a legenda e marca-texto. Serve
// pros dados do mapa ($67, +278, R$25, 11 mil). Full ou overlay-canto (transparent+anchor).
// AJUSTES: impactFrame, prefix/suffix, value, caption/captionHighlight, color, anchor.
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { loadFont } from "@remotion/google-fonts/Inter";
import { clamp, countUp, Flash, KIN, Ricochet, useImpact, Vignette } from "./fx";

const SANS = loadFont("normal", { weights: ["600", "800"], subsets: ["latin"] }).fontFamily;

export const numKinSchema = z.object({
  value: z.number(),
  prefix: z.string().default(""),
  suffix: z.string().default(""),
  caption: z.string().default(""),
  captionHighlight: z.string().default(""),
  impactFrame: z.number().default(20),
  color: z.string().default(KIN.green),
  transparent: z.boolean().optional(),
  anchor: z.enum(["center", "top"]).default("center"),
});
type Props = z.infer<typeof numKinSchema>;

const split = (p: string, h: string) => {
  if (!h) return [p, "", ""] as const;
  const i = p.toLowerCase().indexOf(h.toLowerCase());
  return i < 0 ? [p, "", ""] as const : [p.slice(0, i), p.slice(i, i + h.length), p.slice(i + h.length)] as const;
};

export const MotionNumero: React.FC<Props> = ({
  value, prefix, suffix, caption, captionHighlight, impactFrame, color, transparent, anchor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const atTop = transparent && anchor === "top";
  const { flash, shakeX, shakeY } = useImpact(frame, fps, impactFrame, { shake: atTop ? 1.5 : 3, pulse: 0 });

  const COUNT_DUR = Math.max(10, impactFrame - 6);
  const val = countUp(frame, 4, COUNT_DUR, value);
  const shown = prefix + Math.round(val).toLocaleString("pt-BR") + suffix;

  const punch = spring({ frame: frame - impactFrame, fps, config: { damping: 11, mass: 0.5, stiffness: 200 } });
  const punchScale = interpolate(punch, [0, 0.5, 1], [1, 1.14, 1], clamp);
  const enter = spring({ frame: frame - 2, fps, config: { damping: 13, mass: 0.5, stiffness: 160 } });
  const enterScale = interpolate(enter, [0, 1], [0.6, 1], clamp);
  const enterOp = interpolate(enter, [0, 0.4], [0, 1], clamp);

  const cardIn = interpolate(frame - impactFrame - 2, [0, 12], [0, 1], clamp);
  const paint = interpolate(frame - impactFrame - 6, [0, 12], [0, 1], clamp);
  const [before, hit, after] = split(caption, captionHighlight);

  const numSize = atTop ? 150 : 300;
  const halo = transparent ? "0 0 4px #000, 0 0 12px rgba(0,0,0,0.8), 0 6px 16px rgba(0,0,0,0.9)" : `0 12px 40px rgba(0,0,0,0.5), 0 0 40px ${color}55`;

  return (
    <AbsoluteFill style={{ background: transparent ? "transparent" : KIN.bg, overflow: "hidden",
      justifyContent: atTop ? "flex-start" : "center", alignItems: atTop ? "flex-start" : "center",
      paddingTop: atTop ? 60 : 0, paddingLeft: atTop ? 80 : 0 }}>
      {!transparent && <Vignette color={color} />}
      <div style={{ display: "flex", flexDirection: "column", alignItems: atTop ? "flex-start" : "center",
        transform: `translate(${shakeX}px, ${shakeY}px) scale(${atTop ? 1 : 1})`, transformOrigin: atTop ? "top left" : "center" }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: numSize, lineHeight: 1, letterSpacing: -4,
          color, textShadow: halo, opacity: enterOp, transform: `scale(${enterScale * punchScale})` }}>
          {shown}
        </div>
        {caption && (
          <div style={{ marginTop: atTop ? 14 : 40, padding: atTop ? "12px 22px" : "24px 40px", borderRadius: 18,
            background: "#12151C", border: `1.5px solid ${color}55`,
            boxShadow: transparent ? "0 10px 30px rgba(0,0,0,0.7)" : "0 20px 50px rgba(0,0,0,0.5)",
            opacity: cardIn, transform: `translateY(${(1 - cardIn) * 20}px)`,
            fontFamily: SANS, fontWeight: 700, fontSize: atTop ? 30 : 46, color: "#EAEAF2" }}>
            {before}
            <span style={{ position: "relative", display: "inline-block", whiteSpace: "pre-wrap" }}>
              <span style={{ position: "absolute", left: -5, right: -5, top: "16%", bottom: "10%", background: color,
                width: `calc(${paint * 100}% + 10px)`, borderRadius: 3, opacity: 0.9, zIndex: 0 }} />
              <span style={{ position: "relative", zIndex: 1, color: paint > 0.5 ? "#0B0D12" : "#EAEAF2" }}>{hit}</span>
            </span>
            {after}
          </div>
        )}
      </div>
      {!atTop && <div style={{ position: "absolute", left: "50%", top: "44%" }}>
        <Ricochet frame={frame} fps={fps} impactFrame={impactFrame} colors={[color, "#fff"]} spread={150} count={12} />
      </div>}
      <Flash opacity={flash} color={color} />
    </AbsoluteFill>
  );
};

export const numKinDefaults: Props = {
  value: 278, prefix: "+", suffix: "", caption: "inscritos em 28 dias", captionHighlight: "28 dias",
  impactFrame: 20, color: KIN.green, anchor: "center",
};
