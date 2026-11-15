"""Validación y formateo de fechas (campo sensible del datepicker de vTools)."""

from __future__ import annotations

from datetime import datetime

from .constants import MONTHS_EN, _MONTHS_EN_LOOKUP, _DATETIME_RE


def validate_datetime_str(value: str) -> datetime:
    """
    Valida que `value` cumpla el formato "DD MMM YYYY hh:mm AM/PM" (con
    abreviatura de mes en inglés). Lanza ValueError con un mensaje claro si
    no es válido. El parseo es manual (no usa strptime con "%b") para no
    depender del idioma configurado en el sistema operativo.
    """
    raw = value.strip()
    match = _DATETIME_RE.match(raw)
    if not match:
        raise ValueError(
            f"Fecha/hora inválida: '{raw}'. "
            f"Formato esperado: 'DD Mon YYYY hh:mm AM/PM', ej: '09 Jul 2026 02:03 PM'."
        )

    month_key = match.group("month").lower()
    if month_key not in _MONTHS_EN_LOOKUP:
        raise ValueError(
            f"Mes no reconocido en '{raw}'. Usa abreviaturas en inglés: "
            + ", ".join(MONTHS_EN)
        )

    day = int(match.group("day"))
    month = _MONTHS_EN_LOOKUP[month_key]
    year = int(match.group("year"))
    hour12 = int(match.group("hour"))
    minute = int(match.group("minute"))
    ampm = match.group("ampm").upper()

    if not (1 <= hour12 <= 12) or not (0 <= minute <= 59):
        raise ValueError(f"Hora inválida en '{raw}'.")

    hour24 = (hour12 % 12) + (12 if ampm == "PM" else 0)
    try:
        return datetime(year, month, day, hour24, minute)
    except ValueError as exc:
        raise ValueError(f"Fecha inválida: '{raw}' ({exc})") from exc


def format_vtools_datetime(dt: datetime) -> str:
    """Inverso de validate_datetime_str: datetime -> texto en el formato de vTools."""
    hour12 = dt.hour % 12
    hour12 = 12 if hour12 == 0 else hour12
    ampm = "AM" if dt.hour < 12 else "PM"
    return f"{dt.day:02d} {MONTHS_EN[dt.month - 1]} {dt.year} {hour12:02d}:{dt.minute:02d} {ampm}"


def validate_event_dates(event: dict) -> None:
    """Valida start_time/end_time y que end > start. Lanza ValueError si algo falla."""
    start_dt = validate_datetime_str(event["start_time"])
    end_dt = validate_datetime_str(event["end_time"])
    if end_dt <= start_dt:
        raise ValueError(
            f"La fecha de fin ({event['end_time']}) debe ser posterior "
            f"a la fecha de inicio ({event['start_time']})."
        )
