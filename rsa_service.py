"""Adaptador entre la lógica RSA y los contratos que utiliza la interfaz.

No accede a widgets ni vuelve a implementar los algoritmos matemáticos.
La clase que debe recibir RSAApp es RealRSAService.
"""

from contracts import (
    DecryptRequest,
    DecryptResult,
    DetailRow,
    EncryptRequest,
    EncryptResult,
)
from logica.operaciones import desencriptar, encriptar


def _crear_detalles(bloques_originales, bloques_cifrados, desencriptando=False):
    """Construye una fila por pareja, conservando incluso el espacio de relleno."""
    detalles = []

    for numero, (original, cifrado) in enumerate(
        zip(bloques_originales, bloques_cifrados), start=1
    ):
        texto_original = f"{original:06d}"
        texto_cifrado = f"{cifrado:06d}"
        primer_ascii = texto_original[:3]
        segundo_ascii = texto_original[3:]
        pareja = chr(int(primer_ascii)) + chr(int(segundo_ascii))

        # La propia tabla aplica repr a characters para hacer visibles espacios.
        # Por eso aquí se guarda la pareja real, sin agregar comillas.
        entrada = texto_cifrado if desencriptando else texto_original
        salida = texto_original if desencriptando else texto_cifrado

        detalles.append(
            DetailRow(
                block=numero,
                characters=pareja,
                ascii_codes=f"{primer_ascii} {segundo_ascii}",
                input_block=entrada,
                output_block=salida,
            )
        )

    return detalles


class RealRSAService:
    """Cumple el protocolo RSAService de contracts.py mediante encrypt/decrypt."""

    def encrypt(self, request: EncryptRequest) -> EncryptResult:
        if not isinstance(request, EncryptRequest):
            raise ValueError("Se esperaba una solicitud EncryptRequest.")

        try:
            datos = encriptar(request.message, request.p, request.q, request.e)
        except TypeError as error:
            # El contrato exige ValueError; las validaciones existentes también
            # utilizan TypeError cuando un dato tiene un tipo incorrecto.
            raise ValueError(str(error)) from error

        # Importación local para poder probar decrypt aunque esta función de
        # conversiones todavía esté pendiente en la rama del compañero.
        try:
            from logica.conversiones import formatear_cifrado
        except ImportError as error:
            raise ValueError(
                "Falta integrar formatear_cifrado en logica/conversiones.py."
            ) from error

        try:
            cifrado = formatear_cifrado(datos["bloques_cifrados"])
        except TypeError as error:
            raise ValueError(str(error)) from error

        return EncryptResult(
            ciphertext=cifrado,
            length=datos["longitud"],
            public_key=(request.e, datos["n"]),
            n=datos["n"],
            phi=datos["phi"],
            padding_used=datos["relleno"],
            details=_crear_detalles(
                datos["bloques_originales"], datos["bloques_cifrados"]
            ),
        )

    def decrypt(self, request: DecryptRequest) -> DecryptResult:
        if not isinstance(request, DecryptRequest):
            raise ValueError("Se esperaba una solicitud DecryptRequest.")

        try:
            datos = desencriptar(
                request.ciphertext, request.length, request.p, request.q, request.e
            )
        except TypeError as error:
            raise ValueError(str(error)) from error

        return DecryptResult(
            message=datos["mensaje"],
            d=datos["d"],
            n=datos["n"],
            phi=datos["phi"],
            padding_removed=datos["relleno"],
            details=_crear_detalles(
                datos["bloques_originales"], datos["bloques_cifrados"],
                desencriptando=True,
            ),
        )
