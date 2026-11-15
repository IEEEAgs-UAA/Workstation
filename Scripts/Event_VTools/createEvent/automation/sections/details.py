"""Sección Details (título, categoría, fechas, textos)."""

from __future__ import annotations

from playwright.sync_api import Page

from ..dates import validate_datetime_str
from ..tinymce import fill_tinymce


def fill_title(page: Page, title: str):
    page.fill("#meeting_title", title)


def select_category(page: Page, category_label: str):
    page.select_option("#meeting_category_id", label=category_label)
    page.wait_for_timeout(800)


def select_subcategory(page: Page, subcategory_label: str):
    page.select_option("#meeting_subcategory_id", label=subcategory_label)


def set_wie_event(page: Page, checked: bool = True):
    checkbox = page.locator("#meeting_wie_event")
    if checkbox.is_checked() != checked:
        checkbox.click()


def fill_start_end_time(page: Page, start_text: str, end_text: str):
    """
    CAMPO SENSIBLE: valida el formato antes de tocar la página. El picker
    de vTools no avisa si el texto no calza con "DD MMM YYYY hh:mm A".
    """
    validate_datetime_str(start_text)
    validate_datetime_str(end_text)

    for selector, value in [("#start_time_in_zone", start_text), ("#end_time_in_zone", end_text)]:
        page.fill(selector, value)
        page.eval_on_selector(
            selector,
            "el => el.dispatchEvent(new Event('change', { bubbles: true }))",
        )


def select_timezone(page: Page, timezone_value: str):
    page.select_option("#meeting_tm_zone_info", value=timezone_value)


def fill_description(page: Page, html_content: str):
    fill_tinymce(page, "meeting_description", html_content)


def fill_header(page: Page, html_content: str):
    fill_tinymce(page, "meeting_header", html_content)


def fill_footer(page: Page, html_content: str):
    fill_tinymce(page, "meeting_footer", html_content)


def fill_agenda(page: Page, html_content: str):
    fill_tinymce(page, "meeting_agenda", html_content)


def fill_keywords(page: Page, keywords: str):
    page.fill("#meeting_keywords", keywords)


def fill_survey_url(page: Page, url: str):
    page.fill("#meeting_survey_url", url)
