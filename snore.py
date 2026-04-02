#!/usr/bin/env python3
"""
mac-snore
A silly macOS menu bar app that snores when you go idle.
GitHub: github.com/Baranidharanv06/mac-snore
"""

import rumps
import threading
import time
import subprocess
import os
from pynput import mouse, keyboard

# ── Config ────────────────────────────────────────────────────────────────────
IDLE_THRESHOLD = 60        # seconds before snoring starts
SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "sounds")
SNORE_SOUND  = os.path.join(SOUNDS_DIR, "snore.mp3")

ICON_IDLE    = "zzZ"
ICON_SNORING = "ZZZ"
ICON_OFF     = "---"

# ── App ───────────────────────────────────────────────────────────────────────
class MacSnoreApp(rumps.App):
    def __init__(self):
        super().__init__(ICON_IDLE, quit_button=None)

        self.menu = [
            rumps.MenuItem("mac-snore", callback=None),
            None,
            rumps.MenuItem("Status: Watching", callback=None),
            rumps.MenuItem("Idle Time: 0s", callback=None),
            None,
            rumps.MenuItem("Enabled", callback=self.toggle),
            None,
            rumps.MenuItem("Quit mac-snore", callback=self.quit_app),
        ]

        self.enabled = True
        self.is_snoring = False
        self._snore_process = None
        self.last_activity = time.time()

        self._start_listeners()

        self._watcher = threading.Thread(target=self._watch_idle, daemon=True)
        self._watcher.start()

        self._tick = rumps.Timer(self._update_menu, 1)
        self._tick.start()

    # ── Use macOS native idle time ─────────────────────────────────────────────
    def _get_idle_seconds(self):
        """Ask macOS how long since the user last touched anything."""
        try:
            result = subprocess.run(
                ["ioreg", "-c", "IOHIDSystem"],
                capture_output=True, text=True
            )
            for line in result.stdout.split("\n"):
                if "HIDIdleTime" in line:
                    ns = int(line.split("=")[-1].strip())
                    return ns / 1_000_000_000  # nanoseconds → seconds
        except Exception:
            pass
        return 0

    # ── Listeners (only used to detect wake from snore) ───────────────────────
    def _start_listeners(self):
        def on_activity(*args, **kwargs):
            if self.is_snoring:
                self._wake_up()

        self._mouse_listener = mouse.Listener(
            on_move=on_activity,
            on_click=on_activity,
            on_scroll=on_activity,
        )
        self._keyboard_listener = keyboard.Listener(on_press=on_activity)
        self._mouse_listener.start()
        self._keyboard_listener.start()

    # ── Idle watcher ──────────────────────────────────────────────────────────
    def _watch_idle(self):
        while True:
            time.sleep(1)
            if not self.enabled:
                continue
            idle = self._get_idle_seconds()
            self.last_activity = idle  # store for menu display
            if idle >= IDLE_THRESHOLD and not self.is_snoring:
                self.is_snoring = True
                self._start_snoring()

    def _start_snoring(self):
        def snore_loop():
            while self.is_snoring and self.enabled:
                self.title = ICON_SNORING
                self._snore_process = subprocess.Popen(["afplay", SNORE_SOUND])
                # Poll every 0.2s so we can stop mid-audio instantly
                while self._snore_process.poll() is None:
                    if not self.is_snoring:
                        self._stop_snore_audio()
                        return
                    time.sleep(0.2)
        threading.Thread(target=snore_loop, daemon=True).start()

    def _stop_snore_audio(self):
        if self._snore_process and self._snore_process.poll() is None:
            self._snore_process.terminate()
            self._snore_process = None

    def _wake_up(self):
        self.is_snoring = False
        self._stop_snore_audio()
        self.title = ICON_IDLE
        rumps.notification(
            title="mac-snore",
            subtitle="",
            message="Oh! You're back!",
            sound=False,
        )

    def _update_menu(self, _):
        idle = int(self._get_idle_seconds())
        self.menu["Idle Time: 0s"].title = f"Idle Time: {idle}s"
        if self.is_snoring:
            self.menu["Status: Watching"].title = "Status: Snoring"
        elif self.enabled:
            self.menu["Status: Watching"].title = "Status: Watching"
        else:
            self.menu["Status: Watching"].title = "Status: Disabled"

    def toggle(self, sender):
        self.enabled = not self.enabled
        if not self.enabled:
            self.is_snoring = False
            self._stop_snore_audio()
            self.title = ICON_OFF
            sender.title = "Disabled"
        else:
            self.title = ICON_IDLE
            sender.title = "Enabled"

    def quit_app(self, _):
        self._stop_snore_audio()
        rumps.quit_application()

if __name__ == "__main__":
    MacSnoreApp().run()
