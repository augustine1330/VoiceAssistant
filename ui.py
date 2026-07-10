# ui.py
import tkinter as tk
import threading
import math
import time

class VoiceUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kofi")

        # ── Window setup ──────────────────────────────────────────
        self.root.overrideredirect(True)       # remove title bar
        self.root.attributes("-topmost", True) # always on top
        self.root.attributes("-alpha", 0.93)   # slight transparency
        self.root.configure(bg="#0a0a0f")

        # Position bottom center of screen
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w    = 420
        win_h    = 280
        x = (screen_w // 2) - (win_w // 2)
        y = screen_h - win_h - 40
        self.root.geometry(f"{win_w}x{win_h}+{x}+{y}")

        # ── State ─────────────────────────────────────────────────
        self.state          = "idle"     # idle | listening | processing | responding
        self._pulse_angle   = 0
        self._pulse_running = False
        self._ring_radii    = [0, 0, 0]
        self._ring_alpha    = [0, 0, 0]

        # ── Colors ────────────────────────────────────────────────
        self.COLORS = {
            "idle":       "#2d2d5e",
            "listening":  "#00d4ff",
            "processing": "#a855f7",
            "responding": "#00ff88",
        }

        self._build_ui()
        self._start_animation()

    # ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        """Build all UI elements."""
        main = tk.Frame(self.root, bg="#0a0a0f")
        main.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        # ── Close button (small X top right) ─────────────────────
        close_btn = tk.Label(
            main, text="✕", bg="#0a0a0f", fg="#444466",
            font=("Segoe UI", 10), cursor="hand2"
        )
        close_btn.place(relx=1.0, rely=0.0, anchor="ne")
        close_btn.bind("<Button-1>", lambda e: self.hide())

        # ── STT display (what user said) ──────────────────────────
        self.stt_var = tk.StringVar(value="")
        stt_label = tk.Label(
            main,
            textvariable=self.stt_var,
            bg="#0a0a0f",
            fg="#00d4ff",
            font=("Segoe UI", 10),
            wraplength=380,
            justify="center",
            anchor="center",
        )
        stt_label.pack(pady=(8, 2))

        # ── TTS display (what Kofi said) ─────────────────────
        self.tts_var = tk.StringVar(value="Say 'Hey Kofi' to begin")
        tts_label = tk.Label(
            main,
            textvariable=self.tts_var,
            bg="#0a0a0f",
            fg="#e8e8ff",
            font=("Segoe UI", 11, "bold"),
            wraplength=380,
            justify="center",
            anchor="center",
        )
        tts_label.pack(pady=(2, 8))

        # ── State label ───────────────────────────────────────────
        self.state_var = tk.StringVar(value="IDLE")
        state_label = tk.Label(
            main,
            textvariable=self.state_var,
            bg="#0a0a0f",
            fg="#444466",
            font=("Segoe UI", 8),
        )
        state_label.pack(pady=(0, 4))

        # ── Canvas for animated mic orb ───────────────────────────
        self.canvas = tk.Canvas(
            main,
            width=140,
            height=140,
            bg="#0a0a0f",
            highlightthickness=0,
        )
        self.canvas.pack()

        # Draw initial orb
        self._draw_orb()

    # ─────────────────────────────────────────────────────────────
    def _draw_orb(self):
        """Draw the mic orb and rings on the canvas."""
        self.canvas.delete("all")
        cx, cy = 70, 70
        color  = self.COLORS.get(self.state, "#2d2d5e")

        # ── Outer glow rings ──────────────────────────────────────
        ring_sizes  = [58, 46, 34]
        ring_colors = ["#0a0a0f", "#0a0a0f", "#0a0a0f"]

        if self.state != "idle":
            # Animate rings expanding outward
            for i, base_r in enumerate(ring_sizes):
                r     = base_r + self._ring_radii[i]
                alpha = max(0, 1.0 - self._ring_alpha[i])
                hex_a = format(int(alpha * 60), '02x')
                ring_color = color + hex_a if len(color) == 7 else color
                self.canvas.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    outline=color,
                    width=1,
                    fill="",
                )

        # ── Core orb ─────────────────────────────────────────────
        core_r = 28
        # Outer glow
        self.canvas.create_oval(
            cx - core_r - 8, cy - core_r - 8,
            cx + core_r + 8, cy + core_r + 8,
            fill="#0a0a0f", outline=color, width=1,
        )
        # Inner glow
        self.canvas.create_oval(
            cx - core_r - 4, cy - core_r - 4,
            cx + core_r + 4, cy + core_r + 4,
            fill="#0a0a0f", outline=color, width=2,
        )
        # Core circle
        self.canvas.create_oval(
            cx - core_r, cy - core_r,
            cx + core_r, cy + core_r,
            fill=color, outline="",
        )

        # ── Mic icon ──────────────────────────────────────────────
        mic_color = "#0a0a0f" if self.state != "idle" else "#444466"

        # Mic body (rounded rectangle approximation)
        self.canvas.create_rectangle(
            cx - 7, cy - 14, cx + 7, cy + 8,
            fill=mic_color, outline="", width=0,
        )
        self.canvas.create_oval(
            cx - 7, cy - 20, cx + 7, cy - 6,
            fill=mic_color, outline="",
        )
        self.canvas.create_oval(
            cx - 7, cy + 2, cx + 7, cy + 16,
            fill=mic_color, outline="",
        )

        # Mic stand arc
        self.canvas.create_arc(
            cx - 12, cy, cx + 12, cy + 24,
            start=0, extent=-180,
            style=tk.ARC, outline=mic_color, width=2,
        )

        # Mic stand line
        self.canvas.create_line(
            cx, cy + 24, cx, cy + 32,
            fill=mic_color, width=2,
        )
        self.canvas.create_line(
            cx - 8, cy + 32, cx + 8, cy + 32,
            fill=mic_color, width=2,
        )

    # ─────────────────────────────────────────────────────────────
    def _start_animation(self):
        """Start the animation loop."""
        self._animate()

    def _animate(self):
        """Animation tick — runs every 50ms."""
        if self.state != "idle":
            # Expand rings outward
            for i in range(3):
                self._ring_radii[i] += 0.8 + i * 0.3
                self._ring_alpha[i] += 0.04 + i * 0.01

                # Reset ring when it's fully expanded
                if self._ring_alpha[i] >= 1.0:
                    self._ring_radii[i] = i * 6.0
                    self._ring_alpha[i] = i * 0.3

        self._draw_orb()
        self.root.after(50, self._animate)

    # ─────────────────────────────────────────────────────────────
    # Public methods — called from main.py
    # ─────────────────────────────────────────────────────────────
    def set_state(self, state: str):
        """
        Update the UI state.
        state: 'idle' | 'listening' | 'processing' | 'responding'
        """
        self.state = state
        labels = {
            "idle":       "IDLE",
            "listening":  "LISTENING...",
            "processing": "THINKING...",
            "responding": "SPEAKING...",
        }
        self.state_var.set(labels.get(state, state.upper()))

        if state == "idle":
            self.tts_var.set("Say 'Hey Jarvis' to begin")
            self.stt_var.set("")
            for i in range(3):
                self._ring_radii[i] = 0
                self._ring_alpha[i] = 0

    def show_stt(self, text: str):
        """Show what the user said."""
        if text:
            self.stt_var.set(f"You: {text}")

    def show_tts(self, text: str):
        """Show what Kofi is saying."""
        if text:
            self.tts_var.set(f"{text}")

    def clear_stt(self):
        self.stt_var.set("")

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()

    def run(self):
        """Start the UI main loop — call this in a thread."""
        self.root.mainloop()