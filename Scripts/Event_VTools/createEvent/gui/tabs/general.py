"""Pestaña Contenido."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class GeneralTabMixin:
    def _build_tab_general(self, parent):
        pad = {"padx": 8, "pady": 4}

        ttk.Label(parent, text="Título del evento:").grid(row=0, column=0, sticky="nw", **pad)
        self.title_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.title_var, width=60).grid(row=0, column=1, sticky="we", **pad)

        ttk.Label(parent, text="Descripción:").grid(row=1, column=0, sticky="nw", **pad)
        self.description_text = tk.Text(parent, height=4, width=60, wrap="word")
        self.description_text.grid(row=1, column=1, sticky="we", **pad)

        ttk.Label(parent, text="Encabezado (header):").grid(row=2, column=0, sticky="nw", **pad)
        self.header_text = tk.Text(parent, height=3, width=60, wrap="word")
        self.header_text.grid(row=2, column=1, sticky="we", **pad)

        ttk.Label(parent, text="Pie de página (footer):").grid(row=3, column=0, sticky="nw", **pad)
        self.footer_text = tk.Text(parent, height=3, width=60, wrap="word")
        self.footer_text.grid(row=3, column=1, sticky="we", **pad)

        ttk.Label(parent, text="Agenda:").grid(row=4, column=0, sticky="nw", **pad)
        self.agenda_text = tk.Text(parent, height=3, width=60, wrap="word")
        self.agenda_text.grid(row=4, column=1, sticky="we", **pad)

        ttk.Label(parent, text="Keywords:").grid(row=5, column=0, sticky="w", **pad)
        self.keywords_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.keywords_var, width=60).grid(row=5, column=1, sticky="we", **pad)

        ttk.Label(parent, text="URL de encuesta (survey_url):").grid(row=6, column=0, sticky="w", **pad)
        self.survey_url_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.survey_url_var, width=60).grid(row=6, column=1, sticky="we", **pad)

        ttk.Label(
            parent,
            text="Los campos de texto aceptan HTML (ej. <p>...</p>) o texto plano;\n"
                 "si escribes texto plano, se envuelve automáticamente en <p>.",
            foreground="#555555",
        ).grid(row=7, column=0, columnspan=2, sticky="w", padx=8, pady=(8, 0))

        parent.columnconfigure(1, weight=1)
