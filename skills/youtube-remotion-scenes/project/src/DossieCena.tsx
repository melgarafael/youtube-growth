// Cena "Documento Dossiê" — identidade v2 "Dossiê" (docs/identidade-visual.md).
// Fundo índigo com bokeh desfocado; documento off-white surge da pasta (spring Keynote);
// emoji + título sans limpa; anotação manuscrita com marca-texto amarelo que "pinta".
// Auto-contida: tokens v2 e fontes (Inter/Caveat) vivem aqui — os tokens v1 (tokens.ts,
// fonts.ts) são da identidade "Sala de Máquinas" rejeitada e não valem para esta cena.
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { z } from "zod";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadCaveat } from "@remotion/google-fonts/Caveat";
import { shouldReduceMotion } from "./motion";

const SANS = loadInter("normal", { weights: ["400", "700"], subsets: ["latin"] })
  .fontFamily;
const HAND = loadCaveat("normal", { weights: ["400", "700"], subsets: ["latin"] })
  .fontFamily;

// Tokens v2 "Dossiê" (docs/identidade-visual.md). Sem roxo.
const V2 = {
  bgDeep: "#0A0E24",
  bgMid: "#141B3C",
  bokehA: "#2A3A7A",
  bokehB: "#4257B0",
  paper: "#F6F5F1",
  ink: "#1A1A1A",
  inkSoft: "#333333",
  highlight: "#EEEA5A",
} as const;

export const dossieSchema = z.object({
  emoji: z.string(),
  title: z.string(),
  annotation: z.string(),
  annotationHighlight: z.string(), // trecho da anotação que recebe o marca-texto
  reducedMotion: z.boolean().optional(),
});

// Quebra a frase em [antes, destaque, depois] na 1ª ocorrência (case-insensitive).
const splitHighlight = (phrase: string, hit: string) => {
  if (!hit) return [phrase, "", ""] as const;
  const i = phrase.toLowerCase().indexOf(hit.toLowerCase());
  if (i < 0) return [phrase, "", ""] as const;
  return [phrase.slice(0, i), phrase.slice(i, i + hit.length), phrase.slice(i + hit.length)] as const;
};

// Bokeh: luzes grandes desfocadas em deriva lenta (parallax). Estáticas p/ reduced.
const BOKEH = [
  { x: 18, y: 24, r: 520, color: V2.bokehB, op: 0.32, ax: 40, ay: 24, ph: 0 },
  { x: 74, y: 30, r: 620, color: V2.bokehA, op: 0.28, ax: 34, ay: 30, ph: 1.7 },
  { x: 60, y: 78, r: 480, color: V2.bokehB, op: 0.24, ax: 46, ay: 22, ph: 3.1 },
  { x: 30, y: 82, r: 560, color: V2.bokehA, op: 0.26, ax: 30, ay: 34, ph: 4.6 },
  { x: 88, y: 66, r: 400, color: V2.bokehB, op: 0.2, ax: 28, ay: 26, ph: 2.2 },
] as const;

export const DossieCena: React.FC<z.infer<typeof dossieSchema>> = ({
  emoji,
  title,
  annotation,
  annotationHighlight,
  reducedMotion,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const reduced = shouldReduceMotion(reducedMotion);

  // Documento surge da pasta: spring suave com overshoot leve (física Keynote), ~0.7s.
  const rise = reduced
    ? 1
    : spring({ frame, fps, config: { damping: 14, stiffness: 100, mass: 0.9 } });
  const docY = interpolate(rise, [0, 1], [340, 0]);
  const docScale = interpolate(rise, [0, 1], [0.9, 1]);
  const docOpacity = interpolate(rise, [0, 0.4], [0, 1], { extrapolateRight: "clamp" });

  // Conteúdo interno entra depois do documento assentar.
  const fadeIn = (delay: number, dur = 8) =>
    reduced
      ? 1
      : interpolate(frame - delay, [0, dur], [0, 1], {
          easing: Easing.out(Easing.cubic),
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });

  const emojiIn = fadeIn(18);
  const titleIn = fadeIn(24);
  const annoIn = fadeIn(42);

  // Marca-texto "pinta" da esquerda p/ direita ~1.2s depois do título (título ~f24).
  const HL_START = 60;
  const HL_DUR = 14;
  const paint = reduced
    ? 1
    : interpolate(frame - HL_START, [0, HL_DUR], [0, 1], {
        easing: Easing.inOut(Easing.cubic),
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });

  const [annoBefore, annoHit, annoAfter] = splitHighlight(annotation, annotationHighlight);

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(160deg, ${V2.bgDeep} 0%, ${V2.bgMid} 100%)`,
        justifyContent: "center",
        alignItems: "center",
        overflow: "hidden",
      }}
    >
      {/* Bokeh — luzes desfocadas em deriva lenta. */}
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

      {/* Documento off-white — herói, com canto dobrado e sombra macia forte. */}
      <div
        style={{
          position: "relative",
          width: 1180,
          padding: "96px 110px 110px",
          borderRadius: 28,
          background: V2.paper,
          boxShadow: "0 50px 90px rgba(0,0,0,0.55), 0 8px 24px rgba(0,0,0,0.35)",
          opacity: docOpacity,
          transform: `translateY(${docY}px) scale(${docScale})`,
          transformOrigin: "center bottom",
        }}
      >
        {/* Canto superior-direito dobrado (file icon). */}
        <div
          style={{
            position: "absolute",
            top: 0,
            right: 0,
            width: 88,
            height: 88,
            borderTopRightRadius: 28,
            background: "linear-gradient(225deg, #DAD8CF 0%, #DAD8CF 50%, transparent 50%)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: 0,
            right: 0,
            width: 88,
            height: 88,
            background: "linear-gradient(225deg, #FBFAF7 0%, #E7E5DC 100%)",
            clipPath: "polygon(100% 0, 0 0, 100% 100%)",
            borderTopRightRadius: 28,
            boxShadow: "-2px 2px 6px rgba(0,0,0,0.12)",
          }}
        />

        {/* Emoji — marcador emocional. */}
        <div
          style={{
            fontSize: 130,
            lineHeight: 1,
            marginBottom: 28,
            opacity: emojiIn,
            transform: `translateY(${(1 - emojiIn) * 12}px)`,
          }}
        >
          {emoji}
        </div>

        {/* Título — sans limpa peso 700, caixa mista. */}
        <div
          style={{
            fontFamily: SANS,
            fontWeight: 700,
            fontSize: 92,
            lineHeight: 1.04,
            letterSpacing: -1.5,
            color: V2.ink,
            opacity: titleIn,
            transform: `translateY(${(1 - titleIn) * 14}px)`,
          }}
        >
          {title}
        </div>

        {/* Anotação manuscrita + marca-texto amarelo que pinta. */}
        <div
          style={{
            fontFamily: HAND,
            fontWeight: 400,
            fontSize: 62,
            lineHeight: 1.18,
            color: V2.inkSoft,
            marginTop: 48,
            maxWidth: 940,
            opacity: annoIn,
          }}
        >
          {annoBefore}
          <span style={{ position: "relative", display: "inline-block" }}>
            {/* Faixa amarela ATRÁS do texto — pinta da esquerda p/ direita. */}
            <span
              style={{
                position: "absolute",
                left: -6,
                right: -6,
                top: "12%",
                bottom: "6%",
                background: V2.highlight,
                width: `calc(${paint * 100}% + 12px)`,
                borderRadius: 3,
                transform: "rotate(-0.6deg)",
                zIndex: 0,
              }}
            />
            <span style={{ position: "relative", zIndex: 1 }}>{annoHit}</span>
          </span>
          {annoAfter}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const dossieDefaults: z.infer<typeof dossieSchema> = {
  emoji: "😓",
  title: "A maioria trava antes de faturar",
  annotation: "não dá pra escalar sem processo pra entregar e manter cliente",
  annotationHighlight: "entregar e manter",
  reducedMotion: undefined,
};
