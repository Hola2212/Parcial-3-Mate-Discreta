"""Paleta y estilos ttk, sin dependencias externas."""
from tkinter import ttk


BG = "#080C10"
PANEL = "#111820"
GREEN = "#39FF14"
CYAN = "#00E5FF"
PURPLE = "#A78BFA"
TEXT = "#E6EDF3"
MUTED = "#9AA7B5"
ERROR = "#FF5470"
WARNING = "#FFD166"


def configure_theme(root):
    root.configure(background=BG)
    root.option_add("*Font", "{Segoe UI} 11")
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(".", background=BG, foreground=TEXT)
    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=PANEL)
    style.configure("TLabel", background=BG, foreground=TEXT)
    style.configure("Muted.TLabel", foreground=MUTED)
    style.configure("Title.TLabel", font=("Segoe UI", 25, "bold"), foreground=CYAN)
    style.configure("Heading.TLabel", font=("Segoe UI", 14, "bold"), foreground=GREEN)
    style.configure("Accent.TLabel", foreground=PURPLE)
    style.configure("TEntry", fieldbackground=PANEL, foreground=TEXT,
                    insertcolor=CYAN, padding=9, bordercolor=MUTED)
    style.map("TEntry", bordercolor=[("focus", CYAN)],
              fieldbackground=[("readonly", PANEL)], foreground=[("readonly", TEXT)])
    style.configure("TButton", background=PANEL, foreground=TEXT,
                    padding=(14, 10), borderwidth=2, bordercolor=PANEL)
    style.map("TButton", background=[("disabled", PANEL), ("pressed", "#254552"),
                                    ("active", "#1C3340")],
              foreground=[("disabled", MUTED), ("active", CYAN)],
              bordercolor=[("focus", CYAN), ("active", CYAN)])
    style.configure("Primary.TButton", background=GREEN, foreground=BG)
    style.map("Primary.TButton", background=[("disabled", PANEL),
                                             ("pressed", "#68D65A"),
                                             ("active", "#8BFF73")],
              foreground=[("disabled", MUTED), ("active", BG)])
    style.configure("Nav.TButton", anchor="w")
    style.configure("Selected.Nav.TButton", foreground=CYAN, bordercolor=CYAN)
    style.configure("TCheckbutton", background=BG, foreground=TEXT, padding=5)
    style.map("TCheckbutton", background=[("active", PANEL)],
              foreground=[("active", CYAN)])
    style.configure("Treeview", background=PANEL, fieldbackground=PANEL,
                    foreground=TEXT, rowheight=30)
    style.configure("Treeview.Heading", background=BG, foreground=CYAN,
                    padding=8)
    style.map("Treeview", background=[("selected", "#254552")],
              foreground=[("selected", TEXT)])
