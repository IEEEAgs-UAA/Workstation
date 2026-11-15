"""Sección Location (física / virtual / híbrida)."""

from __future__ import annotations

from playwright.sync_api import Page

from ..constants import _noop
from ..tinymce import fill_tinymce


def open_location_section(page: Page):
    page.get_by_text("Location", exact=True).click()
    page.wait_for_timeout(500)


def select_location_type(page: Page, location_type: str):
    page.check(f"input[name='meeting[location_type]'][value='{location_type}']")
    page.wait_for_timeout(300)


def fill_virtual_info(page: Page, html_content: str):
    fill_tinymce(page, "meeting_virtual_info", html_content)


def fill_physical_address(
    page: Page,
    address1: str | None = None,
    address2: str | None = None,
    city: str | None = None,
    postal_code: str | None = None,
    building: str | None = None,
    room_number: str | None = None,
    map_url: str | None = None,
):
    field_map = {
        "#meeting_address1": address1,
        "#meeting_address2": address2,
        "#meeting_city": city,
        "#meeting_postal_code": postal_code,
        "#meeting_building": building,
        "#meeting_room_number": room_number,
        "#meeting_map_url": map_url,
    }
    for selector, value in field_map.items():
        if value is not None:
            page.fill(selector, value)


def select_country(page: Page, country_label: str):
    page.select_option("#meeting_country_id", label=country_label)
    page.wait_for_timeout(1000)


def select_state(page: Page, state_label: str):
    page.select_option("#meeting_state_id", label=state_label)


def set_override_lat_lng(page: Page, latitude: str, longitude: str):
    page.fill("#meeting_user_override_latitude", latitude)
    page.fill("#meeting_user_override_longitude", longitude)


def fill_location(page: Page, location: dict, log=_noop):
    loc_type = location.get("type", "physical")
    log(f"Configurando ubicación tipo '{loc_type}'...")
    select_location_type(page, loc_type)

    if loc_type in ("physical", "hybrid"):
        fill_physical_address(
            page,
            address1=location.get("address1"),
            address2=location.get("address2"),
            city=location.get("city"),
            postal_code=location.get("postal_code"),
            building=location.get("building"),
            room_number=location.get("room_number"),
            map_url=location.get("map_url"),
        )
        if location.get("country"):
            select_country(page, location["country"])
        if location.get("state"):
            select_state(page, location["state"])

    if loc_type in ("virtual", "hybrid") and location.get("virtual_info_html"):
        fill_virtual_info(page, location["virtual_info_html"])
