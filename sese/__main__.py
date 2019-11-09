from sese.contenedor import Almacen, Tarea, NoHayItems


ARCHIVO_ALMACEN = 'almacen.json'
ARCHIVO_FINAL = 'final.json'
ARCHIVO_TAREAS = 'tareas.json'
ARCHIVO_PEDIDOS = 'pedidos.json'


def main():
    almacen = Almacen()
    almacen.leer(ARCHIVO_ALMACEN)

    pedidos = Almacen()
    pedidos.leer(ARCHIVO_PEDIDOS)

    tareas = []
    for pedido in pedidos:
        try:
            tareas.append(Tarea(almacen, pedido))
        except NoHayItems as e:
            print(e)

    for estanteria in almacen:
        for item in estanteria:
            print(item)
        print("---")


if __name__ == '__main__':
    main()
