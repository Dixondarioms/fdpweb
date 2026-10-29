"""Calendario de publicaciones: arma la carpeta lista para programar en Meta Business Suite y TikTok Studio.

Uso (desde la carpeta del repositorio, después de generar los videos):
    python videos/generador/calendario.py

Crea videos-redes/programar/ con una carpeta por publicación (video, portada, texto para Instagram y
texto para TikTok) y calendario.html: la página con todas las publicaciones y botones para copiar los textos.
"""
import base64, io, json, os, shutil, subprocess
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


# Videos de las apps hechos aparte (ya terminados). Están en videos-redes/apps/, que no se sube a git.
GP = 'Búscala gratis en Google Play'
SALUD = 'Ritmo Diario te ayuda a organizarte; no reemplaza la indicación de tu médico.'
APOYO = 'Bloom es una app de autocuidado; si estás pasando por un momento muy difícil, busca también apoyo profesional.'

PUBLICACIONES += [
    dict(fecha='2026-11-23', dia='Lunes 23 de noviembre', archivo='MarceloGo-criollas',
         instagram=f"""Bolas criollas como en el patio 🎯

Lanza tu bola lo más cerca de la bolita: rodada, media, bombita o con curva. Gana la mano quien quede más cerca. Y si tu pana está lejos, juégalas en línea con él.

{GP}: «Marcelo Go».

#MarceloGo #BolasCriollas #JuegosVenezolanos #JuegosMoviles #FDPAplicaciones""",
         tiktok="Bolas criollas en el celular 🎯 ¿Rodada, media o bombita? Busca «Marcelo Go» en Google Play. #MarceloGo #BolasCriollas #Venezuela #JuegosMoviles #FDPAplicaciones"),

    dict(fecha='2026-11-25', dia='Miércoles 25 de noviembre', archivo='RitmoDiario-tu-dia',
         instagram=f"""Vivir con una enfermedad autoinmune ya es bastante. Tu día, a tu ritmo 💜

Con Ritmo Diario tu compañero te pregunta cómo amaneciste, ves tu salud de un vistazo y el mes en colores, con tus rachas buenas y malas. Y tu constancia se celebra.

{SALUD}
{GP}: «Ritmo Diario».

#RitmoDiario #Autoinmune #DolorCronico #Bienestar #FDPAplicaciones""",
         tiktok="Tu día, a tu ritmo 💜 Una app para quien vive con síntomas crónicos. Busca «Ritmo Diario» en Google Play. #RitmoDiario #Autoinmune #DolorCronico #Bienestar #FDPAplicaciones"),

    dict(fecha='2026-11-27', dia='Viernes 27 de noviembre', archivo='Bloom-jardin',
         instagram=f"""Cuidarte también puede florecer 🌸

En Bloom, cada día que te priorizas tu jardín crece. Ganas medallas por tu constancia, llegan compañeros a pasear por tu jardín y, con los escudos de racha, un mal día no borra tu progreso.

{GP}: «Bloom».

#Bloom #Autocuidado #BienestarEmocional #Sanacion #FDPAplicaciones""",
         tiktok="Cada día que te priorizas, tu jardín crece 🌸 Busca «Bloom» en Google Play. #Bloom #Autocuidado #BienestarEmocional #AmorPropio #FDPAplicaciones"),

    dict(fecha='2026-11-30', dia='Lunes 30 de noviembre', archivo='MarceloGo-tejo',
         instagram=f"""Jala, suelta y revienta la mecha 💥

Tejo en Marcelo Go: dale a las mechas para que revienten y, mientras más cerca del centro, más puntos. Empieza en la cancha del barrio y llega hasta la final nacional.

{GP}: «Marcelo Go».

#MarceloGo #Tejo #JuegosTradicionales #JuegosMoviles #FDPAplicaciones""",
         tiktok="¿Revientas la mecha? 💥 Tejo del barrio a la final nacional. Busca «Marcelo Go» en Google Play. #MarceloGo #Tejo #JuegosMoviles #Venezuela #FDPAplicaciones"),

    dict(fecha='2026-12-02', dia='Miércoles 2 de diciembre', archivo='RitmoDiario-medicinas',
         instagram=f"""Que no se te pase ninguna toma 💊

En Ritmo Diario anotas cada medicina con su dibujo (pastilla, cápsula, gotas o jarabe) y recibes recordatorios cada 4, 6, 8 o 12 horas, como te la mandaron. Ves tu próxima toma, el dolor, la energía y el agua en la pantalla de inicio, sin abrir la app.

{SALUD}
{GP}: «Ritmo Diario».

#RitmoDiario #Medicamentos #Recordatorios #Salud #FDPAplicaciones""",
         tiktok="Que no se te pase ninguna toma 💊 Recordatorios cada 4, 6, 8 o 12 horas. Busca «Ritmo Diario» en Google Play. #RitmoDiario #Salud #Medicamentos #Bienestar #FDPAplicaciones"),

    dict(fecha='2026-12-04', dia='Viernes 4 de diciembre', archivo='Bloom-ansiedad',
         instagram=f"""La ansiedad no avisa. Bloom te acompaña 🌙

Aprende a bajarle el volumen a la ansiedad. Si llega un ataque de pánico, Bloom te guía paso a paso hasta que pase, con el método 5-4-3-2-1 para volver al presente. Y el botón SOS siempre está a un toque.

{APOYO}
{GP}: «Bloom».

#Bloom #Ansiedad #SaludMental #Respiracion #FDPAplicaciones""",
         tiktok="La ansiedad no avisa. Bloom te acompaña 🌙 Guía paso a paso y botón SOS. Busca «Bloom» en Google Play. #Bloom #Ansiedad #SaludMental #Calma #FDPAplicaciones"),

    dict(fecha='2026-12-07', dia='Lunes 7 de diciembre', archivo='MarceloGo-mahjong',
         instagram=f"""Fichas grandes. Junta las parejas 🀄

Mahjong en Marcelo Go: encuentra las parejas libres antes de que se acabe el tiempo, con pista, deshacer y revolver cuando lo necesites. Cada mundo sube el reto nivel a nivel.

{GP}: «Marcelo Go».

#MarceloGo #Mahjong #JuegosDeMesa #JuegosMoviles #FDPAplicaciones""",
         tiktok="Mahjong con fichas grandes y claras 🀄 Busca «Marcelo Go» en Google Play. #MarceloGo #Mahjong #JuegosMoviles #Puzzle #FDPAplicaciones"),

    dict(fecha='2026-12-09', dia='Miércoles 9 de diciembre', archivo='RitmoDiario-brote-v2',
         instagram=f"""Descubre qué te afecta 🔍

Ritmo Diario tiene un botón grande para los días difíciles. Cuando tienes un brote, ves cómo dormiste y qué sentiste los días previos. Registras dolor, fatiga y sueño en segundos, y cada día registrado suma a tu historia.

{SALUD}
{GP}: «Ritmo Diario».

#RitmoDiario #DolorCronico #Fatiga #Autoinmune #FDPAplicaciones""",
         tiktok="¿Qué pasó antes de tu brote? 🔍 Descúbrelo con Ritmo Diario, gratis en Google Play. #RitmoDiario #DolorCronico #Autoinmune #Salud #FDPAplicaciones"),

    dict(fecha='2026-12-11', dia='Viernes 11 de diciembre', archivo='Bloom-circulo-v2',
         instagram=f"""Hay gente que entiende lo que sientes 🤍

En el Círculo Bloom recibes cartas de ánimo de personas como tú, haces retos juntas, cada una a su ritmo, y te desahogas en el muro sin decir tu nombre. Las charlas son seguras: tú decides con quién.

{GP}: «Bloom».

#Bloom #BienestarEmocional #Comunidad #Sanacion #FDPAplicaciones""",
         tiktok="No estás sola 🤍 Cartas de ánimo, retos juntas y un muro anónimo. Busca «Bloom» en Google Play. #Bloom #BienestarEmocional #Sanacion #Comunidad #FDPAplicaciones"),

    dict(fecha='2026-12-14', dia='Lunes 14 de diciembre', archivo='RitmoDiario-ejercicio-v2',
         instagram=f"""Diez minutos para ti 🧘

En Ritmo Diario eliges tu objetivo y los minutos que tienes, y una silueta te enseña cada movimiento. Hay seis meditaciones con voz, de 3 a 12 minutos, y respiración guiada para los días pesados.

{SALUD}
{GP}: «Ritmo Diario».

#RitmoDiario #EjercicioSuave #Meditacion #Bienestar #FDPAplicaciones""",
         tiktok="Diez minutos para ti 🧘 Ejercicio suave, meditación y respiración guiada. Busca «Ritmo Diario» en Google Play. #RitmoDiario #Meditacion #Bienestar #Ejercicio #FDPAplicaciones"),

    dict(fecha='2026-12-16', dia='Miércoles 16 de diciembre', archivo='Bloom-juego-v2',
         instagram=f"""Relájate jugando 🪷

Jardín de calma es un juego tranquilo de Bloom para despejar la mente: toca las flores antes de que se cierren. Con tu constancia juntas compañeros, y luego los ves pasear por tu jardín.

{GP}: «Bloom».

#Bloom #JuegoRelajante #Calma #Autocuidado #FDPAplicaciones""",
         tiktok="Un juego tranquilo para despejar la mente 🪷 Busca «Bloom» en Google Play. #Bloom #Relajacion #Calma #Autocuidado #FDPAplicaciones"),

    dict(fecha='2026-12-18', dia='Viernes 18 de diciembre', archivo='RitmoDiario-ambientes-v2',
         instagram=f"""Que tu app se sienta como tú 🎄

En Ritmo Diario cambias el fondo según tu ánimo y eliges un ambiente calmado para cada día. También hay temporadas: Navidad, primavera, Halloween… Y celebras tu racha con una tarjeta bonita para compartir.

{GP}: «Ritmo Diario».

#RitmoDiario #Navidad #Bienestar #Autocuidado #FDPAplicaciones""",
         tiktok="Tu app, a tu estilo 🎄 Fondos por ánimo y temporadas, como Navidad. Busca «Ritmo Diario» en Google Play. #RitmoDiario #Navidad #Bienestar #Apps #FDPAplicaciones"),

    dict(fecha='2026-12-21', dia='Lunes 21 de diciembre', archivo='Bloom-miedos-v2',
         instagram=f"""Un día a la vez 🌱

Para superar un miedo, Bloom arma contigo una escalera de pasos pequeños, a tu ritmo, con una meditación de valentía antes de cada escalón. Cuando todo da vueltas, te ayuda a volver al presente. Y el botón SOS está siempre a un toque.

{APOYO}
{GP}: «Bloom».

#Bloom #SuperarMiedos #SaludMental #Autocuidado #FDPAplicaciones""",
         tiktok="Un día a la vez 🌱 Supera tus miedos con pasos pequeños. Busca «Bloom» en Google Play. #Bloom #SaludMental #Valentia #Autocuidado #FDPAplicaciones"),
]


def portada_archivo(video, destino):
    """Portada de un video ya terminado: el cuadro del segundo 1.2, con la frase de gancho completa."""
    tmp = destino + '.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1.2', '-i', video, '-frames:v', '1', tmp], check=True)
    cuadro = Image.open(tmp).convert('RGB')
    limpio = Image.new('RGB', cuadro.size)   # lienzo nuevo: sin metadatos
    limpio.paste(cuadro)
    limpio.save(destino, quality=94)
    os.remove(tmp)


def duracion_archivo(video):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def copia_liviana(video, destino):
    """Chrome sube como máximo 10 MB por archivo: copia más liviana, con la misma resolución."""
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-c:v', 'libx264', '-preset', 'slow', '-crf', '21',
                    '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', destino], check=True)


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
        if 'archivo' in p:   # video de una app, ya terminado
            p = dict(p, video=p['archivo'])
            origen = os.path.join(SALIDA, 'apps', p['archivo'] + '.mp4')
            if not os.path.exists(origen):
                raise SystemExit('Falta el video %s en videos-redes/apps/' % p['archivo'])
            destino = os.path.join(carpeta, p['video'] + '.mp4')
            shutil.copy2(origen, destino)
            if os.path.getsize(destino) > 9.8 * 1024 * 1024:
                copia_liviana(destino, os.path.join(carpeta, p['video'] + '-liviano.mp4'))
            portada_archivo(destino, os.path.join(carpeta, 'portada.jpg'))
            dur = duracion_archivo(destino)
        else:
            origen = os.path.join(SALIDA, p['video'] + '.mp4')
            if not os.path.exists(origen):
                raise SystemExit('Falta el video %s: genéralo primero con videos.py' % p['video'])
            shutil.copy2(origen, os.path.join(carpeta, p['video'] + '.mp4'))
            portada(p['video'], os.path.join(carpeta, 'portada.jpg'))
            _, dur = VIDEOS[p['video']]()
        for red in ('instagram', 'tiktok'):
            with open(os.path.join(carpeta, 'texto-%s.txt' % red), 'w', encoding='utf-8') as f:
                f.write(p[red] + '\n')
        datos.append(dict(p, numero=i, hora=HORA, carpeta=os.path.basename(carpeta), duracion=round(dur),
                          miniatura=miniatura(os.path.join(carpeta, 'portada.jpg'))))
        print('listo', carpeta)
    # página del calendario: la plantilla calendario.html con los datos dentro
    plantilla = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calendario.html'), encoding='utf-8').read()
    js = json.dumps(datos, ensure_ascii=False).replace('</', '<\\/')
    with open(os.path.join(raiz, 'calendario.html'), 'w', encoding='utf-8') as f:
        f.write(plantilla.replace('/*DATOS*/', js))
    print('listo', os.path.join(raiz, 'calendario.html'))
