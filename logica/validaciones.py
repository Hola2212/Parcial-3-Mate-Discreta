from .algoritmos import es_primo, mcd_euclides
import re

def validar_parametros(p, q, e):
    if type(p) is not int or type(q) is not int or type(e) is not int:
        raise TypeError("p, q y e deben ser enteros.")
    if p < 2 or q < 2:
        raise ValueError("p y q deben ser primos mayores o iguales a 2.")
    
    if p == q:
        raise ValueError("p y q deben ser primos distintos.")
    n = p * q
    if not 126126 < n < 1000000:
        raise ValueError("n = p*q debe ser mayor que 126126 y menor que 1000000.")

    if not es_primo(p):
        raise ValueError("p debe ser un número primo.")
    if not es_primo(q):
        raise ValueError("q debe ser un número primo.")
    
    phi = (p - 1) * (q - 1)
    if e <= 1:
        raise ValueError("e debe ser mayor que 1.")
    
    if mcd_euclides(e, phi) != 1:
        raise ValueError("e y phi deben ser primos relativos.")
    return n, phi

def validar_mensaje(mensaje):
    if not isinstance(mensaje, str):
        raise TypeError("El mensaje debe ser una cadena de texto.")
    if mensaje == "": raise ValueError("El mensaje no puede estar vacío.")
    
    for pos, car in enumerate(mensaje, start=1):
        if not 32 <= ord(car) <= 126:
            raise ValueError(
                f"Carácter no permitido en la posición {pos}: "
                f"{car!r}. Solo se admite ASCII del 32 al 126."
            )

def validar_cifrado(cifrado, n):
    if not isinstance(cifrado, str): raise TypeError("El cifrado debe ser una cadena de texto.")
    if type(n) is not int: raise TypeError("n debe ser entero.")
    if n < 2: raise ValueError("n debe ser mayor o igual a 2.")
    if cifrado == "": raise ValueError("El cifrado no puede estar vacío.")
    
    patron = r"[0-9]{6}(?: +[0-9]{6})*"
    if re.fullmatch(patron, cifrado) is None: raise ValueError("El cifrado debe contener bloques de seis dígitos del 0 al 9, separados por espacios.")
    
    bloques = [int(bloque) for bloque in cifrado.split()]
    for posicion, bloque in enumerate(bloques, start=1):
        if not 0 <= bloque < n:
            raise ValueError(f"El bloque {posicion} debe ser mayor o igual a cero y menor que n ({n}).")
    return bloques

def validar_longitud(longitud, cantidad_bloques):
    if type(longitud) is not int or type(cantidad_bloques) is not int: raise TypeError("La longitud y la cantidad de bloques deben ser enteros.")
    if cantidad_bloques <= 0: raise ValueError("Debe existir al menos un bloque cifrado.")
    
    longitud_par = 2*cantidad_bloques
    longitud_impar = longitud_par - 1
    
    if longitud not in (longitud_par, longitud_impar): raise ValueError(f"Para {cantidad_bloques} bloques, la longitud original debe ser {longitud_impar} o {longitud_par}.")
