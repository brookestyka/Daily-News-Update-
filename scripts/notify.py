#!/usr/bin/env python3
"""
Sends the 10am push notification through ntfy.sh (free, no account needed).

Environment:
  NTFY_TOPIC  your private topic name (treat it like a password)
  APP_URL     the address of your briefing page; tapping the notification opens it
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

SHORT = {"us-politics": "US", "economy": "Economy", "tech": "Tech", "foreign-affairs": "World"}
DATA = Path(__file__).resolve().parent.parent / "data" / "briefing.json"


def main() -> int:
    topic = os.environ.get("NTFY_TOPIC", "").strip()
    app_url = os.environ.get("APP_URL", "").strip()
    if not topic:
        print("NTFY_TOPIC is not set; skipping the notification.")
        return 0

    data = json.loads(DATA.read_text(encoding="utf-8"))
    lines = [f"{SHORT.get(c['key'], c['label'])}: {c['stories'][0]['headline']}"
             for c in data.get("categories", []) if c.get("stories")]
    body = "\n".join(lines) or "Tap to read today's briefing."

    headers = {"Title": "Your daily briefing is ready", "Tags": "newspaper"}
    if app_url:
        headers["Click"] = app_url
    req = urllib.request.Request(f"https://ntfy.sh/{topic}", data=body.encode("utf-8"),
                                 method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(f"Notification sent (HTTP {resp.status}).")
    except Exception as exc:
        print(f"ERROR: could not send the notification: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
