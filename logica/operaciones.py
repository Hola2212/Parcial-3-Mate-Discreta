"""Operaciones RSA, independientes de la interfaz y de contracts.py.

Se reutilizan los algoritmos, validaciones y conversiones del proyecto.
Los bloques cifrados se devuelven como enteros: rsa_service.py usará
formatear_cifrado para preparar el texto C que requiere la interfaz.
"""

from .algoritmos import exponenciacion_modular, inverso_modular
from .conversiones import bloques_a_mensaje, mensaje_a_bloques
from .validaciones import (
    validar_cifrado,
    validar_longitud,
    validar_parametros,
)


def encriptar(mensaje: str, p: int, q: int, e: int) -> dict:
    """Valida y cifra M; conserva los bloques para los detalles del proceso."""
    # Validar los parámetros también permite calcular n y phi.
    n, phi = validar_parametros(p, q, e)

    # Esta conversión valida ASCII, cuenta los espacios y agrega el relleno.
    bloques_originales, longitud, relleno = mensaje_a_bloques(mensaje)

    bloques_cifrados = []
    for bloque in bloques_originales:
        cifrado = exponenciacion_modular(bloque, e, n)
        bloques_cifrados.append(cifrado)

    return {
        "bloques_originales": bloques_originales,
        "bloques_cifrados": bloques_cifrados,
        "longitud": longitud,
        "relleno": relleno,
        "n": n,
        "phi": phi,
    }


def desencriptar(cifrado: str, longitud: int, p: int, q: int, e: int) -> dict:
    """Valida y recupera M, retirando únicamente el relleno indicado por L."""
    n, phi = validar_parametros(p, q, e)

    # Se comprueban el formato, c < n y la coherencia de L antes del cálculo.
    bloques_cifrados = validar_cifrado(cifrado, n)
    validar_longitud(longitud, len(bloques_cifrados))

    d = inverso_modular(e, phi)
    bloques_originales = []
    for bloque in bloques_cifrados:
        original = exponenciacion_modular(bloque, d, n)
        bloques_originales.append(original)

    # Esta conversión comprueba los ASCII y el espacio de relleno final.
    # Si L es impar retira exactamente un espacio; si es par no retira nada.
    mensaje = bloques_a_mensaje(bloques_originales, longitud)

    return {
        "mensaje": mensaje,
        "d": d,
        "bloques_originales": bloques_originales,
        "bloques_cifrados": bloques_cifrados,
        "longitud": longitud,
        "relleno": longitud % 2 != 0,
        "n": n,
        "phi": phi,
    }
