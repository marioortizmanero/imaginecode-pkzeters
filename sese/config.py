import argparse


def cargar_argumentos() -> dict:
    # Inicializacion del parser de argumentos y sus opciones
    argparser = argparse.ArgumentParser(
        prog="asistente-sese",
        description="El asistente diseñado para Sesé en la ImagineCode 2019.")

    # Creación de los argumentos del programa
    argparser.add_argument(
        "--debug",
        action="store_true", dest="debug", default=False,
        help="activa el modo debug para ver mensajes informativos")

    argparser.add_argument(
        "--pedido",
        action="store", dest="archivo_pedidos", default='pedidos.json',
        help="configura el nombre del primer archivo de pedidos a leer")

    argparser.add_argument(
        "--almacen",
        action="store", dest="archivo_almacen", default='almacen.json',
        help="configura el nombre del primer archivo de almacén a leer")

    argparser.add_argument(
        "--tareas",
        action="store", dest="archivo_tareas", default='tareas.json',
        help="configura el nombre del archivo con las tareas a escribir")

    argparser.add_argument(
        "--final",
        action="store", dest="archivo_final", default='final.json',
        help="configura el nombre del archivo con los resultados finales")

    return argparser.parse_args()
