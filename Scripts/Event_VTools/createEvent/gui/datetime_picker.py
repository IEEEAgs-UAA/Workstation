"""Selector compuesto de fecha (calendario) + hora/minuto/AM-PM."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None

from .. import automation as event_filler


class DateTimePicker(ttk.Frame):
    """
    Selector compuesto: calendario (DateEntry) + hora/minuto/AM-PM en
    listas desplegables de solo lectura. Nunca produce texto libre, así
    que el formato que exige vTools queda garantizado por construcción.
    """

    def __init__(self, parent):
        super().__init__(parent)

        if DateEntry is None:
            raise RuntimeError(
                "Falta la dependencia 'tkcalendar'. Instálala con: pip install tkcalendar"
            )

        self.date_entry = DateEntry(
            self, date_pattern="dd/mm/yyyy", width=11, background="darkblue",
            foreground="white", borderwidth=2, locale="en_US",
        )
        self.date_entry.grid(row=0, column=0, padx=(0, 6))

        self.hour_var = tk.StringVar(value="12")
        ttk.Combobox(
            self, textvariable=self.hour_var, values=[f"{h:02d}" for h in range(1, 13)],
            width=3, state="readonly",
        ).grid(row=0, column=1)

        ttk.Label(self, text=":").grid(row=0, column=2, padx=2)

        self.minute_var = tk.StringVar(value="00")
        ttk.Combobox(
            self, textvariable=self.minute_var, values=[f"{m:02d}" for m in range(0, 60)],
            width=3, state="readonly",
        ).grid(row=0, column=3)

        self.ampm_var = tk.StringVar(value="PM")
        ttk.Combobox(
            self, textvariable=self.ampm_var, values=["AM", "PM"], width=4, state="readonly",
        ).grid(row=0, column=4, padx=(6, 0))

    def get_vtools_string(self) -> str:
        d = self.date_entry.get_date()
        month_str = event_filler.MONTHS_EN[d.month - 1]
        return f"{d.day:02d} {month_str} {d.year} {self.hour_var.get()}:{self.minute_var.get()} {self.ampm_var.get()}"

    def set_from_string(self, value: str) -> None:
        try:
            dt = event_filler.validate_datetime_str(value)
        except ValueError:
            return
        self.date_entry.set_date(dt.date())
        hour12 = dt.hour % 12
        hour12 = 12 if hour12 == 0 else hour12
        self.hour_var.set(f"{hour12:02d}")
        self.minute_var.set(f"{dt.minute:02d}")
        self.ampm_var.set("AM" if dt.hour < 12 else "PM")
