"""Conversión decimal por segmentos, sin imponer una cota artificial a e."""

import re


def leer_entero_decimal(texto):
    if not isinstance(texto, str) or not re.fullmatch(r"[+-]?[0-9]+", texto):
        raise ValueError("Se requiere un entero decimal sin espacios.")
    signo = -1 if texto.startswith("-") else 1
    digitos = texto[1:] if texto[0] in "+-" else texto
    numero = 0
    for inicio in range(0, len(digitos), 9):
        parte = digitos[inicio:inicio + 9]
        numero = numero * (10 ** len(parte)) + int(parte)
    return signo * numero


def entero_a_decimal(numero):
    if numero < 0:
        return "-" + entero_a_decimal(-numero)
    partes = []
    while numero >= 1000000000:
        numero, resto = divmod(numero, 1000000000)
        partes.append(f"{resto:09d}")
    return str(numero) + "".join(reversed(partes))
