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


VIDEOS = {'01-fdp-software': marca, '02-sigma-mro': sigma, '03-aeroescuela': aeroescuela,
          '04-escenarios-3d': escenarios, '05-fdp-aplicaciones': aplicaciones}

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
