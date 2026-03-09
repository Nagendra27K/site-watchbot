# 🤖 Site WatchBot

> A lightweight Python bot that monitors websites and alerts you the moment they go down or come back up.

No dependencies. No setup. Just Python.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-zero-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- ✅ Monitor unlimited websites
- ⚡ Shows response time in milliseconds
- 🔔 Alerts you when a site **goes down** or **comes back up**
- 📝 Logs every status change to `watchbot.log`
- ➕ Add / remove sites from an easy menu
- 🌈 Clean, colorful terminal output
- 🚫 Zero external dependencies — pure Python stdlib

---

## 🚀 Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/site-watchbot.git
cd site-watchbot
python watchbot.py
```

That's it. No `pip install` needed.

---

## 📸 Demo

```
──────────────────────────────────────────────────
  🤖 Site WatchBot  (press Ctrl+C to stop)
──────────────────────────────────────────────────

  Watching 3 site(s) · checking every 60s

  [14:32:01] Checking...
  ✅  Google          UP     200    142ms
  ✅  GitHub          UP     200    310ms
  ✅  Wikipedia       UP     200    275ms

  [14:33:01] Checking...
  ✅  Google          UP     200    138ms
  ❌  GitHub          DOWN   ---    ---ms  ⚠️  STATUS CHANGED!
  ✅  Wikipedia       UP     200    290ms
```

---

## 🛠️ Usage

```
1  Start monitoring       — begins the watch loop
2  Add a site             — add a new URL to monitor
3  List sites             — see all monitored sites
4  Remove a site          — stop monitoring a site
5  Exit
```

### Add your own sites

Edit `sites.json` directly:

```json
[
  { "name": "My Blog",  "url": "https://myblog.com" },
  { "name": "My API",   "url": "https://api.myapp.com/health" }
]
```

---

## ⚙️ Configuration

At the top of `watchbot.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `CHECK_EVERY` | `60` | Seconds between checks |
| `TIMEOUT` | `10` | Seconds before marking as down |
| `LOG_FILE` | `watchbot.log` | Where to save alerts |

---

## 📋 Log Output

Every status change is saved to `watchbot.log`:

```
[2024-03-09 14:33:01] GitHub (https://github.com) WENT DOWN ❌ — HTTP 0 in 10001ms
[2024-03-09 14:34:01] GitHub (https://github.com) RECOVERED ✅ — HTTP 200 in 312ms
```

---

## ⭐ Star This Repo

If this saved you from finding out your site was down via angry users — leave a star! ⭐

## 📄 License

MIT — free to use, modify, and share.
