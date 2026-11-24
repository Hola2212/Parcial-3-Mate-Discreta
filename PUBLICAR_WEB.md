# Publicar la aplicación del grupo 14

La nueva entrada web es `streamlit_app.py`. El profesor usará una URL pública
en su navegador, sin instalar Python ni introducir credenciales.

## 1. Copiar los archivos al repositorio

Extraer este paquete en una carpeta aparte y copiar su contenido dentro del
repositorio clonado, junto a `main.py`. No crear otra carpeta que envuelva al
proyecto. Conservar la carpeta `.streamlit` con `config.toml` para el tema visual.
No hace falta copiar ningún historial de Git: este paquete no lo contiene.

Cambios principales: `streamlit_app.py`, `requirements.txt`, `.streamlit/config.toml`,
`logica/numeros.py`, dos ajustes de robustez en algoritmos/validaciones,
`tests/test_web.py` y documentación. `main.py` sigue abriendo la versión de escritorio.

## 2. Probar localmente (solo quien desarrolla)

Python recomendado para el despliegue: 3.12.

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

La dirección local que aparece en la terminal sirve para probar en tu equipo;
NO es la dirección que se entrega al profesor. Probar el ejemplo RSA, transferirlo,
desencriptarlo, abrir la tabla, introducir e=2 y comprobar los espacios originales.

Pruebas de lógica y flujo de datos:

```bash
python -m unittest discover -s tests -v
```

Las pruebas de flujo web simulan solo el estado de la sesión y usan el servicio
real. No equivalen a una comprobación visual en un navegador. La instalación
de Streamlit y la vista real deben verificarse en el equipo o en el despliegue.

## 3. Subir a GitHub

Comprobar primero `git status`. Si hay cambios de otra tarea, guardarlos antes.
Integrar esta versión en la rama que se vaya a desplegar mediante el flujo habitual
del equipo. Puede ser `logica-rsa` o `main`; la rama elegida debe contener TODOS
los archivos de esta versión.

```bash
git add streamlit_app.py requirements.txt .streamlit/config.toml
git add logica/algoritmos.py logica/validaciones.py logica/numeros.py
git add tests/test_web.py README.md PUBLICAR_WEB.md USO_IA.txt
git commit -m "Agregar aplicacion web RSA del grupo 14"
git push
```

Si Git rechaza el push o informa conflictos, resolverlos antes de publicar;
no usar `--force`. No es necesario subir un video ni otro ZIP para la nueva
solicitud del profesor: el entregable solicitado es la URL de la aplicación.

## 4. Crear la aplicación en Streamlit Community Cloud

1. Abrir https://share.streamlit.io/ e iniciar sesión con GitHub.
2. Seleccionar **Create app** y la opción para desplegar desde un repositorio.
3. Seleccionar el repositorio `Hola2212/Parcial-3-Mate-Discreta`, si sigue siendo
   el que utiliza el equipo. Elegir la rama a la que se subieron estos cambios.
4. En **Main file path**, escribir exactamente `streamlit_app.py`.
5. En **Advanced settings**, seleccionar Python **3.12** si está disponible.
6. No se requieren secretos ni contraseñas. Pulsar **Deploy**.
7. Esperar a que se instalen las dependencias y se abra la aplicación.

Para desplegar se necesitan permisos de administrador del repositorio. Si solo
eres colaboradora y no aparece o no permite desplegar, debe hacerlo su dueño,
concederte el permiso correspondiente o puedes crear un fork en tu cuenta.

## 5. Comprobar el enlace que se entregará

- Verificar en las opciones de compartir que la aplicación sea pública.
- Abrir la URL de la aplicación en una ventana privada sin iniciar sesión.
- Probar RSA con p=367, q=373 y e=17: C=026054 123875 y L=3.
- Pasar los datos a Desencriptar: debe recuperar RSA y mostrar d=8009.
- Comprobar n, phi, relleno, tabla ASCII y al menos un error, como e=2.
- Entregar únicamente la URL real que termina en `.streamlit.app`.

Community Cloud puede suspender una aplicación tras 12 horas sin tráfico.
Los visitantes pueden reactivarla con el botón de la pantalla de suspensión.
Abrir y comprobar la aplicación antes de la revisión; este servicio gratuito
no garantiza que permanezca siempre despierto.

## Documentación oficial

- Despliegue: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Permisos de GitHub: https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account
- Acceso público: https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app
- Suspensión por inactividad: https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app
