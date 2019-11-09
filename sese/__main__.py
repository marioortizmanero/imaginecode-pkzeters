from sese.contenedor import Almacen, ArchivoTareas, NoHayItems


ARCHIVO_ALMACEN = 'almacen.json'
ARCHIVO_FINAL = 'final.json'
ARCHIVO_TAREAS = 'tareas.json'
ARCHIVO_PEDIDOS = 'pedidos.json'


def main():
    almacen = Almacen()
    almacen.leer(ARCHIVO_ALMACEN)

    pedidos = Almacen()
    pedidos.leer(ARCHIVO_PEDIDOS)
    tareas = ArchivoTareas()

    for i_pedido, pedido in enumerate(pedidos):
        try:
            tareas.generar_tareas(almacen, pedido, i_pedido)
        except NoHayItems as e:
            print(e)

    #tareas.escribir(ARCHIVO_TAREAS)


if __name__ == '__main__':
    main()
