import json


class Contenedor:
    def leer(self, archivo: str) -> None:
        # Guarda los datos del JSON en el objeto
        with open(archivo, 'r') as archivo:
            self.items = json.load(archivo)

        # Asignar los items de cada estanteria del contenedor
        self.estanterias = []
        for estanteria in self.items['items']:
            for nombre, cantidad in estanteria.items():
                self.estanterias.append(Item(nombre, cantidad))

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


class Tarea:
    def __init__(self):
        pass
