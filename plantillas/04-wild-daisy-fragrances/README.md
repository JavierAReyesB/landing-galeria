# 04 — Wild Daisy Fragrances

Landing page de producto (perfumes) en 3 secciones verticales: hero con vídeo + card flotante, panel azul con Eau So Sweet, panel lima con Eau So Extra. Animaciones de entrada con `IntersectionObserver` y transiciones `cubic-bezier(0.22, 1, 0.36, 1)`.

## 🖼️ Preview

![Wild Daisy Fragrances](preview.png)

## 🧱 Tecnologías

Todo vía **CDN**, sin build step. Adaptación al formato del catálogo del spec original (que pedía React + Vite + TypeScript + Tailwind).

- **Tailwind CSS** (CDN runtime, default config — breakpoints `sm:640px`, `md:768px`)
- **React 18.3.1** (UMD dev)
- **Babel Standalone 7.29.0** (transpila JSX en navegador)
- **Sin fonts externas** — tipografía sans-serif del sistema. Inline `Georgia, serif italic` para "Scroll" y `Playfair Display / Didot / Bodoni MT / Times New Roman, serif italic` para "01".

## 🧩 Secciones

1. **Hero** (`min-h-screen`, vídeo de fondo)
   - Header sticky con logo "Wild Daisy / Fragrances" + nav (Shop Now / Cart)
   - Indicador "Scroll" a la derecha (desktop)
   - Slide index "01" gigante en italic a la izquierda (desktop)
   - Card flotante producto **Eau So Fresh** (desktop bottom-right, mobile inline bajo el título)
   - Titular tres líneas: `Sweet Daisy / Personal Scent / Finder`
     - Desktop: paleta `HERO_TEXT #332023` + `#B0A2A1`
     - Mobile: blanco + alpha 80%, con text-shadow

2. **ScentFinder** (panel azul + vídeo)
   - `bg: #4BB3ED` (BG_BLUE)
   - Producto **Eau So Sweet** con 3 notas (Fruity top / Floral heart / Feminine base)
   - Labels esquinas: "Daisy love" · "Sweet"
   - Desktop: grid 2 columnas (panel izq + vídeo der)
   - Mobile: columna apilada con vídeo en strip `height: 75vw`

3. **WildScent** (panel lima + vídeo, espejo del 2)
   - `bg: #BDE84F` (BG_LIME)
   - Producto **Eau So Extra** con 3 notas en negrita (Top / Heart / Base) — `noteStyle="bold"`
   - Labels esquinas: "Daisy wild" · "Playful"
   - Desktop: grid 2 columnas (vídeo izq + panel der)
   - Mobile: `flex-col-reverse` para que el panel quede sobre el vídeo

## 🎨 Sistema de diseño

- **Paleta**: blanco `#fff` (page bg), `HERO_TEXT #332023` (hero ink), `BG_BLUE #4BB3ED`, `BG_LIME #BDE84F`, `TEXT_COLOR #000` (panels).
- **Tipografía**: stack del sistema (sans-serif). Sin Google Fonts.
- **Botones "SHOP NOW"**: borde negro + relleno blanco animado desde la izquierda en hover (`scale-x` con `origin-left`).
- **Card de producto**: rounded `2xl`, sombra suave `0 4px 24px rgba(51,32,35,0.08), 0 1px 4px rgba(51,32,35,0.06)`.

## ⚡ Animaciones

Helper `anim(visible, delay, { y?, x?, duration? })` que devuelve `style` con `opacity` + `transform` + `transition` (easing `cubic-bezier(0.22, 1, 0.36, 1)`).

- **Hero**: `setTimeout(() => setV(true), 200)` tras montar. Stagger 100ms / 500ms / 600ms / 800ms / 1000ms / 1300ms, duraciones 1400–1600ms. Header sube desde y:-10, scroll indicator entra desde x:16, "01" desde x:-24.
- **Secciones 2 y 3**: `IntersectionObserver` (threshold 0.15) por sección. Dentro del `ProductPanel` el stagger es 0 → 300 → 600 → 900 → 1150 ms (top labels → imagen → caption → notas → botón).

## ⚙️ Componentes JS internos

- **`Hero({ v, heroRef })`** — sección 1 completa.
- **`ProductPanel({ bg, product, notes, visible, noteStyle })`** — reutilizable para secciones 2 y 3. `noteStyle="bold"` engruesa las etiquetas de las notas y cambia los labels de esquina ("Daisy wild" / "Playful" en lugar de "Daisy love" / "Sweet").
- **`useEnterOnce(threshold)`** — hook `IntersectionObserver` que dispara `visible=true` una sola vez.

## ▶️ Cómo usarla

1. Abrir `index.html` directamente en el navegador o servirla con cualquier static server (`npx serve .`).
2. Sin `npm install`, sin build.
3. Los vídeos y las imágenes están en CloudFront / `images.higgs.ai` — si caen, sustituir las URLs en los `const` del top del script.

## 📝 Notas / Pendientes

- [x] Añadir `preview.png` (Captura de pantalla 2026-05-13 122722 — hero con corona de margaritas)
- [ ] Validar en móvil real (breakpoint sm:640 oculta la card flotante / scroll / "01"; md:768 activa el grid 2-col)
- [ ] La spec original mencionaba `@supabase/supabase-js` como dependencia permitida pero no la usa — no se incluye nada de Supabase en esta versión CDN.
- [ ] El spec permite `lucide-react` pero la página no usa iconos.
