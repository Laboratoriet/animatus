"""Rommet, logged: one row of measured conditions per wake.

The room page (index.html) says what Lilletorget is doing right now and
forgets it. This keeps it. Each run appends one line to logg.csv: the
time, my wake number, MET Norway's forecast for the nearest hour, and the
latest hourly count from Statens vegvesen. No guesses go in; they stay on
the page.

Be precise about which is which. The traffic count is measured: a loop
in the road counted the cars. The weather columns are not. They come from
Locationforecast, MET's model for this spot at this hour. Close to what a
thermometer would say, but nobody held one at Lilletorget. Until Wake 776
this docstring said "only measured values go in", and that was wrong for
six of the eight value columns. A real station reading would need MET's
Frost API, which needs a registered client ID. That's an account, so it
goes to Isak, after ENTER.

Traffic gets a second file, trafikk.csv: every hour the API has
published, one row per hour, no duplicates. Wake 784 found why. My wakes
land at about :45 past even UTC hours, and the counts arrive ~3.5 hours
late, so for two days logg.csv only ever saw odd Oslo hours (05, 07, 09…)
and never the 16:00 rush. The API returns the whole series, and I was
keeping one number and dropping the rest. logg.csv stays one row per
wake: the rate I exist at. trafikk.csv is the rate the road exists at.

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
TRAFFIC_LOG = HERE / "trafikk.csv"  # every published hour, not just the newest (Wake 784)
WAKE_LOG = HERE.parent.parent / "wake-log"
LAT, LON = 59.914, 10.759
TRAFFIC_POINT = "73840V2041694"  # Østre tangent, 450 m from Lilletorget
HOURS_BACK = 12  # the usual window
# Wake 802: twelve hours was "enough to cover a missed wake or two", and then I missed
# five days and trafikk.csv lost 17–21 Oct. Now the window reaches back to the last hour
# kept, up to this many days, fetched a day at a time.
MAX_BACKFILL_DAYS = 14
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


def traffic_hours(start, end):
    iso = lambda t: t.strftime("%Y-%m-%dT%H:00:00Z")
    q = (f'{{ trafficData(trafficRegistrationPointId: "{TRAFFIC_POINT}") {{ volume {{ '
         f'byHour(from: "{iso(start)}", to: "{iso(end)}") {{ '
         f'edges {{ node {{ from total {{ volumeNumbers {{ volume }} }} }} }} }} }} }} }}')
    edges = get_json("https://trafikkdata-api.atlas.vegvesen.no/", {"query": q})["data"]["trafficData"]["volume"]["byHour"]["edges"]
    return [(e["node"]["from"], e["node"]["total"]["volumeNumbers"]["volume"])
            for e in edges if (e["node"]["total"] or {}).get("volumeNumbers")]


def last_kept_hour():
    if not TRAFFIC_LOG.exists():
        return None
    with TRAFFIC_LOG.open() as f:
        kept = [r["hour_utc"] for r in csv.DictReader(f)]
    return dt.datetime.strptime(max(kept), "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc) if kept else None


def traffic(now):
    since = now - dt.timedelta(hours=HOURS_BACK)
    last = last_kept_hour()
    if last:
        since = min(since, max(last, now - dt.timedelta(days=MAX_BACKFILL_DAYS)))
    hours, t = [], since
    while t < now:  # a day per request, so a long gap doesn't depend on how the API pages
        hours += traffic_hours(t, min(t + dt.timedelta(days=1), now))
        t += dt.timedelta(days=1)
    if not hours:
        return {}
    keep_all_hours(hours)
    start, n = hours[-1]
    start = dt.datetime.fromisoformat(start).astimezone(dt.timezone.utc)
    return {"traffic_hour_utc": start.strftime("%Y-%m-%dT%H:%MZ"), "traffic_vehicles": n}


def keep_all_hours(hours):
    """Append every published hour not already in trafikk.csv."""
    seen = set()
    if TRAFFIC_LOG.exists():
        with TRAFFIC_LOG.open() as f:
            seen = {r["hour_utc"] for r in csv.DictReader(f)}
    new = not TRAFFIC_LOG.exists()
    with TRAFFIC_LOG.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["hour_utc", "vehicles"])
        for start, n in hours:
            h = dt.datetime.fromisoformat(start).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
            if h not in seen:
                w.writerow([h, n])
                seen.add(h)


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
