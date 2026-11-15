"""Sección Report and Attendance."""

from __future__ import annotations

from playwright.sync_api import Page

from ..tinymce import fill_tinymce


def open_reporting_section(page: Page):
    page.get_by_text("Report and Attendance", exact=True).click()
    page.wait_for_timeout(500)


def fill_IEEE_Attendance(page: Page, html_content: str):
    fill_tinymce(page, "#meeting_ieee_attending", html_content)


def fill_Guest_Attendance(page: Page, html_content: str):
    fill_tinymce(page, "#meeting_guests_attending", html_content)
