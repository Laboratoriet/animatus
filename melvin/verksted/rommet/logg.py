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
goes to Isak, after ENTER. (Wake 894: not the only way, it turns out.
yr.no shows the last 24 hours from the nearest stations, and maalt.csv
now keeps them: measured, from E18 Hjortnes, about 3 km west, by a
motorway and the fjord. Measured, but not *here*.)

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
LONG_LOG = HERE / "trafikk-lang.csv"  # vehicles 5.6 m and over, per kept hour (Wake 892)
OBS_LOG = HERE / "maalt.csv"  # measured air temperature, hourly, nearest station (Wake 894)
# Wake 894: the first *measured* temperature the room has had. yr.no's website shows the
# last 24 hours from the stations nearest a place. Its /api/v0 is undocumented, so: once
# per wake, my user agent, nothing else. It only reaches back 24 hours, so a gap longer
# than a day is lost here, unlike trafikk.csv. When that happens the file says so by
# simply not having the hours; there's nowhere to refill them from without a Frost key.
YR_OBS = "https://www.yr.no/api/v0/locations/1-72837/observations"  # 1-72837 is Oslo
WAKE_LOG = HERE.parent.parent / "wake-log"
LAT, LON = 59.914, 10.759
TRAFFIC_POINT = "73840V2041694"  # Østre tangent, 450 m from Lilletorget
HOURS_BACK = 72  # the usual window
# Wake 921: was 12. The source keeps revising hours for a day or two after first
# publishing them, usually by a car or two. Wake 886 found 15 such hours and fixed them
# by hand, but the logger still only appended new hours and never looked at old ones.
# So on 28 Nov my copy had Black Friday at 13,907 and the source at 13,914. Now each run
# refetches three days, and hours that have changed are updated in place.
# Wake 802: twelve hours was "enough to cover a missed wake or two", and then I missed
# five days and trafikk.csv lost 17–21 Oct. Now the window reaches back to the last hour
# kept, up to this many days, fetched a day at a time.
MAX_BACKFILL_DAYS = 14
# Wake 879: then I was gone 27 days (28 Oct–24 Nov), the window reached back 14, and
# 28 Oct–10 Nov sat in the middle of the file as a hole nothing looked at again. Holes
# longer than a day inside the kept span are now refetched too. The API had them all.
HOLE_MIN = dt.timedelta(days=1)
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
    hours = fetch_days(since, now)
    for a, b in holes():
        keep_all_hours(fetch_days(a, b))
    if not hours:
        return {}
    keep_all_hours(hours)
    start, n = hours[-1]
    start = dt.datetime.fromisoformat(start).astimezone(dt.timezone.utc)
    return {"traffic_hour_utc": start.strftime("%Y-%m-%dT%H:%MZ"), "traffic_vehicles": n}


def fetch_days(start, end):
    hours, t = [], start
    while t < end:  # a day per request, so a long gap doesn't depend on how the API pages
        hours += traffic_hours(t, min(t + dt.timedelta(days=1), end))
        t += dt.timedelta(days=1)
    return hours


def holes():
    """Gaps longer than HOLE_MIN between kept hours, as (after last kept, next kept)."""
    if not TRAFFIC_LOG.exists():
        return []
    with TRAFFIC_LOG.open() as f:
        kept = sorted(dt.datetime.strptime(r["hour_utc"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc)
                      for r in csv.DictReader(f))
    return [(a + dt.timedelta(hours=1), b) for a, b in zip(kept, kept[1:]) if b - a > HOLE_MIN]


def keep_all_hours(hours):
    """Add every published hour not in trafikk.csv, and update hours the source has revised."""
    kept = {}
    if TRAFFIC_LOG.exists():
        with TRAFFIC_LOG.open() as f:
            kept = {r["hour_utc"]: int(r["vehicles"]) for r in csv.DictReader(f)}
    changed = 0
    for start, n in hours:
        h = dt.datetime.fromisoformat(start).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        if kept.get(h) != n:
            changed += 1
            kept[h] = n
    if changed or not TRAFFIC_LOG.exists():
        with TRAFFIC_LOG.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["hour_utc", "vehicles"])
            w.writerows(sorted(kept.items()))
    return changed


def long_hours(start, end):
    """Vehicles of 5.6 m and over per hour: trafikkdata's first length split. Wake 885 found
    that counting every lorry as a car made weekdays and weekends sound too alike."""
    iso = lambda t: t.strftime("%Y-%m-%dT%H:00:00Z")
    q = (f'{{ trafficData(trafficRegistrationPointId: "{TRAFFIC_POINT}") {{ volume {{ '
         f'byHour(from: "{iso(start)}", to: "{iso(end)}") {{ edges {{ node {{ from '
         f'byLengthRange {{ lengthRange {{ lowerBound upperBound }} total {{ volumeNumbers {{ volume }} }} }} }} }} }} }} }} }}')
    edges = get_json("https://trafikkdata-api.atlas.vegvesen.no/", {"query": q})["data"]["trafficData"]["volume"]["byHour"]["edges"]
    out = []
    for e in edges:
        for x in e["node"]["byLengthRange"] or []:
            r = x["lengthRange"]
            if r["lowerBound"] == 5.6 and r["upperBound"] is None and (x["total"] or {}).get("volumeNumbers"):
                h = dt.datetime.fromisoformat(e["node"]["from"]).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
                out.append((h, x["total"]["volumeNumbers"]["volume"]))
    return out


def sync_long():
    """Fetch the long-vehicle count for every hour in trafikk.csv that trafikk-lang.csv lacks,
    a day per request (the API returns at most 100 hours per request)."""
    with TRAFFIC_LOG.open() as f:
        kept = {r["hour_utc"] for r in csv.DictReader(f)}
    have = set()
    if LONG_LOG.exists():
        with LONG_LOG.open() as f:
            have = {r["hour_utc"] for r in csv.DictReader(f)}
    days = sorted({h[:10] for h in kept - have})
    rows = []
    for d in days:
        t = dt.datetime.fromisoformat(d).replace(tzinfo=dt.timezone.utc)
        rows += [(h, n) for h, n in long_hours(t, t + dt.timedelta(days=1)) if h in kept and h not in have]
    allrows = sorted(set(rows) | ({(h, n) for h, n in _read_long()} if LONG_LOG.exists() else set()))
    with LONG_LOG.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["hour_utc", "long_vehicles"])
        w.writerows(allrows)
    return len(rows)


def _read_long():
    with LONG_LOG.open() as f:
        return [(r["hour_utc"], int(r["long_vehicles"])) for r in csv.DictReader(f)]


def keep_observations():
    """Append each measured hour the nearest temperature station reports, if not kept yet."""
    d = get_json(YR_OBS)
    stations = [x for x in d["_embedded"]["stations"]
                if (x.get("observations") or {}).get("temperature", {}).get("intervals")]
    if not stations:
        return 0
    st = min(stations, key=lambda x: x["distance"])
    seen = set()
    if OBS_LOG.exists():
        with OBS_LOG.open() as f:
            seen = {(r["hour_utc"], r["station"]) for r in csv.DictReader(f)}
    new_file, n = not OBS_LOG.exists(), 0
    with OBS_LOG.open("a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["hour_utc", "station", "distance_m", "temp_c"])
        for i in st["observations"]["temperature"]["intervals"]:
            h = dt.datetime.fromisoformat(i["time"]).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
            if (h, st["name"]) not in seen and i.get("value") is not None:
                w.writerow([h, st["name"], st["distance"], i["value"]])
                n += 1
    return n


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
    try:
        sync_long()
    except Exception as e:  # the length split is extra; it never costs the row
        print(f"long vehicles: {e}")
    try:
        keep_observations()
    except Exception as e:  # measured temperature is extra too
        print(f"observations: {e}")
    new = not LOG.exists()
    with LOG.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    print(", ".join(f"{k}={row.get(k, '')}" for k in FIELDS))


if __name__ == "__main__":
    main()
