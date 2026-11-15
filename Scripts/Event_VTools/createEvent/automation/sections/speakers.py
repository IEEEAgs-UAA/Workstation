"""Sección Speakers."""

from __future__ import annotations

from playwright.sync_api import Page

from ..constants import _noop
from ..tinymce import fill_tinymce


def open_speakers_section(page: Page):
    page.get_by_text("Speakers", exact=True).click()
    page.wait_for_timeout(500)


def add_speaker(page: Page):
    page.get_by_role("link", name="Add speaker").click()
    page.wait_for_timeout(800)


def expand_speaker_panel(page: Page, index: int = 1):
    page.click(f"#_event_speaker{index}_heading a")
    page.wait_for_timeout(400)


def fill_speaker(
    page: Page,
    index: int = 1,
    topic: str | None = None,
    dlp_speaker: bool | None = None,
    topic_description_html: str | None = None,
    prefix: str | None = None,
    first_name: str | None = None,
    middle_name: str | None = None,
    last_name: str | None = None,
    suffix: str | None = None,
    display_name: str | None = None,
    speaker_url: str | None = None,
    address1: str | None = None,
    address2: str | None = None,
    city: str | None = None,
    country_label: str | None = None,
    state_label: str | None = None,
    postal_code: str | None = None,
    email: str | None = None,
    biography_html: str | None = None,
    organization: str | None = None,
):
    prefix_id = f"speakers_speaker{index}"

    simple_fields = {
        f"#{prefix_id}_topic": topic,
        f"#{prefix_id}_prefix": prefix,
        f"#{prefix_id}_first_name": first_name,
        f"#{prefix_id}_middle_name": middle_name,
        f"#{prefix_id}_last_name": last_name,
        f"#{prefix_id}_suffix": suffix,
        f"#{prefix_id}_display_name": display_name,
        f"#{prefix_id}_speaker_url": speaker_url,
        f"#{prefix_id}_address1": address1,
        f"#{prefix_id}_address2": address2,
        f"#{prefix_id}_city": city,
        f"#{prefix_id}_postal_code": postal_code,
        f"#{prefix_id}_email": email,
        f"#{prefix_id}_organization": organization,
    }
    for selector, value in simple_fields.items():
        if value is not None:
            page.fill(selector, value)

    if dlp_speaker is not None:
        checkbox = page.locator(f"#{prefix_id}_dlp_speaker")
        if checkbox.is_checked() != dlp_speaker:
            checkbox.click()

    if topic_description_html is not None:
        fill_tinymce(page, f"{prefix_id}_topic_description", topic_description_html)

    if biography_html is not None:
        fill_tinymce(page, f"{prefix_id}_biography", biography_html)

    if country_label is not None:
        page.select_option(f"#{prefix_id}__country_id", label=country_label)
        page.wait_for_timeout(1000)

    if state_label is not None:
        page.select_option(f"#{prefix_id}__state_id", label=state_label)


def fill_speakers(page: Page, speakers: list, log=_noop):
    for i, speaker_data in enumerate(speakers, start=1):
        log(f"Llenando speaker #{i}: {speaker_data.get('display_name', '(sin nombre)')}")
        if i > 2:
            add_speaker(page)
        expand_speaker_panel(page, index=i)
        fill_speaker(
            page,
            index=i,
            topic=speaker_data.get("topic"),
            dlp_speaker=speaker_data.get("dlp_speaker"),
            topic_description_html=speaker_data.get("topic_description_html"),
            prefix=speaker_data.get("prefix"),
            first_name=speaker_data.get("first_name"),
            middle_name=speaker_data.get("middle_name"),
            last_name=speaker_data.get("last_name"),
            suffix=speaker_data.get("suffix"),
            display_name=speaker_data.get("display_name"),
            speaker_url=speaker_data.get("speaker_url"),
            address1=speaker_data.get("address1"),
            address2=speaker_data.get("address2"),
            city=speaker_data.get("city"),
            country_label=speaker_data.get("country"),
            state_label=speaker_data.get("state"),
            postal_code=speaker_data.get("postal_code"),
            email=speaker_data.get("email"),
            biography_html=speaker_data.get("biography_html"),
            organization=speaker_data.get("organization"),
        )
