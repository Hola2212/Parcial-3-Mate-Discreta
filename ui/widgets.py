"""Widgets reutilizables: desplazamiento, texto seleccionable y detalles."""
import tkinter as tk
from tkinter import ttk

from ui import theme as t


class ScrollFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg=t.BG, highlightthickness=0)
        bar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=bar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        bar.grid(row=0, column=1, sticky="ns")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.body = ttk.Frame(self.canvas, padding=24)
        self.window = self.canvas.create_window(0, 0, window=self.body, anchor="nw")
        self.body.bind("<Configure>", self._resize_body)
        self.canvas.bind("<Configure>", self._resize_canvas)
        # Enlaces locales: no se reemplazan eventos globales de otros controles.
        self.bind("<Map>", self._bind_wheel)

    def _resize_body(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_canvas(self, event):
        self.canvas.itemconfigure(self.window, width=event.width)

    def _bind_wheel(self, event):
        def attach(widget):
            if not isinstance(widget, (tk.Text, ttk.Treeview)):
                widget.bind("<MouseWheel>", self._wheel, add="+")
                widget.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
                widget.bind("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))
            for child in widget.winfo_children():
                attach(child)
        attach(self.body)

    def _wheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
        return "break"


class TextBox(ttk.Frame):
    def __init__(self, parent, height=4, readonly=False):
        super().__init__(parent)
        self.readonly = readonly
        self.text = tk.Text(self, height=height, width=30, wrap="char", bg=t.PANEL,
                            fg=t.TEXT, insertbackground=t.CYAN, selectbackground="#254552",
                            selectforeground=t.TEXT, relief="flat", padx=12, pady=10,
                            highlightthickness=1, highlightbackground=t.MUTED,
                            highlightcolor=t.CYAN, undo=not readonly, takefocus=True,
                            font=("Consolas", 11))
        bar = ttk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=bar.set)
        self.text.grid(row=0, column=0, sticky="nsew")
        bar.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # Tab navega; el contenido pegado permanece intacto para validarlo después.
        self.text.bind("<Tab>", self._next)
        self.text.bind("<Shift-Tab>", self._previous)
        self.text.bind("<Control-a>", self._select_all)
        if readonly:
            self.text.configure(state="disabled")

    def _next(self, event):
        self.text.tk_focusNext().focus_set()
        return "break"

    def _previous(self, event):
        self.text.tk_focusPrev().focus_set()
        return "break"

    def _select_all(self, event):
        self.text.tag_add("sel", "1.0", "end-1c")
        return "break"

    def get(self):
        # Solo excluye el salto interno obligatorio de Text, no el texto ingresado.
        return self.text.get("1.0", "end-1c")

    def set(self, value):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", str(value))
        if self.readonly:
            self.text.configure(state="disabled")


class DetailWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("RSA | Detalles del proceso")
        self.geometry("900x420")
        self.minsize(560, 280)
        self.configure(bg=t.BG)
        self.transient(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.caption = ttk.Label(self, padding=16, foreground=t.CYAN)
        self.caption.grid(row=0, column=0, sticky="w")
        panel = ttk.Frame(self, padding=12)
        panel.grid(row=1, column=0, sticky="nsew")
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(0, weight=1)
        columns = ("block", "characters", "ascii", "input", "output")
        self.table = ttk.Treeview(panel, columns=columns, show="headings")
        for key, name in zip(columns, ("Bloque", "Caracteres (repr)", "Códigos ASCII",
                                       "Bloque de entrada", "Bloque de salida")):
            self.table.heading(key, text=name)
            self.table.column(key, width=155, minwidth=90)
        self.table.grid(row=0, column=0, sticky="nsew")
        vertical = ttk.Scrollbar(panel, command=self.table.yview)
        horizontal = ttk.Scrollbar(panel, orient="horizontal", command=self.table.xview)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        self.table.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        ttk.Button(self, text="Cerrar", command=self.destroy).grid(row=2, column=0, pady=12)
        self.bind("<Escape>", lambda event: self.destroy())

    def show_rows(self, operation, rows):
        self.caption.configure(text=f"{operation} · {len(rows)} bloques" if rows
                               else f"{operation} · Sin datos del proceso todavía")
        self.table.delete(*self.table.get_children())
        for row in rows:
            self.table.insert("", "end", values=(row.block, repr(row.characters),
                              row.ascii_codes, row.input_block, row.output_block))
        self.deiconify()
        self.lift()
        self.focus_set()
