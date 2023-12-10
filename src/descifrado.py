from sympy import symbols, expand
import os
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        
        
def obtener_llave(x_valores: list, y_valores: list):
    """
    Construye el polinomio de interpolación de Lagrange 
    y regresa el término independiente.

    Args:
        x_valores (list): Lista de valores x.
        y_valores (list): Lista de valores p(x) 
            correspondientes a los valores x.

    Returns:
        int: Término independiente del polinomio de Lagrange. 
    """

    # Definir la variable simbólica e inicializar el polinomio
    x = symbols('x')
    polinomio_interpolacion = 0

    # Construye el polinomio de interpolación de Lagrange
    for i in range(len(x_valores)):
        termino = y_valores[i]
        for j in range(len(x_valores)):
            if i != j:
                termino *= (x - x_valores[j]) / (x_valores[i] - x_valores[j])
        polinomio_interpolacion += termino
        
    # Expandir el polinomio para obtener una forma más legible
    polinomio_interpolacion = expand(polinomio_interpolacion)
    
    # Obtener los coeficientes del polinomio
    poly_obj = polinomio_interpolacion.as_poly()
    
    # Verificar que poly_obj no sea None
    if poly_obj is not None:
        coeficientes = poly_obj.coeffs()
        return coeficientes[-1]
    else:
        return polinomio_interpolacion


def int_to_bytes(numero: int):
    """
    Convierte un entero a bytes

    Args:
        numero (int): el entero a convertir

    Returns:
        bytes: el entero como bytes
    """
    if(numero < 0):
        return numero.to_bytes(
            (8 + (numero + (numero < 0)).bit_length()) // 8, byteorder='big', signed=True
        )
    else:
        return numero.to_bytes(
            (numero.bit_length() + 7) // 8, byteorder='big'
        )
    
def descifrar(archivo_eval: str, archivo_cifrado: str):
    """
    Descifra un archivo dado con las evaluaciones de 
    otro archivo. Luego crea un archivo con el mismo 
    nombre del cifrado con el mensaje descifrado.

    Args:
        archivo_eval (str): el archivo con las evaluaciones
        archivo_cifrado (str): el arcivo cifrado

    Raises:
        Exception: cuando hay un error en las evaluaciones
    """
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
            if(linea[0]=="("):
                break
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
    archivo_claro = archivo_cifrado
    with open(archivo_claro, 'wb') as salida:
        salida.write(texto_descifrado[16:])
    
    print("Archivo descifrado: ", archivo_claro)
