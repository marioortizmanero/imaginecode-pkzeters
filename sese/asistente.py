import random

from sese.contenedor import Tarea

from google_speech import Speech


class Asistente:
    """
    Esta clase genera los mensajes aleatorios para las instrucciones
    de las tareas.
    """

    def __init__(self) -> None:
        self.interfaz_tareas = InterfazTareas()
        self.interfaz_msg_final = InterfazMsgFinal()

    def hablar(self, mensaje: str) -> None:
        """
        Usa Google Speech para hablar al usuario con una frase aleatoria.
        """

        habla = Speech(mensaje, 'es')
        habla.play()

    def hablar_msg_final(self):
        """
        Selecciona y dice un mensaje aleatorio corto para finalizar una
        tarea.
        """

        self.hablar(self.interfaz_msg_final.msg_aleatorio())

    def hablar_tarea(self, tarea: Tarea):
        """
        Usa la interfaz de tareas para escoger y decir uno de sus mensajes.
        Mensajes preestablecidos, con orden de formato:
            * 0: tarea.inicio
            * 1: tarea.final
            * 2: tarea.item.nombre
            * 3: tarea.item.cantidad
        """

        self.hablar(self.interfaz_tareas.msg_aleatorio(
            tarea.inicio, tarea.final, tarea.item.nombre,
            tarea.item.cantidad))


class Interfaz:
    """
    Una interfaz es un módulo del asistente que contiene frases
    predeterminadas de un tipo que se escogerán de forma pseudo-aleatoria.
    Los diferentes mensajes se crearán en __init__ y se accederá al
    mensaje aleatorio con msg_aleatorio(), que puede re-implementarse
    en caso de tener una generación de mensajes diferente.
    """
    def __init__(self) -> None:
        # Aquí deberían ir los mensajes usados en la interfaz.
        self.msg_iniciales = ()
        self.mensajes = ()

        # Se guarda el ultimo mensaje para que no se repita
        self.msg_anterior = ''

        # El contador para saber los mensajes ya dichos
        self.num = 0

    def msg_aleatorio(self, *format_args: any):
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


class InterfazTareas(Interfaz):
    def __init__(self) -> None:
        """
        Mensajes preestablecidos, con orden de formato:
            * 0: tarea.inicio
            * 1: tarea.final
            * 2: tarea.item.nombre
            * 3: tarea.item.cantidad
        """

        super().__init__()

        # Tiene diferentes frases dependiendo del número de mensajes ya
        # reproducidos. Unos para cuando empieza, y otros para cuando ya
        # ha dicho alguno anteriormente.
        self.msg_iniciales = (
            "Para comenzar, por favor mueva {3} {2} al pedido {1}, que"
            " podrá recoger de la caja {0}.",
            "Bienvenido... Puede empezar por mover al pedido {1} {3} {2} de"
            " la caja número {0} del almacén."
        )
        self.mensajes = (
            "LLeve desde la caja número {0} al pedido número {1} {3} {2}.",
            "Coja {3} {2} de la caja número {0} y llévela a la entrega número"
            " {1}, por favor.",
            "Por favor, mueva al pedido {1} {3} {2} de la caja número {0} del"
            " almacén.",
            "Su tarea consiste en coger {3} {2} de la caja {0} y depositarlas"
            " en la entrega número {1}.",
            "Tendrá que mover de la caja número {0} del almacén {3} {2} a"
            " la número {1} de los pedidos."
        )


class InterfazMsgFinal(Interfaz):
    def __init__(self) -> None:
        """
        Mensajes preestablecidos.
        """

        super().__init__()

        self.mensajes = (
            "Muchas gracias!",
            "Gracias",
            "Continuemos",
            "A por el siguiente...",
            "Buen trabajo"
        )