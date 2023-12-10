import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/..")

import shamir_cifrado
from shamir_cifrado import *

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from secrets import SystemRandom

class Test_Cifrado(unittest.TestCase):

    def test_generar_clave_secreta(self):

        for i in range(10):
            caracteres = ["qwertyuiopasdfghjklzxcvbnm1234567890"]
            contrasena = ""
            while len(contrasena) < 20:
                contrasena += caracteres[SystemRandom().randint(0, len(caracteres)-1)]
            
            clave = hashes.Hash(hashes.SHA256(), backend=default_backend())
            clave.update(contrasena.encode('utf-8'))

            self.assertEqual(shamir_cifrado.generar_clave_secreta(contrasena), clave.finalize())
    
    def test_generar_polinomio(self):
        clave_secreta_test = shamir_cifrado.generar_clave_secreta("ContrasenaPolinomio")

        for i in range(10):          
            t = SystemRandom().randint(5,20)

            coeficientes = shamir_cifrado.generar_polinomio(clave_secreta_test, t)

            self.assertEqual(t, len(coeficientes))
            for coef in coeficientes:
                self.assertIsInstance(coef, int)
    
    def test_evaluar_polinomio(self):
        clave_secreta_test = shamir_cifrado.generar_clave_secreta("ContrasenaPolinomio")
        t = SystemRandom().randint(5,20)
        polinomio = shamir_cifrado.generar_polinomio(clave_secreta_test, t)

        puntos = []
        for i in range(t):
            puntos.append(SystemRandom().randint(1,2**256))
        
        evaluado = shamir_cifrado.evaluar_polinomio(polinomio, puntos)
        
        self.assertEqual(t, len(evaluado))

        for i in range(len(puntos)):
            resultado = 0
            for coeficiente in reversed(polinomio):
                resultado = resultado * puntos[i] + coeficiente
            self.assertEqual(resultado, evaluado[i])
  
if __name__ == '__main__':
    unittest.main()