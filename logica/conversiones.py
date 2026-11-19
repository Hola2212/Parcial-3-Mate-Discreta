from .validaciones import validar_mensaje, validar_longitud

def mensaje_a_bloques(mensaje: str) -> tuple[list[int], int, bool]:
    validar_mensaje(mensaje)
    longitud = len(mensaje)
    relleno = longitud % 2 != 0
    mensaje_preparado = mensaje
    
    if relleno: mensaje_preparado += " "
    bloques = []
    
    for posicion in range(0, len(mensaje_preparado), 2):
        pareja = mensaje_preparado[posicion:posicion + 2]
        codigo_primero = f"{ord(pareja[0]):03d}"
        codigo_segundo = f"{ord(pareja[1]):03d}"
        bloque = int(codigo_primero + codigo_segundo)
        bloques.append(bloque)
    return bloques, longitud, relleno

def bloques_a_mensaje(bloques: list[int], longitud: int) -> str:
    if not isinstance(bloques, list): raise TypeError("Los bloques deben proporcionarse como una lista.")
    
    validar_longitud(longitud, len(bloques))
    caracteres = []
    
    for posicion, bloque in enumerate(bloques, start=1):
        if type(bloque) is not int: raise TypeError(f"El bloque {posicion} debe ser un entero.")
        if not 0 <= bloque <= 999999: raise ValueError(f"El bloque {posicion} no puede representarse con seis dígitos.")
        
        bloque_formateado = f"{bloque:06d}"
        codigo_primero = int(bloque_formateado[:3])
        codigo_segundo = int(bloque_formateado[3:])
        if not (32 <= codigo_primero <= 126 and 32 <= codigo_segundo <= 126): raise ValueError(f"El bloque {posicion} contiene códigos ASCII fuera del rango permitido.")
        
        caracteres.append(chr(codigo_primero))
        caracteres.append(chr(codigo_segundo))
    
    mensaje = "".join(caracteres)
    if longitud % 2 != 0:
        if mensaje[-1] != " ": raise ValueError("El mensaje recuperado no contiene el espacio de relleno esperado.")
        
        mensaje = mensaje[:-1]
    return mensaje
