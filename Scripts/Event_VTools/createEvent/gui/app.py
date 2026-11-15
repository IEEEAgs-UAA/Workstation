"""Ventana principal (ensambla las pestañas y acciones)."""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext

try:
    from dotenv import load_dotenv
except ImportError:  # dotenv es opcional; sin él simplemente no se autocargan credenciales
    load_dotenv = None

from .. import automation as event_filler
from ..data.EventsVtools import events
from .actions import ActionsMixin
from .constants import APP_TITLE
from .datetime_picker import DateEntry
from .event_binding import EventBindingMixin
from .helpers import _env_file_path
from .tabs.chrome import ChromeTabMixin
from .tabs.cohosts import CohostsTabMixin
from .tabs.fecha import FechaTabMixin
from .tabs.general import GeneralTabMixin
from .tabs.ubicacion import UbicacionTabMixin


class App(
    GeneralTabMixin, FechaTabMixin, UbicacionTabMixin, ChromeTabMixin, CohostsTabMixin,
    EventBindingMixin, ActionsMixin, tk.Tk,
):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("820x780")
        self.minsize(760, 680)

        self.log_queue: queue.Queue[str] = queue.Queue()
        self.controller = event_filler.AutomationController()
        self.worker_thread: threading.Thread | None = None

        if load_dotenv is not None:
            load_dotenv(_env_file_path())

        self._build_ui()
        self._poll_log_queue()

    def _build_ui(self):
        pad = {"padx": 8, "pady": 4}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)
        ttk.Label(top, text="Evento base:").pack(side="left")
        self.event_titles = [e["title"] for e in events]
        self.event_combo = ttk.Combobox(top, values=self.event_titles, state="readonly", width=55)
        self.event_combo.pack(side="left", padx=8)
        self.event_combo.current(0)
        self.event_combo.bind("<<ComboboxSelected>>", self._on_event_selected)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, **pad)

        self.tab_general = ttk.Frame(notebook)
        self.tab_fecha = ttk.Frame(notebook)
        self.tab_ubicacion = ttk.Frame(notebook)
        self.tab_chrome = ttk.Frame(notebook)
        self.tab_cohosts = ttk.Frame(notebook)

        notebook.add(self.tab_chrome, text="Host / Chrome")
        notebook.add(self.tab_cohosts, text="Co-hosts")
        notebook.add(self.tab_ubicacion, text="Ubicación")
        notebook.add(self.tab_fecha, text="Fecha y hora")
        notebook.add(self.tab_general, text="Contenido")
        
        self._build_tab_chrome(self.tab_chrome)
        self._build_tab_cohosts(self.tab_cohosts)
        self._build_tab_ubicacion(self.tab_ubicacion)
        self._build_tab_general(self.tab_general)
        self._build_tab_fecha(self.tab_fecha)

        # --- Botones de acción (siempre visibles) ---
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", **pad)

        self.run_btn = ttk.Button(action_frame, text="Ejecutar automatización", command=self._on_run_clicked)
        self.run_btn.pack(side="left", padx=4)

        self.save_btn = ttk.Button(action_frame, text="Guardar como borrador", command=self._on_save_clicked, state="disabled")
        self.save_btn.pack(side="left", padx=4)

        self.close_btn = ttk.Button(action_frame, text="Cerrar navegador", command=self._on_close_clicked, state="disabled")
        self.close_btn.pack(side="left", padx=4)

        # --- Log (siempre visible) ---
        log_frame = ttk.LabelFrame(self, text="Registro")
        log_frame.pack(fill="both", expand=True, **pad)
        self.log_widget = scrolledtext.ScrolledText(log_frame, height=10, state="disabled", wrap="word")
        self.log_widget.pack(fill="both", expand=True, padx=4, pady=4)

        self._on_event_selected()
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)


def main():
    if DateEntry is None:
        # Fallamos con un mensaje claro en vez de un traceback críptico.
        import tkinter.messagebox as mb
        root = tk.Tk()
        root.withdraw()
        mb.showerror(
            "Falta una dependencia",
            "Falta instalar 'tkcalendar' (usado para el selector de fecha).\n\n"
            "Ejecuta: pip install tkcalendar",
        )
        return
    app = App()
    app.mainloop()
