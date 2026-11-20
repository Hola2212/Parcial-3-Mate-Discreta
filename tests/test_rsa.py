"""Pruebas reales de operaciones y servicio; no necesitan una pantalla.

Ejecutar desde la carpeta que contiene main.py:
    python -m unittest discover -s tests -v

Las cuatro pruebas de IntegracionCompletaTests se omiten si todavía no existe
formatear_cifrado. Esas omisiones son integración PENDIENTE, no pruebas aprobadas.
No se reemplaza el formateador por una función simulada.
"""

import unittest

from contracts import (
    DecryptRequest,
    DecryptResult,
    DetailRow,
    EncryptRequest,
    EncryptResult,
)
from logica import conversiones
from logica.operaciones import desencriptar, encriptar
from rsa_service import RealRSAService


PARAMETROS = (367, 373, 17)
TIENE_FORMATEADOR = hasattr(conversiones, "formatear_cifrado")


class OperacionesTests(unittest.TestCase):
    def comprobar_recuperacion(self, mensaje, parametros=PARAMETROS):
        datos = encriptar(mensaje, *parametros)
        # Serialización de los datos de prueba para probar las operaciones
        # independientemente del formateador que desarrolla el compañero.
        cifrado = " ".join(f"{bloque:06d}" for bloque in datos["bloques_cifrados"])
        recuperado = desencriptar(cifrado, datos["longitud"], *parametros)
        self.assertEqual(recuperado["mensaje"], mensaje)
        self.assertEqual(datos["longitud"], len(mensaje))
        self.assertEqual(datos["relleno"], len(mensaje) % 2 != 0)
        self.assertEqual(recuperado["bloques_originales"], datos["bloques_originales"])

    def test_encriptacion_ejemplo_pdf(self):
        resultado = encriptar("RSA", *PARAMETROS)
        self.assertEqual(resultado["n"], 136891)
        self.assertEqual(resultado["phi"], 136152)
        self.assertEqual(resultado["longitud"], 3)
        self.assertTrue(resultado["relleno"])
        self.assertEqual(resultado["bloques_originales"], [82083, 65032])
        self.assertEqual(resultado["bloques_cifrados"], [26054, 123875])

    def test_desencriptacion_ejemplo_pdf(self):
        resultado = desencriptar("026054 123875", 3, *PARAMETROS)
        self.assertEqual(resultado["mensaje"], "RSA")
        self.assertEqual(resultado["d"], 8009)
        self.assertTrue(resultado["relleno"])
        self.assertEqual(17 * resultado["d"] % resultado["phi"], 1)

    def test_longitudes_signos_y_espacios(self):
        for mensaje in ("AB", "ABC", "Aa09!?", "  Aa1!  z  ", " A ", "A  ", " ", "  ", "   ", " ~"):
            with self.subTest(mensaje=repr(mensaje)):
                self.comprobar_recuperacion(mensaje)

    def test_todas_las_9025_parejas_ascii(self):
        mensaje = "".join(
            chr(a) + chr(b) for a in range(32, 127) for b in range(32, 127)
        )
        self.comprobar_recuperacion(mensaje)

    def test_e_mayor_que_phi_y_e_compuesto_valido(self):
        for e in (136169, 25):
            with self.subTest(e=e):
                self.comprobar_recuperacion(" Prueba 123! ", (367, 373, e))

    def test_parametros_rsa_invalidos(self):
        for parametros in ((367, 367, 17), (369, 373, 17), (3, 5, 17),
                           (1009, 1013, 17), (367, 373, 1), (367, 373, 2),
                           (-367, 373, 17), (1, 373, 17),
                           (2, 63063, 17), (2, 500000, 17)):
            with self.subTest(parametros=parametros), self.assertRaises(ValueError):
                encriptar("RSA", *parametros)

    def test_mensajes_no_admitidos(self):
        for mensaje in ("", "café", "ñ", "a\nb", "a\tb", "\x1f", "\x7f", "🙂"):
            with self.subTest(mensaje=repr(mensaje)), self.assertRaises(ValueError):
                encriptar(mensaje, *PARAMETROS)

    def test_formato_de_cifrado_invalido(self):
        for cifrado in ("", "26054", "0026054", "02605a", "+26054",
                        "０２６０５４", "026054,123875", "026054\t123875",
                        "026054\n123875", " 026054", "026054 "):
            with self.subTest(cifrado=repr(cifrado)), self.assertRaises(ValueError):
                desencriptar(cifrado, 2, *PARAMETROS)

    def test_cifrado_fuera_del_modulo(self):
        for cifrado in ("136891", "999999"):
            with self.subTest(cifrado=cifrado), self.assertRaises(ValueError):
                desencriptar(cifrado, 2, *PARAMETROS)

    def test_longitudes_inconsistentes(self):
        for longitud in (-1, 0, 1, 2, 5, 6):
            with self.subTest(longitud=longitud), self.assertRaises(ValueError):
                desencriptar("026054 123875", longitud, *PARAMETROS)

    def test_ascii_recuperado_invalido(self):
        with self.assertRaisesRegex(ValueError, "ASCII"):
            desencriptar("000000", 2, *PARAMETROS)

    def test_rechazo_de_relleno_inconsistente(self):
        datos = encriptar("AB", *PARAMETROS)
        cifrado = " ".join(f"{b:06d}" for b in datos["bloques_cifrados"])
        with self.assertRaisesRegex(ValueError, "relleno"):
            desencriptar(cifrado, 1, *PARAMETROS)

    def test_l_par_conserva_el_espacio_final(self):
        resultado = desencriptar("026054 123875", 4, *PARAMETROS)
        self.assertEqual(resultado["mensaje"], "RSA ")
        self.assertFalse(resultado["relleno"])


class ServicioTests(unittest.TestCase):
    def setUp(self):
        self.servicio = RealRSAService()

    def test_contrato_de_desencriptacion(self):
        resultado = self.servicio.decrypt(DecryptRequest("026054 123875", 3, *PARAMETROS))
        self.assertIsInstance(resultado, DecryptResult)
        self.assertEqual(resultado.message, "RSA")
        self.assertEqual((resultado.d, resultado.n, resultado.phi), (8009, 136891, 136152))
        self.assertTrue(resultado.padding_removed)

    def test_detalles_de_desencriptacion(self):
        resultado = self.servicio.decrypt(DecryptRequest("026054 123875", 3, *PARAMETROS))
        self.assertEqual(resultado.details, [
            DetailRow(1, "RS", "082 083", "026054", "082083"),
            DetailRow(2, "A ", "065 032", "123875", "065032"),
        ])

    def test_no_agrega_comillas_a_los_caracteres_de_la_tabla(self):
        # La UI ya usa repr(row.characters); el servicio entrega la pareja real.
        resultado = self.servicio.decrypt(DecryptRequest("026054 123875", 3, *PARAMETROS))
        self.assertEqual(resultado.details[-1].characters, "A ")
        self.assertEqual(len(resultado.details[-1].characters), 2)

    def test_tipos_invalidos_se_presentan_como_valueerror(self):
        solicitudes = [DecryptRequest("026054 123875", "3", *PARAMETROS),
                       DecryptRequest("026054 123875", 3, "367", 373, 17)]
        for solicitud in solicitudes:
            with self.subTest(solicitud=solicitud), self.assertRaises(ValueError):
                self.servicio.decrypt(solicitud)
        with self.assertRaises(ValueError):
            self.servicio.encrypt(EncryptRequest("RSA", "367", 373, 17))

    def test_rechaza_solicitud_incorrecta_para_encrypt(self):
        with self.assertRaises(ValueError):
            self.servicio.encrypt(None)

    def test_rechaza_solicitud_incorrecta_para_decrypt(self):
        with self.assertRaises(ValueError):
            self.servicio.decrypt(None)

    def test_propaga_errores_matematicos_y_de_contenido(self):
        with self.assertRaises(ValueError):
            self.servicio.encrypt(EncryptRequest("RSA", 367, 373, 2))
        with self.assertRaises(ValueError):
            self.servicio.encrypt(EncryptRequest("ñ", *PARAMETROS))
        with self.assertRaises(ValueError):
            self.servicio.decrypt(DecryptRequest("000000", 2, *PARAMETROS))


@unittest.skipUnless(
    TIENE_FORMATEADOR,
    "PENDIENTE: integrar formatear_cifrado real en logica/conversiones.py",
)
class IntegracionCompletaTests(unittest.TestCase):
    def setUp(self):
        self.servicio = RealRSAService()

    def test_formateador_real_conserva_ceros_y_separa_por_un_espacio(self):
        self.assertEqual(conversiones.formatear_cifrado([26054, 123875]), "026054 123875")
        self.assertEqual(conversiones.formatear_cifrado([0, 1, 999999]), "000000 000001 999999")

    def test_resultado_y_detalles_de_encriptacion(self):
        resultado = self.servicio.encrypt(EncryptRequest("RSA", *PARAMETROS))
        self.assertIsInstance(resultado, EncryptResult)
        self.assertEqual(resultado.ciphertext, "026054 123875")
        self.assertEqual(resultado.length, 3)
        self.assertEqual(resultado.public_key, (17, 136891))
        self.assertEqual((resultado.n, resultado.phi), (136891, 136152))
        self.assertTrue(resultado.padding_used)
        self.assertEqual(resultado.details, [
            DetailRow(1, "RS", "082 083", "082083", "026054"),
            DetailRow(2, "A ", "065 032", "065032", "123875"),
        ])

    def test_recuperacion_completa_y_direccion_de_la_tabla(self):
        for mensaje in ("AB", "RSA", "  Aa1!  z  ", " ", "  ", "A  ",
                        "".join(chr(i) for i in range(32, 127))):
            with self.subTest(mensaje=repr(mensaje)):
                enc = self.servicio.encrypt(EncryptRequest(mensaje, *PARAMETROS))
                dec = self.servicio.decrypt(DecryptRequest(enc.ciphertext, enc.length, *PARAMETROS))
                self.assertEqual(dec.message, mensaje)
                self.assertEqual(len(enc.details), (len(mensaje) + 1) // 2)
                self.assertEqual(len(enc.details), len(dec.details))
                for entrada, salida in zip(enc.details, dec.details):
                    self.assertEqual(entrada.characters, salida.characters)
                    self.assertEqual(entrada.input_block, salida.output_block)
                    self.assertEqual(entrada.output_block, salida.input_block)

    def test_otra_llave_publica_valida(self):
        enc = self.servicio.encrypt(EncryptRequest("RSA", 367, 373, 136169))
        self.assertEqual(enc.public_key, (136169, 136891))
        dec = self.servicio.decrypt(DecryptRequest(enc.ciphertext, enc.length, 367, 373, 136169))
        self.assertEqual(dec.message, "RSA")


if __name__ == "__main__":
    unittest.main()
