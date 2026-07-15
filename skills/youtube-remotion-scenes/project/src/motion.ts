import { Easing, interpolate } from "remotion";

// Movimento seco: 150–300ms, ease-out. Nada de bounce.
// A 30fps: ~5–9 frames. Default DRY_FRAMES = 7 (~230ms).
export const DRY_FRAMES = 7;

// prefers-reduced-motion: se ligado, salta pro estado final (progress = 1).
// Prop tem prioridade; senão consulta o SO (vale no Studio/preview).
export const shouldReduceMotion = (propOverride?: boolean): boolean => {
  if (propOverride !== undefined) return propOverride;
  if (typeof window === "undefined" || !window.matchMedia) return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
};

// Entrada seca 0→1 (opacidade/escala). reduced => sempre 1.
export const dryIn = (
  frame: number,
  delay = 0,
  duration = DRY_FRAMES,
  reduced = false,
) => {
  if (reduced) return 1;
  return interpolate(frame - delay, [0, duration], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
};
