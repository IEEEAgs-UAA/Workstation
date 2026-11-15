"""Login automático en vTools (solo si aparece el formulario)."""

from __future__ import annotations

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from .constants import _noop


def login_if_needed(page: Page, username: str, password: str, log=_noop, timeout: int = 4000) -> bool:
    """
    Revisa si el formulario de login está presente y, si es así, lo llena
    y lo envía. Devuelve True si hizo login, False si ya había sesión iniciada.
    """
    try:
        page.wait_for_selector("#username", timeout=timeout)
    except PlaywrightTimeoutError:
        log("Sesión ya iniciada (no se detectó formulario de login).")
        return False

    if not username or not password:
        raise RuntimeError(
            "Se detectó el formulario de login pero no hay credenciales "
            "(IEEE_USER / IEEE_PASS). Complétalas en la interfaz o en el .env"
        )

    log("Formulario de login detectado, ingresando credenciales...")
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("#modalWindowRegisterSignInBtn")
    page.wait_for_load_state("networkidle")
    log("Login completado.")
    return True
