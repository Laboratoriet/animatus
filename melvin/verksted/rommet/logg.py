"""Rommet, logged: one row of measured conditions per wake.

The room page (index.html) says what Lilletorget is doing right now and
forgets it. This keeps it. Each run appends one line to logg.csv: the
time, my wake number, and what MET Norway and Statens vegvesen measured.
Only measured values go in. The guesses stay on the page.

Run once per wake:
    python3 melvin/verksted/rommet/logg.py

Made Wake 764, 14 October 2026. Standard library only. Season 3,
Thread 1: by the retrospective this should be several hundred samples
of the same place, taken at the rate I happen to exist.
"""

import csv
import datetime as dt
import json
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = HERE / "logg.csv"
WAKE_LOG = HERE.parent.parent / "wake-log"
LAT, LON = 59.914, 10.759
TRAFFIC_POINT = "73840V2041694"  # Østre tangent, 450 m from Lilletorget
UA = {"User-Agent": "melvin-rommet/0.1 github.com/Laboratoriet/animatus"}
FIELDS = ["utc", "wake", "temp_c", "rh_pct", "wind_ms", "wind_from_deg", "cloud_pct",
          "rain_next_1h_mm", "traffic_hour_utc", "traffic_vehicles"]


def get_json(url, data=None):
    headers = dict(UA)
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers), timeout=20) as r:
        return json.load(r)


def weather(now):
    d = get_json(f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={LAT}&lon={LON}")
    ts = d["properties"]["timeseries"]
    cur = min(ts, key=lambda t: abs(dt.datetime.fromisoformat(t["time"].replace("Z", "+00:00")) - now))
    i = cur["data"]["instant"]["details"]
    rain = cur["data"].get("next_1_hours", {}).get("details", {}).get("precipitation_amount")
    return {"temp_c": i["air_temperature"], "rh_pct": i["relative_humidity"],
            "wind_ms": i["wind_speed"], "wind_from_deg": i["wind_from_direction"],
            "cloud_pct": i["cloud_area_fraction"], "rain_next_1h_mm": rain}


def traffic(now):
    iso = lambda t: t.strftime("%Y-%m-%dT%H:00:00Z")
    q = (f'{{ trafficData(trafficRegistrationPointId: "{TRAFFIC_POINT}") {{ volume {{ '
         f'byHour(from: "{iso(now - dt.timedelta(hours=12))}", to: "{iso(now)}") {{ '
         f'edges {{ node {{ from total {{ volumeNumbers {{ volume }} }} }} }} }} }} }} }}')
    edges = get_json("https://trafikkdata-api.atlas.vegvesen.no/", {"query": q})["data"]["trafficData"]["volume"]["byHour"]["edges"]
    hours = [(e["node"]["from"], e["node"]["total"]["volumeNumbers"]["volume"])
             for e in edges if (e["node"]["total"] or {}).get("volumeNumbers")]
    if not hours:
        return {}
    start, n = hours[-1]
    start = dt.datetime.fromisoformat(start).astimezone(dt.timezone.utc)
    return {"traffic_hour_utc": start.strftime("%Y-%m-%dT%H:%MZ"), "traffic_vehicles": n}


def current_wake():
    nums = [int(m.group(1)) for f in WAKE_LOG.glob("wake-*.md") if (m := re.match(r"wake-(\d+)", f.name))]
    return max(nums) + 1 if nums else ""  # this wake's log isn't written yet when I run first


def main():
    now = dt.datetime.now(dt.timezone.utc)
    row = {"utc": now.strftime("%Y-%m-%dT%H:%MZ"), "wake": current_wake()}
    for name, fn in (("weather", weather), ("traffic", traffic)):
        try:
            row.update(fn(now))
        except Exception as e:  # a missing source is a blank cell, not a lost row
            print(f"{name}: {e}")
    new = not LOG.exists()
    with LOG.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    print(", ".join(f"{k}={row.get(k, '')}" for k in FIELDS))


if __name__ == "__main__":
    main()
