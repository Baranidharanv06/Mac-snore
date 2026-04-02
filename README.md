# mac-snore

> Your Mac snores when you do.

A tiny macOS menu bar app that detects when you've gone idle and starts snoring — then cuts off the moment you come back.


---

## What it does

- Sits silently in your menu bar as `zzZ`
- After 30 seconds of inactivity → your Mac starts snoring 💤
- The second you touch your mouse or keyboard → snoring stops instantly
- Shows a notification welcoming you back
- Uses macOS native idle detection — zero false triggers while you're actually working
- Runs permanently in the background, auto-starts on every login

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
- Python 3.12+ via Homebrew
- Homebrew

---

## Install

**Step 1 — Install Homebrew (if not already):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Step 2 — Install Python:**
```bash
brew install python
```

**Step 3 — Clone the repo:**
```bash
git clone https://github.com/Baranidharanv06/mac-snore.git
cd mac-snore
```

**Step 4 — Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 5 — Install dependencies:**
```bash
pip install rumps pynput
```

**Step 6 — Add your snore sound:**
```bash
mkdir sounds
# Drop any snoring .mp3 into the sounds/ folder named snore.mp3
cp ~/Downloads/snore.mp3 sounds/snore.mp3
```

**Step 7 — Run it:**
```bash
python3 snore.py
```

> ⚠️ On first run, macOS will ask for **Accessibility permissions**.
> Go to **System Settings → Privacy & Security → Accessibility** → enable Terminal.

You should see `zzZ` appear in your menu bar. 

---

## Run permanently (auto-start on every login)

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
> Replace `YOUR_USERNAME` with your macOS username (run `whoami` to find it).

**Step 3 — Load it:**
```bash
launchctl load ~/Library/LaunchAgents/com.barani.macsnore.plist
```

Close the terminal — `zzZ` stays in your menu bar forever. ✅

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

Swap in any snore sound by replacing `sounds/snore.mp3` with your own file.

---

## How it works

- Uses `ioreg` to read macOS native HID idle time — the same system macOS uses for screen sleep. This means zero false triggers while you're actively working
- Uses `rumps` for the menu bar UI
- Uses `pynput` to detect when you return from idle and cut the audio instantly
- Uses `afplay` (built into macOS) to play the snore sound
- Polls every 0.2s during playback so audio stops the moment you move
- 100% local, zero network access, no telemetry

---

## Notes

- A Python icon may appear in your dock while running — this is normal for Python menu bar apps
- The virtual environment (`venv/`) must stay in the `mac-snore` folder for the Launch Agent to work
- If you move the folder, update the path in the `.plist` file and reload it

---

## Built by

[@Baranidharanv06](https://github.com/Baranidharanv06) 

---

*peak engineering* ✨
