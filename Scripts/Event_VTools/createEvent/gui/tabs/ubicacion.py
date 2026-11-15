"""Pestaña Ubicación."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..constants import LOCATION_TYPES


class UbicacionTabMixin:
    def _build_tab_ubicacion(self, parent):
        pad = {"padx": 8, "pady": 4}

        ttk.Label(parent, text="Tipo de ubicación:").grid(row=0, column=0, sticky="w", **pad)
        self.location_type_var = tk.StringVar(value="physical")
        type_frame = ttk.Frame(parent)
        type_frame.grid(row=0, column=1, sticky="w", **pad)
        for value, label in LOCATION_TYPES:
            ttk.Radiobutton(
                type_frame, text=label, value=value, variable=self.location_type_var,
                command=self._update_location_visibility,
            ).pack(side="left", padx=4)

        # --- Campos físicos ---
        self.physical_frame = ttk.LabelFrame(parent, text="Dirección física")
        self.physical_frame.grid(row=1, column=0, columnspan=2, sticky="we", padx=8, pady=6)

        self.address1_var = tk.StringVar()
        self.address2_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.postal_code_var = tk.StringVar()
        self.building_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.state_var = tk.StringVar()

        rows = [
            ("Dirección 1:", self.address1_var),
            ("Dirección 2:", self.address2_var),
            ("Ciudad:", self.city_var),
            ("Código postal:", self.postal_code_var),
            ("Edificio:", self.building_var),
            ("País:", self.country_var),
            ("Estado:", self.state_var),
        ]
        self.physical_entries: list[ttk.Entry] = []
        for i, (label, var) in enumerate(rows):
            ttk.Label(self.physical_frame, text=label).grid(row=i, column=0, sticky="w", **pad)
            entry = ttk.Entry(self.physical_frame, textvariable=var, width=45)
            entry.grid(row=i, column=1, sticky="we", **pad)
            self.physical_entries.append(entry)
        self.physical_frame.columnconfigure(1, weight=1)

        # --- Campo virtual ---
        self.virtual_frame = ttk.LabelFrame(parent, text="Información virtual (link, instrucciones, etc.)")
        self.virtual_frame.grid(row=2, column=0, columnspan=2, sticky="we", padx=8, pady=6)
        self.virtual_info_text = tk.Text(self.virtual_frame, height=4, width=60, wrap="word")
        self.virtual_info_text.pack(fill="x", padx=8, pady=8)

        parent.columnconfigure(1, weight=1)
        self._update_location_visibility()

    def _update_location_visibility(self):
        loc_type = self.location_type_var.get()
        physical_enabled = loc_type in ("physical", "hybrid")
        virtual_enabled = loc_type in ("virtual", "hybrid")

        for entry in self.physical_entries:
            entry.config(state="normal" if physical_enabled else "disabled")

        self.virtual_info_text.config(state="normal" if virtual_enabled else "disabled")
