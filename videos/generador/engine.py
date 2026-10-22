"""Motor de los videos publicitarios verticales (1080x1920) de FDP Software.

Cada video es una lista de elementos (textos, tarjetas con imágenes o tomas de video,
logos) con un tiempo de entrada y de salida. Las imágenes nunca se muestran por encima
de su tamaño original (regla de HD): si se intenta, el programa se detiene con un error.
Los guiones de cada video están en videos.py; la guía está en videos/LEEME.md.
"""
import os, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(HERE, '..', '..'))   # carpeta del repositorio
IMG = os.path.join(RAIZ, 'public', 'img')                  # las mismas imágenes de la web
FUENTES = os.path.join(RAIZ, 'public', 'fonts')            # Inter e Inter Tight
CLIPS = os.path.join(RAIZ, 'videos', 'clips')              # tomas de video cortas
SALIDA = os.path.join(RAIZ, 'videos-redes')                # videos terminados (no se suben a git)

NIGHT = (11, 13, 26)
WHITE = (255, 255, 255)
MUTED = (184, 189, 214)
KICK = (94, 214, 190)          # verde azulado claro, legible sobre fondo oscuro
GRAD = [(59, 70, 196), (31, 154, 135), (227, 134, 43), (201, 48, 122)]
GRAD_TEXT = [(110, 125, 255), (52, 205, 178), (240, 160, 70), (232, 80, 150)]


# ---------- utilidades ----------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def ease_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3

def ease_in(x):
    x = clamp(x); return x ** 3

def ease_inout(x):
    x = clamp(x); return 3 * x * x - 2 * x * x * x

def lerp(a, b, u):
    return a + (b - a) * u

_fonts = {}
def font(kind, size, weight):
    key = (kind, size, weight)
    if key not in _fonts:
        path = os.path.join(FUENTES, 'inter-tight-latin.woff2' if kind == 'display' else 'inter-latin.woff2')
        f = ImageFont.truetype(path, size)
        f.set_variation_by_axes([weight])
        _fonts[key] = f
    return _fonts[key]

def gradient_strip(w, h, colors):
    xs = np.linspace(0, 1, w)
    seg = len(colors) - 1
    out = np.zeros((w, 3))
    for c in range(3):
        out[:, c] = np.interp(xs, np.linspace(0, 1, seg + 1), [col[c] for col in colors])
    return Image.fromarray(np.repeat(out[None, :, :], h, axis=0).astype(np.uint8), 'RGB')

def with_alpha(im, alpha):
    if alpha >= 0.999:
        return im
    im = im.copy()
    a = im.getchannel('A').point(lambda v: int(v * alpha))
    im.putalpha(a)
    return im

def put(canvas, im, x, y, alpha=1.0):
    """Compone una capa RGBA en el lienzo, recortando lo que sale del cuadro."""
    if alpha <= 0.003:
        return
    x, y = int(round(x)), int(round(y))
    w, h = im.size
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x0 >= x1 or y0 >= y1:
        return
    part = im.crop((x0 - x, y0 - y, x1 - x, y1 - y))
    canvas.alpha_composite(with_alpha(part, alpha), (x0, y0))

def rounded_mask(w, h, r):
    s = 3  # supermuestreo para bordes suaves
    m = Image.new('L', (w * s, h * s), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * s - 1, h * s - 1), r * s, fill=255)
    return m.resize((w, h), Image.LANCZOS)

_shadows = {}
def shadow(w, h, r, blur=40, opacity=150):
    key = (w, h, r)
    if key not in _shadows:
        pad = blur * 2
        sh = Image.new('L', (w + pad * 2, h + pad * 2), 0)
        ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 18, pad + w, pad + h + 18), r, fill=opacity)
        sh = sh.filter(ImageFilter.GaussianBlur(blur))
        im = Image.new('RGBA', sh.size, (0, 0, 0, 0)); im.putalpha(sh)
        _shadows[key] = (im, pad)
    return _shadows[key]


# ---------- fondo ----------
def make_background(seed=0, blobs=None):
    bw, bh = W + 120, H + 120
    yy, xx = np.mgrid[0:bh, 0:bw].astype(np.float32)
    img = np.zeros((bh, bw, 3), np.float32) + np.array(NIGHT, np.float32)
    blobs = blobs or [
        (0.85, 0.16, 0.55, 0.30, (59, 70, 196), 0.80),
        (0.10, 0.08, 0.45, 0.22, (31, 154, 135), 0.45),
        (1.00, 0.62, 0.50, 0.30, (201, 48, 122), 0.55),
        (0.05, 0.90, 0.55, 0.28, (227, 134, 43), 0.30),
        (0.55, 1.02, 0.60, 0.25, (75, 43, 214), 0.45),
    ]
    for cx, cy, rx, ry, col, op in blobs:
        d = ((xx / bw - cx) / rx) ** 2 + ((yy / bh - cy) / ry) ** 2
        a = np.clip(1 - np.sqrt(d) / 1.0, 0, 1) ** 1.6 * op
        img = img * (1 - a[..., None]) + np.array(col, np.float32) * a[..., None]
    img *= 0.62  # más oscuro: el contenido es el protagonista
    rng = np.random.default_rng(seed)
    img += rng.normal(0, 1.1, img.shape)  # leve grano para evitar bandas en el degradado
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')


# ---------- elementos ----------
class El:
    t0 = 0; t1 = 0
    def active(self, t):
        return self.t0 <= t <= self.t1


class Text(El):
    """Bloque de texto con aparición línea por línea (sube desde una máscara)."""
    def __init__(self, lines, t0, t1, x=80, y=300, size=84, weight=800, kind='display',
                 color=WHITE, align='left', leading=1.08, stagger=0.08, rise=1.0, exit=True):
        self.t0, self.t1 = t0, t1
        self.layers = []
        f = font(kind, size, weight)
        asc, desc = f.getmetrics()
        lh = int(size * leading)
        cy = y
        for line in lines:
            style = color
            if isinstance(line, tuple):
                line, style = line
            bbox = f.getbbox(line)
            w = bbox[2] + 4
            h = asc + desc + 6
            mask = Image.new('L', (w, h), 0)
            ImageDraw.Draw(mask).text((0, 0), line, font=f, fill=255)
            if style == 'grad':
                fill = gradient_strip(w, h, GRAD_TEXT)
            else:
                fill = Image.new('RGB', (w, h), style)
            layer = fill.convert('RGBA'); layer.putalpha(mask)
            lx = {'left': x, 'center': (W - w) // 2, 'right': W - x - w}[align]
            self.layers.append((layer, lx, cy, h))
            cy += lh
        self.bottom = cy
        self.stagger, self.rise, self.exit = stagger, rise, exit

    def draw(self, cv, t):
        for i, (layer, x, y, h) in enumerate(self.layers):
            s = self.t0 + i * self.stagger
            p = ease_out((t - s) / 0.55)
            if p <= 0:
                continue
            alpha = clamp(p * 1.4)
            dy = (1 - p) * h * 0.9 * self.rise
            if self.exit:
                q = ease_in((t - (self.t1 - 0.32)) / 0.32)
                alpha *= 1 - q
                dy -= q * 26
            # recorte: la línea "sube" dentro de su propia caja
            top = int(round(dy))
            vis = layer.crop((0, 0, layer.width, max(0, min(layer.height, layer.height - top)))) if top > 0 else layer
            put(cv, vis, x, y + max(top, 0) if top > 0 else y + top, alpha)


class Bar(El):
    """Barra con el degradado de la marca que crece de izquierda a derecha."""
    def __init__(self, t0, t1, x=80, y=280, w=140, h=8, align='left'):
        self.t0, self.t1, self.y, self.w, self.h = t0, t1, y, w, h
        self.x = (W - w) // 2 if align == 'center' else x
        self.align = align
        im = gradient_strip(w, h, GRAD).convert('RGBA')
        im.putalpha(rounded_mask(w, h, h // 2))
        self.im = im

    def draw(self, cv, t):
        p = ease_out((t - self.t0) / 0.6)
        q = ease_in((t - (self.t1 - 0.3)) / 0.3)
        w = int(self.w * p)
        if w < 2:
            return
        x = self.x + (self.w - w) // 2 if self.align == 'center' else self.x
        put(cv, self.im.crop((0, 0, w, self.h)), x, self.y, 1 - q)


class Card(El):
    """Imagen en tarjeta redondeada con paneo/zoom lento. Escala siempre <= 1."""
    def __init__(self, src, t0, t1, box, c0=None, c1=None, s0=1.0, s1=None, radius=30,
                 enter='up', exit='fade', move=None):
        s1 = s0 if s1 is None else s1
        smax = max(s0, s1)
        assert smax <= 1.0001, 'no se amplían imágenes'
        im = Image.open(os.path.join(IMG, src)).convert('RGB') if isinstance(src, str) else src
        self.iw, self.ih = im.size
        self.pre = im.resize((round(self.iw * smax), round(self.ih * smax)), Image.LANCZOS) if smax < 0.999 else im
        self.smax = smax
        self.t0, self.t1 = t0, t1
        self.x, self.y, self.w, self.h = box
        if self.x == 'center':
            self.x = (W - self.w) // 2
        self.c0 = c0 or (self.iw / 2, self.ih / 2)
        self.c1 = c1 or self.c0
        self.s0, self.s1 = s0, s1
        self.mask = rounded_mask(self.w, self.h, radius)
        self.radius = radius
        self.enter, self.exit = enter, exit
        self.move = move or (t0, t1)

    def frame(self, t):
        u = ease_inout((t - self.move[0]) / (self.move[1] - self.move[0]))
        s = lerp(self.s0, self.s1, u)
        cx, cy = lerp(self.c0[0], self.c1[0], u), lerp(self.c0[1], self.c1[1], u)
        hw, hh = self.w / 2 / s, self.h / 2 / s     # medio tamaño de la ventana, en px de la fuente
        cx = clamp(cx, hw, self.iw - hw); cy = clamp(cy, hh, self.ih - hh)
        k = self.smax / s
        a, c = k, cx * self.smax - (self.w / 2) * k
        e, f = k, cy * self.smax - (self.h / 2) * k
        if abs(k - 1) < 1e-6 and abs(c - round(c)) < 1e-3 and abs(f - round(f)) < 1e-3:
            return self.pre.crop((round(c), round(f), round(c) + self.w, round(f) + self.h))
        return self.pre.transform((self.w, self.h), Image.AFFINE, (a, 0, c, 0, e, f), Image.BICUBIC)

    def draw(self, cv, t):
        p = ease_out((t - self.t0) / 0.6)
        q = ease_in((t - (self.t1 - 0.35)) / 0.35) if self.exit else 0
        alpha = clamp(p * 1.3) * (1 - q)
        dx = dy = 0
        if self.enter == 'up':
            dy = (1 - p) * 120
        elif self.enter == 'right':
            dx = (1 - p) * 300
        if self.exit == 'up':
            dy -= q * 60
        img = self.frame(t).convert('RGBA')
        img.putalpha(self.mask)
        sh, pad = shadow(self.w, self.h, self.radius)
        put(cv, sh, self.x - pad + dx, self.y - pad + dy, alpha)
        put(cv, img, self.x + dx, self.y + dy, alpha)
        # borde fino claro
        put(cv, self.border(), self.x + dx, self.y + dy, alpha * 0.9)

    def border(self):
        if not hasattr(self, '_border'):
            s = 3
            m = Image.new('L', (self.w * s, self.h * s), 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, self.w * s - 1, self.h * s - 1), self.radius * s, outline=60, width=2 * s)
            m = m.resize((self.w, self.h), Image.LANCZOS)
            b = Image.new('RGBA', (self.w, self.h), (255, 255, 255, 0)); b.putalpha(m)
            self._border = b
        return self._border


class VideoCard(Card):
    """Como Card, pero el contenido es un fragmento de video (recortado a 1x por ffmpeg)."""
    def __init__(self, path, start, t0, t1, box, crop, scale=1.0, radius=30, enter='up', exit='fade'):
        cw, ch = crop[2], crop[3]
        ow, oh = round(cw * scale), round(ch * scale)
        assert scale <= 1.0001
        self.path, self.start, self.crop, self.scale = path, start, crop, scale
        self.t0, self.t1 = t0, t1
        self.x, self.y = box[0], box[1]
        self.w, self.h = ow, oh
        if self.x == 'center':
            self.x = (W - ow) // 2
        self.mask = rounded_mask(ow, oh, radius)
        self.radius, self.enter, self.exit = radius, enter, exit
        self.proc = None; self.idx = -1; self.last = None

    def _open(self):
        dur = self.t1 - self.t0 + 0.5
        vf = 'crop=%d:%d:%d:%d,fps=%d' % (self.crop[2], self.crop[3], self.crop[0], self.crop[1], FPS)
        if self.scale < 0.999:
            vf += ',scale=%d:%d:flags=lanczos' % (self.w, self.h)
        self.proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(self.start), '-i', self.path, '-t', str(dur),
                                      '-vf', vf, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def frame(self, t):
        if self.proc is None:
            self._open()
        want = int((t - self.t0) * FPS)
        n = self.w * self.h * 3
        while self.idx < want:
            buf = self.proc.stdout.read(n)
            if len(buf) < n:
                break
            self.last = Image.frombytes('RGB', (self.w, self.h), buf)
            self.idx += 1
        return self.last


class Logo(El):
    """Logo en baldosa redondeada (los logos vienen sobre fondo oscuro)."""
    def __init__(self, src, t0, t1, size, x='center', y=500, radius=None, exit=True):
        im = Image.open(os.path.join(IMG, src)).convert('RGB')
        assert size <= im.width
        im = im.resize((size, size), Image.LANCZOS).convert('RGBA')
        im.putalpha(rounded_mask(size, size, radius if radius is not None else size // 6))
        self.im, self.t0, self.t1, self.size = im, t0, t1, size
        self.x = (W - size) // 2 if x == 'center' else x
        self.y, self.exit = y, exit

    def draw(self, cv, t):
        p = ease_out((t - self.t0) / 0.7)
        q = ease_in((t - (self.t1 - 0.3)) / 0.3) if self.exit else 0
        sh, pad = shadow(self.size, self.size, self.size // 6, blur=50, opacity=170)
        dy = (1 - p) * 60
        put(cv, sh, self.x - pad, self.y - pad + dy, p * (1 - q))
        put(cv, self.im, self.x, self.y + dy, clamp(p * 1.3) * (1 - q))


class Pill(El):
    """Etiqueta en píldora con borde, como las de la web."""
    def __init__(self, text, t0, t1, x=80, y=250, size=30, align='left', color=KICK):
        f = font('body', size, 650)
        bbox = f.getbbox(text)
        tw, th = bbox[2], size
        padx, pady = 26, 14
        w, h = tw + padx * 2, th + pady * 2 + 4
        s = 3
        m = Image.new('L', (w * s, h * s), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w * s - 1, h * s - 1), h * s // 2, outline=255, width=2 * s)
        m = m.resize((w, h), Image.LANCZOS)
        im = Image.new('RGBA', (w, h), color + (0,))
        border = Image.new('RGBA', (w, h), color + (0,)); border.putalpha(m.point(lambda v: v * 0.55))
        im.alpha_composite(border)
        bg = Image.new('RGBA', (w, h), color + (0,)); bg.putalpha(rounded_mask(w, h, h // 2).point(lambda v: v * 0.12))
        im.alpha_composite(bg)
        d = ImageDraw.Draw(im)
        d.text((padx, pady - bbox[1] + 2), text, font=f, fill=color + (255,))
        self.im, self.t0, self.t1 = im, t0, t1
        self.x = (W - w) // 2 if align == 'center' else x
        self.y = y

    def draw(self, cv, t):
        p = ease_out((t - self.t0) / 0.5)
        q = ease_in((t - (self.t1 - 0.3)) / 0.3)
        put(cv, self.im, self.x - (1 - p) * 40, self.y, clamp(p * 1.3) * (1 - q))


class Header(El):
    """Marca fija arriba: logo pequeño + nombre."""
    def __init__(self, name, t0, t1, logo='logo-fdp-512.png'):
        size = 64
        lg = Image.open(os.path.join(IMG, logo)).convert('RGB').resize((size, size), Image.LANCZOS).convert('RGBA')
        lg.putalpha(rounded_mask(size, size, 14))
        f = font('display', 34, 750)
        bbox = f.getbbox(name)
        w = size + 18 + bbox[2] + 4
        im = Image.new('RGBA', (w, size), (0, 0, 0, 0))
        im.alpha_composite(lg)
        ImageDraw.Draw(im).text((size + 18, (size - 34) // 2 - bbox[1] + 2), name, font=f, fill=WHITE + (255,))
        self.im, self.t0, self.t1 = im, t0, t1

    def draw(self, cv, t):
        p = ease_out((t - self.t0) / 0.6)
        q = ease_in((t - (self.t1 - 0.4)) / 0.4)
        put(cv, self.im, 80, 150, p * (1 - q))


# ---------- escenas reutilizables ----------
def hook(lines, t0, t1, y=640, size=118):
    d = 0.3 if t0 > 0 else 0.1  # a mitad del video, espera a que salga el texto anterior
    return [Bar(t0 + d - 0.05, t1 - 0.15, y=y - 50, w=160),
            Text(lines, t0 + d, t1 - 0.15, y=y, size=size, weight=850, leading=1.04)]

def beat(kicker, lines, t0, t1, media, size=80):
    """Etiqueta + titular arriba y media (Card/VideoCard) debajo."""
    out = [Pill(kicker, t0 + 0.22, t1, y=320)] if kicker else []
    txt = Text(lines, t0 + 0.3, t1, y=410, size=size, weight=820)
    out += [txt]
    out += media if isinstance(media, list) else [media]
    return out

# Redes sociales de FDP: aparecen al final de cada video
REDES = ['Instagram  @freethepress05', 'TikTok  @freethepress5']

def cta(t0, t1, logo='logo-software.webp', title=('Solicita una', 'demostración'), extra=None):
    """Cierre: logo, llamado a la acción, contacto y redes sociales."""
    els = [Logo(logo, t0 + 0.25, t1 + 1, 380, y=330, exit=False),
           Text(list(title), t0 + 0.45, t1 + 1, y=790, size=88, weight=850, align='center', exit=False),
           Bar(t0 + 0.65, t1 + 1, y=1000, w=180, align='center')]
    lines = extra or [('WhatsApp  +58 412-0846332', WHITE), ('fdpsoftware.org', 'grad'), ('contacto@fdpsoftware.org', MUTED)]
    y, d = 1050, t0 + 0.75
    for i, (text, style) in enumerate(lines):
        if style == 'grad':     # la web, grande y con el degradado de la marca
            size, kw = 64, dict(weight=850)
        elif i == 0:
            size, kw = 50, dict(weight=600, kind='body')
        else:
            size, kw = 40, dict(weight=500, kind='body')
        els.append(Text([(text, style)], d, t1 + 1, y=y, size=size, align='center', exit=False, **kw))
        y += int(size * 1.6); d += 0.12
    y += 10
    for red in REDES:
        els.append(Text([red], d, t1 + 1, y=y, size=40, weight=600, kind='body', align='center', color=KICK, exit=False))
        y += 58; d += 0.12
    return els


# ---------- render ----------
def render(elements, duration, out_path, seed=0, preview_times=None):
    bg = make_background(seed)
    total = int(round(duration * FPS))
    if preview_times is not None:
        frames = []
        for pt in preview_times:
            frames.append(compose(bg, elements, pt, duration))
        return frames
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS),
           '-i', '-', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-shortest',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
           '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
           '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(total):
        fr = compose(bg, elements, i / FPS, duration)
        p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    return out_path

def compose(bg, elements, t, duration):
    drift = t / duration
    ox, oy = int(60 + 50 * math.sin(drift * math.pi)), int(30 + 70 * drift)
    cv = bg.crop((ox, oy, ox + W, oy + H))
    for e in elements:
        if e.active(t):
            e.draw(cv, t)
    return cv
