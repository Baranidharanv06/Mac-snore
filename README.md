# mac-snore 😴

> Your Mac falls asleep when you do.

A silly macOS menu bar app that **snores when you go idle** — and wakes up with a startled sound + notification when you come back.

Inspired by [spank](https://github.com/taigrr/spank) — because your Mac deserves feelings.

---

## Demo

| State | What happens |
|-------|-------------|
| You go idle for 30s | Mac starts snoring 💤 |
| You move the mouse | Mac wakes up startled 👀 + notification |
| Menu bar icon | Shows 😴 (watching) or 💤 (snoring) |

---

## Requirements

- macOS (Apple Silicon or Intel)
- Python 3.8+
- Terminal with **Accessibility permissions**

---

## Install & Run

```bash
# 1. Clone
git clone https://github.com/Baranidharanv06/mac-snore.git
cd mac-snore

# 2. Setup
chmod +x setup.sh
./setup.sh

# 3. Run
python3 snore.py
```

> ⚠️ On first run, macOS will ask for **Accessibility permissions** for Terminal.
> Go to **System Settings → Privacy & Security → Accessibility** and enable Terminal.

---

## Configuration

Edit the top of `snore.py` to customize:

```python
IDLE_THRESHOLD = 30   # seconds before snoring starts
SNORE_INTERVAL = 4    # seconds between each snore sound
```

---

## Custom Sounds

Drop your own `.aiff` files into the `sounds/` folder:

| Filename | When it plays |
|----------|--------------|
| `snore.aiff` | While idle/snoring |
| `wake.aiff` | When you come back |

No custom sounds? It falls back to built-in macOS sounds automatically.

---

## How it works

- Uses **pynput** to detect mouse/keyboard activity
- Uses **rumps** to live in the macOS menu bar
- Uses **afplay** (built into macOS) to play sounds
- Zero network access, 100% local

---

## Menu Bar

Click the 😴 icon in your menu bar to:
- See how long you've been idle
- Toggle it on/off
- Quit

---

## Made by

[@Baranidharanv06](https://github.com/Baranidharanv06) — built for fun, shipped with love 🚀

---

*peak engineering* ✨
