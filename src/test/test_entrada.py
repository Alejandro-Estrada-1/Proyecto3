import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/..")

import main
from main import *

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

class Test_Entrada(unittest.TestCase):

    def test_entrada(self):
        entrada_test = ["Proyecto3.py"]
        with patch.object(sys, 'argv', entrada_test):

            with self.assertRaises(SystemExit):
                main.entrada()

            entrada_test = ["c", "./bomba.txt", "5", "3", "bomba_cifrado.txt"]

            try:
                main.entrada()
            except:
                self.fail
    
if __name__ == '__main__':
    unittest.main()