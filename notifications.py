import tkinter as tk
from tkinter import ttk
from typing import Optional

import theme


class NotificationWindow(tk.Toplevel):
    def __init__(self, master, message: str):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg=theme.BG_PANEL)

        self.label = ttk.Label(
            self,
            text=message,
            style="Notification.TLabel",
            anchor="center",
            justify="center",
            wraplength=420,
        )
        self.label.pack(padx=16, pady=12)

        self.update_idletasks()
        self._reposition(master)

    def _reposition(self, master):
        master.update_idletasks()

        window_width = self.winfo_width()
        window_height = self.winfo_height()
        x = master.winfo_rootx() + master.winfo_width() - window_width - 20
        y = master.winfo_rooty() + 20

        if x < 0:
            x = 20
        if y < 0:
            y = 20

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")


class NotificationManager:
    def __init__(self, root, enabled=True, timeout_seconds=5.0):
        self.root = root
        self.enabled = enabled
        self.timeout_seconds = float(timeout_seconds)
        self._window = None
        self._hide_job = None

    def update_settings(self, enabled=None, timeout_seconds=None):
        if enabled is not None:
            self.enabled = bool(enabled)
        if timeout_seconds is not None:
            self.timeout_seconds = max(0.5, float(timeout_seconds))

    def show(self, message: str, duration_seconds: Optional[float] = None):
        if not self.enabled:
            return
        if duration_seconds is None:
            duration_seconds = self.timeout_seconds
        duration_ms = int(max(0.5, float(duration_seconds)) * 1000)
        self.root.after(0, lambda: self._show(message, duration_ms))

    def _show(self, message: str, duration_ms: int):
        if self._window is None or not self._window.winfo_exists():
            self._window = NotificationWindow(self.root, message)
        else:
            self._window.label.config(text=message)
            self._window.deiconify()
            self._window._reposition(self.root)

        if self._hide_job is not None:
            self.root.after_cancel(self._hide_job)
        self._hide_job = self.root.after(duration_ms, self._hide)

    def _hide(self):
        if self._window and self._window.winfo_exists():
            self._window.withdraw()
        self._hide_job = None

    def destroy(self):
        if self._hide_job is not None:
            self.root.after_cancel(self._hide_job)
            self._hide_job = None
        if self._window and self._window.winfo_exists():
            self._window.destroy()
            self._window = None
