# Web de FDP Software — instrucciones para Claude

Este repositorio es la página web pública de **FDP SOFTWARE**, una empresa venezolana de software de alta gama.
Está en línea en **https://fdpsoftware.org** (también responde en `www.fdpsoftware.org`).
Quien te pide cambios es socia de la empresa y tiene acceso total: ayúdala a modificar textos, imágenes,
secciones y diseño, explicando cada paso en español sencillo, sin jerga técnica.

## Cómo está hecha

- Sitio **estático**: HTML, CSS y JavaScript puros, sin frameworks y sin paso de compilación.
- Todo lo que se publica está en `public/`:
  - `index.html`: todo el contenido (una sola página).
  - `css/styles.css`: el diseño. Los colores y las fuentes están en las variables de `:root`, al inicio.
  - `js/main.js`: el menú móvil, el carrusel de la portada, las pestañas de sectores, el carril de soluciones y la animación de aparición.
  - `img/`: logos, íconos y capturas de proyectos (WebP y PNG).
  - `404.html`, `_headers` (seguridad y caché) y `robots.txt`.
- `wrangler.jsonc` publica `public/` en **Cloudflare Workers** (archivos estáticos) y conecta el dominio. No toques sus `routes`.
- `LEEME.md` es la guía para personas. Mantenla al día si cambias la forma de trabajar.

### Secciones de `index.html` (por `id`)

`inicio` (portada con carrusel: `slide-1` FDP Software, `slide-2` SIGMA MRO, `slide-3` Escenarios 3D,
`slide-4` simuladores de tiro) → `soluciones` (carril horizontal de tarjetas) → `proyectos` (SIGMA MRO destacado,
`tiro` con galería, y una cuadrícula con AeroEscuela, DespachoPro, entrenamiento táctico, Escenarios 3D y control
aéreo) → `apps` (Marcelo Go, Minijuegos de Marcelo Go y Ritmo Diario en Google Play) → `sectores` (pestañas) →
cita de la misión → `metodo` → `nosotros` (misión, visión, marcas y equipo por áreas) → `contacto` → pie de página.

Cada diapositiva tiene enlace directo, por ejemplo `https://fdpsoftware.org/#slide-4`.

### Estilo visual

- Inspirado en adobe.com: encabezado flotante con efecto vidrio, portada a pantalla completa con carrusel,
  hoja blanca con esquinas redondeadas que sube sobre la portada, títulos muy grandes y gruesos
  (fuente *Inter Tight*, clase `.display`), botones en píldora negros o blancos y tarjetas redondeadas.
- Colores de marca tomados del logo: azul `--blue`, verde azulado `--teal`, verde `--green`, naranja `--orange`,
  magenta `--magenta` y violeta `--violet`, más el degradado `--brand-gradient`.
- Antes de crear un componente nuevo, reutiliza los que ya existen: `.feature`, `.media-card`
  (y `.media-card--wide`), `.rail-card`, `.app-card`, `.brand`, `.sector`, `.pill`, `.checks` y `.badge--*`.
- Si agregas un tipo de tarjeta nuevo, súmalo a la lista `revealItems` en `js/main.js` para que tenga la animación de aparición.
- Todo debe verse bien en computador (1280 y 1920 px) y en celular (375 px), sin desplazamiento lateral.

## Reglas de contenido (obligatorias)

1. **Nombre de la empresa y marcas**: siempre **FDP Software**, **FDP Simuladores** y **FDP Aplicaciones**.
   Nunca escribas "FD" a secas.
2. **Sin nombres de personas**: no publiques nombres de directivos ni de miembros del equipo, ni usuarios de GitHub u
   otros datos que identifiquen a alguien. El equipo se muestra solo por áreas.
3. **Proyectos de defensa**: pueden mostrarse capturas, pero hay que recortar o tapar escudos, emblemas y logos
   institucionales. No menciones instituciones militares (DIDA, FANB, AMB ni Aviación Militar Bolivariana) ni los nombres
   propios de esos sistemas (IGLA-S, S.I.E.T.E., MANPADS, CODAI). Usa descripciones generales, como "simuladores de
   tiro" o "entrenamiento táctico y estratégico". Del simulador de control e interceptación aérea no se publican capturas.
   Tampoco uses grabaciones hechas con celular a pantallas de sistemas reales.
4. **Revisa cada captura antes de publicarla**: no deben aparecer rutas de archivos de un computador
   (`C:\Users\...`), nombres de usuario, punteros del mouse ni datos personales. Si aparecen, recórtalos o tápalos
   con el color del fondo.
5. **Contacto**: WhatsApp +58 412-0846332 (`https://wa.me/584120846332`) y correo `contacto@fdpsoftware.org`.
   Aparecen en la sección de contacto, en el pie de página y en el botón flotante; si cambian, cámbialos en todos.
6. Escribe en español, tuteando al visitante, con frases claras y sin exagerar. No inventes clientes, cifras ni
   testimonios.

## Imágenes: siempre en HD (regla estricta)

Ninguna imagen puede verse borrosa ni de mala calidad.

- Usa la imagen original de mayor resolución que haya. Si viene de un video, extrae el fotograma en PNG
  (`ffmpeg -ss <segundo> -i video.mp4 -frames:v 1 cuadro.png`) y recórtalo con Pillow (Python).
- **Nunca amplíes** una imagen por encima de su tamaño original, ni con CSS (`object-fit: cover` en una caja
  más grande, `transform: scale` o zooms al pasar el mouse) ni al exportarla. Si la fuente es pequeña, muéstrala
  pequeña y pide una versión de mayor resolución.
- Exporta a WebP: las capturas con texto casi sin pérdida (`quality=100, near_lossless=60`) y las fotos con
  calidad 92 o más. Al exportar se eliminan los metadatos: vuelve a pegar la imagen en un lienzo nuevo antes de guardarla.
- Los atributos `width` y `height` de cada `<img>` deben coincidir con el tamaño real del archivo.
- Antes de publicar, mide en el navegador que ninguna imagen se muestre por encima de 1×: compara
  el tamaño en pantalla con `naturalWidth` y `naturalHeight` a 1280×800, 1920×1080 y 375 px de ancho.

## Cómo trabajar

1. Al empezar: `git pull`, para traer los últimos cambios.
2. Edita los archivos dentro de `public/`.
3. Revisa los cambios en local: `python -m http.server 8080 --directory public` y abre `http://localhost:8080`.
   Comprueba la vista de computador y la de celular, y que la consola del navegador no muestre errores.
4. Guarda el cambio: `git add -A`, luego `git commit -m "<qué cambió, en español>"` y `git push`.
5. Publica **solo cuando ella lo confirme**, porque el cambio sale a internet:
   `npx.cmd wrangler deploy` (en Windows usa `npx.cmd`: PowerShell bloquea `npx.ps1`).
   Si pide iniciar sesión, ejecuta `npx.cmd wrangler login` y avísale que autorice en el navegador de inmediato,
   porque la autorización expira en pocos minutos.
6. Verifica que el cambio esté en línea, por ejemplo con
   `curl -s "https://fdpsoftware.org/?v=<número>"`, y cuéntale qué quedó publicado.

No subas al repositorio carpetas temporales (`.wrangler/`, `node_modules/`), contraseñas ni claves.
