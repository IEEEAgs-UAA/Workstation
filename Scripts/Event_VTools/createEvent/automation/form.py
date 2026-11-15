"""Orquestación de alto nivel: llena el formulario completo de un evento."""

from __future__ import annotations

from playwright.sync_api import Page

from .constants import _noop
from .dates import validate_event_dates
from .sections.details import (
    fill_agenda, fill_description, fill_footer, fill_header, fill_keywords,
    fill_start_end_time, fill_survey_url, fill_title, select_category,
    select_subcategory, select_timezone,
)
from .sections.host import fill_cohosts, fill_contact_email, fill_host_organizational_unit
from .sections.location import fill_location, open_location_section
from .sections.navigation import open_details_section
from .sections.registration import open_registration_section, select_registration_type_none
from .sections.speakers import fill_speakers, open_speakers_section


def fill_event_form(
    page: Page,
    event: dict,
    host_org_name: str,
    host_spoid: str,
    host_contact_email: str,
    log=_noop,
) -> None:
    """
    Ejecuta el llenado completo del formulario para un evento, en el mismo
    orden que el script original. Lanza ValueError si las fechas no son válidas.
    """
    # Validación temprana de campos sensibles antes de tocar el DOM
    validate_event_dates(event)

    log("Esperando formulario de creación de evento...")
    page.wait_for_selector("#_event_host_spoid_0", timeout=15000)

    log("Llenando datos del host...")
    fill_host_organizational_unit(page, org_name=host_org_name, spoid=host_spoid)
    fill_contact_email(page, host_contact_email)

    if event.get("cohosts"):
        fill_cohosts(page, event["cohosts"], log=log)

    open_details_section(page)

    log(f"Llenando detalles del evento: {event['title']}")
    fill_title(page, event["title"])
    select_category(page, event["category"])
    if event.get("subcategory"):
        select_subcategory(page, event["subcategory"])

    log(f"Fecha/hora inicio: {event['start_time']} | fin: {event['end_time']} ({event['timezone']})")
    fill_start_end_time(page, event["start_time"], event["end_time"])
    select_timezone(page, event["timezone"])
    fill_description(page, event["description"])
    fill_header(page, event["header"])
    fill_footer(page, event["footer"])
    fill_agenda(page, event["agenda"])
    fill_keywords(page, event["keywords"])
    fill_survey_url(page, event.get("survey_url", ""))

    open_location_section(page)
    fill_location(page, event["location"], log=log)
    open_registration_section(page)
    select_registration_type_none(page)


    if event.get("speakers"):
        open_speakers_section(page)
        fill_speakers(page, event["speakers"], log=log)

    # Only works if its published, so we will not use it for now
    # open_reporting_section(page)

    # if event.get("ieee_attendance"):
    #     page.fill("#meeting_ieee_attending", event["ieee_attendance"])

    # if event.get("guests_attendance"):
    #     page.fill("#meeting_guests_attending", event["guests_attendance"])

    log("Formulario llenado. Revísalo en el navegador antes de guardar.")
