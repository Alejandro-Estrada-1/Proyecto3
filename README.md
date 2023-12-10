# Proyecto03
Proyecto03, Modelado y Programación.

## Integrantes
  * Morales Flores Luis Enrique (Regla de Horner, Interpolación de Langrange)
  * Sánchez Estrada Alejandro (Llave K sha-265, Cifrado con AES, Evaluación del polinomio)
  * Acevedo Romero Miroslava (Pruebas Unitarias)
  * Rivera Lara Sandra Valeria (Entrada y descifrar)
## Requerimientos
El programa funciona con Python 3 y tiene los siguientes requerimientos:

## Instrucciones de Ejecución
Es recomendable crear primero un entorno virtual dentro de la carpeta Proyecto3. Para hacerlo y activarlo, se deben de seguir las siguientes instrucciones: https://python.land/virtual-environments/virtualenv

### Instalación de paquetes
Dentro de la carpeta Proyecto3 escribir:

pip install -r requirements.txt

Para confirmar que se instaló todo de "Bibliotecas y paquetes" correctamente, revisar que estén en la lista obtenida con el siguiente comando:

pip list

De no haberse instalado algún paquete de requirements.txt, escribir el comando:

pip install [nombre paquete]

### Pruebas unitarias

Abrir una terminal en la carpeta Proyecto3/src y ejecutar el comando:

python -m unittest

para correr todas las pruebas unitarias del modelo.

### Ejecución

Escribir en la consola en la ruta donde se encuentre este README el siguiente comando:

python src\main.py

Con los siguientes argumentos, según lo que se quiera hacer:

Para cifrar el archivo ingrese los siguientes argumentos:
1. Bandera c.
2. Nombre del archivo para guardar las evaluaciones.
3. Número total de evaluaciones requeridas (n > 2).
4. Número mínimo de puntos necesarios para descifrar (1 < t ≤ n).
5. Nombre del archivo a cifrar'.

Para descifrar el archivo ingrese los siguientes argumentos:
1. Bandera d.
2. Nombre del archivo con las evaluaciones.
3. Nombre del archivo a descifrar'.