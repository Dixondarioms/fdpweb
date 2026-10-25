# Página web de FDP Software

Sitio estático (HTML, CSS y JavaScript) publicado en **Cloudflare** en <https://fdpsoftware.org>
(también responde en <https://www.fdpsoftware.org>).

```
WEB/
├── LEEME.md          ← esta guía (no se publica)
├── wrangler.jsonc    ← configuración de publicación en Cloudflare (no se publica)
├── videos/          ← generador de videos para redes sociales (no se publica)
└── public/           ← ESTA es la carpeta que se publica
    ├── index.html    ← contenido de la página
    ├── 404.html      ← página de "no encontrado"
    ├── css/styles.css← diseño y colores
    ├── js/main.js    ← menú móvil, carrusel de portada, pestañas y animaciones
    ├── img/          ← logos, íconos y capturas de los proyectos (en HD)
    ├── _headers      ← seguridad y caché (Cloudflare lo lee solo)
    └── robots.txt    ← permite que Google indexe el sitio
```

## 1. Editar la página

- **Textos**: la página de inicio está en `public/index.html` y cada proyecto tiene su propia página en
  `public/proyectos/<nombre>/index.html` (por ejemplo <https://fdpsoftware.org/proyectos/sigma-mro/>).
- **Correo**: `contacto@fdpsoftware.org` (sección de contacto y pie de página).
- **WhatsApp**: +58 412-0846332 (`https://wa.me/584120846332`), en contacto, pie de página y botón flotante.
- **Imágenes**: reemplaza el archivo en `public/img/` con el mismo nombre. Úsalas siempre en HD: a su
  resolución original y sin reducirlas por debajo del tamaño en que se muestran.
- **Colores de la marca**: al inicio de `public/css/styles.css` (`--blue`, `--teal`, `--orange`, `--magenta`…).

Para ver los cambios en tu computador antes de publicar:

```
python -m http.server 8080 --directory public
```

y abre <http://localhost:8080>.

### Versión en inglés

La web también está en inglés en <https://fdpsoftware.org/en/> (botón **EN** / **ES** en el menú). Esas páginas se crean
solas a partir del español: después de cambiar un texto, ejecuta

```
python sitio/ingles/construir.py
```

Si el programa avisa de textos sin traducir, agrega su traducción en `sitio/ingles/traducciones.json` y ejecútalo de nuevo.

## 2. Publicar los cambios

Desde la carpeta `WEB`, en PowerShell (usa `npx.cmd`, porque PowerShell bloquea `npx.ps1`):

```
npx.cmd wrangler deploy
```

En unos segundos los cambios quedan en línea en fdpsoftware.org. Si Wrangler pide iniciar sesión,
ejecuta primero `npx.cmd wrangler login` y autoriza en el navegador **apenas se abra** la página
(la autorización expira en pocos minutos).

## 3. Enlaces directos

Cada diapositiva de la portada tiene su propio enlace, útil para compartir:

- `https://fdpsoftware.org/#slide-2` → SIGMA MRO
- `https://fdpsoftware.org/#slide-3` → Escenarios 3D
- `https://fdpsoftware.org/#slide-4` → Simuladores de tiro
- `https://fdpsoftware.org/#tiro` → sección de simuladores de tiro

Y cada proyecto tiene su página propia, ideal para enviar por WhatsApp (se ve con su propia imagen de vista previa):

- `https://fdpsoftware.org/proyectos/sigma-mro/`
- `https://fdpsoftware.org/proyectos/aeroescuela/`
- `https://fdpsoftware.org/proyectos/simak/` (SIMAK, con videos y el dossier en PDF)
- `https://fdpsoftware.org/proyectos/simuladores-de-tiro/`
- `https://fdpsoftware.org/proyectos/entrenamiento-tactico/`
- `https://fdpsoftware.org/proyectos/escenarios-3d/`
- `https://fdpsoftware.org/proyectos/control-aereo/`
- `https://fdpsoftware.org/proyectos/apps-moviles/`

## 4. Correo contacto@fdpsoftware.org (gratis)

Los mensajes que llegan a **contacto@fdpsoftware.org** se reenvían automáticamente a dos Gmail con
**Cloudflare Email Routing** y un pequeño programa (Email Worker) que está en la carpeta `correo/`.

- **Cambiar o agregar destinos**: edita `DESTINOS` en `correo/wrangler.jsonc` (separados por comas) y publica
  desde esa carpeta con `npx.cmd wrangler deploy`. Cada destino nuevo debe agregarse antes en Cloudflare →
  **Email Routing → Destination addresses** y confirmarse con el correo de verificación que recibe.
- La regla está en **Email Routing → Routing rules**: `contacto@fdpsoftware.org` → *Send to a Worker* → `fdp-correo`.
- Este correo solo **recibe**. Al responder desde Gmail, la respuesta sale desde la dirección de Gmail.
  Para responder como contacto@fdpsoftware.org hace falta un servicio de correo con el dominio
  (por ejemplo Zoho Mail o Google Workspace) y ajustar los registros SPF y DKIM.

## Estadísticas de visitas

Cloudflare cuenta las visitas sin cookies (Web Analytics, configuración automática). Para verlas: entra a Cloudflare →
**Analytics & Logs → Web Analytics → fdpsoftware.org**. Ahí aparecen visitas, páginas más vistas, países y dispositivos.
No hay que tocar la web: Cloudflare agrega el contador solo.

## 5. Google (Search Console)

`fdpsoftware.org` está registrado y verificado en **Google Search Console**
(<https://search.google.com/search-console>, propiedad de dominio), con el sitemap `https://fdpsoftware.org/sitemap.xml`.

- No borres el registro DNS `TXT google-site-verification=…`: es la prueba de que el dominio es suyo.
- Si cambian mucho la portada, actualiza `<lastmod>` en `public/sitemap.xml` y, en Search Console,
  usa **Inspección de URLs → Solicitar indexación** con `https://fdpsoftware.org/`.
- Ahí también se ve cuántas personas encuentran la web en Google y con qué búsquedas.

## 6. Dominio

`fdpsoftware.org` está registrado en Cloudflare. Mantén activa la **renovación automática** en
**Domain Registration → Manage Domains**.

Ajustes de seguridad ya configurados en el panel de Cloudflare (no los desactives):

- **SSL/TLS → Edge Certificates**: *Always Use HTTPS* activado y *Minimum TLS Version* en **TLS 1.2**.
- **DNS → Settings**: **DNSSEC** activado.
- **DNS → Records**: `TXT _dmarc "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s"`, que impide que alguien
  envíe correos falsos desde @fdpsoftware.org. Los registros MX, SPF y DKIM de Email Routing los administra
  Cloudflare: no los edites a mano. Si algún día envían correo con el dominio (por ejemplo con Zoho), hay que
  ajustar el SPF y agregar DKIM según las instrucciones de ese proveedor.

## 7. Trabajar en equipo con git

El código de la web vive en un repositorio git. Así cada persona trabaja en su copia y los cambios
quedan guardados con su historial.

**Acceso total para una socia o socio** (lo hace el dueño de cada cuenta):

1. **GitHub**: en el repositorio, ve a **Settings → Collaborators → Add people** e invita a su usuario.
2. **Cloudflare** (publicar la web, el dominio y el correo): **Manage Account → Members → Invite**,
   con su correo y el rol **Administrator**.

**Primera vez en otra computadora** (necesita [Git](https://git-scm.com), [Node.js](https://nodejs.org) y Python):

```
git clone <dirección del repositorio>
cd <carpeta del repositorio>
npx.cmd wrangler login
```

**Para cada cambio:**

```
git pull                         # 1. trae los últimos cambios
                                 # 2. edita los archivos en public/ y revisa en http://localhost:8080
git add -A
git commit -m "Describe el cambio"
git push                         # 3. guarda el cambio en GitHub
npx.cmd wrangler deploy          # 4. publica en fdpsoftware.org
```

Hagan siempre `git pull` antes de empezar, para no pisar el trabajo de la otra persona.

## 8. Videos para redes sociales

Los videos publicitarios verticales (Instagram, TikTok, Shorts y Estados) se arman con un programa que está en
`videos/`. La guía completa, con cómo cambiar textos, hacer videos nuevos y las reglas del estilo, está en
[videos/LEEME.md](videos/LEEME.md). Para generarlos todos:

```
python videos/generador/videos.py
```

Los videos terminados quedan en `videos-redes/` y no se suben a git.

Redes de FDP: Instagram [@freethepress05](https://www.instagram.com/freethepress05/) y TikTok
[@freethepress5](https://www.tiktok.com/@freethepress5). Aparecen en el pie de página de la web y al final de cada video.
