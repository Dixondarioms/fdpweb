# Página web de FDP Software

Sitio estático (HTML, CSS y JavaScript) publicado en **Cloudflare** en <https://fdpsoftware.org>
(también responde en <https://www.fdpsoftware.org>).

```
WEB/
├── LEEME.md          ← esta guía (no se publica)
├── wrangler.jsonc    ← configuración de publicación en Cloudflare (no se publica)
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

- **Textos**: están en `public/index.html`.
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

## 4. Correo con tu dominio (gratis)

- **Solo recibir** en tu Gmail: en Cloudflare, ve a `fdpsoftware.org` → **Email → Email Routing** y crea
  `contacto@fdpsoftware.org` → tu correo personal.
- **Buzón completo** (enviar y recibir): usa Zoho Mail y sigue su asistente para agregar los registros DNS en Cloudflare.

## 5. Dominio

`fdpsoftware.org` está registrado en Cloudflare. Mantén activa la **renovación automática** en
**Domain Registration → Manage Domains**.

## 6. Trabajar en equipo con git

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
