"""Raíz única y coordinación de las pantallas."""
import tkinter as tk
from tkinter import ttk

from contracts import PendingRSAService
from ui import theme
from ui.screens import InfoScreen, LoginScreen, OperationScreen
from ui.widgets import DetailWindow


class RSAApp(tk.Tk):
    def __init__(self, service=None):
        super().__init__()
        self.service = service if service is not None else PendingRSAService()
        self.title("RSA LAB | Matemática Discreta")
        self.geometry("1120x780")
        self.minsize(760, 520)
        theme.configure_theme(self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.container = ttk.Frame(self)
        self.container.grid(sticky="nsew")
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.detail_window = None
        self.detail_owner = None
        self.login = None
        self.shell = None
        self.screens = {}
        self.show_login()

    def show_login(self):
        self.close_details()
        if self.shell is not None:
            self.shell.destroy()
            self.shell = None
        self.screens = {}
        self.login = LoginScreen(self.container, self)
        self.login.grid(row=0, column=0, sticky="nsew")
        self.after_idle(self.login.username.focus_set)

    def open_session(self, username):
        self.login.destroy()
        self.login = None
        self.shell = ttk.Frame(self.container)
        self.shell.grid(row=0, column=0, sticky="nsew")
        self.shell.columnconfigure(1, weight=1)
        self.shell.rowconfigure(0, weight=1)
        sidebar = ttk.Frame(self.shell, padding=16)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.rowconfigure(7, weight=1)
        ttk.Label(sidebar, text="RSA / LAB", style="Heading.TLabel").grid(sticky="w", pady=(8, 5))
        ttk.Label(sidebar, text=f"Usuario: {username}", style="Muted.TLabel").grid(sticky="w", pady=(0, 26))
        content = ttk.Frame(self.shell)
        content.grid(row=0, column=1, sticky="nsew")
        content.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)
        self.screens = {
            "Inicio": InfoScreen(content, "Laboratorio RSA", [
                ("Explora el proyecto", "Utiliza el menú para ingresar los datos de cada operación y consultar sus resultados."),
                ("Encriptar", "Prepara un mensaje y los parámetros p, q y e. La pantalla dispone de salidas para C, L y la llave pública."),
                ("Desencriptar", "Ingresa C, L y los parámetros RSA para recuperar el mensaje cuando se conecte la lógica matemática."),
                ("Estado del desarrollo", "La navegación y los formularios están disponibles. Lógica RSA pendiente de integrar. No se generan resultados simulados."),
            ]),
            "Encriptar": OperationScreen(content, self),
            "Desencriptar": OperationScreen(content, self, decrypt=True),
            "Ayuda": InfoScreen(content, "Ayuda y acerca de", [
                ("Encriptación", "Requiere mensaje original, p, q y e. Los caracteres admitidos por el proyecto son ASCII imprimibles del 32 al 126. Tildes, ñ, tabulaciones y saltos de línea no están admitidos."),
                ("Desencriptación", "Requiere C, longitud original L, p, q y e. Conserva C y L juntos. Cada bloque de C tiene seis dígitos y se separa del siguiente por espacios."),
                ("Relleno y espacios", "Cuando el mensaje tiene longitud impar, RSA debe añadir exactamente un espacio final. Al recuperar el mensaje se retira solo ese relleno. Los espacios originales iniciales, finales y consecutivos se conservan."),
                ("Validaciones", "Esta interfaz comprueba campos obligatorios y formatos enteros y del cifrado. La validación matemática, la coherencia de L y los caracteres admitidos corresponden al futuro servicio RSA."),
                ("Detalles del proceso", "La ventana auxiliar mostrará caracteres, ASCII y bloques recibidos del servicio matemático. Sin el servicio conectado permanece vacía."),
                ("Acceso de demostración", "Usuario: estudiante. Contraseña: rsa2026. El login solo demuestra la navegación; no guarda contraseñas ni proporciona autenticación real."),
                ("Tecnología", "Interfaz de escritorio desarrollada exclusivamente con Python, tkinter y ttk. Consulta las instrucciones del proyecto y USO_IA.txt para conocer el alcance de la asistencia con IA."),
            ]),
        }
        self.navigation = {}
        for index, (name, screen) in enumerate(self.screens.items(), start=2):
            screen.grid(row=0, column=0, sticky="nsew")
            button = ttk.Button(sidebar, text=name, style="Nav.TButton",
                                command=lambda key=name: self.navigate(key))
            button.grid(row=index, column=0, sticky="ew", pady=5)
            self.navigation[name] = button
        ttk.Label(sidebar, text="MM2015 · Interfaz demo", style="Accent.TLabel").grid(row=8, sticky="w", pady=12)
        ttk.Button(sidebar, text="Cerrar sesión", command=self.show_login).grid(row=9, sticky="ew")
        self.navigate("Inicio")

    def navigate(self, name):
        self.close_details()
        screen = self.screens[name]
        screen.tkraise()
        for key, button in self.navigation.items():
            button.configure(style="Selected.Nav.TButton" if key == name else "Nav.TButton")
        if isinstance(screen, OperationScreen):
            screen.content.text.focus_set()
        else:
            self.navigation[name].focus_set()

    def close_details(self):
        if self.detail_window is not None and self.detail_window.winfo_exists():
            self.detail_window.destroy()
        self.detail_window = None
        self.detail_owner = None

    def open_details(self, screen):
        if self.detail_window is None or not self.detail_window.winfo_exists():
            self.detail_window = DetailWindow(self)
        self.detail_owner = screen
        self.detail_window.show_rows(screen.operation, screen.details)

    def refresh_details(self, screen):
        if (self.detail_owner is screen and self.detail_window is not None
                and self.detail_window.winfo_exists()):
            self.detail_window.show_rows(screen.operation, screen.details)
