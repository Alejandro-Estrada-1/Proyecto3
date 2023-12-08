import sys
import os
#from Crypto.Cipher import AES
from shamir_cifrado import cifrar_archivo
from LagrangePolinomio import obtener_llave

entrada = sys.argv[1:]
if len(entrada) == 0:
    sys.exit("Error, argumentos inválidos para cifrar.")
# Cifrar
if entrada[0] == 'c':
    if len(entrada) != 5:
        sys.exit("Error, argumentos inválidos para cifrar.")
    try:
        archivo_eval = entrada[1]
        num_eval = int(entrada[2])
        if num_eval <= 2:
            sys.exit("Error, argumentos inválidos para cifrar.")
        min_puntos = int(entrada[3])
        if (min_puntos <= 1) or (num_eval < min_puntos):
            sys.exit("Error, argumentos inválidos para cifrar.")
        archivo_claro = entrada[4]
    except:
        sys.exit("Error, argumentos inválidos para cifrar.")
    cifrar_archivo(archivo_claro, archivo_eval, num_eval, min_puntos)


# Descifrar
# Leer entrada
elif entrada[0] == 'd':
    if len(entrada) != 3:
        sys.exit("Error, argumentos inválidos.")
    archivo_eval = entrada[1]
    archivo_cifrado = entrada[2]
    
    # Leer archivo con evaluaciones
    file1 = open(archivo_eval, 'r')
    evaluaciones = file1.readlines()
    x_valores = []
    y_valores = []
    for linea in evaluaciones:
        evaluacion = linea.split(",")
        x_valores.append(int(evaluacion[0]))
        y_valores.append(int(evaluacion[1][:-2]))
    print("x: ", x_valores)
    print("y: ", y_valores)

    # Descifrar archivo
    llave = obtener_llave(x_valores, y_valores)
    print("termino independiente: ", llave)

    # Crear archivo descifrado
    directorio_cifrado = os.path.dirname(archivo_cifrado)
    nombre_base, _ = os.path.splitext(archivo_cifrado)
    archivo_claro = nombre_base + '.txt'

    
else:
    sys.exit("Error, argumentos inválidos.")