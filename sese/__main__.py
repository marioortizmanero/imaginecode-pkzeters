from sese.contenedor import Almacen, ArchivoTareas, NoHayItems
from sese.asistente import Asistente


ARCHIVO_ALMACEN = 'almacen.json'
ARCHIVO_FINAL = 'final.json'
ARCHIVO_TAREAS = 'tareas.json'
ARCHIVO_PEDIDOS = 'pedidos.json'


def main():
    # Genera los contenidos del almacén a partir del JSON
    almacen = Almacen()
    almacen.leer(ARCHIVO_ALMACEN)

    # Genera los pedidos a partir del archivo JSON
    pedidos = Almacen()
    pedidos.leer(ARCHIVO_PEDIDOS)
    tareas = ArchivoTareas()

    # Genera las tareas usando el almacén y los pedidos
    for i_pedido, pedido in enumerate(pedidos):
        try:
            tareas.generar_tareas(almacen, pedido, i_pedido)
        except NoHayItems as e:
            print(e)

    tareas.escribir(ARCHIVO_TAREAS)

    # Hablar al usuario con las instrucciones, donde la conversación típica
    # sigue el siguiente esquema:
    #     * La asistente dice la tarea que el usuario tiene que llevar a cabo
    #     * Se escuchan diferentes eventos:
    #          - El usuario pide que se repita la frase
    #          - El usuario indica que ya lo ha completado
    #     * Una frase corta al final se reproduce
    asistente = Asistente()
    for tarea in tareas:
        asistente.hablar_tarea(tarea)
        asistente.escuchar()
        asistente.hablar_msg_final()


if __name__ == '__main__':
    main()
