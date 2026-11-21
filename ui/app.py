"""Raíz única y coordinación de las pantallas."""
import tkinter as tk
from tkinter import ttk

from contracts import PendingRSAService
from users import DemoUser, credentials_help
from ui import theme
from ui.screens import InfoScreen, LoginScreen, OperationScreen
from ui.widgets import DetailWindow


class RSAApp(tk.Tk):
    def __init__(self, service=None):
        super().__init__()
        self.service = service if service is not None else PendingRSAService()
        self.title("RSA LAB | Matemática Discreta")
        width = int(self.winfo_screenwidth() * 0.8)
        height = int(self.winfo_screenheight() * 0.8)
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(min(700, width), min(460, height))
        self.resizable(True, True)
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
        self.current_user = None
        self.shell = None
        self.screens = {}
        self.show_login()

    def show_login(self):
        self.close_details()
        self.current_user = None
        if self.shell is not None:
            self.shell.destroy()
            self.shell = None
        self.screens = {}
        self.login = LoginScreen(self.container, self)
        self.login.grid(row=0, column=0, sticky="nsew")
        self.after_idle(self.login.username.focus_set)

    def open_session(self, user: DemoUser):
        self.current_user = user
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
        self.user_badge = ttk.Label(sidebar, text=f"Usuario: {user.username}\nRol: {user.role}",
                                    style="Muted.TLabel")
        self.user_badge.grid(sticky="w", pady=(0, 26))
        content = ttk.Frame(self.shell)
        content.grid(row=0, column=1, sticky="nsew")
        content.rowconfigure(1, weight=1)
        content.columnconfigure(0, weight=1)
        topbar = ttk.Frame(content, padding=(24, 14))
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.columnconfigure(0, weight=1)
        self.breadcrumb = ttk.Label(topbar, text="WORKSPACE / INICIO", style="Accent.TLabel")
        self.breadcrumb.grid(row=0, column=0, sticky="w")
        ttk.Label(topbar, text=f"● {user.role.upper()}", foreground=theme.PURPLE
                  if user.role == "Administrador" else theme.GREEN).grid(row=0, column=1)
        self.screens = {
            "Inicio": InfoScreen(content, "Laboratorio RSA", [
                ("Explora el proyecto", "Utiliza el menú para ingresar los datos de cada operación y consultar sus resultados."),
                ("Encriptar", "Prepara un mensaje y los parámetros p, q y e. La pantalla dispone de salidas para C, L y la llave pública."),
                (
                    "Desencriptar",
                    "Ingresa C, L y los parámetros RSA para recuperar exactamente "
                    "el mensaje original, incluidos sus espacios.",
                ),
                (
                    "Estado del proyecto",
                    "La interfaz está conectada con los algoritmos RSA. "
                    "Puedes encriptar, desencriptar y consultar los detalles del proceso.",
                ),
            ]),
            "Encriptar": OperationScreen(content, self),
            "Desencriptar": OperationScreen(content, self, decrypt=True),
            "Ayuda": InfoScreen(content, "Ayuda y acerca de", [
                ("Encriptación", "Requiere mensaje original, p, q y e. Los caracteres admitidos por el proyecto son ASCII imprimibles del 32 al 126. Tildes, ñ, tabulaciones y saltos de línea no están admitidos."),
                ("Desencriptación", "Requiere C, longitud original L, p, q y e. Conserva C y L juntos. Cada bloque de C tiene seis dígitos y se separa del siguiente por espacios."),
                ("Relleno y espacios", "Cuando el mensaje tiene longitud impar, RSA debe añadir exactamente un espacio final. Al recuperar el mensaje se retira solo ese relleno. Los espacios originales iniciales, finales y consecutivos se conservan."),
                (
                    "Validaciones",
                    "El programa comprueba los parámetros RSA, los caracteres ASCII "
                    "admitidos, el formato y rango del cifrado, la coherencia de L "
                    "y el relleno recuperado.",
                ),
                (
                    "Detalles del proceso",
                    "Después de ejecutar una operación, abre los detalles para consultar "
                    "los caracteres, sus códigos ASCII y los bloques de entrada y salida. "
                    "Los espacios se representan de forma visible en la tabla.",
                ),
                ("Acceso de demostración", credentials_help() + "\nLas tres cuentas permiten explorar las mismas funciones. El rol identifica la sesión; no se han definido permisos adicionales. Las credenciales son públicas y locales, sin registro ni base de datos."),
                ("Tecnología", "Interfaz de escritorio desarrollada exclusivamente con Python, tkinter y ttk. Consulta las instrucciones del proyecto y USO_IA.txt para conocer el alcance de la asistencia con IA."),
                (
                    "Datos privados",
                    "Los parámetros p, q, phi y el exponente privado d están ocultos "
                    "inicialmente. Activa Mostrar datos privados para consultarlos. "
                    "Este control cambia su visibilidad; no asigna claves propias "
                    "a cada usuario.",
                ),
            ]),
        }
        self.navigation = {}
        for index, (name, screen) in enumerate(self.screens.items(), start=2):
            screen.grid(row=1, column=0, sticky="nsew")
            button = ttk.Button(sidebar, text=f"0{index - 1}   {name}   →", style="Nav.TButton",
                                command=lambda key=name: self.navigate(key))
            button.grid(row=index, column=0, sticky="ew", pady=5)
            self.navigation[name] = button
        ttk.Label(sidebar, text="MM2015 · Interfaz demo", style="Accent.TLabel").grid(row=8, sticky="w", pady=12)
        ttk.Button(sidebar, text="Cerrar sesión", command=self.show_login).grid(row=9, sticky="ew")
        self.navigate("Inicio")

    def navigate(self, name):
        self.close_details()
        self.breadcrumb.configure(text=f"WORKSPACE / {name.upper()}")
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
