"""Pestaña Host / Chrome."""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk

from ..constants import (
    DEFAULT_HOST_CONTACT_EMAIL,
    DEFAULT_HOST_ORG_NAME,
    DEFAULT_HOST_SPOID,
)


class ChromeTabMixin:
    def _build_tab_chrome(self, parent):
        pad = {"padx": 8, "pady": 4}

        host_frame = ttk.LabelFrame(parent, text="Organización anfitriona")
        host_frame.pack(fill="x", padx=8, pady=8)

        ttk.Label(host_frame, text="Nombre:").grid(row=0, column=0, sticky="w", **pad)
        self.host_org_var = tk.StringVar(value=DEFAULT_HOST_ORG_NAME)
        ttk.Entry(host_frame, textvariable=self.host_org_var, width=40).grid(row=0, column=1, sticky="we", **pad)

        ttk.Label(host_frame, text="SPOID:").grid(row=0, column=2, sticky="w", **pad)
        self.host_spoid_var = tk.StringVar(value=DEFAULT_HOST_SPOID)
        ttk.Entry(host_frame, textvariable=self.host_spoid_var, width=15).grid(row=0, column=3, sticky="w", **pad)

        ttk.Label(host_frame, text="Email de contacto:").grid(row=1, column=0, sticky="w", **pad)
        self.host_email_var = tk.StringVar(value=DEFAULT_HOST_CONTACT_EMAIL)
        ttk.Entry(host_frame, textvariable=self.host_email_var, width=40).grid(row=1, column=1, columnspan=3, sticky="we", **pad)
        host_frame.columnconfigure(1, weight=1)

        chrome_frame = ttk.LabelFrame(parent, text="Navegador y credenciales")
        chrome_frame.pack(fill="x", padx=8, pady=8)

        self.launch_chrome_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            chrome_frame,
            text="Iniciar Chrome automáticamente (perfil temporal + login automático)",
            variable=self.launch_chrome_var,
            command=self._on_switch_toggle,
        ).grid(row=0, column=0, columnspan=2, sticky="w", **pad)

        self.switch_help = ttk.Label(chrome_frame, text="", foreground="#555555", wraplength=680, justify="left")
        self.switch_help.grid(row=1, column=0, columnspan=2, sticky="w", padx=8)

        ttk.Label(chrome_frame, text="Usuario IEEE:").grid(row=2, column=0, sticky="w", **pad)
        self.username_var = tk.StringVar(value=os.getenv("IEEE_USER", ""))
        ttk.Entry(chrome_frame, textvariable=self.username_var, width=35).grid(row=2, column=1, sticky="w", **pad)

        ttk.Label(chrome_frame, text="Contraseña IEEE:").grid(row=3, column=0, sticky="w", **pad)
        self.password_var = tk.StringVar(value=os.getenv("IEEE_PASS", ""))
        ttk.Entry(chrome_frame, textvariable=self.password_var, width=35, show="*").grid(row=3, column=1, sticky="w", **pad)

        self._on_switch_toggle()

    def _on_switch_toggle(self):
        if self.launch_chrome_var.get():
            self.switch_help.config(
                text="Se abrirá Chrome con un perfil temporal y se iniciará sesión automáticamente con las "
                     "credenciales de abajo."
            )
        else:
            self.switch_help.config(
                text="Se usará una instancia de Chrome que TÚ debes tener abierta con:\n"
                     "google-chrome-stable --user-data-dir=/tmp/chrome-playwright --remote-debugging-port=9222\n"
                     "(en Windows: chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\chrome-playwright)"
            )
