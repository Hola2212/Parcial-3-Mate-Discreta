# Proyecto RSA — MM2015 Matemática Discreta 1

## Integrantes

- Juan Pablo Flores Chávez.
- Zabdi Soham Pelicó Hernández.
- Grupo 14.

## Requisitos y ejecución

Python 3.10 o posterior, con Tkinter instalado.

Solo se utiliza la biblioteca estándar de Python. No se necesitan paquetes
externos ni instalación mediante pip.

1. Extraer completamente el ZIP.
2. Abrir una terminal en la carpeta que contiene main.py.
3. Ejecutar:

    python main.py

En Windows también puede usarse `py main.py`; en Linux/macOS,
`python3 main.py`.

Tkinter normalmente se incluye con Python en Windows. En Ubuntu/Debian,
si falta, instalar el paquete de sistema `python3-tk`.

La aplicación necesita una sesión de escritorio. No necesita Internet ni
recursos externos y no utiliza rutas absolutas.

## Acceso de demostración

| Usuario | Contraseña | Rol |
| --- | --- | --- |
| estudiante1 | rsa2026 | Estudiante |
| estudiante2 | rsa2026 | Estudiante |
| admin | admin2026 | Administrador |

Las tres cuentas permiten realizar las mismas operaciones.
Son cuentas locales de demostración, sin registro ni base de datos.

## Encriptar

1. Abrir Encriptar.
2. Introducir el mensaje M, los primos p y q y el exponente e.
3. Pulsar Encriptar.
4. Consultar C, L, la llave pública (e, n), n, phi y el relleno utilizado.
5. Abrir los detalles para consultar caracteres, ASCII y bloques.
6. Conservar C y L por separado.

Los botones Copiar cifrado y Copiar longitud L permiten copiar esos datos.

Activar “Mostrar datos privados (p, q, phi y d)” para consultar los valores
ocultos. Este control solo cambia su visibilidad.

## Desencriptar

1. Abrir Desencriptar.
2. Introducir C, longitud original L y los mismos p, q y e.
3. Pulsar Desencriptar.
4. Consultar el mensaje recuperado, d, n, phi y el relleno retirado.
5. Abrir los detalles para ver los bloques y caracteres recuperados.

El cifrado debe contener bloques de seis dígitos separados por espacios,
sin saltos de línea ni espacios en los extremos.

Editar las entradas invalida los resultados anteriores. Los errores se
muestran en la interfaz sin cerrar la aplicación. Limpiar vacía los campos.

## Ejemplo completo del enunciado

Las comillas delimitan los mensajes y no deben escribirse.

| Dato | Valor |
| --- | --- |
| Mensaje M | "RSA" |
| p | 367 |
| q | 373 |
| e | 17 |
| n | 136891 |
| phi | 136152 |
| MCD(e, phi) | 1 |
| L | 3 |
| Texto con relleno | "RSA " |
| Bloques ASCII | 082083 065032 |
| C | 026054 123875 |
| Llave pública | (17, 136891) |
| d | 8009 |
| Llave privada | (8009, 136891) |
| Mensaje recuperado | "RSA" |

Para recuperar el ejemplo, ingresar C = 026054 123875, L = 3,
p = 367, q = 373 y e = 17.

## Reglas matemáticas y relleno

- p y q deben ser enteros primos distintos.
- Debe cumplirse 126126 < p*q < 1000000.
- e debe ser entero, mayor que 1 y primo relativo con phi.
- e puede ser compuesto y puede ser mayor que phi.
- Solo se admiten caracteres ASCII imprimibles del 32 al 126.
- Se rechazan ñ, tildes, emojis, tabulaciones y saltos de línea.
- No se sustituyen ni eliminan caracteres inválidos automáticamente.
- Cada carácter se representa con tres dígitos; cada pareja forma un bloque.
- Cada bloque cifrado se escribe con exactamente seis dígitos.
- L cuenta todos los caracteres originales, incluidos los espacios.
- Si L es impar se agrega exactamente un espacio ASCII 032.
- Al recuperar, se comprueba y retira únicamente ese espacio adicional.
- Si L es par no se retira ningún carácter.
- Nunca se aplica strip ni rstrip al mensaje para retirar el relleno.
- Con k bloques, L debe ser 2k o 2k-1.
- Se comprueban el rango de C, los ASCII recuperados y el relleno.
- El mensaje vacío se rechaza; un mensaje formado por espacios sí se acepta.

C y L deben conservarse juntos. Por ejemplo, el cifrado del ejemplo con
L = 4 recupera "RSA ", mientras que con L = 3 recupera "RSA".

## Organización y algoritmos propios

| Archivo / función | Responsabilidad |
| --- | --- |
| main.py | Inicia RSAApp con RealRSAService |
| contracts.py | Solicitudes, resultados y filas de detalles |
| logica/algoritmos.py: es_primo | Primalidad mediante división de prueba |
| logica/algoritmos.py: mcd_euclides | Máximo común divisor mediante Euclides |
| logica/algoritmos.py: bezout e inverso_modular | Euclides extendido e inverso modular |
| logica/algoritmos.py: exponenciacion_modular | Exponenciación binaria iterativa |
| logica/validaciones.py | Validaciones de parámetros, mensaje, C y L |
| logica/conversiones.py | Parejas ASCII, relleno y formato del cifrado |
| logica/operaciones.py | Encriptación y desencriptación |
| logica/numeros.py | Conversión decimal de enteros extensos |
| rsa_service.py | Conecta la lógica con los contratos y prepara la tabla |
| ui/ | Interfaz gráfica |
| users.py | Cuentas de demostración |
| tests/ | Pruebas automatizadas |

No se utilizan math.gcd, pow modular, inversos de biblioteca ni paquetes
criptográficos. La exponenciación reduce módulo n en cada multiplicación;
no calcula primero la potencia completa.

## Pruebas

Desde la carpeta que contiene main.py:

    python -m unittest discover -s tests -v

La revisión incluye 29 pruebas de lógica y servicio. Se comprueban:

- El ejemplo oficial y los ceros iniciales del cifrado.
- Mensajes pares e impares.
- Mayúsculas, minúsculas, números y signos.
- Espacios iniciales, finales y consecutivos.
- Las 9025 parejas ASCII permitidas.
- Parámetros inválidos y caracteres no admitidos.
- Formato de C, bloques fuera de rango y longitudes inconsistentes.
- ASCII recuperados inválidos y relleno inconsistente.
- Resultados tipados y detalles de las tablas.
- Exponentes válidos grandes y conversiones decimales extensas.

Las pruebas automáticas no sustituyen la revisión visual de la interfaz.

## Video y entrega

El enlace accesible estará en ENLACE_VIDEO.txt.

La asistencia con inteligencia artificial se describe en USO_IA.txt.