# Proyecto RSA — MM2015 Matemática Discreta 1

## Integrantes

- Juan Pablo Flores Chávez.
- Zabdi Soham Pelicó Hernández.
- Grupo 14.

## Versión web para la revisión en línea

La entrada pública es **`streamlit_app.py`**, implementada con Streamlit y el
mismo `RealRSAService` del proyecto. No requiere login. Permite encriptar,
desencriptar, consultar n, phi, d, L, relleno, ASCII y tablas de bloques.
Incluye ejemplos y transferencia de C, L y parámetros entre operaciones.

Para ejecutar localmente (solo los desarrolladores):

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Python recomendado para la versión web: **3.12**. `requirements.txt` fija
Streamlit 1.51.0. No hay bibliotecas externas de criptografía.

Para publicarla y obtener la URL que se entrega al profesor, seguir
**`PUBLICAR_WEB.md`**. El profesor solo abre la URL pública del despliegue:
no instala Python ni dependencias. La dirección localhost no es pública.
La URL definitiva se obtiene después del despliegue; no se incluye una inventada.

La interfaz Tkinter original sigue disponible mediante `python main.py`.
Las cuentas descritas abajo corresponden únicamente a esa versión de escritorio.

## Versión de escritorio: requisitos y ejecución

Python 3.10 o posterior, con Tkinter instalado.

La versión de escritorio utiliza la biblioteca estándar y Tkinter.
La versión web utiliza además Streamlit, declarado en requirements.txt.

1. Extraer completamente el ZIP.
2. Abrir una terminal en la carpeta que contiene main.py.
3. Ejecutar:

    python main.py

En Windows también puede usarse `py main.py`; en Linux/macOS,
`python3 main.py`.

Tkinter normalmente se incluye con Python en Windows. En Ubuntu/Debian,
si falta, instalar el paquete de sistema `python3-tk`.

La interfaz Tkinter necesita una sesión de escritorio; la web funciona en el
navegador. La lógica RSA no utiliza rutas absolutas ni recursos externos.

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
| streamlit_app.py | Interfaz pública en el navegador |
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

La versión web incluye 32 pruebas de lógica, servicio y flujo de datos. Se comprueban:

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
Las ocho pruebas de flujo web simulan el estado de Streamlit y ejecutan el
servicio real; no prueban la instalación de Streamlit ni el navegador.
En el entorno de preparación no se pudo instalar Streamlit por restricciones
de acceso al índice de paquetes. Verificar la apertura real al probar localmente
o publicar, siguiendo PUBLICAR_WEB.md.

## Entrega

Para la nueva revisión solicitada por el profesor se entrega únicamente la URL
pública de la aplicación funcionando. La publicación aún debe realizarse desde
la cuenta de Streamlit/GitHub del equipo. El video corresponde a la entrega
anterior y no sustituye el enlace de la aplicación.

La asistencia con inteligencia artificial se describe en USO_IA.txt.