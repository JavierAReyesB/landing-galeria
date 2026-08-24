# 15 — VEX · Shaping tomorrow with vision and action

Hero único minimalista para una marca VC/Studio. **Vídeo de fondo a opacidad completa** (sin overlay ni dimming — crítico per spec), navbar `liquid-glass` con CTA, heading con **animación carácter a carácter** (stagger 30ms), subtítulo y botones con FadeIn escalonado, y un tag glass *"Investing. Building. Advisory."* alineado bottom-right.

## 🖼️ Preview

![VEX](preview.png)

## 🧱 Tecnologías

Vía **CDN**, sin build step. Adaptación de la spec original (React + TS + Vite + Tailwind) al formato del catálogo.

- **Tailwind CSS** (CDN runtime, `tailwind.config` extendiendo `fontFamily.sans: ['Inter', 'sans-serif']`)
- **React 18.3.1** (UMD dev)
- **Babel Standalone 7.29.0**
- **Google Fonts**: Inter (300/400/500/600) aplicada globalmente con smoothing `antialiased`

## 🎨 Sistema de diseño

- **Fondo**: negro `#000`. Texto blanco / `text-gray-300` secundario. Borders `white/20`. **Sin morados, sin índigos**.
- **Tipografía**: Inter (`font-sans` por defecto en todo el documento vía `tailwind.config`).
- **Heading**: 4xl → md:5xl → lg:6xl → xl:7xl, `font-normal`, `letter-spacing: -0.04em`.
- **Liquid Glass**: variante específica de esta plantilla con `background: rgba(0, 0, 0, 0.4)` (más opaca que la sutil de plantillas anteriores), `blur(4px)`, máscara gradiente top/bottom.

## ⚙️ Componentes reutilizables

### `<FadeIn delay duration>`
Wrapper que arranca con `opacity: 0` y transiciona a 1 tras `setTimeout(delay)`. Usa `transition-opacity` de Tailwind + `transitionDuration` inline. Stagger del hero:

| Elemento | delay | duration |
|---|---|---|
| Heading char-by-char | 200ms | 500ms/char |
| Subtítulo | 800ms | 1000ms |
| Botones | 1200ms | 1000ms |
| Tag derecha | 1400ms | 1000ms |

### `<AnimatedHeading text initialDelay charDelay>`
1. Split por `\n` → líneas
2. Cada línea split por chars
3. Cada char es un `<span style="display: inline-block">` con CSS transition:
   - Inicial: `opacity: 0, translateX(-18px)`
   - Final: `opacity: 1, translateX(0)`
   - Delay por char: `(lineIndex * lineLength * 30ms) + (charIndex * 30ms)`
   - Duración: `500ms` por char
4. Spaces se renderizan como nbsp (`' '`)

Animación dispara tras `initialDelay = 200ms` cuando `setState(true)`.

## 🧩 Estructura JSX

```
<div min-h-screen bg-black overflow-hidden>
  ├─ <video> absolute fullscreen, NO overlay (z-0)
  └─ <div z-10 flex-col min-h-screen>
       ├─ <div px-6 md:px-12 lg:px-16 pt-6>
       │     └─ <nav liquid-glass rounded-xl px-4 py-2>
       │            ├─ "VEX" (text-2xl semibold)
       │            ├─ 4 links centrales (Story/Investing/Building/Advisory)
       │            └─ "Start a Chat" pill blanca
       └─ <div flex-1 flex-col justify-end pb-12 lg:pb-16>
            └─ <div lg:grid lg:grid-cols-2 lg:items-end>
                 ├─ Columna izq:
                 │    ├─ AnimatedHeading "Shaping tomorrow\nwith vision and action."
                 │    ├─ FadeIn 800ms: subtítulo
                 │    └─ FadeIn 1200ms: 2 botones
                 └─ Columna der:
                      └─ FadeIn 1400ms: glass tag pill xl
```

## ⚠️ Notas críticas de la spec

- **El vídeo no lleva ningún overlay** (ni `bg-black/X`, ni gradient, ni semi-transparent). El vídeo se renderiza raw a opacidad completa, así sale del CDN. Verificado en preview: `overlayCount: 0`.
- **No icons**: la spec lista `lucide-react` como opcional pero ninguno se usa en este hero. Plantilla 100% texto + glass.

## ▶️ Cómo usarla

1. Abrir `index.html` directamente o vía el viewer del catálogo.
2. Sin `npm install`, sin build.
3. El vídeo está en CloudFront — si cae, sustituir `VIDEO_SRC`.

## 📝 Notas / Pendientes

- [x] Añadir `preview.png` (Captura de pantalla 2026-05-14 082359 — skyline urbano con rascacielos sobre vegetación, navbar VEX glass arriba, heading "Shaping tomorrow / with vision and action." bottom-left con 2 CTAs, tag "Investing. Building. Advisory." bottom-right)
- [ ] El char-by-char animation tiene un easing implícito `ease-out` — la spec no lo nombra explícitamente pero queda mejor que linear. Si quieres `linear`, sustituir `500ms ease-out` por `500ms linear` en el style del char.
- [ ] La fórmula del stagger (lineIndex * lineLength * charDelay) acumula bastante delay para la segunda línea. Con `charDelay=30ms` y línea de 16 chars, la segunda línea arranca a `200 + 480 = 680ms` desde el primer char. Si se ve excesivo, bajar `charDelay` a 20ms.
