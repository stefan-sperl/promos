#!/usr/bin/env python3
"""Checks promos.json: valid JSON, required fields, unique ids, dates,
https links and that every image URL points to a file in this repo."""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = "https://raw.githubusercontent.com/stefan-sperl/promos/main/"
errors = []


def err(msg):
    errors.append(msg)


data = json.loads((ROOT / "promos.json").read_text(encoding="utf-8"))
promos = data.get("promos")
if not isinstance(promos, list):
    sys.exit("promos.json: \"promos\" muss eine Liste sein")

ids = set()
for i, p in enumerate(promos):
    where = f"promos[{i}]"
    if not isinstance(p, dict):
        err(f"{where}: kein Objekt")
        continue
    for key in ("id", "app", "title", "text"):
        if not isinstance(p.get(key), str) or not p[key]:
            err(f"{where}: Pflichtfeld \"{key}\" fehlt oder ist leer")
    pid = p.get("id")
    if isinstance(pid, str):
        if pid in ids:
            err(f"{where}: id \"{pid}\" doppelt")
        ids.add(pid)
        if not re.fullmatch(r"[a-z0-9-]+", pid):
            err(f"{where}: id nur aus a-z, 0-9 und - bilden")
        where = f"promos[{i}] ({pid})"
    for key in ("ios", "android"):
        v = p.get(key)
        if v is not None and not (isinstance(v, str) and v.startswith("https://")):
            err(f"{where}: \"{key}\" muss mit https:// beginnen")
    if not p.get("ios") and not p.get("android"):
        err(f"{where}: weder \"ios\" noch \"android\" gesetzt, wird nie gezeigt")
    for key in ("from", "until"):
        v = p.get(key)
        if v is not None:
            try:
                date.fromisoformat(v)
            except (TypeError, ValueError):
                err(f"{where}: \"{key}\" muss JJJJ-MM-TT sein")
    if p.get("from") and p.get("until") and p["from"] > p["until"]:
        err(f"{where}: \"from\" liegt nach \"until\"")
    images = p.get("images", [])
    if not isinstance(images, list):
        err(f"{where}: \"images\" muss eine Liste sein")
        images = []
    for url in images:
        if not isinstance(url, str) or not url.startswith(RAW):
            err(f"{where}: Bild-URL muss mit {RAW} beginnen: {url}")
            continue
        if not (ROOT / url[len(RAW):]).is_file():
            err(f"{where}: Bilddatei fehlt im Repo: {url[len(RAW):]}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"promos.json ok: {len(promos)} Kampagne(n), "
      f"{sum(1 for p in promos if p.get('enabled', True))} aktiv")
