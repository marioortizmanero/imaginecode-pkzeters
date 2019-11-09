import logging

from sese.contenedor import Almacen, ArchivoTareas, NoHayItems
from sese.asistente import Asistente
from sese.config import cargar_argumentos


def main():
    # Carga de los argumentos pasados por el usuario con configuración
    args = cargar_argumentos()

    # Inicializa el logger
    nivel_logger = logging.INFO if args.debug else logging.ERROR
    logging.basicConfig(level=nivel_logger,
                        format="[%(asctime)s.%(msecs)03d] %(levelname)s:"
                        " %(message)s", datefmt="%H:%M:%S")

    # Genera los contenidos del almacén a partir del JSON
    almacen = Almacen()
    almacen.leer(args.archivo_almacen)

    # Genera los pedidos a partir del archivo JSON
    pedidos = Almacen()
    pedidos.leer(args.archivo_pedidos)
    tareas = ArchivoTareas()

    # Genera las tareas usando el almacén y los pedidos
    logging.info("Generando tareas a partir de los datos del almacén"
                 " y de los pedidos.")
    for i_pedido, pedido in enumerate(pedidos):
        try:
            tareas.generar_tareas(almacen, pedido, i_pedido)
        except NoHayItems as e:
            logging.info(str(e))

    tareas.escribir(args.archivo_tareas)

    # Hablar al usuario con las instrucciones, donde la conversación típica
    # sigue el siguiente esquema:
    #     * La asistente dice la tarea que el usuario tiene que llevar a cabo
    #     * Se escuchan diferentes eventos:
    #          - El usuario pide que se repita la frase
    #          - El usuario indica que ya lo ha completado
    #     * Una frase corta al final se reproduce
    logging.info("Iniciando el asistente de voz y procesando las tareas"
                 " una a una.")
    asistente = Asistente()
    for tarea in tareas:
        asistente.hablar_tarea(tarea)
        asistente.escuchar(tarea)
        asistente.hablar_basico(asistente.interfaz_final)


if __name__ == '__main__':
    main()
