"""Helpers de la GUI: ruta del .env y conversión texto <-> HTML."""

from __future__ import annotations

import sys
from pathlib import Path


def _env_file_path() -> Path:
    """
    Ubicación del .env: junto al ejecutable cuando corre empaquetado
    (PyInstaller), o junto al script cuando corre como .py normal.
    """
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).parent.parent
    return base / ".env"


def _wrap_html(text: str) -> str:
    """Convierte texto plano en un <p>...</p> (si el usuario ya escribió HTML, lo respeta)."""
    text = text.strip()
    if not text:
        return "<p></p>"
    if text.startswith("<"):
        return text
    return f"<p>{text}</p>"


def _unwrap_html(html: str) -> str:
    """Inverso simple de _wrap_html, para mostrar contenido editable sin etiquetas de sobra."""
    text = (html or "").strip()
    if text.startswith("<p>") and text.endswith("</p>"):
        return text[3:-4]
    return text
