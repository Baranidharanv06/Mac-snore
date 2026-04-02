# mac-snore

> Your Mac snores when you do.

A tiny macOS menu bar app that detects when you've gone idle and starts snoring — then cuts off the moment you come back.

Inspired by [spank](https://github.com/taigrr/spank) — because your Mac deserves a personality.

---

## What it does

- Sits silently in your menu bar as `zzZ`
- After 30 seconds of inactivity → your Mac starts snoring 💤
- The second you touch your mouse or keyboard → snoring stops instantly
- Shows a notification welcoming you back
- Uses macOS native idle detection — zero false triggers while you're actually working

---

## Menu bar states

| Icon | Meaning |
|------|---------|
| `zzZ` | Watching, you're active |
| `ZZZ` | Snoring, you're idle |
| `---` | Disabled |

---

## Requirements

- macOS (Apple Silicon or Intel)
- Python 3.12+
- Homebrew

---

## Install

```bash
# 1. Clone
git clone https://github.com/Baranidharanv06/mac-snore.git
cd mac-snore

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install rumps pynput

# 4. Add your snore sound
# Drop any .mp3 into the sounds/ folder named snore.mp3
mkdir sounds
# cp ~/Downloads/snore.mp3 sounds/snore.mp3

# 5. Run
python3 snore.py
```

> ⚠️ macOS will ask for **Accessibility permissions** on first run.
> Go to **System Settings → Privacy & Security → Accessibility** → enable Terminal.

---

## Run permanently (auto-start on login)

**Step 1 — Create a launch script:**
```bash
cat > ~/mac-snore/run.sh << 'SCRIPT'
#!/bin/bash
cd ~/mac-snore
source venv/bin/activate
python3 snore.py
SCRIPT
chmod +x ~/mac-snore/run.sh
```

**Step 2 — Create a Launch Agent:**
```bash
cat > ~/Library/LaunchAgents/com.barani.macsnore.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.barani.macsnore</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/YOUR_USERNAME/mac-snore/run.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
PLIST
```
> Replace `YOUR_USERNAME` with your macOS username.

**Step 3 — Load it:**
```bash
launchctl load ~/Library/LaunchAgents/com.barani.macsnore.plist
```

Close the terminal. `zzZ` lives in your menu bar forever now.

---

## Controls

| Action | Command |
|--------|---------|
| Stop temporarily | `launchctl unload ~/Library/LaunchAgents/com.barani.macsnore.plist` |
| Start again | `launchctl load ~/Library/LaunchAgents/com.barani.macsnore.plist` |
| Remove permanently | `launchctl unload ~/Library/LaunchAgents/com.barani.macsnore.plist && rm ~/Library/LaunchAgents/com.barani.macsnore.plist` |

---

## Customize

Edit the top of `snore.py`:

```python
IDLE_THRESHOLD = 30   # seconds before snoring starts
```

Swap in any snore sound by replacing `sounds/snore.mp3`.

---

## How it works

- Uses `ioreg` to read macOS native HID idle time — the same system macOS uses for screen sleep
- Uses `rumps` for the menu bar UI
- Uses `pynput` to detect when you return from idle
- Uses `afplay` to play audio (built into macOS, no dependencies)
- 100% local, zero network access, no telemetry

---

## Built by

[@Baranidharanv06](https://github.com/Baranidharanv06) 

---

*peak engineering* ✨
