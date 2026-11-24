"""Interfaz web pública; reutiliza el servicio y los algoritmos del proyecto.

Ejecutar: python -m streamlit run streamlit_app.py
No importa Tkinter, no almacena mensajes en archivos ni requiere autenticación.
"""

import streamlit as st

from contracts import DecryptRequest, EncryptRequest
from logica.numeros import entero_a_decimal, leer_entero_decimal
from rsa_service import RealRSAService


def invalidar(prefijo):
    st.session_state[prefijo + "_resultado"] = None
    st.session_state[prefijo + "_error"] = ""


def cargar_ejemplo(prefijo, espacios=False):
    invalidar(prefijo)
    for nombre, valor in (("p", "367"), ("q", "373"), ("e", "17")):
        st.session_state[f"{prefijo}_{nombre}"] = valor
    if prefijo == "enc":
        st.session_state["enc_texto"] = "  Aa1!  z  " if espacios else "RSA"
    else:
        st.session_state["dec_texto"] = "026054 123875"
        st.session_state["dec_l"] = "3"
        st.session_state["dec_aviso"] = ""


def limpiar(prefijo):
    invalidar(prefijo)
    for nombre in ("texto", "p", "q", "e"):
        st.session_state[f"{prefijo}_{nombre}"] = ""
    if prefijo == "dec":
        st.session_state["dec_l"] = ""
        st.session_state["dec_aviso"] = ""


def ejecutar(prefijo):
    invalidar(prefijo)
    try:
        parametros = []
        for nombre in ("p", "q", "e"):
            try:
                numero = leer_entero_decimal(st.session_state[f"{prefijo}_{nombre}"])
            except ValueError:
                raise ValueError(f"{nombre} debe ser un entero decimal, sin espacios ni letras.") from None
            parametros.append(numero)
        servicio = RealRSAService()
        texto = st.session_state[f"{prefijo}_texto"]
        if prefijo == "enc":
            resultado = servicio.encrypt(EncryptRequest(texto, *parametros))
            st.session_state["enc_parametros"] = tuple(parametros)
        else:
            try:
                longitud = leer_entero_decimal(st.session_state["dec_l"])
            except ValueError:
                raise ValueError("L debe ser un entero decimal.") from None
            resultado = servicio.decrypt(DecryptRequest(texto, longitud, *parametros))
        st.session_state[prefijo + "_resultado"] = resultado
    except (ValueError, TypeError) as error:
        st.session_state[prefijo + "_error"] = str(error)


def transferir():
    resultado = st.session_state["enc_resultado"]
    if resultado is None:
        return
    invalidar("dec")
    st.session_state["dec_texto"] = resultado.ciphertext
    st.session_state["dec_l"] = str(resultado.length)
    for nombre, numero in zip(("p", "q", "e"), st.session_state["enc_parametros"]):
        st.session_state[f"dec_{nombre}"] = entero_a_decimal(numero)
    st.session_state["dec_aviso"] = "C, L, p, q y e transferidos. Pulsa Desencriptar mensaje."


def mostrar_tabla(resultado, descifrando=False):
    st.subheader("Proceso por bloques")
    st.caption("Las comillas de la columna Pareja permiten ver los espacios. No forman parte del mensaje.")
    filas = []
    for fila in resultado.details:
        filas.append({
            "#": fila.block,
            "Pareja (repr)": repr(fila.characters),
            "ASCII (3 + 3)": fila.ascii_codes,
            "Entrada c" if descifrando else "Entrada m": fila.input_block,
            "Salida m" if descifrando else "Salida c": fila.output_block,
        })
    st.dataframe(filas, hide_index=True, use_container_width=True)
    st.caption("m = c^d mod n" if descifrando else "c = m^e mod n")


def mostrar_resultado(prefijo):
    resultado = st.session_state[prefijo + "_resultado"]
    if st.session_state[prefijo + "_error"]:
        st.error(st.session_state[prefijo + "_error"])
    if resultado is None:
        st.info("Completa las entradas y ejecuta la operación para ver el resultado.")
        return
    descifrando = prefijo == "dec"
    st.success("Mensaje recuperado correctamente." if descifrando else "Encriptación completada.")
    st.subheader("Mensaje recuperado M" if descifrando else "Cifrado C")
    st.code(resultado.message if descifrando else resultado.ciphertext, language=None)
    a, b, c = st.columns(3)
    a.metric("Módulo n", str(resultado.n))
    b.metric("φ (phi)", str(resultado.phi))
    longitud = len(resultado.message) if descifrando else resultado.length
    c.metric("Longitud original L", str(longitud))
    if descifrando:
        st.write(f"**Exponente privado d:** {resultado.d}")
        st.write(f"**Llave privada (d, n):** ({resultado.d}, {resultado.n})")
        st.write("**Relleno retirado:** " + ("Sí, exactamente un espacio." if resultado.padding_removed else "No."))
        st.caption("Mensaje entre comillas, para verificar sus espacios:")
        st.code(repr(resultado.message), language=None)
        st.download_button("Descargar mensaje exacto", data=resultado.message.encode("ascii"),
                           file_name="mensaje_recuperado.txt", mime="text/plain",
                           key="dec_descarga", on_click="ignore")
    else:
        e, n = resultado.public_key
        llave = f"({entero_a_decimal(e)}, {n})"
        st.caption("Llave pública (e, n)")
        st.code(llave, language=None)
        st.write("**Relleno utilizado:** " + ("Sí, un espacio ASCII 032." if resultado.padding_used else "No."))
        st.write("**MCD(e, φ):** 1")
        st.button("Pasar C y L a desencriptación", key="transferir", on_click=transferir)
        st.caption("Después abre la pestaña Desencriptar. El botón también copia p, q y e.")
        st.download_button("Descargar C y L", data=f"C: {resultado.ciphertext}\nL: {resultado.length}\nLlave publica (e, n): {llave}\n",
                           file_name="cifrado_rsa.txt", mime="text/plain", key="enc_descarga", on_click="ignore")


def mostrar_operacion(prefijo):
    descifrando = prefijo == "dec"
    izquierda, derecha = st.columns([1, 1], gap="large")
    with izquierda:
        st.subheader("Entradas")
        if descifrando and st.session_state["dec_aviso"]:
            st.info(st.session_state["dec_aviso"])
        st.text_area("Cifrado C" if descifrando else "Mensaje original M",
                     key=prefijo + "_texto", height=130, on_change=invalidar, args=(prefijo,),
                     help="Bloques de seis dígitos separados por espacios." if descifrando else
                     "ASCII 32 a 126. Los espacios iniciales y finales cuentan; no uses tildes, ñ ni saltos de línea.")
        if not descifrando:
            st.caption(f"{len(st.session_state['enc_texto'])} caracteres, incluidos todos los espacios.")
        primero, segundo, tercero = st.columns(3)
        for columna, nombre, etiqueta in ((primero, "p", "Primo p"), (segundo, "q", "Primo q"), (tercero, "e", "Exponente e")):
            with columna:
                st.text_input(etiqueta, key=f"{prefijo}_{nombre}", on_change=invalidar, args=(prefijo,))
        if descifrando:
            st.text_input("Longitud original L", key="dec_l", on_change=invalidar, args=(prefijo,))
        st.button("Desencriptar mensaje" if descifrando else "Encriptar mensaje",
                  type="primary", key=prefijo + "_ejecutar", on_click=ejecutar, args=(prefijo,))
        ejemplo, vaciar = st.columns(2)
        ejemplo.button("Cargar ejemplo RSA", key=prefijo + "_ejemplo", on_click=cargar_ejemplo, args=(prefijo,))
        vaciar.button("Limpiar", key=prefijo + "_limpiar", on_click=limpiar, args=(prefijo,))
        if not descifrando:
            st.button("Ejemplo con espacios", key="enc_espacios", on_click=cargar_ejemplo, args=("enc", True))
    with derecha:
        st.subheader("Resultado")
        mostrar_resultado(prefijo)
    resultado = st.session_state[prefijo + "_resultado"]
    if resultado is not None:
        st.divider()
        mostrar_tabla(resultado, descifrando)


def main():
    st.set_page_config(page_title="RSA LAB · Grupo 14", page_icon="🔐", layout="wide")
    defaults = {"enc_texto": "RSA", "dec_texto": "", "dec_l": "", "dec_aviso": ""}
    for prefijo in ("enc", "dec"):
        defaults.update({f"{prefijo}_p": "367", f"{prefijo}_q": "373", f"{prefijo}_e": "17",
                         prefijo + "_resultado": None, prefijo + "_error": ""})
    for clave, valor in defaults.items():
        st.session_state.setdefault(clave, valor)

    st.caption("MM2015 / MATEMÁTICA DISCRETA 1 / GRUPO 14")
    st.title("RSA / Laboratorio de criptografía")
    st.write("Encripta y recupera mensajes con algoritmos propios en Python.")
    st.caption("Juan Pablo Flores Chávez · Zabdi Soham Pelicó Hernández")
    encriptar_tab, desencriptar_tab, guia_tab = st.tabs(["Encriptar", "Desencriptar", "Cómo funciona"])
    with encriptar_tab:
        mostrar_operacion("enc")
    with desencriptar_tab:
        mostrar_operacion("dec")
    with guia_tab:
        st.subheader("Reglas del proyecto")
        st.markdown("""
- p y q deben ser **primos distintos** y cumplir **126126 < p·q < 1000000**.
- e es un entero mayor que 1, con **MCD(e, φ) = 1**; puede ser mayor que φ.
- Se admiten códigos **ASCII 32 a 126**, incluidos espacios, mayúsculas, números y signos.
- Cada pareja se convierte en dos códigos de tres dígitos. `AB` → `065066`.
- Si L es impar, se agrega **un espacio**. Al recuperar se comprueba y retira solo ese relleno.
- **Conserva C y L por separado**: C tiene bloques de seis dígitos separados por espacios.
- Los detalles muestran las parejas, sus ASCII y los bloques antes y después de la operación.
        """)
        st.subheader("Ejemplo del enunciado")
        st.code("M = 'RSA'\np = 367; q = 373; e = 17\nn = 136891; phi = 136152\nL = 3; relleno = un espacio\nC = 026054 123875\nd = 8009; M recuperado = 'RSA'", language=None)
        st.write("Algoritmos propios: Euclides, Bézout, inverso modular y exponenciación modular binaria.")
    st.divider()
    st.caption("Proyecto académico · Aplicación pública sin credenciales · Los mensajes se procesan en la sesión y no se guardan en archivos.")


if __name__ == "__main__":
    main()
