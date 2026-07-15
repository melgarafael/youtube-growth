import { Config } from "@remotion/cli/config";

// Alpha por padrão (ProRes 4444 .mov). O CLI pode sobrescrever por flags.
// Ver SKILL.md para o fallback .webm/vp8 alpha e o de fundo sólido H.264.
Config.setVideoImageFormat("png");
Config.setPixelFormat("yuva444p10le");
Config.setCodec("prores");
// ProRes profile fica por-composição (alphaDefaults em Root.tsx), não global:
// setá-lo aqui quebra render H.264 de fundo sólido (validação codec×profile).
