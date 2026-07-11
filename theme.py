# colors
BG = "#0d1117"          # background
BG_PANEL = "#161b22"    # cards / frames / debug bar
BG_RAISED = "#1c2128"   # buttons
BORDER = "#30363d"      # separators / outlines

TEXT = "#c9d1d9"        # primary text
TEXT_DIM = "#8b949e"    # secondary text
TEXT_BRIGHT = "#f0f3f6" # headings

ACCENT = "#58a6ff"      # links
START_COLOR = "#00e08a" # START
DEATH_COLOR = "#ff5c5c" # DEATH

# fonts
FONT_DISPLAY = ("Segoe UI", 20, "bold")
FONT_SUBTITLE = ("Segoe UI", 10)
FONT_CAPTION = ("Segoe UI", 8)
FONT_SECTION = ("Segoe UI", 12, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 10) # status / debug
FONT_MONO_BOLD = ("Consolas", 10, "bold")

REGION_ACCENTS = {"START": START_COLOR, "DEATH": DEATH_COLOR}

def apply_ttk_theme(style):
    style.theme_use("clam")

    style.configure(".", background=BG, foreground=TEXT, font=FONT_BODY)

    style.configure("TFrame", background=BG)
    style.configure("Panel.TFrame", background=BG_PANEL)

    style.configure("TLabel", background=BG, foreground=TEXT, font=FONT_BODY)
    style.configure(
        "Title.TLabel", background=BG, foreground=TEXT_BRIGHT, font=FONT_DISPLAY
    )
    style.configure(
        "Subtitle.TLabel", background=BG, foreground=TEXT_DIM, font=FONT_SUBTITLE
    )
    style.configure(
        "Caption.TLabel", background=BG, foreground=TEXT_DIM, font=FONT_CAPTION
    )
    style.configure(
        "Section.TLabel", background=BG, foreground=TEXT_BRIGHT, font=FONT_SECTION
    )
    style.configure(
        "Status.TLabel", background=BG, foreground=ACCENT, font=FONT_MONO
    )
    style.configure(
        "Notification.TLabel",
        background=BG_PANEL,
        foreground=TEXT,
        font=FONT_BODY,
        padding=8,
    )
    style.configure(
        "Start.TLabel", background=BG, foreground=START_COLOR, font=FONT_SECTION
    )
    style.configure(
        "Death.TLabel", background=BG, foreground=DEATH_COLOR, font=FONT_SECTION
    )

    style.configure(
        "TSeparator", background=BORDER,
    )

    style.configure(
        "TButton",
        background=BG_RAISED,
        foreground=TEXT_BRIGHT,
        font=FONT_BODY,
        borderwidth=1,
        focusthickness=0,
        relief="flat",
        padding=(10, 8),
    )
    style.map(
        "TButton",
        background=[("active", BORDER), ("pressed", BORDER), ("disabled", BG_PANEL)],
        foreground=[("disabled", TEXT_DIM)],
    )

    style.configure(
        "Accent.TButton",
        background=ACCENT,
        foreground="#04121f",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        padding=(10, 10),
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#7cb8ff"), ("pressed", "#3f8ee6")],
    )

    style.configure(
        "Stop.TButton",
        background=DEATH_COLOR,
        foreground="#1a0000",
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        padding=(10, 10),
    )
    style.map(
        "Stop.TButton",
        background=[("active", "#ff8080"), ("pressed", "#e64545")],
    )