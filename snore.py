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
IDLE_THRESHOLD = 30        # seconds before snoring starts
SNORE_INTERVAL = 5         # seconds between each snore sound
SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "sounds")
SNORE_SOUND  = os.path.join(SOUNDS_DIR, "snore.aiff")

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
        self.last_activity = time.time()

        self._ensure_snore_sound()
        self._start_listeners()

        self._watcher = threading.Thread(target=self._watch_idle, daemon=True)
        self._watcher.start()

        self._tick = rumps.Timer(self._update_menu, 1)
        self._tick.start()

    def _ensure_snore_sound(self):
        os.makedirs(SOUNDS_DIR, exist_ok=True)
        if not os.path.exists(SNORE_SOUND):
            subprocess.run(["say", "-v", "Fred", "khrrrr... khrrrr", "-o", SNORE_SOUND])

    def _start_listeners(self):
        def on_activity(*args, **kwargs):
            was_snoring = self.is_snoring
            self.last_activity = time.time()
            if was_snoring:
                self._wake_up()

        self._mouse_listener = mouse.Listener(
            on_move=on_activity,
            on_click=on_activity,
            on_scroll=on_activity,
        )
        self._keyboard_listener = keyboard.Listener(on_press=on_activity)
        self._mouse_listener.start()
        self._keyboard_listener.start()

    def _watch_idle(self):
        while True:
            time.sleep(1)
            if not self.enabled:
                continue
            idle = time.time() - self.last_activity
            if idle >= IDLE_THRESHOLD and not self.is_snoring:
                self.is_snoring = True
                self._start_snoring()

    def _start_snoring(self):
        def snore_loop():
            while self.is_snoring and self.enabled:
                self.title = ICON_SNORING
                subprocess.Popen(["afplay", SNORE_SOUND])
                time.sleep(SNORE_INTERVAL)
        threading.Thread(target=snore_loop, daemon=True).start()

    def _wake_up(self):
        self.is_snoring = False
        self.title = ICON_IDLE
        rumps.notification(
            title="mac-snore",
            subtitle="",
            message="Oh! You're back!",
            sound=False,
        )

    def _update_menu(self, _):
        idle = int(time.time() - self.last_activity)
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
            self.title = ICON_OFF
            sender.title = "Disabled"
        else:
            self.title = ICON_IDLE
            self.last_activity = time.time()
            sender.title = "Enabled"

    def quit_app(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    MacSnoreApp().run()
