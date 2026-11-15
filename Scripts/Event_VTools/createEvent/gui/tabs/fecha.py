"""Pestaña Fecha y hora."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..constants import COMMON_TIMEZONES
from ..datetime_picker import DateTimePicker


class FechaTabMixin:
    def _build_tab_fecha(self, parent):
        pad = {"padx": 8, "pady": 8}

        ttk.Label(
            parent,
            text="Selecciona la fecha con el calendario y la hora con las listas desplegables.\n"
                 "Esto evita errores de formato: vTools requiere exactamente 'DD Mon YYYY hh:mm AM/PM'.",
            foreground="#555555",
            justify="left",
        ).grid(row=0, column=0, columnspan=2, sticky="w", **pad)

        ttk.Label(parent, text="Inicio:").grid(row=1, column=0, sticky="w", **pad)
        self.start_picker = DateTimePicker(parent)
        self.start_picker.grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(parent, text="Fin:").grid(row=2, column=0, sticky="w", **pad)
        self.end_picker = DateTimePicker(parent)
        self.end_picker.grid(row=2, column=1, sticky="w", **pad)

        ttk.Label(parent, text="Zona horaria:").grid(row=3, column=0, sticky="w", **pad)
        self.timezone_var = tk.StringVar()
        ttk.Combobox(parent, textvariable=self.timezone_var, values=COMMON_TIMEZONES, width=30).grid(
            row=3, column=1, sticky="w", **pad
        )
