"""Acciones: ejecutar, guardar borrador, cerrar, log."""

from __future__ import annotations

import queue
import threading
from tkinter import messagebox

from .. import automation as event_filler


class ActionsMixin:
    def _log(self, msg: str):
        # Seguro para llamarse desde el worker thread: solo encola.
        self.log_queue.put(msg)

    def _poll_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_widget.configure(state="normal")
                self.log_widget.insert("end", msg + "\n")
                self.log_widget.see("end")
                self.log_widget.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(150, self._poll_log_queue)

    def _set_running_state(self, running: bool):
        self.run_btn.config(state="disabled" if running else "normal")

    def _on_run_clicked(self):
        event = self._current_event()

        try:
            event_filler.validate_event_dates(event)
        except ValueError as exc:
            messagebox.showerror("Fecha inválida", str(exc))
            return

        launch_chrome = self.launch_chrome_var.get()
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if launch_chrome and (not username or not password):
            if not messagebox.askyesno(
                "Sin credenciales",
                "No indicaste usuario/contraseña. Si Chrome pide login, la automatización "
                "se detendrá. ¿Deseas continuar de todas formas?",
            ):
                return

        self._set_running_state(True)
        self.worker_thread = threading.Thread(
            target=self._run_worker,
            args=(event, launch_chrome, username, password),
            daemon=True,
        )
        self.worker_thread.start()

    def _run_worker(self, event: dict, launch_chrome: bool, username: str, password: str):
        try:
            self._log("=== Iniciando automatización ===")
            self.controller.connect(launch_chrome, username, password, log=self._log)
            self.controller.fill(
                event,
                host_org_name=self.host_org_var.get().strip(),
                host_spoid=self.host_spoid_var.get().strip(),
                host_contact_email=self.host_email_var.get().strip(),
                log=self._log,
            )
            self._log("=== Listo. Revisa el formulario en el navegador. ===")
            self.save_btn.config(state="normal")
            self.close_btn.config(state="normal")
        except Exception as exc:  # noqa: BLE001 - queremos capturar y mostrar cualquier error
            self._log(f"ERROR: {exc}")
            self.after(0, lambda: messagebox.showerror("Error durante la automatización", str(exc)))
        finally:
            self.after(0, lambda: self._set_running_state(False))

    def _on_save_clicked(self):
        def worker():
            try:
                self.controller.save_draft(log=self._log)
            except Exception as exc:  # noqa: BLE001
                self._log(f"ERROR al guardar: {exc}")
                self.after(0, lambda: messagebox.showerror("Error al guardar", str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_close_clicked(self):
        def worker():
            self.controller.close(log=self._log)
            self.after(0, lambda: self.save_btn.config(state="disabled"))
            self.after(0, lambda: self.close_btn.config(state="disabled"))

        threading.Thread(target=worker, daemon=True).start()

    def _on_window_close(self):
        try:
            self.controller.close(log=lambda _m: None)
        except Exception:
            pass
        self.destroy()
