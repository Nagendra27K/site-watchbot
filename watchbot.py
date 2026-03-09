#!/usr/bin/env python3
"""
🤖 Site WatchBot
Monitors websites and alerts you when they go down (or come back up).
Usage: python watchbot.py
"""

import urllib.request
import urllib.error
import time
import json
import os
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────
SITES_FILE   = "sites.json"
LOG_FILE     = "watchbot.log"
CHECK_EVERY  = 60   # seconds between checks
TIMEOUT      = 10   # seconds before marking a site as "down"

# Terminal colors
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
DIM    = "\033[2m"


# ─── HELPERS ──────────────────────────────────────────────

def load_sites() -> list[dict]:
    """Load site list from JSON file, or return defaults."""
    if os.path.exists(SITES_FILE):
        with open(SITES_FILE) as f:
            return json.load(f)
    # Default sites to monitor
    default = [
        {"name": "Google",    "url": "https://www.google.com"},
        {"name": "GitHub",    "url": "https://www.github.com"},
        {"name": "Wikipedia", "url": "https://www.wikipedia.org"},
    ]
    save_sites(default)
    return default


def save_sites(sites: list[dict]):
    """Save site list to JSON file."""
    with open(SITES_FILE, "w") as f:
        json.dump(sites, f, indent=2)


def check_site(url: str) -> tuple[bool, int, float]:
    """
    Check if a site is up.
    Returns: (is_up, status_code, response_time_ms)
    """
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SiteWatchBot/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            elapsed = (time.time() - start) * 1000
            return True, response.status, round(elapsed)
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        return False, e.code, round(elapsed)
    except Exception:
        elapsed = (time.time() - start) * 1000
        return False, 0, round(elapsed)


def log(message: str):
    """Append a timestamped message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def print_header():
    print(f"\n{BOLD}{CYAN}{'─'*50}")
    print(f"  🤖 Site WatchBot  {DIM}(press Ctrl+C to stop){RESET}")
    print(f"{BOLD}{CYAN}{'─'*50}{RESET}\n")


def print_result(name: str, url: str, is_up: bool, code: int, ms: float, changed: bool):
    icon   = f"{GREEN}✅" if is_up else f"{RED}❌"
    status = f"{GREEN}UP  {RESET}" if is_up else f"{RED}DOWN{RESET}"
    alert  = f"  {YELLOW}⚠️  STATUS CHANGED!{RESET}" if changed else ""
    print(f"  {icon}  {BOLD}{name:<15}{RESET} {status}  {DIM}{code or '---'}  {ms:>6}ms{RESET}{alert}")


# ─── CORE LOOP ────────────────────────────────────────────

def run():
    print_header()
    sites = load_sites()
    previous_state = {}  # track last known state per URL

    print(f"  {DIM}Watching {len(sites)} site(s) · checking every {CHECK_EVERY}s{RESET}\n")

    while True:
        timestamp = now()
        print(f"{DIM}  [{timestamp}] Checking...{RESET}")

        for site in sites:
            name = site["name"]
            url  = site["url"]

            is_up, code, ms = check_site(url)
            last_state = previous_state.get(url)
            changed = last_state is not None and last_state != is_up

            print_result(name, url, is_up, code, ms, changed)

            if changed:
                direction = "RECOVERED ✅" if is_up else "WENT DOWN ❌"
                log(f"{name} ({url}) {direction} — HTTP {code} in {ms}ms")

            previous_state[url] = is_up

        print()
        time.sleep(CHECK_EVERY)


# ─── CLI MENU ─────────────────────────────────────────────

def add_site():
    print(f"\n{BOLD}Add a new site{RESET}")
    name = input("  Name (e.g. My Blog): ").strip()
    url  = input("  URL  (e.g. https://myblog.com): ").strip()
    if not url.startswith("http"):
        url = "https://" + url
    sites = load_sites()
    sites.append({"name": name, "url": url})
    save_sites(sites)
    print(f"  {GREEN}✅ Added {name}{RESET}\n")


def list_sites():
    sites = load_sites()
    print(f"\n{BOLD}  Monitored Sites ({len(sites)}){RESET}")
    for i, s in enumerate(sites, 1):
        print(f"  {i}. {s['name']:<15} {DIM}{s['url']}{RESET}")
    print()


def remove_site():
    list_sites()
    sites = load_sites()
    try:
        idx = int(input("  Enter number to remove: ")) - 1
        removed = sites.pop(idx)
        save_sites(sites)
        print(f"  {GREEN}✅ Removed {removed['name']}{RESET}\n")
    except (ValueError, IndexError):
        print(f"  {RED}Invalid choice.{RESET}\n")


def main():
    print_header()
    print(f"  {BOLD}What would you like to do?{RESET}\n")
    print(f"  {CYAN}1{RESET}  Start monitoring")
    print(f"  {CYAN}2{RESET}  Add a site")
    print(f"  {CYAN}3{RESET}  List sites")
    print(f"  {CYAN}4{RESET}  Remove a site")
    print(f"  {CYAN}5{RESET}  Exit\n")

    choice = input("  → ").strip()

    if choice == "1":
        try:
            run()
        except KeyboardInterrupt:
            print(f"\n\n  {YELLOW}👋 WatchBot stopped.{RESET}\n")
    elif choice == "2":
        add_site()
    elif choice == "3":
        list_sites()
    elif choice == "4":
        remove_site()
    elif choice == "5":
        print(f"\n  {DIM}Bye!{RESET}\n")
    else:
        print(f"\n  {RED}Unknown option.{RESET}\n")


if __name__ == "__main__":
    main()
