import random
import logging
from typing import Tuple

from jotason.contenedor import Tarea

# Reconocimiento de voz
import speech_recognition as sr
# Sintetizador de voz
from google_speech import Speech


class Interfaz:
    """
    Una interfaz es un módulo del asistente que contiene frases
    predeterminadas de un tipo que se escogerán de forma pseudo-aleatoria.
    Los diferentes mensajes se crearán en __init__ y se accederá al
    mensaje aleatorio con msg_aleatorio(), que puede re-implementarse
    en caso de tener una generación de mensajes diferente.

    Los mensajes se leerán de un archivo pasado por parámetro, siendo los
    iniciales opcionales.
    """
    def __init__(self, archivo_mensajes: str,
                 archivo_iniciales: str = None) -> None:
        # Aquí deberían ir los mensajes usados en la interfaz.
        self.mensajes = self.leer_mensajes(archivo_mensajes)
        if archivo_iniciales is not None:
            self.msg_iniciales = self.leer_mensajes(archivo_iniciales)
        else:
            self.msg_iniciales = []

        # Se guarda el ultimo mensaje para que no se repita
        self.msg_anterior = ''

        # El contador para saber los mensajes ya dichos
        self.num = 0

    def leer_mensajes(self, archivo: str) -> Tuple[str]:
        """
        Leer los mensajes de un archivo especial para almacenarlos.
        Tienen una sintaxis simple: cada mensaje es una línea nueva.
        El archivo sólo tiene su nombre dentro de jotason/dialogos/.
        """

        with open(f"jotason/dialogos/{archivo}", 'r') as f:
            mensajes = f.readlines()
        # Elimina espacios extra y los saltos de línea
        mensajes = [x.strip().rstrip('\n') for x in mensajes]

        return mensajes

    def msg_aleatorio(self, *format_args: any) -> str:
        """
        Genera un texto aleatorio de forma que no se repita el mismo
        dos veces seguidas. Muestra un mensaje distinto cuando es el primero.
        """

        if self.num == 0 and len(self.msg_iniciales) > 0:
            self.msg_anterior = random.choice(self.msg_iniciales)
        else:
            self.msg_anterior = random.choice([m for m in self.mensajes
                                               if m != self.msg_anterior])
        self.num += 1
        return self.msg_anterior if len(format_args) == 0 \
            else self.msg_anterior.format(*format_args)


class Asistente:
    """
    Esta clase genera los mensajes aleatorios para las instrucciones
    de las tareas.
    """

    def __init__(self) -> None:
        # Inicializacion de las interfaces de voz del asistente
        self.interfaz_tareas = Interfaz(
            'tareas_mensajes.txt', archivo_iniciales='tareas_iniciales.txt')
        self.interfaz_final = Interfaz('final.txt')
        self.interfaz_repetir = Interfaz('repetir.txt')

        # Keywords para acciones especiales. Este tipo de datos tendrían que
        # situarse en archivos fuera del programa por comodidad, pero para
        # su uso limitado actual no es necesario.
        self.keys_repite = ('repite', 'repetido', 'otra', 'qué?', 'repetir',
                            'repítelo', 'repítemelo')
        self.keys_siguiente = ('avanzar', 'terminado', 'hecho', 'acabado',
                               'ya', 'está', 'finalizado', 'acabé', 'acaba',
                               'terminé', 'finalicé', 'continuar', 'seguir',
                               'sigamos', 'continuemos', 'continúa',
                               'proseguir', 'prosigamos', 'vale', 'okay',
                               'ok', 'sigue')

        # Inicializacion del reconocimiento de voz
        self.recognizer = sr.Recognizer()

    def hablar(self, mensaje: str) -> None:
        """
        Usa Google Speech para hablar al usuario con una frase aleatoria.
        """

        habla = Speech(mensaje, 'es')
        habla.play()

    def buscar_keyword(self, reconocido: str, keywords: Tuple[str]) -> bool:
        """
        Comprueba si un keyword está en el texto ofrecido por el recognizer.
        """

        for palabra in reconocido.split():
            for keyword in keywords:
                if palabra == keyword:
                    return True

        return False

    def escuchar(self, tarea: Tarea) -> None:
        """
        Loop que espera a recibir una de las keywords para actual acorde a
        ella.
        """

        logging.info("Se ha iniciado el bucle de una tarea.")
        while True:
            with sr.Microphone() as fuente:
                audio = self.recognizer.listen(fuente)

            try:
                recognized = self.recognizer.recognize_google(
                    audio, language='es-ES')
                logging.info(f"Audio reconocido: {recognized}")
                if self.buscar_keyword(recognized, self.keys_repite):
                    # Repite la tarea y continúa el bucle esperando
                    logging.info("Repitiendo la tarea")
                    self.hablar_basico(self.interfaz_repetir)
                    self.hablar_tarea(tarea)
                elif self.buscar_keyword(recognized, self.keys_siguiente):
                    logging.info("Fin de la tarea")
                    # Si ya ha acabado se termina la función directamente
                    return
            except sr.UnknownValueError:
                logging.info("No se pudo entender el audio")
            except sr.RequestError as e:
                logging.info(f"No se pudieron obtener resultados: {e}")

    def hablar_basico(self, interfaz: Interfaz) -> None:
        """
        Selecciona y dice un mensaje aleatorio corto a partir de una interfaz
        sin formato necesario.
        """

        self.hablar(interfaz.msg_aleatorio())

    def hablar_tarea(self, tarea: Tarea) -> None:
        """
        Usa la interfaz de tareas para escoger y decir uno de sus mensajes.
        Mensajes preestablecidos, con orden de formato:
            * 0: tarea.inicio
            * 1: tarea.final
            * 2: tarea.item.nombre
            * 3: tarea.item.cantidad
        """

        self.hablar(self.interfaz_tareas.msg_aleatorio(
            tarea.inicio + 1, tarea.final + 1, tarea.item.nombre,
            tarea.item.cantidad))