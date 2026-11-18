from .algoritmos import es_primo, mcd_euclides

def validar_parametros(p, q, e):
    if type(p) is not int or type(q) is not int or type(e) is not int:
        raise TypeError("p, q y e deben ser enteros.")
    if not es_primo(p):
        raise ValueError("p debe ser un número primo.")
    if not es_primo(q):
        raise ValueError("q debe ser un número primo.")
    
    if p == q:
        raise ValueError("p y q deben ser primos distintos.")
    n = p * q
    if not 126126 < n < 1000000:
        raise ValueError("n = p*q debe ser mayor que 126126 y menor que 1000000.")
    
    phi = (p - 1) * (q - 1)
    if e <= 1:
        raise ValueError("e debe ser mayor que 1.")
    
    if mcd_euclides(e, phi) != 1:
        raise ValueError("e y phi deben ser primos relativos.")
    return n, phi