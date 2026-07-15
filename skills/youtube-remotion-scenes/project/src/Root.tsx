import { Composition } from "remotion";
import { DossieCena, dossieDefaults, dossieSchema } from "./DossieCena";
import { MotionLettering, letterDefaults, letterSchema } from "./MotionLettering";
import { MotionNumero, numKinDefaults, numKinSchema } from "./MotionNumero";

const FPS = 30;

// Kit mínimo de cenas de EXEMPLO (identidade "Dossiê"). São gabaritos para adaptar à
// marca do canal — textos/emoji/highlight/paleta são props (edite no Studio ou via
// defaultProps). O reutilizável de fato é o kit em fx.tsx + a doutrina "emoção→coreografia"
// em references/doutrina-cenas.md; estas 3 cenas mostram como montar sobre ele.
// Render CLI: npx remotion render src/index.ts <id> <out.mp4> --codec=h264 --pixel-format=yuv420p
export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* cena base "Dossiê" (tela cheia, com fundo) — ponto de partida p/ uma cena nova */}
      <Composition id="DossieCena" component={DossieCena}
        durationInFrames={150} fps={FPS} width={1920} height={1080}
        schema={dossieSchema} defaultProps={dossieDefaults} />
      {/* utilitário de texto kinetic (lettering) */}
      <Composition id="MotionLettering" component={MotionLettering}
        durationInFrames={90} fps={FPS} width={1920} height={1080}
        schema={letterSchema} defaultProps={letterDefaults} />
      {/* utilitário de número kinetic (count-up) */}
      <Composition id="MotionNumero" component={MotionNumero}
        durationInFrames={95} fps={FPS} width={1920} height={1080}
        schema={numKinSchema} defaultProps={numKinDefaults} />
    </>
  );
};
