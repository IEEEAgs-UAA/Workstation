"""Pestaña Co-hosts."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class CohostsTabMixin:
    def _build_tab_cohosts(self, parent):
        pad = {"padx": 8, "pady": 4}

        self.cohost_enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            parent,
            text="Habilitar Add cohost en la automatización",
            variable=self.cohost_enabled_var,
            command=self._update_cohost_visibility,
        ).grid(row=0, column=0, columnspan=2, sticky="w", **pad)

        ttk.Label(
            parent,
            text="Activa esta casilla para que la automatización marque 'Add cohost' y luego complete cada bloque.",
            foreground="#555555",
            justify="left",
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 8))

        self.cohost_rows_frame = ttk.Frame(parent)
        self.cohost_rows_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=8, pady=4)
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(2, weight=1)

        self.add_cohost_row_btn = ttk.Button(parent, text="Agregar otro cohost", command=self._add_cohost_row)
        self.add_cohost_row_btn.grid(row=3, column=0, sticky="w", padx=8, pady=(8, 4))

        self.cohost_rows: list[dict] = []
        self._add_cohost_row()

        self._update_cohost_visibility()

    def _add_cohost_row(self, initial_data: dict | None = None):
        initial_data = initial_data or {}
        row_number = len(self.cohost_rows) + 1

        row_frame = ttk.LabelFrame(self.cohost_rows_frame, text=f"Cohost #{row_number}")
        row_frame.pack(fill="x", expand=True, pady=4)

        org_var = tk.StringVar(value=initial_data.get("organization", ""))
        spoid_var = tk.StringVar(value=initial_data.get("spoid", ""))
        email_var = tk.StringVar(value=initial_data.get("email", ""))

        ttk.Label(row_frame, text="Organización:").grid(row=0, column=0, sticky="w", padx=8, pady=4)
        org_entry = ttk.Entry(row_frame, textvariable=org_var, width=40)
        org_entry.grid(row=0, column=1, sticky="we", padx=8, pady=4)

        ttk.Label(row_frame, text="SPOID:").grid(row=0, column=2, sticky="w", padx=8, pady=4)
        spoid_entry = ttk.Entry(row_frame, textvariable=spoid_var, width=15)
        spoid_entry.grid(row=0, column=3, sticky="w", padx=8, pady=4)

        ttk.Label(row_frame, text="Email de contacto:").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        email_entry = ttk.Entry(row_frame, textvariable=email_var, width=40)
        email_entry.grid(row=1, column=1, columnspan=3, sticky="we", padx=8, pady=4)

        row_frame.columnconfigure(1, weight=1)

        self.cohost_rows.append(
            {
                "frame": row_frame,
                "org_var": org_var,
                "spoid_var": spoid_var,
                "email_var": email_var,
                "org_entry": org_entry,
                "spoid_entry": spoid_entry,
                "email_entry": email_entry,
            }
        )
        self._update_cohost_visibility()

    def _update_cohost_visibility(self):
        enabled = self.cohost_enabled_var.get()

        for row in self.cohost_rows:
            state = "normal" if enabled else "disabled"
            row["org_entry"].config(state=state)
            row["spoid_entry"].config(state=state)
            row["email_entry"].config(state=state)

        if hasattr(self, "add_cohost_row_btn"):
            self.add_cohost_row_btn.config(state="normal" if enabled else "disabled")

    def _load_cohosts(self, cohosts: list[dict]):
        while len(self.cohost_rows) < max(1, len(cohosts)):
            self._add_cohost_row()

        for idx, row in enumerate(self.cohost_rows):
            data = cohosts[idx] if idx < len(cohosts) else {}
            row["org_var"].set(data.get("organization", ""))
            row["spoid_var"].set(data.get("spoid", ""))
            row["email_var"].set(data.get("email", ""))

        self.cohost_enabled_var.set(bool(cohosts))
        self._update_cohost_visibility()
