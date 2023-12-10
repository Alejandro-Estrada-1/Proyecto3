import sys
from shamir_cifrado import cifrar_archivo
from descifrado import descifrar

def entrada():
    error_argumento = "Error, argumentos inválidos para cifrar."
    error_cifrado = error_argumento + '\nPara cifrar el archivo ingrese los siguientes argumentos:\n1. Bandera c\n2. Nombre del archivo para guardar las evaluaciones\n3. Número total de evaluaciones requeridas (n > 2)\n4. Número mínimo de puntos necesarios para descifrar (1 < t ≤ n)\n5. Nombre del archivo a cifrar'
    error_descifrado = error_argumento + '\nPara descifrar el archivo ingrese los siguientes argumentos:\n1. Bandera d\n2. Nombre del archivo con las evaluaciones\n3. Nombre del archivo a descifrar'
                            
    entrada = sys.argv[1:]
    if len(entrada) == 0:
        sys.exit(error_argumento)
        
    # Cifrar
    if entrada[0] == 'c':
        if len(entrada) != 5:
            sys.exit(error_cifrado)
        try:
            archivo_eval = entrada[1]
            num_eval = int(entrada[2])
            if num_eval <= 2:
                sys.exit(error_cifrado)
            min_puntos = int(entrada[3])
            if (min_puntos <= 1) or (num_eval < min_puntos):
                sys.exit(error_cifrado)
            archivo_claro = entrada[4]
        except:
            sys.exit(error_cifrado)
        cifrar_archivo(archivo_claro, archivo_eval, num_eval, min_puntos)


    # Descifrar
    elif entrada[0] == 'd':
        # Leer entrada
        if len(entrada) != 3:
            sys.exit(error_descifrado)
        archivo_eval = entrada[1]
        archivo_cifrado = entrada[2]
        descifrar(archivo_eval, archivo_cifrado)
            
    else:
        sys.exit(error_argumento)

entrada()