import argparse
import getpass
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from secrets import SystemRandom


def generar_clave_secreta(contrasena):
    """
    Genera una clave secreta a partir de una contrasena utilizando SHA-256.

    Args:
        contrasena (str): La contrasena.

    Returns:
        bytes: La clave secreta generada.
    """
    dg = hashes.Hash(hashes.SHA256(), backend=default_backend())
    dg.update(contrasena.encode('utf-8'))
    return dg.finalize()


def generar_polinomio(clave_secreta, t):
    """
    Genera un polinomio con el término independiente como la clave secreta.

    Args:
        clave_secreta (bytes): La clave secreta.
        t (int): Número mínimo de puntos necesarios para descifrar.

    Returns:
        list: Lista de coeficientes del polinomio.
    """
    coeficientes = [int.from_bytes(clave_secreta, byteorder='big')]
    for _ in range(t - 1):
        coeficientes.append(SystemRandom().randint(1, 2**256))
    return coeficientes


def evaluar_polinomio(coeficientes: list, x_puntos: list):
    """
    Evalúa un polinomio utilizando la regla de Horner.

    Args:
        coeficientes (list): Lista de coeficientes del polinomio, donde 
            el elemento en la posición i es el coeficiente del término x^i.
        x_puntos (list): Valores en los cuales evaluaremos el polinomio.

    Returns:
        list: Una lista con el resultado de evaluar el polinomio 
        en cada punto de x_puntos con su orden correspondiente.
    """
    y_puntos = []
    for x in x_puntos:
        resultado = 0
        for coeficiente in reversed(coeficientes):
            resultado = resultado * x + coeficiente
        y_puntos.append(resultado)
    return y_puntos


def guardar_evaluaciones(archivo_evaluaciones, evaluaciones, t):
    """
    Guarda las evaluaciones del polinomio en un archivo.

    Args:
        archivo_evaluaciones (str): Nombre del archivo para guardar las evaluaciones.
        evaluaciones (list): Lista de evaluaciones del polinomio.
    """
    with open(archivo_evaluaciones, 'w') as archivo:
        n=1
        for punto, evaluacion in enumerate(evaluaciones, start=1):
            if n>t:
                archivo.write(f"({punto},{evaluacion})\n")
            else:
                archivo.write(f"{punto},{evaluacion}\n")
                n+=1


def cifrar_archivo(archivo_entrada, archivo_evaluaciones, total_evaluaciones, min_puntos_descifrar):
    """
    Cifra un archivo y guarda las evaluaciones del polinomio en archivos.

    Args:
        archivo_entrada (str): Nombre del archivo con el documento claro.
        archivo_evaluaciones (str): Nombre del archivo para guardar las evaluaciones.
        total_evaluaciones (int): Número total de evaluaciones requeridas (n > 2).
        min_puntos_descifrar (int): Número mínimo de puntos necesarios para descifrar (1 < t ≤ n).
    """
    contrasena = getpass.getpass("Ingrese la contrasena para generar la llave: ")
    clave_secreta = generar_clave_secreta(contrasena)

    coeficientes = generar_polinomio(clave_secreta, min_puntos_descifrar)

    puntos_evaluacion = list(range(1, total_evaluaciones + 1))
    
    archivo_evaluaciones = os.path.join(os.path.dirname(archivo_entrada), os.path.basename(archivo_evaluaciones))

    evaluaciones = evaluar_polinomio(coeficientes, puntos_evaluacion)

    guardar_evaluaciones(archivo_evaluaciones, evaluaciones, min_puntos_descifrar)

    with open(archivo_entrada, 'rb') as archivo:
        textoplano = archivo.read()

    iv = os.urandom(16)
    
    nombre_base, _ = os.path.splitext(archivo_entrada)
    archivo_cifrado = nombre_base + '.aes'
    
    cifrar = Cipher(algorithms.AES(bytes(clave_secreta)), modes.CFB(iv), backend=default_backend())
    cifrador = cifrar.encryptor()
    textocifrado = cifrador.update(textoplano) + cifrador.finalize()

    with open(archivo_entrada, 'wb') as archivo:
        archivo.write(iv + textocifrado)
    print(f'Archivo cifrado: {archivo_cifrado}')
    print(f'Evaluaciones del polinomio guardadas en {archivo_evaluaciones}.')

def main():
    parser = argparse.ArgumentParser(description='Cifrado basado en polinomios y umbral de Shamir.')
    parser.add_argument('archivo_entrada', type=str, help='Nombre del archivo con el documento claro.')
    parser.add_argument('archivo_evaluaciones', type=str, help='Nombre del archivo para guardar las evaluaciones.')
    parser.add_argument('total_evaluaciones', type=int, help='Número total de evaluaciones requeridas (n > 2).')
    parser.add_argument('min_puntos_descifrar', type=int, help='Número mínimo de puntos necesarios para descifrar (1 < t ≤ n).')
    args = parser.parse_args()

    cifrar_archivo(args.archivo_entrada, args.archivo_evaluaciones, args.total_evaluaciones, args.min_puntos_descifrar)

if __name__ == "__main__":
    main()
