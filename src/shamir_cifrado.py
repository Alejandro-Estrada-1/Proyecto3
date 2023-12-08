import argparse
import getpass
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from secrets import SystemRandom
from LagrangePolinomio import evaluar_polinomio


def generar_clave_secreta(password):
    """
    Genera una clave secreta a partir de una contraseña utilizando SHA-256.

    Args:
        password (str): La contraseña.

    Returns:
        bytes: La clave secreta generada.
    """
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode('utf-8'))
    return digest.finalize()


def generar_polinomio(clave_secreta, n, t):
    """
    Genera un polinomio con el término independiente como la clave secreta.

    Args:
        clave_secreta (bytes): La clave secreta.
        n (int): Número total de coeficientes del polinomio.
        t (int): Número mínimo de puntos necesarios para descifrar.

    Returns:
        list: Lista de coeficientes del polinomio.
    """
    coeficientes = [int.from_bytes(clave_secreta, byteorder='big')]
    for _ in range(t - 1):
        coeficientes.append(SystemRandom().randint(1, 2**256))
    return coeficientes


def guardar_evaluaciones(archivo_evaluaciones, evaluaciones):
    """
    Guarda las evaluaciones del polinomio en un archivo.

    Args:
        archivo_evaluaciones (str): Nombre del archivo para guardar las evaluaciones.
        evaluaciones (list): Lista de evaluaciones del polinomio.
    """
    with open(archivo_evaluaciones, 'w') as file:
        for punto, evaluacion in enumerate(evaluaciones, start=1):
            file.write(f"{punto},{evaluacion}\n")


def cifrar_archivo(archivo_entrada, archivo_evaluaciones, total_evaluaciones, min_puntos_descifrar):
    """
    Cifra un archivo y guarda las evaluaciones del polinomio en archivos.

    Args:
        archivo_entrada (str): Nombre del archivo con el documento claro.
        archivo_evaluaciones (str): Nombre del archivo para guardar las evaluaciones.
        total_evaluaciones (int): Número total de evaluaciones requeridas (n > 2).
        min_puntos_descifrar (int): Número mínimo de puntos necesarios para descifrar (1 < t ≤ n).
    """
    password = getpass.getpass("Ingrese la contraseña para generar la llave: ")
    clave_secreta = generar_clave_secreta(password)

    coeficientes = generar_polinomio(clave_secreta, total_evaluaciones, min_puntos_descifrar)

    puntos_evaluacion = list(range(1, total_evaluaciones + 1))

    directorio_cifrado = os.path.dirname(archivo_entrada)
    nombre_evaluaciones = os.path.join(directorio_cifrado, "evaluaciones.frg")

    evaluaciones = evaluar_polinomio(coeficientes, puntos_evaluacion)

    guardar_evaluaciones(nombre_evaluaciones, evaluaciones)

    with open(archivo_entrada, 'rb') as file:
        plaintext = file.read()

    iv = os.urandom(16)
    
    nombre_base, _ = os.path.splitext(archivo_entrada)
    archivo_cifrado = nombre_base + '.aes'
    
    cipher = Cipher(algorithms.AES(bytes(clave_secreta)), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(archivo_cifrado, 'wb') as file:
        file.write(iv + ciphertext)

    print(f'Archivo cifrado: {archivo_cifrado}')
    print(f'Evaluaciones del polinomio guardadas en {nombre_evaluaciones}.')

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
