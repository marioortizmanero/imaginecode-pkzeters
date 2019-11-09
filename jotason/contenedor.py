from typing import Tuple
import json


class NoHayItems(Exception):
    """
    Excepción usada para indicar que el almacén no tiene los suficientes
    items para completar un pedido.
    """

    def __init__(self, *args) -> None:
        super().__init__(*args)


class Item:
    def __init__(self, nombre: str, cantidad: int) -> None:
        self.nombre = nombre
        self.cantidad = cantidad

    def __str__(self) -> str:
        return f'{self.nombre}: {self.cantidad}'


class Almacen:
    """
    Representa un conjunto de estanterías o pedidos.
    """
    def escribir(self, archivo_final_almacen)->None:
        formato = dict()
        formato['almacen'] = []
        for estanteria in self.estanterias:
            for item in estanteria:
                if item.cantidad > 0:
                    formato['almacen'].append({item.nombre: item.cantidad})
        with open(archivo_final_almacen, 'w') as archivo_almacen:
            json.dump(formato, archivo_almacen)

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

    def __iter__(self) -> Tuple[Tuple[Item]]:
        # Para iterar cada estanteria del contenedor
        for estanteria in self.estanterias:
            yield estanteria

    def __str__(self) -> str:
        s = "################\n"
        for estanteria in self.estanterias:
            for item in estanteria:
                s += f'# {item}\n'
            s += "################\n"
        return s


class Tarea:
    def __init__(self, inicio: int, final: int, nombre: str,
                 cantidad: int) -> None:
        self.inicio = inicio
        self.final = final
        # El item tiene que ser una copia para que no se modifique antes
        # de escribir el archivo.
        self.item = Item(nombre, cantidad)

    def __str__(self) -> str:
        return f"LLevar {self.item.cantidad} {self.item.nombre} desde la" \
               f" estantería {self.inicio} hasta {self.final}."


class ArchivoTareas:
    def __init__(self) -> None:
        self.tareas = []

    def __iter__(self) -> Tarea:
        for tarea in self.tareas:
            yield tarea

    def es_posible(self, almacen: Almacen, pedido: Tuple[Item]) -> bool:
        for item in pedido:
            contador = 0
            for estanteria in almacen:
                for item_disponible in estanteria:
                    if item_disponible.nombre == item.nombre:
                        contador += item_disponible.cantidad
            if contador < item.cantidad:
                return False

        return True

    def generar_tareas(self, almacen: Almacen, pedido: Tuple[Item],
                       i_pedido: int) -> None:
        if not self.es_posible(almacen, pedido):
            msg = "No se pudo completar el pedido:\n"
            for item in pedido:
                msg += str(item)
                msg += '\n'
            raise NoHayItems(msg)

        # Itera cada item del pedido
        for item_pedido in pedido:
            # Los busca en todos los items del almacén
            for i_estanteria, estanteria in enumerate(almacen):
                for item_disponible in estanteria:
                    # Se mueven los items del almacén requeridos a los del
                    # pedido.
                    if item_pedido.nombre == item_disponible.nombre \
                            and item_pedido.cantidad > 0:
                        if item_pedido.cantidad > item_disponible.cantidad:
                            # Si en el contendor no hay suficientes o estan
                            # justas me llevo todo lo que puedo
                            item_pedido.cantidad -= item_disponible.cantidad
                            # Se añade una tarea nueva a la lista interna
                            self.tareas.append(Tarea(i_estanteria, i_pedido,
                                                     item_disponible.nombre,
                                                     item_disponible.cantidad))
                            item_disponible.cantidad = 0
                            # Si ya no quedan pedidos, se termina la
                            # iteración del item.
                        elif item_pedido.cantidad == item_disponible.cantidad:
                            self.tareas.append(Tarea(i_estanteria, i_pedido,
                                                     item_disponible.nombre,
                                                     item_disponible.cantidad))
                            item_disponible.cantidad = 0;
                            item_pedido.cantidad = 0;
                            break
                        else:
                            self.tareas.append(Tarea(i_estanteria, i_pedido,
                                                     item_pedido.nombre,
                                                     item_pedido.cantidad))
                            # En la estanteria hay de sobra para el pedido
                            item_disponible.cantidad -= item_pedido.cantidad
                            break
                            
    def escribir(self, archivo: str) -> None:
        """
        Se escribe el JSON correctamente, siguiendo el mismo formato usado
        para el almacén y los pedidos.
        """

        formato = dict()
        formato['tareas'] = []
        for tarea in self.tareas:
            formato['tareas'].append({
                'inicio': tarea.inicio,
                'final': tarea.final,
                'item': {
                    'nombre': tarea.item.nombre,
                    'cantidad': tarea.item.cantidad
                }
            })
        with open(archivo, 'w') as archivo_tareas:
            json.dump(formato, archivo_tareas)
