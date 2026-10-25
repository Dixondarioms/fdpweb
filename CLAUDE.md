# Web de FDP Software — instrucciones para Claude

Este repositorio es la página web pública de **FDP SOFTWARE**, una empresa venezolana de software de alta gama.
Está en línea en **https://fdpsoftware.org** (también responde en `www.fdpsoftware.org`).
Quien te pide cambios es socia de la empresa y tiene acceso total: ayúdala a modificar textos, imágenes,
secciones y diseño, explicando cada paso en español sencillo, sin jerga técnica.

## Cómo está hecha

- Sitio **estático**: HTML, CSS y JavaScript puros, sin frameworks y sin paso de compilación.
- Todo lo que se publica está en `public/`:
  - `index.html`: la página de inicio.
  - `proyectos/<nombre>/index.html`: una página por proyecto (ver más abajo).
  - `servicios/index.html`: los servicios (desarrollo a la medida), con el mismo encabezado y pie que las páginas de proyecto.
  - `css/styles.css`: el diseño. Los colores y las fuentes están en las variables de `:root`, al inicio.
  - `js/main.js`: el menú móvil, el carrusel de la portada, las pestañas de sectores, el carril de soluciones y la animación de aparición.
  - `img/`: logos, íconos y capturas de proyectos (WebP y PNG).
  - `video/simak/`: videos de SIMAK (fondo en bucle `fondo-1912.mp4` / `fondo-1280.mp4` para celular, un clip de 8 s por
    escenario y `sala.mp4`) con su imagen de espera `.webp`. `video/antiaereo/`: lo mismo para el simulador antiaéreo
    (fondo de 1920×760). `video/radar/`: control e interceptación aérea (fondo de 1680×900 con los paneles desenfocados y tres
    clips del mapa). `docs/`: los dossiers en PDF (`simak-dossier.pdf`, `antiaereo-dossier.pdf` y `control-aereo-dossier.pdf`).
  - `img/p/`: capturas de las páginas de proyecto; `img/og/`: la imagen para redes (1200×630) de cada página de proyecto.
  - `404.html`, `_headers` (seguridad y caché), `robots.txt` y `sitemap.xml` (lista de páginas para Google).
- `wrangler.jsonc` publica `public/` en **Cloudflare Workers** (archivos estáticos) y conecta el dominio. No toques sus `routes`.
- `sitio/worker.js` solo atiende `/video/*`: entrega los videos por partes ("Range"), que Safari en iPhone exige para
  reproducirlos. Todo lo demás lo sirven los archivos estáticos con las cabeceras de `_headers`.
- **Versión en inglés** (`public/en/`): se genera desde el español con `python sitio/ingles/construir.py`; no edites
  `public/en/` a mano. Las traducciones están en `sitio/ingles/traducciones.json` ("textos": español → inglés, y "whatsapp":
  el mensaje ya escrito de cada página). Después de cambiar un texto en español, corre el programa: si avisa de "textos sin
  traducir", agrégalos al JSON (en inglés estadounidense, mismo tono) y vuelve a correrlo. El programa también pone el botón
  ES/EN del menú (`.nav__lang`) y las etiquetas `hreflang` en las dos versiones. `js/main.js` elige sus textos según `lang`.
  Las imágenes, videos y dossiers PDF son los mismos (los PDF están en español y así se indica en inglés).
- `LEEME.md` es la guía para personas. Mantenla al día si cambias la forma de trabajar.
- `correo/` es un Email Worker aparte (`fdp-correo`) que reenvía `contacto@fdpsoftware.org` a las direcciones de
  `DESTINOS` en `correo/wrangler.jsonc`. Se publica desde esa carpeta con `npx.cmd wrangler deploy`. Esas direcciones
  son datos privados: nunca las muestres en la web.

### Secciones de `index.html` (por `id`)

`inicio` (portada con carrusel: `slide-1` FDP Software, `slide-2` SIGMA MRO, `slide-3` Escenarios 3D,
`slide-4` simulador de tiro antiaéreo, `slide-5` SIMAK) → `soluciones` (carril horizontal de tarjetas) → `proyectos` (SIGMA MRO destacado
y una cuadrícula con AeroEscuela, entrenamiento táctico y Escenarios 3D) → `control` (control e interceptación aérea, `.vband--radar`) → `control-escenas` (tres clips) → `tiro` (simulador antiaéreo: franja con video de fondo, `.vband--franja`) → `tiro-escenarios` (seis clips) →
`simak` (franja con video de fondo, `.vband`) → `simak-escenarios` (seis clips, `.clips`) → `apps` (Marcelo Go, Minijuegos de Marcelo Go y Ritmo Diario en Google Play) → `sectores` (pestañas) →
cita de la misión → `metodo` → `nosotros` (misión, visión, marcas y equipo por áreas) → `contacto` → pie de página.

Cada diapositiva tiene enlace directo, por ejemplo `https://fdpsoftware.org/#slide-4`.

### Páginas de proyecto (`public/proyectos/`)

`sigma-mro`, `aeroescuela`, `simuladores-de-tiro` (solo el simulador antiaéreo), `simak` (simulador de tiro con láser),
`entrenamiento-tactico`, `escenarios-3d`, `control-aereo` y `apps-moviles`. La de `simak` empieza con video de fondo (`.vband`)
en lugar de `.phero` y tiene los clips de escenarios. Todas siguen el mismo orden: portada oscura (`.phero`, con ruta de navegación `.crumbs`) → ficha rápida
(`.specs`) → "Qué incluye" (`#incluye`, tarjetas `.pfeature`; en apps, filas `.prow`) → galería (`#galeria`,
`.pgallery`, con `.is-full` para las capturas a lo ancho) → contacto (`#contacto`) → otros proyectos (`.more`) → pie.

- Usan rutas absolutas (`/css/...`, `/img/...`, `/#proyectos`), porque están dentro de carpetas.
- Cada una tiene su propio `<title>`, descripción, `canonical`, imagen para redes (`img/og/<nombre>.jpg`) y datos
  para Google (`application/ld+json`). Si cambias el nombre o la descripción de un proyecto, cámbialos en esos lugares.
- El mensaje de WhatsApp de cada página ya nombra el proyecto (`...quiero%20informaci%C3%B3n%20sobre%20SIGMA%20MRO.`).
- El encabezado, el pie de página y la lista "Otros proyectos" se repiten en las ocho páginas de proyecto y en `servicios/`: si cambias uno, cambia todos.
- Si agregas un proyecto: copia una página parecida, agrégala a `sitemap.xml`, enlázala desde la tarjeta del proyecto en
  `index.html`, desde el pie de página y desde "Otros proyectos" de las demás páginas.

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

## Videos en la web (SIMAK)

- Son MP4 (H.264) sin sonido, en `public/video/`, con `muted loop playsinline preload="none" data-autoplay` y la imagen de espera
  en `data-poster` (no en `poster`, para que no se descargue al abrir la página). `js/main.js` carga la imagen cuando el video
  está cerca, lo reproduce solo mientras se ve y lo pausa al salir. Cada video tiene un botón `.vtoggle` con
  `data-video-toggle` dentro del contenedor `[data-video]`. Con "reducir movimiento" activado no arrancan solos.
- Se sacan del video del stand de SIMAK con `ffmpeg`, solo del tramo de los escenarios: el inicio y el final de ese video muestran
  un escudo institucional. Los del antiaéreo salen del video de presentación recortando la franja `crop=1920:760:0:175`, que deja
  fuera el título, la etiqueta, el escudo de la esquina y los subtítulos (que nombran el sistema); en la consola se quita el
  panel del lanzador, que lleva su designación (9K38), y se usan solo tramos sin la ventana de la consola superpuesta. Recorta el borde blanco de la grabación (4 px) y nunca amplíes por encima del tamaño original.
- Mantén los videos livianos: el fondo pesa unos 3 MB (1,7 MB la versión de celular) y cada clip menos de 700 KB.
- `sala.mp4` fue generado con IA; en la web se aclara que es una recreación ilustrativa.

## Videos para redes sociales (`videos/`)

- `videos/generador/videos.py` tiene el guion de cada video (textos, imágenes, tomas y tiempos) y `engine.py` el
  diseño (fondo de marca, animaciones, tarjetas y cierre). Se generan con `python videos/generador/videos.py [nombre]`
  y quedan en `videos-redes/`, que está en `.gitignore`: nunca subas videos terminados. Guía para personas: `videos/LEEME.md`.
- Usa las imágenes de `public/img/` y las tomas cortas de `videos/clips/` (recortadas a su tamaño original).
  Para un video nuevo, copia la función de uno parecido y agrégalo a `VIDEOS`. Mantén el estilo: vertical
  1080×1920 a 30 fps, de 15 a 25 s, gancho → escenas con etiqueta y titular → cierre `cta()`, y nada importante
  por encima de 250 px ni por debajo de 1480 px.
- Los videos **no muestran el simulador IGLA ni los simuladores de tiro**, y van sin música (se agrega al publicar).
  También valen las reglas de contenido y de HD de abajo: el programa se detiene si una imagen se amplía por encima de 1×.
- `videos/generador/calendario.py` arma `videos-redes/programar/` (video, portada y textos por publicación, más `calendario.html`) para programar en Meta Business Suite y TikTok Studio. La página publicada del calendario es https://claude.ai/artifact/YPZ1Yr9gQjsajYNHJTxaAk.
- Revisa cada video antes de entregarlo (`... <nombre> previa 1,4.5,24`, o una hoja de cuadros con ffmpeg).
- Redes de FDP: Instagram `@freethepress05` y TikTok `@freethepress5`. Están en `REDES` (en `engine.py`), en el pie
  de página de las diez páginas y en `sameAs` de los datos para Google de `index.html`; si cambian, cámbialas en todos.

## Reglas de contenido (obligatorias)

1. **Nombre de la empresa y marcas**: siempre **FDP Software**, **FDP Simuladores** y **FDP Aplicaciones**.
   Nunca escribas "FD" a secas.
2. **Sin nombres de personas**: no publiques nombres de directivos ni de miembros del equipo, ni usuarios de GitHub u
   otros datos que identifiquen a alguien. El equipo se muestra solo por áreas.
3. **Proyectos de defensa**: pueden mostrarse capturas, pero hay que recortar o tapar escudos, emblemas y logos
   institucionales. No menciones instituciones militares (DIDA, FANB, AMB ni Aviación Militar Bolivariana) ni los nombres
   propios de esos sistemas (IGLA-S, S.I.E.T.E., MANPADS, CODAI, ni la designación 9K38). Usa descripciones generales, como "simuladores de
   tiro" o "entrenamiento táctico y estratégico". Del simulador de control e interceptación aérea (CODAI) solo se publican imágenes sin datos sensibles: nunca el nombre
   del sistema, los escudos, las bases o aeródromos militares (SVBL, La Carlota…), los aviones reales (F-16, Su-30), las
   coberturas o ubicaciones de radar, ni los registros de eventos y radio; usa solo el mapa acercado sobre el mar y
   desenfoca los paneles laterales (ver `video/radar/`).
   En el entrenamiento táctico no muestres qué país real es cada bando (por ejemplo "Azul (Venezuela)"): tápalo.
   En SIMAK, la bandera y el escudo del uniforme del soldado de la portada y de la consola van difuminados.
   Tampoco uses grabaciones hechas con celular a pantallas de sistemas reales.
4. **Revisa cada captura antes de publicarla**: no deben aparecer rutas de archivos de un computador
   (`C:\Users\...`), nombres de usuario, punteros del mouse ni datos personales. Si aparecen, recórtalos o tápalos
   con el color del fondo.
5. **Contacto**: WhatsApp +58 412-0846332 (los enlaces llevan un mensaje ya escrito: `https://wa.me/584120846332?text=Hola%20FDP%20Software%2C...`) y correo `contacto@fdpsoftware.org`.
   Aparecen en la sección de contacto, en el pie de página y en el botón flotante; si cambian, cámbialos en todos.
6. Escribe en español, tuteando al visitante, con frases claras y sin exagerar. No inventes clientes, cifras ni
   testimonios.

## Velocidad

- **Versión de CSS y JS**: `styles.css` y `main.js` se cargan con `?v=AAAAMMDD` y se guardan 30 días en caché.
  Cada vez que los cambies, actualiza ese número en `index.html`, `404.html`, las ocho páginas de `proyectos/` y `servicios/`
  (y luego regenera el inglés),
  o los visitantes seguirán viendo la versión vieja.
- **Imágenes responsive**: cada imagen de contenido tiene versiones más pequeñas (`nombre-480.webp`, `nombre-800.webp`…)
  declaradas en `srcset`, con un `sizes` que describe su ancho real en pantalla. Si agregas o reemplazas una imagen,
  genera también sus versiones (solo anchos menores al original) y escribe su `srcset`/`sizes`.
- Las imágenes de las diapositivas 2 a 4 de la portada usan `data-src`/`data-srcset` y `js/main.js` las carga después del
  arranque; no les pongas `src` directo.
- Las imágenes que no están al inicio de la página llevan `loading="lazy"`.

## Imágenes: siempre en HD (regla estricta)

Ninguna imagen puede verse borrosa ni de mala calidad.

- Usa la imagen original de mayor resolución que haya. Si viene de un video, extrae el fotograma en PNG
  (`ffmpeg -ss <segundo> -i video.mp4 -frames:v 1 cuadro.png`) y recórtalo con Pillow (Python).
- **Nunca amplíes** una imagen por encima de su tamaño original, ni con CSS (`object-fit: cover` en una caja
  más grande, `transform: scale` o zooms al pasar el mouse) ni al exportarla. Si la fuente es pequeña, muéstrala
  pequeña y pide una versión de mayor resolución.
- Exporta a WebP: las capturas con texto casi sin pérdida (`quality=100, near_lossless=60`) y las fotos con
  calidad 92 o más (también las capturas con mapas satelitales, que casi sin pérdida pesan demasiado). Al exportar se eliminan los metadatos: vuelve a pegar la imagen en un lienzo nuevo antes de guardarla.
- Los atributos `width` y `height` de cada `<img>` deben coincidir con el tamaño real del archivo.
- Antes de publicar, mide en el navegador que ninguna imagen se muestre por encima de 1×: compara
  el tamaño en pantalla con `naturalWidth` y `naturalHeight` a 1280×800, 1920×1080 y 375 px de ancho.

## Seguridad (no la debilites)

`public/_headers` aplica una política de seguridad estricta (Content-Security-Policy, HSTS, anti-iframe, etc.).

- **Nada de código en línea**: no escribas `<script>` sin `src`, ni `onclick=`, ni atributos `style="..."` en el
  HTML; el navegador los bloquea. Los estilos van en `css/styles.css` y el JavaScript en `js/main.js`.
  Tampoco uses `innerHTML`, `eval` ni `document.write` (Trusted Types está activo); usa `textContent` y `createElement`.
- **Recursos externos**: solo están permitidas las estadísticas de Cloudflare (`static.cloudflareinsights.com`).
  Los videos solo pueden venir de este mismo sitio (`media-src 'self'`); no incrustes YouTube ni otros reproductores.
  Las fuentes (Inter e Inter Tight) están en `public/fonts/` con su licencia; no vuelvas a usar Google Fonts. Si hace falta algo de otro dominio (un video, un mapa, un script),
  agrégalo a la directiva correcta de la CSP en `_headers`, explica a ella el riesgo y pruébalo antes de publicar.
- Los enlaces que abren otra pestaña (`target="_blank"`) llevan siempre `rel="noopener"`.
- La web solo responde en `fdpsoftware.org` (`workers_dev` y `preview_urls` están en `false` en `wrangler.jsonc`).
- Después de publicar, revisa en la consola del navegador que no haya mensajes de "Content Security Policy".
- `public/.well-known/security.txt` dice cómo reportar problemas de seguridad; renueva su fecha `Expires` antes de que venza.

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
