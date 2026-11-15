"""Sincroniza el formulario con el evento seleccionado."""

from __future__ import annotations

import tkinter as tk

from ..data.EventsVtools import events
from .helpers import _unwrap_html, _wrap_html


class EventBindingMixin:
    def _set_text(self, widget: tk.Text, value: str):
        prev_state = widget.cget("state")
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", _unwrap_html(value))
        widget.config(state=prev_state)

    def _on_event_selected(self, _evt=None):
        idx = self.event_combo.current()
        if idx < 0:
            return
        event = events[idx]

        self.title_var.set(event["title"])
        self.start_picker.set_from_string(event["start_time"])
        self.end_picker.set_from_string(event["end_time"])
        self.timezone_var.set(event.get("timezone", "America/Mexico_City"))

        self._set_text(self.description_text, event.get("description", ""))
        self._set_text(self.header_text, event.get("header", ""))
        self._set_text(self.footer_text, event.get("footer", ""))
        self._set_text(self.agenda_text, event.get("agenda", ""))
        self.keywords_var.set(event.get("keywords", ""))
        self.survey_url_var.set(event.get("survey_url", ""))

        loc = event.get("location", {})
        self.location_type_var.set(loc.get("type", "physical"))
        self.address1_var.set(loc.get("address1", ""))
        self.address2_var.set(loc.get("address2", ""))
        self.city_var.set(loc.get("city", ""))
        self.postal_code_var.set(loc.get("postal_code", ""))
        self.building_var.set(loc.get("building", ""))
        self.country_var.set(loc.get("country", ""))
        self.state_var.set(loc.get("state", ""))
        self._update_location_visibility()
        self._set_text(self.virtual_info_text, loc.get("virtual_info_html", ""))
        self._update_location_visibility()

        self._load_cohosts(event.get("cohosts", []))

    def _current_event(self) -> dict:
        idx = self.event_combo.current()
        base = dict(events[idx])

        base["title"] = self.title_var.get().strip()
        base["start_time"] = self.start_picker.get_vtools_string()
        base["end_time"] = self.end_picker.get_vtools_string()
        base["timezone"] = self.timezone_var.get().strip()

        base["description"] = _wrap_html(self.description_text.get("1.0", "end-1c"))
        base["header"] = _wrap_html(self.header_text.get("1.0", "end-1c"))
        base["footer"] = _wrap_html(self.footer_text.get("1.0", "end-1c"))
        base["agenda"] = _wrap_html(self.agenda_text.get("1.0", "end-1c"))
        base["keywords"] = self.keywords_var.get().strip()
        base["survey_url"] = self.survey_url_var.get().strip()

        base["location"] = {
            "type": self.location_type_var.get(),
            "address1": self.address1_var.get().strip(),
            "address2": self.address2_var.get().strip(),
            "city": self.city_var.get().strip(),
            "postal_code": self.postal_code_var.get().strip(),
            "building": self.building_var.get().strip(),
            "country": self.country_var.get().strip(),
            "state": self.state_var.get().strip(),
            "virtual_info_html": _wrap_html(self.virtual_info_text.get("1.0", "end-1c")),
        }
        base["cohosts"] = [
            {
                "organization": row["org_var"].get().strip(),
                "spoid": row["spoid_var"].get().strip(),
                "email": row["email_var"].get().strip(),
            }
            for row in self.cohost_rows
            if any(
                (
                    row["org_var"].get().strip(),
                    row["spoid_var"].get().strip(),
                    row["email_var"].get().strip(),
                )
            )
        ]
        return base
