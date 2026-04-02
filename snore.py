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
        self.last_activity = time.time()
        self._snore_process = None  # track afplay so we can kill it

        self._start_listeners()

        self._watcher = threading.Thread(target=self._watch_idle, daemon=True)
        self._watcher.start()

        self._tick = rumps.Timer(self._update_menu, 1)
        self._tick.start()

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
                self._snore_process = subprocess.Popen(["afplay", SNORE_SOUND])
                self._snore_process.wait()  # wait for audio to finish naturally
        threading.Thread(target=snore_loop, daemon=True).start()

    def _stop_snore_audio(self):
        """Kill the afplay process immediately."""
        if self._snore_process and self._snore_process.poll() is None:
            self._snore_process.terminate()
            self._snore_process = None

    def _wake_up(self):
        self.is_snoring = False
        self._stop_snore_audio()  # cut the audio instantly
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
            self._stop_snore_audio()
            self.title = ICON_OFF
            sender.title = "Disabled"
        else:
            self.title = ICON_IDLE
            self.last_activity = time.time()
            sender.title = "Enabled"

    def quit_app(self, _):
        self._stop_snore_audio()
        rumps.quit_application()

if __name__ == "__main__":
    MacSnoreApp().run()
