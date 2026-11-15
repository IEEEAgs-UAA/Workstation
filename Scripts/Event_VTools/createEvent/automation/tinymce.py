"""Helper genérico para campos TinyMCE."""

from __future__ import annotations

from playwright.sync_api import Page


def fill_tinymce(page: Page, textarea_id: str, html_content: str):
    iframe_id = f"{textarea_id}_ifr"
    frame = page.frame_locator(f"#{iframe_id}")
    body = frame.locator("body#tinymce")
    body.click()
    body.evaluate(
        """(el, html) => {
            el.innerHTML = html;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""",
        html_content,
    )
