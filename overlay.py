import ctypes
import tkinter as tk

TRANSPARENT_KEY = "#010101"

REGION_COLORS = {"START": "#00ff00", "DEATH": "#ff0000"}

def _make_click_through(window: tk.Toplevel):
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    WS_EX_TRANSPARENT = 0x00000020

    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    styles = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(
        hwnd, GWL_EXSTYLE, styles | WS_EX_LAYERED | WS_EX_TRANSPARENT
    )

class Overlay(tk.Toplevel):
    def __init__(self, master, monitor_width, monitor_height, targets):
        super().__init__(master)
        self.monitor_width = monitor_width
        self.monitor_height = monitor_height
        self.targets = targets

        self.overrideredirect(True)
        self.geometry(f"{monitor_width}x{monitor_height}+0+0")
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", TRANSPARENT_KEY)
        self.config(bg=TRANSPARENT_KEY)

        self.canvas = tk.Canvas(self, bg=TRANSPARENT_KEY, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._draw()

        self.after(0, lambda: _make_click_through(self))

    def _draw(self):
        for name, region in self.targets:
            color = REGION_COLORS.get(name, "#ffff00")

            x = region["left"] * self.monitor_width
            y = region["top"] * self.monitor_height
            w = region["width"] * self.monitor_width
            h = region["height"] * self.monitor_height

            self.canvas.create_rectangle(x, y, x + w, y + h, outline=color, width=3)

            if name.upper() == "START":
                self.canvas.create_text(
                    x + w / 2, y + h + 8, text=name, fill=color,
                    font=("Segoe UI", 12, "bold"), anchor="n",
                )
            else:
                self.canvas.create_text(
                    x + w / 2, y - 8, text=name, fill=color,
                    font=("Segoe UI", 12, "bold"), anchor="s",
                )

    def update_targets(self, targets):
        self.targets = targets
        self.canvas.delete("all")
        self._draw()

class CaptureRegionEditor(tk.Toplevel):

    HANDLE = 10
    MIN_SIZE = 20

    def __init__(self, master, monitor_width, monitor_height, name,
                 region, default_region, color, on_save, on_cancel):
        super().__init__(master)
        self.monitor_width = monitor_width
        self.monitor_height = monitor_height
        self.name = name
        self.region = dict(region)
        self.default_region = dict(default_region)
        self.color = color
        self.on_save = on_save
        self.on_cancel = on_cancel

        self.overrideredirect(True)
        self.geometry(f"{monitor_width}x{monitor_height}+0+0")
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", TRANSPARENT_KEY)
        self.config(bg=TRANSPARENT_KEY)

        self.canvas = tk.Canvas(self, bg=TRANSPARENT_KEY, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._drag_mode = None
        self._drag_start = (0, 0)
        self._drag_start_rect = None

        self._build_controls()
        self._draw()

        self.canvas.bind("<Button-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<Motion>", self._on_hover)
        self.bind("<Escape>", lambda e: self._cancel())

        self.focus_force()

    def _build_controls(self):
        bar = tk.Frame(self, bg="#1e1e1e")
        self.canvas.create_window(20, 20, anchor="nw", window=bar)

        tk.Label(
            bar, text=f"Editing: {self.name}  (Esc to cancel)",
            bg="#1e1e1e", fg="white", font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(8, 12), pady=6)

        tk.Button(bar, text="Save", command=self._save, width=10).pack(side="left", padx=4, pady=6)
        tk.Button(bar, text="Reset to Default", command=self._reset, width=14).pack(side="left", padx=4, pady=6)
        tk.Button(bar, text="Cancel", command=self._cancel, width=10).pack(side="left", padx=(4, 8), pady=6)

    def _rect_px(self):
        r = self.region
        x = r["left"] * self.monitor_width
        y = r["top"] * self.monitor_height
        w = r["width"] * self.monitor_width
        h = r["height"] * self.monitor_height
        return x, y, w, h

    def _set_rect_px(self, x, y, w, h):
        w = max(w, self.MIN_SIZE)
        h = max(h, self.MIN_SIZE)
        x = max(0, min(x, self.monitor_width - w))
        y = max(0, min(y, self.monitor_height - h))
        self.region = {
            "left": x / self.monitor_width,
            "top": y / self.monitor_height,
            "width": w / self.monitor_width,
            "height": h / self.monitor_height,
        }

    def _handle_centers(self, x, y, w, h):
        return {
            "nw": (x, y), "ne": (x + w, y), "sw": (x, y + h), "se": (x + w, y + h),
            "n": (x + w / 2, y), "s": (x + w / 2, y + h),
            "w": (x, y + h / 2), "e": (x + w, y + h / 2),
        }

    def _draw(self):
        self.canvas.delete("region")
        x, y, w, h = self._rect_px()

        self.canvas.create_rectangle(
            x, y, x + w, y + h, outline=self.color, width=3, tags="region"
        )

        if self.name.upper() == "START":
            label_y, anchor = y + h + 8, "n"
        else:
            label_y, anchor = y - 8, "s"
        self.canvas.create_text(
            x + w / 2, label_y, text=self.name, fill=self.color,
            font=("Segoe UI", 12, "bold"), anchor=anchor, tags="region",
        )

        for hx, hy in self._handle_centers(x, y, w, h).values():
            self.canvas.create_rectangle(
                hx - self.HANDLE / 2, hy - self.HANDLE / 2,
                hx + self.HANDLE / 2, hy + self.HANDLE / 2,
                fill=self.color, outline="white", tags="region",
            )

    def _handle_at(self, px, py):
        x, y, w, h = self._rect_px()
        for name, (hx, hy) in self._handle_centers(x, y, w, h).items():
            if abs(px - hx) <= self.HANDLE and abs(py - hy) <= self.HANDLE:
                return name
        if x <= px <= x + w and y <= py <= y + h:
            return "move"
        return None

    _CURSORS = {
        "nw": "size_nw_se", "se": "size_nw_se",
        "ne": "size_ne_sw", "sw": "size_ne_sw",
        "n": "sb_v_double_arrow", "s": "sb_v_double_arrow",
        "e": "sb_h_double_arrow", "w": "sb_h_double_arrow",
        "move": "fleur",
    }

    def _on_hover(self, event):
        if self._drag_mode is not None:
            return
        hit = self._handle_at(event.x, event.y)
        self.canvas.config(cursor=self._CURSORS.get(hit, "arrow"))

    def _on_press(self, event):
        hit = self._handle_at(event.x, event.y)
        if hit:
            self._drag_mode = hit
            self._drag_start = (event.x, event.y)
            self._drag_start_rect = self._rect_px()

    def _on_drag(self, event):
        if not self._drag_mode:
            return
        dx = event.x - self._drag_start[0]
        dy = event.y - self._drag_start[1]
        x, y, w, h = self._drag_start_rect

        if self._drag_mode == "move":
            x, y = x + dx, y + dy
        else:
            if "n" in self._drag_mode:
                new_y = y + dy
                if (y + h) - new_y >= self.MIN_SIZE:
                    h = (y + h) - new_y
                    y = new_y
            if "s" in self._drag_mode:
                h = max(h + dy, self.MIN_SIZE)
            if "w" in self._drag_mode:
                new_x = x + dx
                if (x + w) - new_x >= self.MIN_SIZE:
                    w = (x + w) - new_x
                    x = new_x
            if "e" in self._drag_mode:
                w = max(w + dx, self.MIN_SIZE)

        self._set_rect_px(x, y, w, h)
        self._draw()

    def _on_release(self, event):
        self._drag_mode = None

    def _save(self):
        self.on_save(dict(self.region))
        self.destroy()

    def _reset(self):
        self.region = dict(self.default_region)
        self._draw()

    def _cancel(self):
        self.on_cancel()
        self.destroy()