"""Pruebas de callbacks web con estado aislado y servicio RSA real.

Se simula únicamente session_state: no se necesita instalar Streamlit para
comprobar el flujo de datos. Estas pruebas no sustituyen probar el navegador.
"""

import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch


class FlujoWebTests(unittest.TestCase):
    def setUp(self):
        self.estado = {}
        falso = SimpleNamespace(session_state=self.estado)
        ruta = Path(__file__).resolve().parents[1] / "streamlit_app.py"
        spec = importlib.util.spec_from_file_location("web_en_prueba", ruta)
        self.web = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"streamlit": falso}):
            spec.loader.exec_module(self.web)
        self.web.cargar_ejemplo("enc")
        self.web.cargar_ejemplo("dec")

    def test_encriptar_ejemplo_y_transferir(self):
        self.web.ejecutar("enc")
        r = self.estado["enc_resultado"]
        self.assertEqual(r.ciphertext, "026054 123875")
        self.assertEqual(r.length, 3)
        self.web.transferir()
        self.assertEqual(self.estado["dec_texto"], r.ciphertext)
        self.assertEqual(self.estado["dec_l"], "3")
        self.assertEqual(self.estado["dec_p"], "367")
        self.web.ejecutar("dec")
        self.assertEqual(self.estado["dec_resultado"].message, "RSA")

    def test_espacios_originales_no_se_recortan(self):
        self.web.cargar_ejemplo("enc", espacios=True)
        original = self.estado["enc_texto"]
        self.assertEqual(len(original), 11)
        self.web.ejecutar("enc")
        self.web.transferir()
        self.web.ejecutar("dec")
        self.assertEqual(self.estado["dec_resultado"].message, original)

    def test_error_matematico_borra_resultado_previo(self):
        self.web.ejecutar("enc")
        self.estado["enc_e"] = "2"
        self.web.ejecutar("enc")
        self.assertIsNone(self.estado["enc_resultado"])
        self.assertIn("primos relativos", self.estado["enc_error"])

    def test_caracter_invalido_no_se_sustituye(self):
        self.estado["enc_texto"] = "niño"
        self.web.ejecutar("enc")
        self.assertIsNone(self.estado["enc_resultado"])
        self.assertIn("ASCII", self.estado["enc_error"])
        self.assertEqual(self.estado["enc_texto"], "niño")

    def test_longitud_y_cifrado_invalidos_muestran_error(self):
        self.estado["dec_l"] = "0"
        self.web.ejecutar("dec")
        self.assertIsNone(self.estado["dec_resultado"])
        self.assertTrue(self.estado["dec_error"])
        self.estado["dec_l"] = "2"
        self.estado["dec_texto"] = "136891"
        self.web.ejecutar("dec")
        self.assertIn("menor que n", self.estado["dec_error"])

    def test_formato_numerico_y_limpieza(self):
        self.estado["enc_p"] = "abc"
        self.web.ejecutar("enc")
        self.assertIn("entero decimal", self.estado["enc_error"])
        self.web.limpiar("enc")
        self.assertEqual(self.estado["enc_texto"], "")
        self.assertEqual(self.estado["enc_p"], "")
        self.assertEqual(self.estado["enc_error"], "")
        self.assertIsNone(self.estado["enc_resultado"])

    def test_editar_invalida_resultado_sin_tocar_la_otra_operacion(self):
        self.web.ejecutar("enc")
        self.web.ejecutar("dec")
        dec = self.estado["dec_resultado"]
        self.web.invalidar("enc")
        self.assertIsNone(self.estado["enc_resultado"])
        self.assertIs(self.estado["dec_resultado"], dec)

    def test_exponente_grande_y_rechazo_temprano_de_primos_gigantes(self):
        e = 17 + 136152 * 10 ** 400
        self.estado["enc_e"] = str(e)
        self.web.ejecutar("enc")
        self.assertEqual(self.estado["enc_resultado"].ciphertext, "026054 123875")
        self.web.transferir()
        self.web.ejecutar("dec")
        self.assertEqual(self.estado["dec_resultado"].message, "RSA")
        self.estado["enc_p"] = "9" * 5000
        self.web.ejecutar("enc")
        self.assertIsNone(self.estado["enc_resultado"])
        self.assertIn("1000000", self.estado["enc_error"])


if __name__ == "__main__":
    unittest.main()
