"""Detección y lanzamiento de Chrome con depuración remota."""

from __future__ import annotations

import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from .constants import CREATE_EVENT_URL, DEBUG_PORT, _noop


def find_chrome_executable() -> str | None:
    """Busca un ejecutable de Chrome/Chromium en Windows, Linux o macOS."""
    candidates: list[str] = []

    if sys.platform.startswith("win"):
        import os as _os
        program_files = [
            _os.environ.get("PROGRAMFILES", r"C:\Program Files"),
            _os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
            _os.environ.get("LOCALAPPDATA", ""),
        ]
        for pf in program_files:
            if pf:
                candidates.append(str(Path(pf) / "Google" / "Chrome" / "Application" / "chrome.exe"))
        candidates += ["chrome.exe", "chrome"]
    elif sys.platform == "darwin":
        candidates.append("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        candidates += ["google-chrome", "chromium"]
    else:  # Linux y similares
        candidates += [
            "google-chrome-stable",
            "google-chrome",
            "chromium-browser",
            "chromium",
        ]

    for cand in candidates:
        # Ruta absoluta que ya existe
        if Path(cand).is_file():
            return cand
        # Buscar en PATH
        found = shutil.which(cand)
        if found:
            return found

    return None


def _port_is_open(port: int, host: str = "127.0.0.1", timeout: float = 0.5) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0


def launch_chrome_with_debugging(
    chrome_path: str,
    url: str = CREATE_EVENT_URL,
    port: int = DEBUG_PORT,
    wait_seconds: float = 15.0,
    log=_noop,
) -> subprocess.Popen:
    """
    Lanza Chrome con --remote-debugging-port en un perfil temporal dedicado
    (para no interferir con la sesión normal del usuario) y espera hasta
    que el puerto de depuración responda.
    """
    user_data_dir = tempfile.mkdtemp(prefix="ieee_vtools_chrome_")
    args = [
        chrome_path,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        url,
    ]
    log(f"Iniciando Chrome: {chrome_path}")
    proc = subprocess.Popen(args)

    waited = 0.0
    step = 0.5
    while waited < wait_seconds:
        if _port_is_open(port):
            log("Puerto de depuración de Chrome listo.")
            return proc
        time.sleep(step)
        waited += step

    raise RuntimeError(
        f"Chrome no respondió en el puerto {port} tras {wait_seconds}s. "
        "Revisa que no haya otra instancia de Chrome bloqueando el puerto."
    )
