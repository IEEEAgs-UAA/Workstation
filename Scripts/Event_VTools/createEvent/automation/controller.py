"""Controlador de sesión: mantiene vivo el browser/page entre clics de la GUI."""

from __future__ import annotations

import subprocess
import time

from playwright.sync_api import Page, sync_playwright

from .chrome import _port_is_open, find_chrome_executable, launch_chrome_with_debugging
from .constants import CREATE_EVENT_URL, DEBUG_PORT, _noop
from .form import fill_event_form
from .login import login_if_needed
from .sections.navigation import save_as_draft


class AutomationController:
    """
    Envuelve el ciclo de vida de Playwright + Chrome para que la GUI pueda:
      1) Conectar (lanzando Chrome o reusando uno ya abierto)
      2) Llenar el formulario
      3) Guardar como borrador
      4) Cerrar todo
    manteniendo el mismo `page` vivo entre pasos.
    """

    def __init__(self):
        self._playwright = None
        self._browser = None
        self._chrome_process: subprocess.Popen | None = None
        self.page: Page | None = None

    def connect(
        self,
        launch_chrome: bool,
        username: str,
        password: str,
        log=_noop,
    ) -> Page:
        self._playwright = sync_playwright().start()

        if launch_chrome:
            chrome_path = find_chrome_executable()
            if not chrome_path:
                raise RuntimeError(
                    "No se encontró Chrome instalado en este sistema. "
                    "Instálalo o desactiva la opción 'Iniciar Chrome automáticamente' "
                    "y ábrelo manualmente con --remote-debugging-port=9222."
                )
            self._chrome_process = launch_chrome_with_debugging(chrome_path, log=log)
            # Da tiempo a que la pestaña inicial cargue la URL
            time.sleep(1.5)
        else:
            if not _port_is_open(DEBUG_PORT):
                raise RuntimeError(
                    f"No hay ninguna instancia de Chrome escuchando en el puerto {DEBUG_PORT}. "
                    "Actívalo manualmente con:\n"
                    "  google-chrome-stable --user-data-dir=/tmp/chrome-playwright "
                    f"--remote-debugging-port={DEBUG_PORT}\n"
                    "o activa la opción 'Iniciar Chrome automáticamente'."
                )

        log("Conectando a Chrome vía CDP...")
        self._browser = self._playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{DEBUG_PORT}")
        context = self._browser.contexts[0] if self._browser.contexts else self._browser.new_context()

        page = None
        for candidate in context.pages:
            if "event/create"  in candidate.url:
                page = candidate
                break
            if "event/edit" in candidate.url:
                page = candidate
                break
        if page is None:
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(CREATE_EVENT_URL)

        login_if_needed(page, username, password, log=log)

        self.page = page
        return page

    def fill(self, event: dict, host_org_name: str, host_spoid: str, host_contact_email: str, log=_noop):
        if self.page is None:
            raise RuntimeError("No hay conexión activa. Ejecuta connect() primero.")
        fill_event_form(self.page, event, host_org_name, host_spoid, host_contact_email, log=log)

    def save_draft(self, log=_noop):
        if self.page is None:
            raise RuntimeError("No hay conexión activa.")
        save_as_draft(self.page, log=log)

    def close(self, log=_noop):
        try:
            if self._browser:
                self._browser.close()
        except Exception:
            pass
        try:
            if self._playwright:
                self._playwright.stop()
        except Exception:
            pass
        if self._chrome_process:
            try:
                self._chrome_process.terminate()
            except Exception:
                pass
        log("Sesión cerrada.")
        self.page = None
