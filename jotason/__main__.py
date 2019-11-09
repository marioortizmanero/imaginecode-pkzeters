import os
import sys
from contextlib import contextmanager
from typing import Tuple
import logging

from jotason.contenedor import Almacen, ArchivoTareas, NoHayItems
from jotason.asistente import Asistente
from jotason.config import cargar_argumentos


def loop_asistente(config: dict):
    # Inicializa el logger
    nivel_logger = logging.INFO if config.debug else logging.ERROR
    logging.basicConfig(level=nivel_logger,
                        format="[%(asctime)s.%(msecs)03d] %(levelname)s:"
                        " %(message)s", datefmt="%H:%M:%S")

    # Inicializacion de los módulos usados en el bucle
    almacen = Almacen()
    pedidos = Almacen()
    tareas = ArchivoTareas()
    # El asistente comenzará con un mensaje introductorio
    asistente = Asistente()
    asistente.hablar(asistente.interfaz_intro)

    while True:
        # Genera los contenidos del almacén a partir del JSON
        almacen.leer(config.archivo_almacen)

        # Genera los pedidos a partir del archivo JSON
        pedidos.leer(config.archivo_pedidos)

        # Genera las tareas usando el almacén y los pedidos
        logging.info("Generando tareas a partir de los datos del almacén y de"
                     " los pedidos.")
        for i_pedido, pedido in enumerate(pedidos):
            try:
                tareas.generar_tareas(almacen, pedido, i_pedido)
            except NoHayItems as e:
                print(e)

        tareas.escribir(config.archivo_tareas)

        # Hablar al usuario con las instrucciones, donde la conversación típica
        # sigue el siguiente esquema:
        #     * La asistente dice la tarea que el usuario tiene que llevar
        #       a cabo.
        #     * Se escuchan diferentes eventos:
        #          - El usuario pide que se repita la frase
        #          - El usuario indica que ya lo ha completado
        #     * Una frase corta al final se reproduce
        logging.info("Iniciando el asistente de voz y procesando las tareas"
                     " una a una.")
        for tarea in tareas:
            asistente.hablar_tarea(tarea)
            asistente.escuchar(tarea)
            asistente.hablar(asistente.interfaz_final)

        # Se guarda el almacén en el archivo final
        almacen.escribir(config.archivo_final)
        # El asistente pide los archivos nuevos para continuar el programa
        asistente.hablar(asistente.interfaz_pedir_archivos)
        try:
            print("Introduzca un archivo de almacén: ", end='')
            archivo_almacen = input()
            print("Introduzca un archivo de pedidos: ", end='')
            archivo_pedidos = input()
        except KeyboardInterrupt:
            asistente.hablar(asistente.interfaz_despedir)
            print()
            break

        if archivo_almacen not in (None, ''):
            config.archivo_almacen = archivo_almacen
        else:
            config.archivo_almacen = config.archivo_final

        if archivo_pedidos not in (None, ''):
            config.archivo_almacen = archivo_almacen
        else:
            print("No se especificó un archivo de pedidos nuevo.")
            asistente.hablar(asistente.interfaz_despedir)
            break


@contextmanager
def stderr_redirected(to: str = os.devnull) -> None:
    """
    Redireccionar el stderr a /dev/null sin leaks. Esto se usa porque ALSA
    puede enviar mensajes de error aún cuando no son de nivel crítico.
    """

    fd = sys.stderr.fileno()

    def _redirect_stderr(to: str) -> None:
        sys.stderr.close()  # + implicit flush()
        os.dup2(to.fileno(), fd)  # fd writes to 'to' file
        sys.stderr = os.fdopen(fd, 'w')  # Python writes to fd

    with os.fdopen(os.dup(fd), 'w') as old_stderr:
        with open(to, 'w') as file:
            _redirect_stderr(to=file)
        try:
            # Allow code to be run with the redirected stderr
            yield
        finally:
            # Restore stderr. Some flags may change
            _redirect_stderr(to=old_stderr)


def main():
    # Carga de los argumentos pasados por el usuario con configuración
    args = cargar_argumentos()
    # Si no se ha escogido el modo debug, no se muestra stderr
    if not args.debug:
        with stderr_redirected():
            loop_asistente(args)
    else:
        loop_asistente(args)


if __name__ == '__main__':
    main()
