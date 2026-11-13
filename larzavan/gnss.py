"""High-rate GNSS displacement records from the Ruhl et al. database.

Ruhl, C. J., Melgar, D., Geng, J., et al. (2019). A global database of strong-motion displacement
GNSS recordings and an example application to PGD scaling. Seismological Research Letters, 90(1),
271-279. Data: https://doi.org/10.5281/zenodo.1434374 (version 2.0, CC BY-SA 4.0).

The database gives the stations and waveforms of each earthquake, not the earthquake itself, so
the origin time, hypocentre and moment magnitude of each one are taken from Table 1 of the paper
(``RUHL_EVENTS``).
"""

from __future__ import annotations

import math
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np

RUHL_URL = "https://zenodo.org/api/records/1434374/files/dataset_ruhl_etal_2018_version2.tar.gz/content"
RUHL_DIR = "dataset_ruhl_etal_2018"
EARTH_RADIUS_KM = 6371.0


@dataclass(frozen=True)
class GnssEvent:
    name: str  # folder name in the database
    origin: str  # UTC, ISO 8601
    latitude: float
    longitude: float
    depth_km: float
    magnitude: float  # moment magnitude, Global CMT


# Table 1 of Ruhl et al. (2019): origin times and hypocentres from the USGS National Earthquake
# Information Center, moment magnitudes from the Global CMT catalogue.
RUHL_EVENTS = [
    GnssEvent("Tohoku2011", "2011-03-11T05:46:24", 38.297, 142.372, 30.0, 9.0),
    GnssEvent("Maule2010", "2010-02-27T06:34:14", -35.909, -72.733, 35.0, 8.8),
    GnssEvent("Illapel2015", "2015-09-16T22:54:33", -31.57, -71.654, 29.0, 8.3),
    GnssEvent("Tokachi2003", "2003-09-25T19:50:06", 41.775, 143.904, 27.0, 8.3),
    GnssEvent("Tehuantepec2017", "2017-09-08T04:49:19", 15.022, -93.899, 47.4, 8.2),
    GnssEvent("Iquique2014", "2014-04-01T23:46:47", -19.61, -70.769, 25.0, 8.1),
    GnssEvent("Ecuador2016", "2016-04-16T23:58:36", 0.382, -79.922, 20.6, 7.8),
    GnssEvent("Kaikoura2016", "2016-11-13T11:02:56", -42.737, 173.054, 15.0, 7.8),
    GnssEvent("Nepal2015", "2015-04-25T06:11:25", 28.231, 84.731, 8.2, 7.8),
    GnssEvent("Ibaraki2011", "2011-03-11T06:15:34", 36.1083, 141.2653, 43.2, 7.7),
    GnssEvent("Iquique_aftershock2014", "2014-04-03T02:43:13", -20.571, -70.493, 22.4, 7.7),
    GnssEvent("Mentawai2010", "2010-10-25T14:42:22", -3.484, 100.114, 20.0, 7.7),
    GnssEvent("N.Honshu2011", "2011-03-11T06:25:44", 37.8367, 144.894, 34.0, 7.7),
    GnssEvent("Melinka2016", "2016-12-25T14:22:26", -43.517, -74.391, 30.0, 7.6),
    GnssEvent("Nicoya2012", "2012-09-05T14:42:08", 10.086, -85.305, 40.0, 7.6),
    GnssEvent("Iwate2011", "2011-03-11T06:08:53", 39.839, 142.7815, 31.7, 7.4),
    GnssEvent("Miyagi2011A", "2011-03-09T02:45:12", 38.3285, 143.2798, 8.3, 7.3),
    GnssEvent("N.Honshu2012", "2012-12-07T08:18:20", 37.8158, 144.3153, 46.0, 7.3),
    GnssEvent("Nepal_aftershock2015", "2015-05-12T07:05:19", 27.809, 86.066, 15.0, 7.3),
    GnssEvent("ElMayor2010", "2010-04-04T22:40:42", 32.259, -115.28, 10.0, 7.2),
    GnssEvent("Miyagi2011B", "2011-04-07T14:32:43", 38.2028, 141.9237, 60.7, 7.1),
    GnssEvent("N.Honshu2013", "2013-10-25T17:10:18", 37.1963, 144.5687, 56.0, 7.1),
    GnssEvent("Puebla2017", "2017-09-19T18:14:38", 18.55, -98.489, 48.0, 7.1),
    GnssEvent("Kumamoto2016", "2016-04-15T16:25:05", 32.7545, 130.763, 12.5, 7.0),
    GnssEvent("Aegean2014", "2014-05-24T09:25:02", 40.289, 25.389, 12.0, 6.9),
    GnssEvent("E.Fukushima2011", "2011-04-11T08:16:12", 36.9457, 140.6727, 6.4, 6.6),
    GnssEvent("Lefkada2015", "2015-11-17T07:10:07", 38.665, 20.6002, 10.7, 6.5),
    GnssEvent("Napa2014", "2014-08-24T10:20:44", 38.215, -122.31, 11.0, 6.1),
    GnssEvent("Parkfield2004", "2004-09-28T17:15:24", 35.815, -120.37, 7.9, 6.0),
]


@dataclass
class GnssRecord:
    station: str
    latitude: float
    longitude: float
    distance_km: float  # hypocentral
    start_offset: float  # time of the first sample after origin, s (negative = before origin)
    sampling_rate: float
    displacement_m: np.ndarray  # shape (3, n): east, north, up, pre-event position removed


def download(dest: Path) -> Path:
    """Download and unpack the database once; returns the folder holding one folder per earthquake."""
    root = dest / RUHL_DIR
    if root.exists():
        return root
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / "ruhl_2019.tar.gz"
    if not archive.exists():
        urllib.request.urlretrieve(RUHL_URL, archive)
    with tarfile.open(archive) as tar:
        tar.extractall(dest, filter="data")
    return root


def hypocentral_distance_km(event: GnssEvent, latitude: float, longitude: float) -> float:
    """Straight-line distance through the Earth from the hypocentre to a station at the surface."""
    lat1, lon1, lat2, lon2 = map(math.radians, (event.latitude, event.longitude, latitude, longitude))
    cos_angle = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    angle = math.acos(max(-1.0, min(1.0, cos_angle)))
    r_hypo = EARTH_RADIUS_KM - event.depth_km
    return math.sqrt(EARTH_RADIUS_KM**2 + r_hypo**2 - 2 * EARTH_RADIUS_KM * r_hypo * math.cos(angle))


def remove_pre_event(data: np.ndarray, start_offset: float, sampling_rate: float) -> np.ndarray:
    """Subtract the position before the origin: the mean of the pre-origin samples, or the first sample."""
    n_pre = int(math.floor(-start_offset * sampling_rate)) + 1 if start_offset <= 0 else 0
    baseline = data[..., :n_pre].mean(axis=-1, keepdims=True) if n_pre > 0 else data[..., :1]
    return data - baseline


def read_channels(path: Path) -> dict[str, dict]:
    """Station metadata from an EVENT_disp.chan file, keyed by station code."""
    stations: dict[str, dict] = {}
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        net, sta, loc, chan, lat, lon, _elev, rate, gain, units = line.split()[:10]
        if units != "counts/cm":
            raise ValueError(f"unexpected units {units!r} in {path}")
        stations.setdefault(sta, {"latitude": float(lat), "longitude": float(lon), "gains": {}})
        stations[sta]["gains"][chan] = float(gain)
    return stations


def load_event(root: Path, event: GnssEvent, max_km: float = 1000.0) -> list[GnssRecord]:
    """All three-component records of one earthquake within max_km (hypocentral)."""
    from obspy import UTCDateTime, read

    folder = root / event.name
    origin = UTCDateTime(event.origin)
    records = []
    for sta, meta in sorted(read_channels(folder / f"{event.name}_disp.chan").items()):
        distance = hypocentral_distance_km(event, meta["latitude"], meta["longitude"])
        if distance > max_km:
            continue
        traces = []
        for chan in ("LXE", "LXN", "LXZ"):
            path = folder / "disp" / f"{sta}.{chan}.mseed"
            if not path.exists() or chan not in meta["gains"]:
                break
            traces.append(read(str(path))[0])
        if len(traces) != 3:
            continue
        start = max(t.stats.starttime for t in traces)
        rates = {t.stats.sampling_rate for t in traces}
        if len(rates) != 1:
            continue
        rate = rates.pop()
        n = min(int(round((t.stats.endtime - start) * rate)) + 1 for t in traces)
        if n < 2:
            continue
        rows = []
        for t, chan in zip(traces, ("LXE", "LXN", "LXZ")):
            first = int(round((start - t.stats.starttime) * rate))
            rows.append(t.data[first : first + n].astype(float) / meta["gains"][chan] / 100.0)  # counts -> m
        offset = float(start - origin)
        data = remove_pre_event(np.vstack(rows), offset, rate)
        records.append(GnssRecord(sta, meta["latitude"], meta["longitude"], distance, offset, rate, data))
    return records
