from typing import Tuple
import json


class Almacen:
    def leer(self, archivo: str) -> None:
        # Guarda los datos del JSON en el objeto
        with open(archivo, 'r') as archivo:
            self.items = json.load(archivo)

        # Asignar los items de cada estanteria del contenedor
        self.estanterias = []
        for estanteria in self.items['items']:
            items = []
            for nombre, cantidad in estanteria.items():
                items.append(Item(nombre, cantidad))
            self.estanterias.append(items)

    def __iter__(self):
        # Para iterar cada estanteria del contenedor
        for estanteria in self.estanterias:
            yield estanteria


class Item:
    def __init__(self, nombre: str, cantidad: int) -> None:
        self.nombre = nombre
        self.cantidad = cantidad

    def __str__(self) -> str:
        return f'{self.nombre}: {self.cantidad}'


class NoHayItems(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(self, msg)


class Tarea:
    def __init__(self, almacen: Almacen, pedido: Tuple[Item]):
        if not self.se_puede(almacen, pedido):
            raise NoHayItems('No se puede hacer el pedido: {pedido}')

        # Itera cada item del pedido
        for item_pedido in pedido:
            # Los busca en todos los items del almacén
            for estanteria in almacen:
                for item_disponible in estanteria:
                    # Se mueven los items del almacén requeridos a los del
                    # pedido.
                    if item_disponible.nombre == item.nombre:


    def se_puede(self, almacen: Almacen, pedido: Tuple[Item]):
        for item in pedido:
            contador = 0
            for estanteria in almacen:
                for item_disponible in estanteria:
                    if item_disponible.nombre == item.nombre:
                        contador += item_disponible.cantidad
            if contador < item.cantidad:
                return False

        return True
