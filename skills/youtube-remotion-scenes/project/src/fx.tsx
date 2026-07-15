// fx — primitivas de motion "estado-da-arte" compartilhadas pelas cenas Motion*.
// Fonte da régua: memória feedback-motion-estado-da-arte + gold standard MotionCerebroAbsorve.
// Extrair aqui garante que TODOS os motions tenham o MESMO pico de impacto e ricochete
// (consistência = identidade). Cada cena importa isto e escreve só sua coreografia única.
import React from "react";
import { AbsoluteFill, Easing, interpolate, spring } from "remotion";

// ── Curvas de ease (a assinatura de movimento do canal) ───────────────────────
export const SUCK = Easing.bezier(0.55, 0, 1, 0.45); // sucção: lento → puxado → acelera
export const OUT = Easing.out(Easing.cubic); // saída seca
export const SNAP = Easing.bezier(0.34, 1.4, 0.64, 1); // overshoot p/ "encaixe" mecânico

export const clamp = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

// ── Pico de impacto sincronizado a UM frame: flash + screen-shake + valor de pulso ──
export function useImpact(
  frame: number,
  fps: number,
  impactFrame: number,
  o: { shake?: number; flashDur?: number; pulse?: number } = {},
) {
  const shakeMax = o.shake ?? 3.2;
  const flash = interpolate(frame - impactFrame, [0, 3, o.flashDur ?? 8], [0, 0.42, 0], clamp);
  const amt = interpolate(frame - impactFrame, [0, 7], [shakeMax, 0], clamp);
  const on = frame >= impactFrame && frame < impactFrame + 7;
  const shakeX = on ? Math.sin(frame * 3.1) * amt : 0;
  const shakeY = on ? Math.cos(frame * 2.7) * amt : 0;
  const pulse = interpolate(
    spring({ frame: frame - impactFrame, fps, config: { damping: 8, mass: 0.5, stiffness: 200 } }),
    [0, 0.45, 1],
    [0, o.pulse ?? 0.16, 0],
    { extrapolateLeft: "clamp" },
  );
  return { flash, shakeX, shakeY, pulse };
}

// Camada de flash (mix-blend screen) — por cima de tudo, no impacto.
export const Flash: React.FC<{ opacity: number; color: string; at?: string }> = ({
  opacity,
  color,
  at = "50% 44%",
}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(50% 50% at ${at}, ${color}, transparent 60%)`,
      opacity,
      mixBlendMode: "screen",
      pointerEvents: "none",
    }}
  />
);

// Partículas de ricochete pós-impacto (vida residual — "nada engole e acaba seco").
export const Ricochet: React.FC<{
  frame: number;
  fps: number;
  impactFrame: number;
  colors: [string, string];
  count?: number;
  spread?: number;
}> = ({ frame, fps, impactFrame, colors, count = 14, spread = 150 }) => {
  const parts = Array.from({ length: count }, (_, i) => {
    const a = (i / count) * Math.PI * 2 + 0.3;
    const p = spring({
      frame: frame - impactFrame - (i % 4),
      fps,
      config: { damping: 15, mass: 0.4, stiffness: 120 },
    });
    const d = interpolate(p, [0, 1], [0, spread + (i % 3) * 40]);
    return {
      x: Math.cos(a) * d,
      y: Math.sin(a) * d - interpolate(p, [0, 1], [0, 40]),
      op: interpolate(p, [0, 0.2, 1], [0, 1, 0]),
      s: interpolate(p, [0, 1], [1, 0.3]),
      c: i % 2 ? colors[0] : colors[1],
    };
  });
  return (
    <>
      {parts.map((p, i) =>
        p.op <= 0.01 ? null : (
          <div
            key={i}
            style={{
              position: "absolute",
              left: "50%",
              top: "50%",
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: p.c,
              boxShadow: `0 0 12px ${p.c}`,
              opacity: p.op,
              transform: `translate(${p.x}px, ${p.y}px) scale(${p.s})`,
            }}
          />
        ),
      )}
    </>
  );
};

// Count-up com desaceleração — número sobe e "assenta". Retorna valor cru (formatar no call site).
export function countUp(frame: number, startF: number, dur: number, to: number): number {
  const t = interpolate(frame - startF, [0, dur], [0, 1], { ...clamp, easing: OUT });
  return to * t;
}

// Glow SVG reutilizável.
export const GlowDefs: React.FC<{ id: string; std?: number }> = ({ id, std = 3.5 }) => (
  <filter id={id} x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation={std} result="b" />
    <feMerge>
      <feMergeNode in="b" />
      <feMergeNode in="SourceGraphic" />
    </feMerge>
  </filter>
);

// Vinheta radial de fundo (só quando NÃO-overlay).
export const Vignette: React.FC<{ color: string }> = ({ color }) => (
  <AbsoluteFill
    style={{ background: `radial-gradient(50% 46% at 50% 44%, ${color}22, transparent 72%)` }}
  />
);

// Paleta kinetic comum aos Motion* (escuro + dourado + ciano + verde-dinheiro + vermelho-YT).
export const KIN = {
  bg: "#0B0D12",
  gold: "#FFC24B",
  cyan: "#4DD0E1",
  green: "#3BD07A",
  red: "#E4574C",
  paper: "#F4F2EC",
  ink: "#B9B5A8",
  grid: "#2A3340",
} as const;
