# Instrucciones Parcial 3 - Proyecto

Interfaz de demostración para MM2015. Incluye login local, navegación, formularios,
validaciones de formato, salidas seleccionables y una ventana auxiliar de detalles.


## Archivos

```text
Parcial_3_Proyecto/
├── main.py
├── contracts.py
├── users.py
├── instrucciones Parcial 3 - Proyecto.md
├── .gitignore
├── USO_IA.txt
└── ui/
    ├── __init__.py
    ├── app.py
    ├── screens.py
    ├── theme.py
    └── widgets.py
```

El código completo está en los archivos Python de esta carpeta.

## Ejecución

Requiere Python 3.10 o posterior con tkinter disponible. No utiliza paquetes
externos ni necesita requirements.txt. En Windows, tkinter normalmente se incluye
con Python; si falta, modifica la instalación de Python para incluir Tcl/Tk.

Desde esta carpeta ejecuta:

```powershell
python main.py
```

También puedes ejecutar `python Parcial_3_Proyecto/main.py` desde la carpeta superior.
Hay tres cuentas locales de demostración:

| Usuario | Contraseña | Rol |
| --- | --- | --- |
| `estudiante1` | `rsa2026` | Estudiante |
| `estudiante2` | `rsa2026` | Estudiante |
| `admin` | `admin2026` | Administrador |

Enter permite enviar el formulario de acceso. El usuario y su rol se muestran
durante la sesión. Las tres cuentas acceden a las mismas funciones actuales;
no se han definido permisos exclusivos del administrador. Las credenciales de
demostración están en `users.py`, sin registro ni base de datos. No son un sistema
de autenticación de producción. Cerrar sesión limpia la identidad y los formularios.

## Uso

La ventana abre centrada al 80% del ancho y del alto de la pantalla, sin forzar
pantalla completa ni maximización. Puedes redimensionarla libremente.
La cabecera tiene una animación decorativa y las tarjetas y botones reaccionan
al cursor. Los formularios muestran contadores de caracteres, progreso de campos
y resaltado de enteros con formato incorrecto mientras escribes. Este progreso
solo indica formato básico, no verifica la validez matemática de los parámetros.
Usa Ctrl+Enter dentro de las entradas para solicitar la operación.

- **Inicio:** presenta las funcionalidades y el estado de desarrollo.
- **Encriptar:** recibe el mensaje original y p, q, e. Prepara salidas para C, L,
  llave pública, n, phi y relleno.
- **Desencriptar:** recibe C, L, p, q, e. Prepara salidas para el mensaje, d, n,
  phi y relleno retirado.
- **Detalles:** abre una única ventana con tabla desplazable. Sin resultados
  integrados muestra un estado vacío.
- **Ayuda:** explica entradas, ASCII, conservación de C y L y manejo del relleno.

Mientras no exista un servicio matemático, los botones de operación muestran
“Lógica RSA pendiente de integrar”. No se presentan resultados ficticios.
Las acciones de copia se habilitan al recibir resultados. Modificar entradas o
limpiar invalida resultados previos. Los campos de salida permiten seleccionar
y copiar, pero no editarlos. Tab y Mayús+Tab permiten recorrer controles.

Para explorar el formulario de encriptación puedes ingresar `RSA`, p `367`, q
`373` y e `17`: se comprobará el formato y se mostrará el aviso de lógica pendiente.
Esto no ejecuta el ejemplo matemático del parcial.

## Comprobaciones manuales

- Ingresar con campos vacíos, credenciales incorrectas y credenciales demo.
- Enviar con Enter y alternar la visibilidad de contraseña.
- Recorrer las cuatro pantallas con el menú y los controles con Tab/Mayús+Tab.
- Ingresar enteros incorrectos y bloques cifrados mal formados: comprobar errores.
- Enviar entradas con formato válido: comprobar el aviso de lógica pendiente.
- Escribir espacios al principio y al final: verificar que permanecen en el campo.
- Confirmar que las salidas no se editan y las copias están deshabilitadas sin datos.
- Abrir detalles varias veces: verificar que se reutiliza una única ventana.
- Redimensionar y comprobar desplazamiento en formularios y tabla.
- Limpiar, cerrar sesión y volver a ingresar: verificar campos y resultados vacíos.
- Tras integrar RSA, comprobar resultados, copia exacta, detalles y manejo de errores.

Este documento describe el uso de la interfaz actual; no sustituye al README final del proyecto
RSA completo. La declaración sobre IA se encuentra en USO_IA.txt.

## Verificación realizada

Se comprobó la compilación de todos los módulos y se ejecutó una prueba de widgets
Tk con la ventana principal oculta: acceso vacío/incorrecto/correcto, navegación,
formatos inválidos, aviso pendiente, conservación de espacios, reutilización de
detalles, presentación y copia de datos de prueba, invalidación de resultados,
limpieza y cierre/reinicio de sesión. Los datos artificiales se usaron solamente
en la prueba y no forman parte de la aplicación. No se comprobó visualmente la
apariencia en pantalla; la lista manual anterior queda disponible para esa revisión.

## Carpeta para el repositorio

Esta carpeta contiene únicamente el proyecto y sus instrucciones de uso.
La guía de implementación GUIA_PARCIAL_3.txt se mantiene fuera.
El repositorio Git no está inicializado; puedes crearlo desde esta carpeta.
El archivo .gitignore excluye cachés de Python, entornos virtuales y archivos del editor.
