from secrets import SystemRandom
import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/..")

from descifrado import obtener_llave
from shamir_cifrado import evaluar_polinomio

class Test_Descifrado(unittest.TestCase):
    
    def test_polinomiosAleatorios(self):
        # Pruebas para ver que los algoritmos funcionen correctamente.
        # Se hacen 10 pruebas con polinomios aleatorios.
        for i in range(10):
            coef = []
            
            # Grado del polinomio.
            n = SystemRandom().randint(0, 20)
            limit = 2**256
            
            # Se agrega el término independiente.
            key = SystemRandom().randint(-limit, limit)
            coef.append(key)
            
            # Se generan los coeficientes del polinomio.
            for j in range(n):
                coef.append(SystemRandom().randint(-limit, limit))
            
            # Se verifica que el evaluar polinomio calcule bien el término independiente.
            self.assertEqual(key, evaluar_polinomio(coef, [0])[0])

            # Se crean las listas de los valores x y y del polinomio.
            x_puntos = []
            for j in range(n+1):
                x_puntos.append(SystemRandom().randint(-limit, limit))
            y_puntos = evaluar_polinomio(coef, x_puntos)
            
            # Se verifica que obtener_llave sea correcto.
            self.assertEqual(key, obtener_llave(x_puntos, y_puntos))
            
            # Muestra el porcentaje de avance de las pruebas.
            carga = ""
            for j in range(i+1):
                carga+="."
            print(f"{carga}  {(i+1)*10}%")

            

if __name__ == '__main__':
    unittest.main()