"""Guiones de los videos publicitarios de FDP Software.

Uso (desde la carpeta del repositorio):
    python videos/generador/videos.py                     -> genera todos los videos
    python videos/generador/videos.py 02-sigma-mro        -> genera uno
    python videos/generador/videos.py 02-sigma-mro previa 1,4.5,24
        -> guarda imágenes de esos segundos en videos-redes/previas, para revisar sin esperar

La guía completa está en videos/LEEME.md.
"""
import os, sys
from PIL import Image
from engine import *

CARD_Y = 760


def wrap(text, size=80, maxw=920, weight=820):
    f = font('display', size, weight)
    words, lines, cur = text.split(), [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if f.getbbox(test)[2] <= maxw:
            cur = test
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

def feat(kicker, title, t0, t1, media, size=80):
    return beat(kicker, wrap(title, size), t0, t1, media, size=size)

def clip(nombre):
    return os.path.join(CLIPS, nombre + '.mp4')

def aero(nombre, t0, t1, enter='up'):
    """Toma de AeroEscuela (videos/clips/aeroescuela-<nombre>.mp4, 1000x570, se muestra a 1x)."""
    return VideoCard(clip('aeroescuela-' + nombre), 0.0, t0, t1, ('center', CARD_Y), (0, 0, 1000, 570), enter=enter)

def marcelo(desde, t0, t1, enter='up'):
    """Toma de Marcelo Go (1000x940), reducida a 0.78 para que quepa con el titular."""
    return VideoCard(clip('marcelo-go-cohete'), desde, t0, t1, ('center', CARD_Y - 20), (0, 0, 1000, 940), scale=0.78, enter=enter)


def sigma():
    img = 'proyecto-sigma-mro.webp'
    els = [Header('FDP Software', 0, 21.3)]
    els += hook(['Mantenimiento', 'aeronáutico,', ('bajo control.', 'grad')], 0, 2.9, y=680, size=112)
    els += feat('SIGMA MRO', 'Mantenimiento aeronáutico inteligente.', 2.7, 6.2,
                Card(img, 2.7, 6.2, ('center', CARD_Y, 1000, 630), s0=0.732, s1=0.78, c0=(683, 430), c1=(683, 360)))
    els += feat('FLOTA Y COMPONENTES', 'Límites por horas, ciclos o calendario.', 6.0, 9.3,
                Card(img, 6.0, 9.3, ('center', CARD_Y, 1000, 700), c0=(500, 350), c1=(700, 380)))
    els += feat('ÓRDENES DE TRABAJO', 'Con firma, inspección y retorno a servicio.', 9.1, 12.4,
                Card(img, 9.1, 12.4, ('center', CARD_Y, 1000, 700), c0=(866, 430), c1=(680, 430)))
    els += feat('INVENTARIO Y COMPRAS', 'Repuestos, compras y directivas AD/SB.', 12.2, 15.5,
                Card(img, 12.2, 15.5, ('center', CARD_Y, 1000, 700), c0=(680, 480), c1=(866, 480)))
    els += feat('IA LOCAL', 'Un asistente que consulta tus manuales, también por voz.', 15.3, 18.6,
                Card(img, 15.3, 18.6, ('center', CARD_Y, 1000, 700), c0=(500, 510), c1=(700, 510)))
    els += hook(['Escritorio y app', 'móvil por tu red', ('local. Sin nube.', 'grad')], 18.4, 21.3, y=720, size=104)
    els += cta(21.1, 25.5)
    return els, 25.5


def aeroescuela():
    els = [Header('FDP Simuladores', 0, 21.1, logo='logo-simuladores.webp')]
    els += hook(['Formar un piloto', 'cuesta caro.', ('Cada hora de', 'grad'), ('vuelo cuenta.', 'grad')], 0, 3.0, y=640, size=110)
    els += feat('AEROESCUELA', 'Simulador de vuelo en una computadora común.', 2.8, 6.2, aero('cabina', 2.8, 6.2))
    els += feat('FÍSICA REAL', 'Validada contra el manual del fabricante.', 6.0, 9.3, aero('fisica', 6.0, 9.3))
    els += feat('INSTRUCTOR VIRTUAL', 'Te guía, te vigila y te corrige en cada lección.', 9.1, 12.4, aero('instructor', 9.1, 12.4))
    els += feat('METEOROLOGÍA', 'Nubes, lluvia, tormentas y niebla.', 12.2, 15.5, aero('meteorologia', 12.2, 15.5))
    els += feat('AEROPUERTOS REALES', 'Venezuela, con su terreno e imagen satelital.', 15.3, 18.6, aero('aeropuertos', 15.3, 18.6))
    els += feat('EVALUACIÓN', 'Gráficas del vuelo e informe para el alumno y el instructor.', 18.4, 21.3,
                aero('evaluacion', 18.4, 21.3), size=76)
    els += cta(21.1, 25.5, logo='logo-simuladores.webp')
    return els, 25.5


def escenarios():
    els = [Header('FDP Software', 0, 16.1)]
    els += hook(['Caracas,', ('en 3D.', 'grad')], 0, 2.7, y=780, size=170)
    els.append(Card('proyecto-escenarios-3d.webp', 2.5, 16.1, ('center', CARD_Y, 1000, 760),
                    c0=(500, 560), c1=(1420, 520), move=(2.5, 16.1)))
    def txt(k, title, t0, t1):
        return [Pill(k, t0 + 0.22, t1, y=320), Text(wrap(title, 76), t0 + 0.3, t1, y=410, size=76, weight=820)]
    els += txt('ESCENARIOS 3D DE VENEZUELA', 'Ciudades reales, convertidas en escenarios 3D.', 2.5, 6.0)
    els += txt('DATOS ABIERTOS', 'OpenStreetMap, relieve satelital e imágenes Sentinel-2.', 5.8, 9.3)
    els += txt('UNREAL ENGINE 5', 'Un proceso automatizado los vuelve escenarios realistas.', 9.1, 12.6)
    els += txt('RECORRIDOS', 'Para recorrer a pie, en vehículo y en vuelo.', 12.4, 16.1)
    els += cta(15.9, 20.0)
    return els, 20.0


def aplicaciones():
    els = [Header('FDP Aplicaciones', 0, 13.1, logo='logo-aplicaciones.webp')]
    els += hook(['Juegos y apps', 'hechos en', 'Venezuela para', ('el mundo.', 'grad')], 0, 3.0, y=620, size=110)
    els += feat('MARCELO GO', 'Burbujas con poderes especiales y retos por niveles.', 2.8, 6.4,
                marcelo(0.1, 2.8, 6.4), size=76)
    els += feat('MINIJUEGOS DE MARCELO GO', 'Billar, carrom, ludo y más, en una sola app.', 6.4, 9.9,
                Card('app-minijuegos.webp', 6.4, 9.9, ('center', CARD_Y + 60, 640, 360)))
    els += feat('RITMO DIARIO', 'Tu diario de salud: dolor, energía, sueño y agua.', 9.7, 13.3,
                Card('app-ritmo-diario.webp', 9.7, 13.3, ('center', CARD_Y + 60, 640, 360)))
    els += cta(13.1, 17.5, logo='logo-aplicaciones.webp', title=('Búscalas en', 'Google Play'),
               extra=[('Marcelo Go · Ritmo Diario', WHITE), ('fdpsoftware.org', 'grad')])
    return els, 17.5


def marca():
    els = [Header('FDP Software', 0, 13.0 + 3.2)]
    els += hook(['Todo lo que', 'tu operación', ('necesita.', 'grad')], 0, 2.8, y=680, size=126)
    q = 2.25  # duración de cada toma rápida
    shots = [
        ('GESTIÓN DE MANTENIMIENTO', 'SIGMA MRO', lambda a, b: Card('proyecto-sigma-mro.webp', a, b, ('center', CARD_Y, 1000, 630), s0=0.732, s1=0.76, enter='right')),
        ('SIMULADOR DE VUELO', 'AeroEscuela', lambda a, b: aero('fisica', a, b, enter='right')),
        ('ENTRENAMIENTO TÁCTICO', 'Sobre mapas reales.', lambda a, b: Card('tactico-mapa.webp', a, b, ('center', CARD_Y, 1000, 700), c0=(700, 494), c1=(950, 494), enter='right')),
        ('ESCENARIOS 3D', 'Caracas, en 3D.', lambda a, b: Card('proyecto-escenarios-3d.webp', a, b, ('center', CARD_Y, 1000, 760), c0=(800, 540), c1=(1100, 540), enter='right')),
        ('APPS EN GOOGLE PLAY', 'Marcelo Go', lambda a, b: marcelo(0.6, a, b, enter='right')),
    ]
    t = 2.6
    for k, title, mk in shots:
        els += feat(k, title, t, t + q, mk(t, t + q))
        t += q - 0.2
    t += 0.2
    end = t + 3.4
    sol = ['Desarrollo web y móvil', 'Inteligencia artificial local', 'Simulación y entrenamiento',
           'Gestión de mantenimiento', 'Sistemas embebidos', 'Soporte y mantenimiento']
    els += [Pill('SOLUCIONES', t + 0.22, end, y=320)]
    els += [Text(sol, t + 0.3, end, y=420, size=70, weight=780, leading=1.38, stagger=0.13)]
    els += [Bar(t + 0.9, end, y=1080, w=180)]
    els += [Text(['Para que tu operación', ('nunca se detenga.', 'grad')], t + 1.0, end, y=1130, size=64, weight=820)]
    els += cta(end - 0.2, end + 4.2)
    return els, round(end + 4.2, 2)


# ---------- Videos cortos para el calendario de publicaciones ----------
SIGMA = 'proyecto-sigma-mro.webp'

def sigma_card(t0, t1, c0, c1):
    """Un recorte de la pantalla de SIGMA MRO a tamaño original (1000x700), con paneo lento."""
    return Card(SIGMA, t0, t1, ('center', CARD_Y, 1000, 700), c0=c0, c1=c1)

def frase(lineas, t0, t1, size=104, y=720):
    """Frase grande sin imagen, a mitad del video."""
    return hook(lineas, t0, t1, y=y, size=size)

def paso(num, titulo, texto, t0, t1):
    """Paso numerado del método de trabajo (01, 02, 03)."""
    return [Text([(num, 'grad')], t0 + 0.3, t1, y=520, size=230, weight=900),
            Text([titulo], t0 + 0.42, t1, y=800, size=112, weight=850),
            Text(wrap(texto, 62, weight=600), t0 + 0.55, t1, y=960, size=62, weight=600, color=MUTED)]


def sin_internet():
    els = [Header('FDP Software', 0, 12.0)]
    els += hook(['¿Tu sistema', 'se cae cuando', 'se va el', ('internet?', 'grad')], 0, 3.0, y=600, size=116)
    els += feat('SIGMA MRO', 'Gestión de mantenimiento 100 % sin nube.', 2.8, 6.1,
                Card(SIGMA, 2.8, 6.1, ('center', CARD_Y, 1000, 630), s0=0.732, s1=0.78))
    els += feat('RED LOCAL', 'Escritorio y app móvil por tu propia red.', 5.9, 9.2,
                sigma_card(5.9, 9.2, (500, 350), (760, 380)))
    els += frase(['Tus datos,', ('bajo tu control.', 'grad')], 9.0, 12.0)
    els += cta(11.8, 16.2)
    return els, 16.2


def marcelo_go():
    els = [Header('FDP Aplicaciones', 0, 10.4, logo='logo-aplicaciones.webp')]
    els += hook(['¿Listo para', 'explotar', ('burbujas?', 'grad')], 0, 2.8, y=680, size=130)
    els += feat('MARCELO GO', 'Poderes especiales: varita, cohete, martillo, bomba y rayo.', 2.6, 6.4,
                marcelo(0.1, 2.6, 6.4), size=76)
    els += feat('RETOS POR NIVELES', 'Premios y recompensas al avanzar.', 6.2, 10.4,
                Card('app-marcelo-go.webp', 6.2, 10.4, ('center', CARD_Y, 860, 700), s0=0.86, c0=(500, 420), c1=(500, 640)))
    els += cta(10.2, 14.6, logo='logo-aplicaciones.webp', title=('Búscalo en', 'Google Play'),
               extra=[('Busca «Marcelo Go»', WHITE), ('fdpsoftware.org', 'grad')])
    return els, 14.6


def ia_local():
    els = [Header('FDP Software', 0, 12.3)]
    els += hook(['IA que trabaja', 'sin enviar', 'tus datos a', ('la nube.', 'grad')], 0, 3.0, y=600, size=116)
    els += feat('ASISTENTE CON IA', 'Consulta tus manuales técnicos, también por voz.', 2.8, 6.4,
                sigma_card(2.8, 6.4, (500, 510), (866, 510)))
    els += feat('IA LOCAL', 'Asistentes de IA sobre tus propios documentos.', 6.2, 9.5,
                Card(SIGMA, 6.2, 9.5, ('center', CARD_Y, 1000, 630), s0=0.78, s1=0.732))
    els += frase(['Tus datos se', ('quedan contigo.', 'grad')], 9.3, 12.3)
    els += cta(12.1, 16.5)
    return els, 16.5


def hecho_en_venezuela():
    els = [Header('FDP Software', 0, 15.4)]
    els += hook(['Hecho en', ('Venezuela.', 'grad')], 0, 2.6, y=760, size=160)
    els += feat('ESCENARIOS 3D', 'Caracas, recreada en 3D con datos reales.', 2.4, 5.8,
                Card('proyecto-escenarios-3d.webp', 2.4, 5.8, ('center', CARD_Y, 1000, 760), c0=(600, 540), c1=(1000, 540)))
    els += feat('AEROESCUELA', 'Vuela sobre aeropuertos reales de Venezuela.', 5.6, 9.0, aero('aeropuertos', 5.6, 9.0))
    els += feat('FDP APLICACIONES', 'Juegos y apps en Google Play.', 8.8, 12.4, marcelo(0.1, 8.8, 12.4))
    els += frase(['De Venezuela', ('para el mundo.', 'grad')], 12.2, 15.4, size=110)
    els += cta(15.2, 19.6)
    return els, 19.6


def a_la_medida():
    els = [Header('FDP Software', 0, 15.4)]
    els += hook(['¿Necesitas un', 'sistema a', ('tu medida?', 'grad')], 0, 2.9, y=680, size=124)
    els += paso('01', 'Diseñamos.', 'Analizamos tus procesos y definimos alcance, tiempos y costo.', 2.7, 6.0)
    els += paso('02', 'Desarrollamos.', 'Por etapas, con pruebas y documentación en cada entrega.', 5.8, 9.1)
    els += paso('03', 'Acompañamos.', 'Instalamos en tu sitio, capacitamos a tu equipo y damos soporte.', 8.9, 12.2)
    els += frase(['Web, móvil,', 'IA y sistemas', ('embebidos.', 'grad')], 12.0, 15.4, y=660)
    els += cta(15.2, 19.6)
    return els, 19.6


def escuelas_de_vuelo():
    els = [Header('FDP Software', 0, 12.6)]
    els += hook(['Para escuelas', 'de vuelo y', 'talleres', ('aeronáuticos.', 'grad')], 0, 3.0, y=600, size=116)
    els += feat('SIGMA MRO', 'Tu flota al día: límites por horas, ciclos o calendario.', 2.8, 6.2,
                sigma_card(2.8, 6.2, (500, 350), (700, 380)), size=76)
    els += feat('AEROESCUELA', 'Entrenamiento de vuelo en una computadora común.', 6.0, 9.4,
                aero('cabina', 6.0, 9.4), size=76)
    els += feat('EVALUACIÓN', 'Gráficas del vuelo e informe para el alumno y el instructor.', 9.2, 12.6,
                aero('evaluacion', 9.2, 12.6), size=72)
    els += cta(12.4, 16.8)
    return els, 16.8


def ritmo_diario():
    els = [Header('FDP Aplicaciones', 0, 10.0, logo='logo-aplicaciones.webp')]
    els += hook(['¿Cómo te', ('sientes hoy?', 'grad')], 0, 2.7, y=760, size=130)
    els += feat('RITMO DIARIO', 'Tu diario de salud: dolor, energía, sueño y agua.', 2.5, 6.6,
                Card('app-ritmo-diario.webp', 2.5, 6.6, ('center', CARD_Y + 60, 640, 360)))
    els += frase(['Registra tus', 'tratamientos y', 'mira tu evolución', ('en gráficas.', 'grad')], 6.4, 10.0, size=96, y=640)
    els += cta(9.8, 14.2, logo='logo-aplicaciones.webp', title=('Búscalo en', 'Google Play'),
               extra=[('Busca «Ritmo Diario»', WHITE), ('fdpsoftware.org', 'grad')])
    return els, 14.2


VIDEOS = {'01-fdp-software': marca, '02-sigma-mro': sigma, '03-aeroescuela': aeroescuela,
          '04-escenarios-3d': escenarios, '05-fdp-aplicaciones': aplicaciones,
          '06-sin-internet': sin_internet, '07-marcelo-go': marcelo_go, '08-ia-local': ia_local,
          '09-hecho-en-venezuela': hecho_en_venezuela, '10-a-la-medida': a_la_medida,
          '11-escuelas-de-vuelo': escuelas_de_vuelo, '12-ritmo-diario': ritmo_diario}

if __name__ == '__main__':
    nombres = [sys.argv[1]] if len(sys.argv) > 1 else list(VIDEOS)
    for name in nombres:
        els, dur = VIDEOS[name]()
        if len(sys.argv) > 2 and sys.argv[2] == 'previa':
            times = [float(x) for x in sys.argv[3].split(',')]
            frames = render(els, dur, None, preview_times=times)
            carpeta = os.path.join(SALIDA, 'previas'); os.makedirs(carpeta, exist_ok=True)
            sheet = Image.new('RGB', (540 * len(frames), 960))
            for i, fr in enumerate(frames):
                sheet.paste(fr.convert('RGB').resize((540, 960), Image.LANCZOS), (540 * i, 0))
            sheet.save(os.path.join(carpeta, name + '.png'))
            print(os.path.join(carpeta, name + '.png'))
        else:
            os.makedirs(SALIDA, exist_ok=True)
            print(render(els, dur, os.path.join(SALIDA, name + '.mp4')))
