"""Pantallas y eventos de presentación; sin cálculos RSA."""
import re
import tkinter as tk
from tkinter import ttk

from contracts import DecryptRequest, EncryptRequest, PENDING
from users import authenticate, credentials_help
from ui import theme as t
from ui.widgets import CyberBanner, ScrollFrame, TextBox


class LoginScreen(ScrollFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.body.columnconfigure(0, weight=1)
        self.body.bind("<Configure>", self._center_form, add="+")
        CyberBanner(self.body).grid(sticky="ew", pady=(12, 22))
        ttk.Label(self.body, text="Bienvenido al laboratorio", style="Heading.TLabel").grid(sticky="w", pady=(0, 8))
        ttk.Label(self.body, text="Acceso de demostración para explorar la interfaz.\n"
                  "Tres cuentas locales con roles; sin registro ni base de datos.",
                  style="Muted.TLabel", wraplength=460).grid(sticky="w", pady=18)
        ttk.Label(self.body, text="Usuario").grid(sticky="w")
        self.username = ttk.Entry(self.body)
        self.username.grid(sticky="ew", pady=(4, 16))
        ttk.Label(self.body, text="Contraseña").grid(sticky="w")
        self.password = ttk.Entry(self.body, show="•")
        self.password.grid(sticky="ew", pady=4)
        self.visible = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.body, text="Mostrar contraseña", variable=self.visible,
                        command=lambda: self.password.configure(show="" if self.visible.get() else "•")).grid(sticky="w")
        self.status = ttk.Label(self.body, foreground=t.ERROR, wraplength=460)
        self.status.grid(sticky="w", pady=10)
        ttk.Button(self.body, text="Ingresar →", style="Primary.TButton",
                   command=self.submit).grid(sticky="ew", pady=8)
        ttk.Label(self.body, text="Cuentas de demostración:\n" + credentials_help(),
                  style="Accent.TLabel", wraplength=480).grid(sticky="w", pady=16)
        for widget in (self.username, self.password):
            widget.bind("<Return>", lambda event: self.submit())
            widget.bind("<KeyRelease>", lambda event: self.status.configure(text=""))

    def _center_form(self, event):
        self.body.configure(padding=(max(24, (event.width - 540) // 2), 24))

    def submit(self):
        if not self.username.get() or not self.password.get():
            self.status.configure(text="Ingresa el usuario y la contraseña.")
            return
        user = authenticate(self.username.get(), self.password.get())
        if user is None:
            self.status.configure(text="Credenciales incorrectas. Usa las credenciales de demostración.")
            return
        self.app.open_session(user)


class InfoScreen(ScrollFrame):
    def __init__(self, parent, title, sections):
        super().__init__(parent)
        self.body.columnconfigure(0, weight=1)
        CyberBanner(self.body).grid(sticky="ew", pady=(0, 22))
        ttk.Label(self.body, text=title, style="Title.TLabel").grid(sticky="w", pady=(0, 20))
        self.paragraphs = []
        for index, (heading, text) in enumerate(sections, start=1):
            card = tk.Frame(self.body, bg=t.PANEL, highlightthickness=1,
                            highlightbackground="#203743", padx=18, pady=14)
            card.grid(sticky="ew", pady=7)
            card.columnconfigure(0, weight=1)
            heading_label = ttk.Label(card, text=f"{index:02d} / {heading}", style="CardHeading.TLabel")
            heading_label.grid(sticky="w", pady=(0, 8))
            label = ttk.Label(card, text=text, wraplength=640, justify="left", style="Card.TLabel")
            label.grid(sticky="ew", pady=(0, 10))
            # La tarjeta reacciona al cursor sin mover el contenido.
            for widget in (card, heading_label, label):
                widget.bind("<Enter>", lambda event, target=card: target.configure(highlightbackground=t.CYAN))
                widget.bind("<Leave>", lambda event, target=card: target.configure(highlightbackground="#203743"))
            self.paragraphs.append(label)
        self.body.bind("<Configure>", self._wrap, add="+")

    def _wrap(self, event):
        for label in self.paragraphs:
            label.configure(wraplength=max(180, event.width - 60))


class OperationScreen(ScrollFrame):
    def __init__(self, parent, app, decrypt=False):
        super().__init__(parent)
        self.app = app
        self.decrypt = decrypt
        self.operation = "Desencriptación" if decrypt else "Encriptación"
        self.mensaje_inicial = (
            "Ingresa el cifrado, la longitud original y los parámetros RSA."
            if decrypt
            else "Ingresa el mensaje y los parámetros RSA."
        )
        self.details = []
        self.result = None
        self.mostrar_privados = tk.BooleanVar(value=False)
        self.campos_privados = []
        self.body.columnconfigure(0, weight=1)
        ttk.Label(self.body, text=self.operation, style="Title.TLabel").grid(sticky="w")
        ttk.Label(self.body, text="01 / ENTRADAS", style="Heading.TLabel").grid(sticky="w", pady=(22, 12))
        ttk.Label(self.body, text="Cifrado C" if decrypt else "Mensaje original").grid(sticky="w")
        self.content = TextBox(self.body)
        self.content.grid(sticky="ew", pady=(6, 8))
        self.input_feedback = ttk.Label(self.body, text="0 caracteres", style="Accent.TLabel")
        self.input_feedback.grid(sticky="w", pady=(0, 6))
        ttk.Label(self.body, text="Bloques de seis dígitos separados por espacios." if decrypt
                  else "Los espacios iniciales, finales y consecutivos se conservan.",
                  style="Muted.TLabel", wraplength=420).grid(sticky="w", pady=(0, 12))
        parameters = ttk.Frame(self.body)
        parameters.grid(sticky="ew")
        self.entries = {}
        keys = [("p", "Primo p"), ("q", "Primo q"), ("e", "Exponente e")]
        if decrypt:
            keys.append(("length", "Longitud L"))
        for index, (key, label) in enumerate(keys):
            row, column = divmod(index, 2)
            parameters.columnconfigure(column, weight=1, uniform="params")
            cell = ttk.Frame(parameters, padding=(0, 4, 12, 8))
            cell.grid(row=row, column=column, sticky="ew")
            cell.columnconfigure(0, weight=1)
            ttk.Label(cell, text=label).grid(sticky="w")
            es_privado = key in ("p", "q")
            entry = ttk.Entry(
                cell,
                width=12,
                show="*" if es_privado else "",
            )
            entry.grid(sticky="ew", pady=5)
            
            self.entries[key] = entry
            if es_privado:
                self.campos_privados.append(entry)
            
        ttk.Checkbutton(
            self.body,
            text="Mostrar datos privados (p, q, phi y d)",
            variable=self.mostrar_privados,
            command=self._alternar_privados,
        ).grid(sticky="w", pady=(8, 4))
        
        self.readiness = ttk.Label(self.body, text="Completa las entradas para continuar.",
                                    style="Muted.TLabel")
        self.readiness.grid(sticky="w", pady=(8, 4))
        self.progress = ttk.Progressbar(self.body, maximum=len(keys) + 1,
                                        style="Ready.Horizontal.TProgressbar", takefocus=False)
        self.progress.grid(sticky="ew", pady=(0, 6))
        actions = ttk.Frame(self.body)
        actions.grid(sticky="ew", pady=12)
        ttk.Button(actions, text="Desencriptar" if decrypt else "Encriptar",
                   style="Primary.TButton", command=self.request_operation).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(actions, text="Limpiar", command=self.clear).grid(row=0, column=1)
        self.status = ttk.Label(
            self.body,
            text=self.mensaje_inicial,
            foreground=t.MUTED,
            wraplength=420,
            justify="left",
        )
        self.status.grid(sticky="ew", pady=8)
        self.body.bind("<Configure>", lambda event: self.status.configure(
            wraplength=max(180, event.width - 60)), add="+")
        ttk.Separator(self.body).grid(sticky="ew", pady=16)
        ttk.Label(self.body, text="02 / RESULTADOS", style="Heading.TLabel").grid(sticky="w", pady=(0, 12))
        ttk.Label(self.body, text="Mensaje recuperado" if decrypt else "Cifrado C").grid(sticky="w")
        self.output = TextBox(self.body, readonly=True)
        self.output.grid(sticky="ew", pady=6)
        results = [("d", "Exponente privado d"), ("n", "Módulo n"),
                   ("phi", "Valor phi"), ("padding", "Relleno retirado")] if decrypt else [
                   ("length", "Longitud original L"), ("key", "Llave pública (e, n)"),
                   ("n", "Módulo n"), ("phi", "Valor phi"), ("padding", "Relleno utilizado")]
        self.values = {}
        for key, label in results:
            ttk.Label(self.body, text=label).grid(sticky="w", pady=(8, 2))
            value = tk.StringVar(value="")
            
            es_privado = key in ("phi", "d")
            campo = ttk.Entry(
                self.body,
                textvariable=value,
                state="readonly",
                show="*" if es_privado else "",
            )
            campo.grid(sticky="ew")
            if es_privado:
                self.campos_privados.append(campo)
            
            self.values[key] = value
        copies = ttk.Frame(self.body)
        copies.grid(sticky="ew", pady=16)
        self.copy_output = ttk.Button(copies, text="Copiar mensaje" if decrypt else "Copiar cifrado",
                                      command=lambda: self.copy(self.output.get()), state="disabled")
        self.copy_output.grid(row=0, column=0, sticky="w", pady=4)
        self.copy_length = None
        if not decrypt:
            self.copy_length = ttk.Button(copies, text="Copiar longitud L", state="disabled",
                                          command=lambda: self.copy(self.values["length"].get()))
            self.copy_length.grid(row=1, column=0, sticky="w", pady=4)
        ttk.Button(copies, text="Abrir detalles del proceso", command=self.show_details).grid(
            row=2, column=0, sticky="w", pady=4)
        # Un cambio de entrada invalida resultados previos y sus botones de copia.
        for entry in self.entries.values():
            variable = tk.StringVar()
            entry.configure(textvariable=variable)
            entry.input_variable = variable
            variable.trace_add("write", self._input_changed)
        self.content.text.bind("<<Modified>>", self._text_changed)
        self.content.text.bind("<Control-Return>", self._submit_shortcut)
        for entry in self.entries.values():
            entry.bind("<Control-Return>", self._submit_shortcut)
        self.content.text.edit_modified(False)
        self._update_feedback()

    def _submit_shortcut(self, event):
        self.request_operation()
        return "break"

    def _update_feedback(self):
        content = self.content.get()
        if self.decrypt:
            blocks = len(content.split())
            self.input_feedback.configure(text=f"{len(content)} caracteres · {blocks} bloques ingresados")
        else:
            self.input_feedback.configure(text=f"{len(content)} caracteres · espacios incluidos")
        ready = int(content != "")
        for entry in self.entries.values():
            raw = entry.get()
            valid = bool(re.fullmatch(r"[+-]?[0-9]+", raw))
            ready += valid
            entry.configure(style="Invalid.TEntry" if raw and not valid else "TEntry")
        total = len(self.entries) + 1
        self.progress.configure(value=ready)
        self.readiness.configure(text=f"{ready}/{total} campos con formato básico · Ctrl+Enter para enviar",
                                 foreground=t.GREEN if ready == total else t.MUTED)

    def _input_changed(self, *args):
        self.reset_results()
        self._update_feedback()
        self.status.configure(
            text=self.mensaje_inicial,
            foreground=t.MUTED,
        )

    def _text_changed(self, event):
        if self.content.text.edit_modified():
            self.content.text.edit_modified(False)
            self._input_changed()

    def reset_results(self):
        self.result = None
        self.details = []
        self.output.set("")
        for value in self.values.values():
            value.set("")
        self.copy_output.state(["disabled"])
        if self.copy_length is not None:
            self.copy_length.state(["disabled"])
        self.app.refresh_details(self)

    def read_request(self):
        content = self.content.get()
        if content == "":
            raise ValueError("Completa el cifrado C." if self.decrypt else "Ingresa el mensaje original.")
        numbers = {}
        for key, entry in self.entries.items():
            raw = entry.get()
            if not re.fullmatch(r"[+-]?[0-9]+", raw):
                entry.focus_set()
                raise ValueError(f"{('L' if key == 'length' else key)} debe ser un entero sin espacios.")
            try:
                numbers[key] = int(raw)
            except ValueError:
                raise ValueError("El entero ingresado es demasiado largo para procesarlo.") from None
        if self.decrypt:
            if not re.fullmatch(r"[0-9]{6}(?: +[0-9]{6})*", content):
                raise ValueError("C debe contener bloques de seis dígitos del 0 al 9, separados por espacios.")
            return DecryptRequest(ciphertext=content, **numbers)
        return EncryptRequest(message=content, **numbers)

    def request_operation(self):
        self.reset_results()
        try:
            request = self.read_request()
            if self.decrypt:
                result = self.app.service.decrypt(request)
            else:
                result = self.app.service.encrypt(request)
            self.present_result(result)
        except NotImplementedError:
            self.status.configure(text=PENDING, foreground=t.WARNING)
        except ValueError as error:
            self.present_error(str(error))
        except Exception:
            self.present_error("No se pudo completar la operación. Revisa la integración del servicio RSA.")

    def present_result(self, result):
        self.result = result
        self.details = list(result.details)
        self.output.set(result.message if self.decrypt else result.ciphertext)
        self.values["n"].set(str(result.n))
        self.values["phi"].set(str(result.phi))
        if self.decrypt:
            self.values["d"].set(str(result.d))
            padding = result.padding_removed
        else:
            self.values["length"].set(str(result.length))
            self.values["key"].set(str(result.public_key))
            self.copy_length.state(["!disabled"])
            padding = result.padding_used
        self.values["padding"].set("Sí · un espacio" if padding else "No")
        self.copy_output.state(["!disabled"])
        self.status.configure(text="Operación completada.", foreground=t.GREEN)
        self.app.refresh_details(self)

    def present_error(self, message):
        self.reset_results()
        self.status.configure(text=message, foreground=t.ERROR)

    def _alternar_privados(self):
        mascara = "" if self.mostrar_privados.get() else "*"
        for campo in self.campos_privados:
            campo.configure(show=mascara)
    
    def clear(self):
        self.content.set("")
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.reset_results()
        self.status.configure(text=PENDING, foreground=t.WARNING)
        self.content.text.focus_set()
        self.mostrar_privados.set(False)
        self._alternar_privados()

    def copy(self, value):
        if self.result is None:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(value)
            self.status.configure(text="Copiado al portapapeles.", foreground=t.CYAN)
        except tk.TclError:
            self.status.configure(text="No se pudo acceder al portapapeles.", foreground=t.ERROR)

    def show_details(self):
        self.app.open_details(self)
