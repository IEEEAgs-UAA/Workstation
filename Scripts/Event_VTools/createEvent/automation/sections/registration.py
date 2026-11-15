"""Sección Registration & Payment."""

from __future__ import annotations

from playwright.sync_api import Page


def open_registration_section(page: Page):
    page.get_by_text("Registration & Payment", exact=True).click()
    page.wait_for_timeout(500)


def select_registration_type_none(page: Page):
    radio = page.locator("#_registration_type_None")
    if not radio.is_checked():
        radio.check()
        page.wait_for_timeout(500)
