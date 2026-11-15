"""Botones y navegación entre secciones."""

from __future__ import annotations

from playwright.sync_api import Page

from ..constants import _noop


def open_details_section(page: Page):
    page.get_by_text("Details", exact=True).click()
    page.wait_for_timeout(500)


def save_as_draft(page: Page, log=_noop):
    log("Guardando como borrador...")
    page.get_by_role("link", name="Save as Draft").click()
    page.wait_for_load_state("networkidle")
    log("Guardado como borrador.")
