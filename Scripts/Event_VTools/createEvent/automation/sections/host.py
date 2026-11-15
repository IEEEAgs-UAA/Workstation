"""Sección Host y Co-hosts."""

from __future__ import annotations

import re

from playwright.sync_api import Page

from ..constants import _noop
from ..tinymce import fill_tinymce


def fill_host_organizational_unit(page: Page, org_name: str, spoid: str | None = None, index: int = 0):
    field_id = f"_event_host_spoid_{index}"
    if spoid:
        page.eval_on_selector(
            f"#{field_id}",
            """(el, spoid) => {
                el.value = spoid;
                el.setAttribute('data-spoid', spoid);
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.dispatchEvent(new Event('input', { bubbles: true }));
            }""",
            spoid,
        )
    else:
        page.fill(f"#_event_host_search_{index}", org_name)
        page.wait_for_selector(f"text={org_name}", timeout=10000)
        page.click(f"text={org_name}")


def fill_contact_email(page: Page, email: str, index: int = 0):
    page.fill(f"#meeting_meeting_host_{index}_contact_email", email)


def fill_extra_contact_info(page: Page, html_content: str):
    fill_tinymce(page, "meeting_contact_display", html_content)


def enable_add_cohost(page: Page):
    button = page.locator(
        'a._add_additional_host_button[data-additional-host-url="/tego_/event/additional_host"]'
    )
    button.wait_for(state="visible", timeout=10000)
    button.click()
    page.wait_for_timeout(1600)


def add_cohost(page: Page):
    page.get_by_role("link", name=re.compile(r"Add\s+Co-Host", re.IGNORECASE)).click()
    page.wait_for_timeout(800)


def fill_cohost(page: Page, index: int = 1, org_name: str | None = None, spoid: str | None = None, email: str | None = None):
    fill_host_organizational_unit(page, org_name=org_name or "", spoid=spoid, index=index)
    if email:
        fill_contact_email(page, email, index=index)


def fill_cohosts(page: Page, cohosts: list, log=_noop):
    if not cohosts:
        return

    log("Habilitando cohosts...")
    enable_add_cohost(page)

    for i, cohost_data in enumerate(cohosts, start=1):
        log(f"Llenando cohost #{i}: {cohost_data.get('organization', '(sin organización)')}")
        if i > 1:
            add_cohost(page)
        fill_cohost(
            page,
            index=i,
            org_name=cohost_data.get("organization"),
            spoid=cohost_data.get("spoid"),
            email=cohost_data.get("email"),
        )
