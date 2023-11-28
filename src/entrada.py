import sys
import getpass
#from Crypto.Cipher import AES

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
#    try:
    contrasena = getpass.getpass()
    print(contrasena)
#    except:
#        sys.exit("Problemas al escribir la contrasena.")




# Descifrar
elif entrada[0] == 'd':
    if len(entrada) != 3:
        sys.exit("Error, argumentos inválidos.")
    archivo_eval = entrada[1]
    archivo_cifrado = entrada[2]
    
else:
    sys.exit("Error, argumentos inválidos.")