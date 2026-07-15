// Tipografia da identidade: display = grotesca black condensada (Anton),
// números/métricas = mono terminal (Space Mono). NUNCA Inter/Roboto por inércia.
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import { loadFont as loadSpaceMono } from "@remotion/google-fonts/SpaceMono";

export const DISPLAY = loadAnton("normal", {
  weights: ["400"],
  subsets: ["latin"],
}).fontFamily; // Anton só tem 400, mas já é black condensada de manchete

export const MONO = loadSpaceMono("normal", {
  weights: ["400", "700"],
  subsets: ["latin"],
}).fontFamily;
