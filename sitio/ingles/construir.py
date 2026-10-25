"""Genera la versión en inglés (public/en/) a partir de las páginas en español y enlaza ambas versiones.

Uso, desde la carpeta WEB:   python sitio/ingles/construir.py

- Traduce textos visibles, atributos (alt, aria-label, title, data-name), metadatos y datos para Google con
  traducciones.json. Si un texto en español no está en el diccionario, lo avisa y lo deja en español:
  agrégalo a "textos" en traducciones.json y vuelve a correr el programa.
- Cambia los enlaces internos a /en/, el idioma, canonical, og:url, og:locale y el mensaje de WhatsApp
  (los mensajes van en "whatsapp" de traducciones.json).
- Agrega el botón ES/EN del menú y las etiquetas hreflang en las dos versiones.
Las páginas en inglés se regeneran desde cero: no las edites a mano.
"""
import glob
import html
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import quote, unquote

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.normpath(os.path.join(AQUI, "..", "..", "public"))
SITE = "https://fdpsoftware.org"
_dic = json.load(open(os.path.join(AQUI, "traducciones.json"), encoding="utf-8"))
D, WA = _dic["textos"], _dic["whatsapp"]

PAGINAS = ["index.html", "servicios/index.html"] + sorted(glob.glob("proyectos/*/index.html", root_dir=WEB))
PAGINAS = [p.replace("\\", "/") for p in PAGINAS]


def ruta_web(p):
    return "/" + p[: -len("index.html")]


def patron(es):
    partes = [re.escape(html.escape(w, quote=False)) for w in es.split(" ")]
    return r"\s+".join(partes)


# Patrones compilados una vez, de los textos más largos a los más cortos
ORDEN = sorted(D, key=len, reverse=True)
TEXTO = [(re.compile(r"(>\s*)" + patron(es) + r"(\s*<)"), html.escape(D[es], quote=False)) for es in ORDEN]
ATRIB = [(re.compile(r'((?:alt|aria-label|title|data-name|content|placeholder)=")' + patron(es).replace(re.escape("&#x27;"), "'") + '"'),
          html.escape(D[es], quote=True)) for es in ORDEN]
JSONS = [(re.compile('"' + re.escape(es) + '"'), json.dumps(D[es], ensure_ascii=False)) for es in ORDEN]


def traducir(h):
    for rx, en in TEXTO:
        h = rx.sub(lambda m: m.group(1) + en + m.group(2), h)
    for rx, en in ATRIB:
        h = rx.sub(lambda m: m.group(1) + en + '"', h)
    # Bloque de datos para Google
    def ld(m):
        b = m.group(0)
        for rx, en in JSONS:
            b = rx.sub(lambda _: en, b)
        return b.replace('"inLanguage": "es"', '"inLanguage": "en"')
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', ld, h, flags=re.S)
    # Íconos con texto dentro de los SVG
    h = h.replace(">TI</text>", ">IT</text>").replace(">IA</text>", ">AI</text>")
    return h


def whatsapp(m):
    texto = unquote(m.group(1))
    r = re.fullmatch(r"Hola FDP Software, quiero información sobre (.+)\.", texto)
    assert r and r.group(1) in WA, texto
    return "text=" + quote(f"Hi FDP Software, I'd like information about {WA[r.group(1)]}.", safe="")


def enlaces_en(h, p):
    # Rutas relativas de la portada (img/…, css/…) pasan a absolutas para que funcionen desde /en/
    h = re.sub(r'(?<=["\s,])(img|css|js|fonts|video|docs)/', r"/\1/", h)
    h = re.sub(r'href="/(proyectos|servicios)/', r'href="/en/\1/', h)
    h = re.sub(r'href="/(#[^"]*)?"', lambda m: f'href="/en/{m.group(1) or ""}"', h)
    h = re.sub(r'"(https://fdpsoftware\.org)/((?:proyectos|servicios)/[^"]*)?"', lambda m: f'"{m.group(1)}/en/{m.group(2) or ""}"', h)
    # Excepciones: la imagen y el logo de los datos para Google no cambian de dirección
    h = h.replace("https://fdpsoftware.org/en/#", "https://fdpsoftware.org/#")
    h = re.sub(r"text=([^\"&]+)", whatsapp, h)
    h = h.replace('<html lang="es">', '<html lang="en">')
    h = h.replace('content="es_VE"', 'content="en_US"')
    return h


def boton_idioma(h, actual, otra_url, otra):
    marca = '<a href="#contacto" class="btn btn--dark btn--small">'
    etiqueta = {"es": ("ES", "Versión en español"), "en": ("EN", "English version")}[otra]
    a = f'<a href="{otra_url}" class="nav__lang" hreflang="{otra}" lang="{otra}" aria-label="{etiqueta[1]}">{etiqueta[0]}</a>\n        '
    h = re.sub(r'\n        <a href="[^"]*" class="nav__lang"[^>]*>[A-Z]{2}</a>', "", h)
    assert h.count(marca) == 1, "no encontré el botón de contacto del menú"
    return h.replace(marca, a + marca, 1)


def hreflang(h, url_es, url_en):
    h = re.sub(r'\n  <link rel="alternate" hreflang="[^"]+" href="[^"]+">', "", h)
    bloque = (f'\n  <link rel="alternate" hreflang="es" href="{url_es}">'
              f'\n  <link rel="alternate" hreflang="en" href="{url_en}">'
              f'\n  <link rel="alternate" hreflang="x-default" href="{url_es}">')
    h, k = re.subn(r'(<link rel="canonical" href="[^"]+">)', r"\1" + bloque.replace("\\", "\\\\"), h, count=1)
    assert k == 1
    return h


ATTRS = {"alt", "aria-label", "title", "placeholder", "data-name"}
META = {"description", "og:title", "og:description", "og:image:alt", "twitter:title", "twitter:description"}
NO_TRADUCIR = re.compile(r"^[A-Z0-9]{1,3}$|^[\w.+-]+@[\w.-]+$")


class Textos(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.textos, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "svg"):
            self.skip += 1
        if tag == "meta" and (a.get("name") in META or a.get("property") in META):
            self.textos.append(a.get("content", ""))
        for k in ATTRS:
            if a.get(k) and not (tag == "a" and "nav__lang" in a.get("class", "")):
                self.textos.append(a[k])

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg"):
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip and d.strip():
            self.textos.append(d.strip())


faltan = set()
for p in PAGINAS:
    t = Textos(); h = open(os.path.join(WEB, p), encoding="utf-8").read(); t.feed(h)
    for x in [re.search(r"<title>(.*?)</title>", h).group(1)] + t.textos:
        x = re.sub(r"\s+", " ", x).strip()
        if x and x not in D and re.search(r"[A-Za-zÁÉÍÓÚáéíóúñÑ]", x) and not NO_TRADUCIR.match(x) and x not in D.values():
            faltan.add(x)
if faltan:
    print("Textos sin traducir (quedan en español en /en/):")
    for x in sorted(faltan):
        print("  -", x)

for p in PAGINAS:
    origen = os.path.join(WEB, p)
    es = open(origen, encoding="utf-8").read()
    url_es = SITE + ruta_web(p)
    url_en = SITE + "/en" + ruta_web(p)
    # Español: botón EN y hreflang
    es = boton_idioma(es, "es", "/en" + ruta_web(p), "en")
    es = hreflang(es, url_es, url_en)
    open(origen, "w", encoding="utf-8", newline="\n").write(es)
    # Inglés
    en = es
    en = traducir(en)
    en = enlaces_en(en, p)
    en = boton_idioma(en, "en", ruta_web(p), "es")
    en = hreflang(en, url_es, url_en)
    destino = os.path.join(WEB, "en", p)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    open(destino, "w", encoding="utf-8", newline="\n").write(en)
    print("ok", "/en" + ruta_web(p))
