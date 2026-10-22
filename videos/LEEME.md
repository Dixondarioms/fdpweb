# Videos publicitarios para redes sociales

Aquí está el programa que arma los videos de FDP para Instagram, TikTok, YouTube Shorts y Estados de WhatsApp.
Todos los videos salen con el mismo estilo y se pueden cambiar o hacer nuevos sin programas de edición.

```
videos/
├── LEEME.md            ← esta guía
├── generador/
│   ├── videos.py       ← EL GUION de cada video: textos, imágenes, tomas y tiempos
│   └── engine.py       ← el diseño: fondo, animaciones, tarjetas y cierre con el contacto
└── clips/              ← tomas de video cortas (AeroEscuela y Marcelo Go)
```

Las imágenes y las fuentes son las mismas de la web (`public/img/` y `public/fonts/`).
Los videos terminados se guardan en la carpeta `videos-redes/`, que **no se sube a git** porque pesan mucho.

## Los videos que hay

| Nombre | Duración | Qué muestra |
|---|---|---|
| `01-fdp-software` | 21 s | La marca: SIGMA MRO, AeroEscuela, entrenamiento táctico, Escenarios 3D, Marcelo Go y las soluciones |
| `02-sigma-mro` | 25 s | Flota, órdenes de trabajo, inventario, asistente con IA y "sin nube" |
| `03-aeroescuela` | 25 s | Tomas reales del simulador de vuelo |
| `04-escenarios-3d` | 20 s | "Caracas, en 3D": recorrido por la ciudad |
| `05-fdp-aplicaciones` | 17 s | Marcelo Go, Minijuegos y Ritmo Diario |
| `06-sin-internet` | 16 s | "¿Tu sistema se cae cuando se va el internet?": SIGMA MRO sin nube |
| `07-marcelo-go` | 15 s | "¿Listo para explotar burbujas?": poderes y retos de Marcelo Go |
| `08-ia-local` | 17 s | IA que no envía tus datos a la nube |
| `09-hecho-en-venezuela` | 20 s | Caracas en 3D, aeropuertos venezolanos en AeroEscuela y Marcelo Go |
| `10-a-la-medida` | 20 s | Método de trabajo: diseñamos, desarrollamos, acompañamos |
| `11-escuelas-de-vuelo` | 17 s | SIGMA MRO y AeroEscuela para escuelas de vuelo y talleres |
| `12-ritmo-diario` | 14 s | "¿Cómo te sientes hoy?": la app Ritmo Diario |

## 1. Preparar el computador (solo la primera vez)

Hacen falta **Python 3** y **ffmpeg**. En PowerShell:

```
winget install Python.Python.3.13
winget install Gyan.FFmpeg
pip install pillow numpy
```

Cierra y vuelve a abrir PowerShell después de instalarlos.

## 2. Generar los videos

Desde la carpeta `WEB`:

```
python videos/generador/videos.py
```

Genera todos los videos en `videos-redes/` (tarda unos minutos). Para generar uno solo:

```
python videos/generador/videos.py 02-sigma-mro
```

**Revisar sin esperar**: este comando guarda en `videos-redes/previas/` una imagen de los segundos 1, 4.5 y 24
del video, para ver cómo queda un cambio antes de generar el video completo:

```
python videos/generador/videos.py 02-sigma-mro previa 1,4.5,24
```

## 3. Cambiar un texto, una imagen o un tiempo

Abre `videos/generador/videos.py`. Cada video es una función (`sigma()`, `aeroescuela()`, `marca()`…).
Cada escena es una línea como esta:

```python
els += feat('ÓRDENES DE TRABAJO', 'Con firma, inspección y retorno a servicio.', 9.1, 12.4,
            Card(img, 9.1, 12.4, ('center', CARD_Y, 1000, 700), c0=(866, 430), c1=(680, 430)))
```

- `'ÓRDENES DE TRABAJO'` es la etiqueta pequeña (en mayúsculas) y `'Con firma, …'` es el titular grande.
  El titular se reparte solo en varias líneas; que no pase de tres.
- `9.1, 12.4` son el segundo en que la escena entra y el segundo en que sale. Cada escena dura unos 3 segundos
  y se cruza 0.2 s con la siguiente. Si alargas una, corre las siguientes.
- `Card('nombre.webp', …)` es una imagen de `public/img/`. `(1000, 700)` es el tamaño de la tarjeta;
  `c0` y `c1` son el punto de la imagen que se ve al principio y al final (así se mueve despacio);
  `s0` y `s1` son el tamaño (1 = tamaño original).
- `aero('fisica', …)` y `marcelo(…)` usan las tomas de video de `videos/clips/`.
- El **cierre** (logo, "Solicita una demostración", WhatsApp, web, correo, Instagram y TikTok) está en la función
  `cta()` de `engine.py`. Los usuarios de las redes están en `REDES`, en ese mismo archivo.

Para hacer un **video nuevo**, copia la función de uno parecido, cámbiale el nombre y los textos, y agrégala a
la lista `VIDEOS` del final de `videos.py`.

## 4. Agregar una toma de video

Las tomas van en `videos/clips/`, ya recortadas y **a su tamaño original** (nunca ampliadas), de 4 a 5 segundos.
Por ejemplo, para sacar 4.2 segundos desde el segundo 20, en un recuadro de 1000×570 que empieza en x=140, y=130:

```
ffmpeg -ss 20 -i original.mp4 -t 4.2 -vf "crop=1000:570:140:130,fps=30" -an -c:v libx264 -crf 12 -pix_fmt yuv420p videos/clips/nombre.mp4
```

Antes de usarla, mírala completa: no debe tener escudos, nombres de instituciones, subtítulos, rutas de archivos,
punteros del mouse ni datos personales.

## 5. Calendario de publicaciones

`videos/generador/calendario.py` tiene las publicaciones del mes: fecha, video, texto para Instagram y texto para
TikTok. Después de generar los videos, ejecuta:

```
python videos/generador/calendario.py
```

Crea `videos-redes/programar/` con una carpeta por publicación (`01-2026-10-26`, `02-2026-10-28`…). Cada una trae el
video, `portada.jpg`, `texto-instagram.txt` y `texto-tiktok.txt`. También crea `calendario.html`, una página con todas las
publicaciones y botones para copiar los textos. Su diseño está en `videos/generador/calendario.html`.

Para el mes siguiente, cambia las fechas y los textos de la lista `PUBLICACIONES` y vuelve a ejecutarlo.

**Cómo programar**
- **Instagram**: en [Meta Business Suite](https://business.facebook.com) → Planificador → Crear reel. Sube el video,
  pega el texto, sube `portada.jpg` como portada y elige **Programar**. Se puede dejar el mes completo programado.
- **TikTok**: en [TikTok Studio](https://www.tiktok.com/tiktokstudio/upload) sube el video, pega el texto, elige la portada
  y en **Cuándo publicar** elige **Programar**. TikTok solo deja programar hasta 10 días antes: cada viernes programa
  las publicaciones de la semana siguiente.

## 6. Reglas del estilo (obligatorias)

- **Formato**: vertical 1080×1920, 30 cuadros por segundo, entre 15 y 25 segundos.
- **Estructura**: una frase de gancho grande al inicio → escenas con etiqueta, titular y una captura o toma →
  cierre con el logo de la marca y el contacto.
- **Zonas seguras**: nada importante por encima de los 250 px ni por debajo de los 1480 px, porque ahí
  Instagram y TikTok ponen sus botones y textos.
- **Imágenes en HD**: nunca por encima de su tamaño original. Si lo intentas, el programa se detiene con el error
  `no se amplían imágenes`: usa una tarjeta más pequeña o una imagen más grande.
- **Contenido**: no muestres el simulador IGLA ni los simuladores de tiro. No muestres escudos ni nombres de
  instituciones militares, ni qué país real es cada bando en el entrenamiento táctico, ni nombres de personas.
  No inventes clientes, cifras ni testimonios.
- **Marcas**: siempre FDP Software, FDP Simuladores y FDP Aplicaciones.
- **Sin música**: se agrega al publicar, desde la biblioteca de Instagram o TikTok
  (así no hay problemas de derechos de autor y las apps los muestran a más gente).

## 7. Con Claude

También puedes pedirle a Claude, en español, cosas como "haz un video de SIGMA MRO más corto" o
"cambia el titular de la segunda escena". Claude conoce este estilo y estas reglas por el archivo `CLAUDE.md`.
