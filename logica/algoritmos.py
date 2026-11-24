def es_primo(n):
    if n <= 1: return False
    if n == 2: return True
    if n%2 == 0: return False
    
    i = 3
    while i * i <= n:
        if n % i == 0: return False
        i += 2
    return True

def mcd_euclides(a,b):
    if type(a) is not int or type(b) is not int:
        raise TypeError("Los argumentos deben ser enteros")
    if a <= 0 or b <= 0:
        raise ValueError("Los argumentos deben ser estrictamente positivos")
    
    def helper (a,b):
        if b == 0: return a
        return helper (b, a%b)
    
    if a > b: return helper(a,b)
    return helper(b,a)

def bezout(a,b):
    if type(a) is not int or type(b) is not int:
        raise TypeError("Los argumentos deben ser enteros")
    if a <= 0 or b <= 0:
        raise ValueError("Los argumentos deben ser estrictamente positivos")
    
    def helper (a,b):
        if b == 0: return (1,0)
        
        x,y = helper(b,a%b)
        q = a//b
        
        return (y, x - q*y)
    
    if a > b: 
        x,y = helper(a,b)
        return (x,y)
    
    y,x = helper(b,a)
    return (x,y)

def exponenciacion_modular(b, e, n):
    if type(e) is not int or type(b) is not int or type(n) is not int:
        raise TypeError("Los argumentos deben ser enteros")
    if b < 0 or e < 0:
        raise ValueError("La base y el exponente deben ser mayores o iguales a cero")
    
    if n < 2: raise ValueError("El módulo debe ser al menos 2")
    # Binaria iterativa: reduce cada producto y admite exponentes grandes
    # sin depender del límite de recursión de Python.
    resultado = 1
    factor = b % n
    while e:
        if e % 2:
            resultado = (resultado * factor) % n
        factor = (factor * factor) % n
        e //= 2
    return resultado

def inverso_modular(e,phi):
    if type(e) is not int or type(phi) is not int:
        raise TypeError("Los argumentos deben ser enteros")
    if e <= 0 or phi <= 1:
        raise ValueError("e debe ser positivo y phi debe ser mayor a 1")
    if mcd_euclides(e, phi) != 1: raise ValueError("e y phi deben ser primos relativos")
    x, y = bezout(e, phi)
    return x%phi
