"""Constantes compartidas y helper `_noop` (logger vacío)."""

from __future__ import annotations

import re

CREATE_EVENT_URL = "https://events.vtools.ieee.org/tego_/event/create"
DEBUG_PORT = 9222

# Formato exacto que exige el datetimepicker de vTools, ej: "09 Jul 2026 02:03 PM"
DATETIME_FORMAT = "%d %b %Y %I:%M %p"

# Abreviaturas de mes en inglés, tal como las espera vTools. Se usan de forma
# explícita (en vez de strftime/strptime con "%b") porque esas funciones
# dependen del locale del sistema operativo: en un Windows configurado en
# español, "%b" produce "jul." en vez de "Jul" y rompe el formulario.
MONTHS_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MONTHS_EN_LOOKUP = {m.lower(): i + 1 for i, m in enumerate(MONTHS_EN)}

_DATETIME_RE = re.compile(
    r"^(?P<day>\d{1,2})\s+(?P<month>[A-Za-z]{3})\s+(?P<year>\d{4})\s+"
    r"(?P<hour>\d{1,2}):(?P<minute>\d{2})\s*(?P<ampm>[AaPp][Mm])$"
)


def _noop(_msg: str) -> None:
    pass
