"""Calendario de publicaciones: arma la carpeta lista para programar en Meta Business Suite y TikTok Studio.

Uso (desde la carpeta del repositorio, después de generar los videos):
    python videos/generador/calendario.py

Crea videos-redes/programar/ con una carpeta por publicación (video, portada, texto para Instagram y
texto para TikTok) y calendario.html: la página con todas las publicaciones y botones para copiar los textos.
"""
import base64, io, json, os, shutil
from PIL import Image
from engine import SALIDA, render
from videos import VIDEOS

HORA = '6:30 p. m.'   # hora de Venezuela

WA = '📲 Escríbenos por WhatsApp: +58 412-0846332'

PUBLICACIONES = [
    dict(fecha='2026-10-26', dia='Lunes 26 de octubre', video='01-fdp-software',
         instagram=f"""Todo lo que tu operación necesita, hecho en Venezuela 🇻🇪

En FDP Software desarrollamos sistemas de gestión con IA local, simuladores de entrenamiento y apps móviles. Software seguro, pensado para trabajar sin depender de internet.

{WA}
🌐 fdpsoftware.org (enlace en el perfil)

#FDPSoftware #SoftwareVenezolano #HechoEnVenezuela #Tecnologia #Venezuela""",
         tiktok="Software, simuladores y apps hechos en Venezuela 🇻🇪 Escríbenos para una demostración. #FDPSoftware #HechoEnVenezuela #Software #Tecnologia #Venezuela"),

    dict(fecha='2026-10-28', dia='Miércoles 28 de octubre', video='02-sigma-mro',
         instagram=f"""Mantenimiento aeronáutico, bajo control ✈️

SIGMA MRO lleva tu flota, componentes y límites por horas, ciclos o calendario; las órdenes de trabajo con firma e inspección; el inventario y las directivas AD/SB. Y tiene un asistente con IA local que consulta tus manuales, también por voz.

Escritorio y app móvil por tu red local, 100 % sin nube.

{WA}

#SIGMAMRO #MantenimientoAeronautico #Aviacion #MRO #FDPSoftware""",
         tiktok="Tu flota al día con SIGMA MRO ✈️ Mantenimiento aeronáutico con IA local y sin nube. #Aviacion #MantenimientoAeronautico #MRO #SoftwareVenezolano #FDPSoftware"),

    dict(fecha='2026-10-30', dia='Viernes 30 de octubre', video='05-fdp-aplicaciones',
         instagram="""Juegos y apps hechos en Venezuela para el mundo 🎮📱

• Marcelo Go: burbujas con poderes especiales y retos por niveles.
• Minijuegos de Marcelo Go: billar, carrom, ludo y más, en una sola app.
• Ritmo Diario: tu diario de salud, con gráficas de tu evolución.

Búscalas en Google Play.

#FDPAplicaciones #MarceloGo #JuegosMoviles #AppsVenezolanas #GooglePlay""",
         tiktok="Juegos y apps hechos en Venezuela 🎮 Búscalas en Google Play. #MarceloGo #JuegosMoviles #Android #HechoEnVenezuela #FDPAplicaciones"),

    dict(fecha='2026-11-02', dia='Lunes 2 de noviembre', video='03-aeroescuela',
         instagram=f"""Formar un piloto cuesta caro. Cada hora de vuelo cuenta ✈️

AeroEscuela lleva el entrenamiento a tu escuela en una computadora común: física validada contra el manual del fabricante, instructor virtual, meteorología, aeropuertos reales de Venezuela y una evaluación con informe para el alumno y el instructor.

{WA}

#AeroEscuela #SimuladorDeVuelo #EscuelaDeVuelo #Aviacion #FDPSimuladores""",
         tiktok="Entrena vuelo en una computadora común con AeroEscuela ✈️ #SimuladorDeVuelo #Aviacion #Piloto #EscuelaDeVuelo #FDPSimuladores"),

    dict(fecha='2026-11-04', dia='Miércoles 4 de noviembre', video='06-sin-internet',
         instagram=f"""¿Tu sistema se cae cuando se va el internet? 🔌

Nuestro software está pensado para no depender de internet. SIGMA MRO, por ejemplo, funciona con escritorio y app móvil por tu propia red, 100 % sin nube. Tus datos, bajo tu control.

{WA}

#SinInternet #IndependenciaTecnologica #SoftwareVenezolano #FDPSoftware #Venezuela""",
         tiktok="Software que no depende de internet 🔌 Tus datos, bajo tu control. #SinInternet #Software #Venezuela #Tecnologia #FDPSoftware"),

    dict(fecha='2026-11-06', dia='Viernes 6 de noviembre', video='07-marcelo-go',
         instagram="""¿Listo para explotar burbujas? 🫧🚀

Marcelo Go tiene poderes especiales (varita, cohete, martillo, bomba y rayo), retos por niveles y premios al avanzar. Pensado para toda la familia.

Búscalo en Google Play: «Marcelo Go».

#MarceloGo #JuegosMoviles #JuegosEnFamilia #GooglePlay #FDPAplicaciones""",
         tiktok="¿Cuántos niveles pasas? 🫧 Busca «Marcelo Go» en Google Play. #MarceloGo #JuegosMoviles #Juegos #Android #FDPAplicaciones"),

    dict(fecha='2026-11-09', dia='Lunes 9 de noviembre', video='04-escenarios-3d',
         instagram=f"""Caracas, en 3D 🏙️

Un proceso automatizado convierte datos abiertos (OpenStreetMap, relieve satelital e imágenes Sentinel-2) en escenarios realistas en Unreal Engine 5, para recorrer a pie, en vehículo y en vuelo.

{WA}

#Caracas #UnrealEngine5 #3D #OpenStreetMap #FDPSoftware""",
         tiktok="Caracas recreada en 3D con datos reales 🏙️ #Caracas #UnrealEngine5 #3D #Venezuela #FDPSoftware"),

    dict(fecha='2026-11-11', dia='Miércoles 11 de noviembre', video='08-ia-local',
         instagram=f"""IA que trabaja sin enviar tus datos a la nube 🤖🔒

Instalamos asistentes de IA sobre tus propios documentos: consultan tus manuales técnicos, también por voz, y tus datos se quedan contigo.

{WA}

#InteligenciaArtificial #IALocal #Privacidad #SoftwareVenezolano #FDPSoftware""",
         tiktok="IA local: tus datos no salen a la nube 🤖🔒 #InteligenciaArtificial #IA #Privacidad #Tecnologia #FDPSoftware"),

    dict(fecha='2026-11-13', dia='Viernes 13 de noviembre', video='09-hecho-en-venezuela',
         instagram="""Hecho en Venezuela, para el mundo 🇻🇪

Caracas en 3D con datos reales, un simulador de vuelo con aeropuertos venezolanos y juegos en Google Play. Todo desarrollado aquí.

🌐 fdpsoftware.org (enlace en el perfil)

#HechoEnVenezuela #TalentoVenezolano #SoftwareVenezolano #Venezuela #FDPSoftware""",
         tiktok="Tecnología hecha en Venezuela 🇻🇪 #HechoEnVenezuela #Venezuela #TalentoVenezolano #Tecnologia #FDPSoftware"),

    dict(fecha='2026-11-16', dia='Lunes 16 de noviembre', video='10-a-la-medida',
         instagram=f"""¿Necesitas un sistema a tu medida? 🛠️

01 Diseñamos: analizamos tus procesos y definimos alcance, tiempos y costo.
02 Desarrollamos: por etapas, con pruebas y documentación en cada entrega.
03 Acompañamos: instalamos en tu sitio, capacitamos a tu equipo y damos soporte.

Web, móvil, IA y sistemas embebidos.
{WA}

#SoftwareAMedida #DesarrolloWeb #AppsMoviles #Empresas #FDPSoftware""",
         tiktok="Así creamos tu sistema a la medida 🛠️ #SoftwareAMedida #DesarrolloDeSoftware #Programacion #Empresas #FDPSoftware"),

    dict(fecha='2026-11-18', dia='Miércoles 18 de noviembre', video='11-escuelas-de-vuelo',
         instagram=f"""Para escuelas de vuelo y talleres aeronáuticos ✈️

SIGMA MRO mantiene tu flota al día, con límites por horas, ciclos o calendario. AeroEscuela entrena a tus alumnos en una computadora común y entrega las gráficas del vuelo y un informe para el alumno y el instructor.

{WA}

#EscuelaDeVuelo #Aviacion #MantenimientoAeronautico #Pilotos #FDPSoftware""",
         tiktok="Dos herramientas para escuelas de vuelo ✈️ #EscuelaDeVuelo #Aviacion #Piloto #MRO #FDPSoftware"),

    dict(fecha='2026-11-20', dia='Viernes 20 de noviembre', video='12-ritmo-diario',
         instagram="""¿Cómo te sientes hoy? 💙

Con Ritmo Diario registras dolor, energía, sueño y vasos de agua, anotas tus tratamientos y miras tu evolución en gráficas.

Búscalo en Google Play: «Ritmo Diario».

#RitmoDiario #Salud #Bienestar #AppsVenezolanas #FDPAplicaciones""",
         tiktok="Tu diario de salud en el celular 💙 Busca «Ritmo Diario» en Google Play. #RitmoDiario #Salud #Bienestar #Apps #FDPAplicaciones"),
]


def portada(nombre, destino):
    """Portada 1080x1920: el cuadro del video con la frase de gancho completa (antes de que salga)."""
    els, dur = VIDEOS[nombre]()
    cuadro = render(els, dur, None, preview_times=[1.5])[0].convert('RGB')
    limpio = Image.new('RGB', cuadro.size)   # lienzo nuevo: sin metadatos
    limpio.paste(cuadro)
    limpio.save(destino, quality=94)


def miniatura(portada_jpg):
    """Portada pequeña (180x320) incrustada en la página del calendario."""
    im = Image.open(portada_jpg).convert('RGB').resize((180, 320), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


if __name__ == '__main__':
    raiz = os.path.join(SALIDA, 'programar')
    os.makedirs(raiz, exist_ok=True)
    datos = []
    for i, p in enumerate(PUBLICACIONES, 1):
        carpeta = os.path.join(raiz, '%02d-%s' % (i, p['fecha']))
        os.makedirs(carpeta, exist_ok=True)
        origen = os.path.join(SALIDA, p['video'] + '.mp4')
        if not os.path.exists(origen):
            raise SystemExit('Falta el video %s: genéralo primero con videos.py' % p['video'])
        shutil.copy2(origen, os.path.join(carpeta, p['video'] + '.mp4'))
        portada(p['video'], os.path.join(carpeta, 'portada.jpg'))
        for red in ('instagram', 'tiktok'):
            with open(os.path.join(carpeta, 'texto-%s.txt' % red), 'w', encoding='utf-8') as f:
                f.write(p[red] + '\n')
        _, dur = VIDEOS[p['video']]()
        datos.append(dict(p, numero=i, hora=HORA, carpeta=os.path.basename(carpeta), duracion=round(dur),
                          miniatura=miniatura(os.path.join(carpeta, 'portada.jpg'))))
        print('listo', carpeta)
    # página del calendario: la plantilla calendario.html con los datos dentro
    plantilla = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calendario.html'), encoding='utf-8').read()
    js = json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')
    with open(os.path.join(raiz, 'calendario.html'), 'w', encoding='utf-8') as f:
        f.write(plantilla.replace('/*DATOS*/', js))
    print('listo', os.path.join(raiz, 'calendario.html'))
