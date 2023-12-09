import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from shamir_cifrado import cifrar_archivo
import os
from cryptography.hazmat.backends import default_backend
from LagrangePolinomio import obtener_llave


def int_to_bytes(numero):
    if(numero < 0):
        return numero.to_bytes(
            (8 + (numero + (numero < 0)).bit_length()) // 8, byteorder='big', signed=True
        )
    else:
        return numero.to_bytes(
            (numero.bit_length() + 7) // 8, byteorder='big'
        )
    
def descifrar(archivo_eval, archivo_cifrado):
    # Leer archivo con evaluaciones
    x_valores = []
    y_valores = []
    try:
        file1 = open(archivo_eval, 'r')
        evaluaciones = file1.readlines()
        for linea in evaluaciones:
            evaluacion = linea.split(",")
            if (len(evaluacion) != 2):
                raise Exception("Error en la linea '", linea, "'")
            x_valores.append(int(evaluacion[0]))
            y_valores.append(int(evaluacion[1]))
    except Exception as error: 
        print(error)
        sys.exit("Ingrese un archivo valido con las evaluaciones.")


    # Obtener la llave
    llave = int(obtener_llave(x_valores, y_valores))
    clave_secreta = int_to_bytes(llave)

    # Descifrar archivo
    try:
        with open(archivo_cifrado, 'rb') as entrada:
            texto_cifrado = entrada.read()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(clave_secreta), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        texto_descifrado = decryptor.update(texto_cifrado) + decryptor.finalize()
    except FileNotFoundError:
        print("No se encontro el archivo: ", archivo_cifrado)
        sys.exit("Ingrese un archivo valido con el mensaje cifrado.")
    except:
        print("Ocurrio un error al leer el archivo: ", archivo_cifrado)
        sys.exit("Ingrese un archivo valido con el mensaje cifrado.")

    # Crear archivo descifrado
    nombre_base, _ = os.path.splitext(archivo_cifrado)
    nombre_base = "descifrado" ########### Quitar al final
    archivo_claro = nombre_base + '.txt'
    with open(archivo_claro, 'wb') as file:
        file.write(texto_descifrado[16:])
    
    print("Archivo descifrado: ", archivo_claro)

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
elif entrada[0] == 'd':
    # Leer entrada
    if len(entrada) != 3:
        sys.exit("Error, argumentos inválidos.")
    archivo_eval = entrada[1]
    archivo_cifrado = entrada[2]
    descifrar(archivo_eval, archivo_cifrado)
        
else:
    sys.exit("Error, argumentos inválidos.")
