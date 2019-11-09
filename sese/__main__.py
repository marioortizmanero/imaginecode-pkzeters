from sese.contenedor import Contenedor


ARCHIVO_ALMACEN = 'almacen.json'
ARCHIVO_FINAL = 'final.json'
ARCHIVO_TAREAS = 'tareas.json'


def main():
    contenedor = Contenedor()
    contenedor.leer(ARCHIVO_ALMACEN)
    for item in contenedor:
        print(item)


if __name__ == '__main__':
    main()
