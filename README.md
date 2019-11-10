# Jotasón

Jotasón es un asistente por voz hecho para el reto de Sesé en la hackatón ImagineCode 2019. Por Jaime Yoldi y Mario Ortiz.

Su misión consistía en asistir a un trabajador que completa pedidos a partir un almacén con hasta 20 cajas de ítems diferentes. El almacén está representado por `almacén.json`, y los pedidos por `pedidos.json`. Jotasón analiza ambos archivos y crea otro archivo con las tareas que hay que realizar para completar todos los pedidos, que irá diciéndole por voz al usuario.

Todo ello se hace con interacción con voz. Los servicios de Google Cloud han sido usados para interaccionar con el usuario, y se ha creado un sistema de diálogo que contiene las conversación usuario - asistente para que se sienta de la forma más humana posible.

# Instalación

Asegúrate de tener las dependencias necesarias listadas en `setup.py` para tu sistema. Posteriormente, ejecuta:

```shell
pip install . --user
```

Y para lanzarlo, simplemente llama a `jotason` desde la terminal.
