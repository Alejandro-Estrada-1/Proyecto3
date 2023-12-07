from sympy import symbols, expand


def evaluar_polinomio(coeficientes, x_puntos):
    """
    Evalúa un polinomio utilizando la regla de Horner.

    Parámetros:
    - coeficientes: Lista de coeficientes del polinomio, donde el elemento en la posición i
                    es el coeficiente del término x^i.
    - x_puntos: Valores en los cuales evaluaremos el polinomio.

    Retorna:
    - Una lista con el resultado de evaluar el polinomio en cada punto de x_puntos con su orden correspondiente.
    """
    y_puntos = []
    for x in x_puntos:
        resultado = 0
        for coeficiente in reversed(coeficientes):
            resultado = resultado * x + coeficiente
        y_puntos.append(resultado)
    return y_puntos
        
        
def obtener_llave(x_valores, y_valores):
    """
    Construye el polinomio de interpolación de Lagrange y regresa el término independiente.

    Parámetros:
    - x_valores: Lista de valores x.
    - param y_valores: Lista de valores p(x) correspondientes a los valores x.
    
    Retorna: 
    - Término independiente del polinomio de Lagrange (un número entero). 
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

