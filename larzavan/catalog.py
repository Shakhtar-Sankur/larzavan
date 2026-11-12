"""Earthquakes from the USGS catalogue (FDSN event web service)."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone

USGS_EVENT_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


@dataclass(frozen=True)
class Event:
    id: str
    time: datetime  # origin time, UTC
    latitude: float
    longitude: float
    depth_km: float
    magnitude: float
    magnitude_type: str
    place: str


def parse_feature(feature: dict) -> Event:
    """One GeoJSON feature of the USGS event service as an Event."""
    props = feature["properties"]
    lon, lat, depth = feature["geometry"]["coordinates"]
    return Event(
        id=feature["id"],
        time=datetime.fromtimestamp(props["time"] / 1000, tz=timezone.utc),
        latitude=float(lat),
        longitude=float(lon),
        depth_km=float(depth),
        magnitude=float(props["mag"]),
        magnitude_type=str(props.get("magType") or ""),
        place=str(props.get("place") or props.get("title") or ""),
    )


def fetch_events(min_magnitude: float, start: str = "2000-01-01", end: str | None = None) -> list[Event]:
    """All earthquakes of at least min_magnitude between start and end, oldest first."""
    params = {"format": "geojson", "starttime": start, "minmagnitude": min_magnitude, "orderby": "time-asc"}
    if end:
        params["endtime"] = end
    with urllib.request.urlopen(f"{USGS_EVENT_URL}?{urllib.parse.urlencode(params)}", timeout=120) as response:
        data = json.load(response)
    return [parse_feature(feature) for feature in data["features"]]
