"""Open seismic recordings near an earthquake, from the public FDSN data centres.

Recordings are downloaded with ObsPy's mass downloader, which queries every open data
centre it knows (IRIS/EarthScope, GEOFON, ORFEUS, RESIF, INGV and others) and keeps the
instrument metadata. Strong-motion accelerometers come first in the channel priorities:
close to a great earthquake, broadband seismometers can clip, accelerometers do not.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from obspy import Inventory, UTCDateTime, read, read_inventory
from obspy.geodetics import gps2dist_azimuth, kilometers2degrees

from larzavan.arrivals import p_and_s
from larzavan.catalog import Event
from larzavan.picker import pick_p

KM_PER_DEG = 111.19
# Vertical components only: accelerometers first, then broadband and short-period velocity sensors.
CHANNEL_PRIORITIES = ["HN[Z]", "EN[Z]", "HL[Z]", "HH[Z]", "BH[Z]", "EH[Z]", "SH[Z]"]
LOCATION_PRIORITIES = ["", "00", "10", "20", "01", "02", "30", "40"]


@dataclass
class StationRecord:
    """One vertical recording, with its ground motion in SI units and its theoretical arrivals."""

    seed_id: str
    latitude: float
    longitude: float
    distance_km: float  # epicentral
    p_time: float  # seconds after origin: the picked P, or the theoretical one when no pick is found
    s_time: float | None
    p_theoretical: float
    p_picked: bool
    sampling_rate: float
    start_offset: float  # seconds of the first sample after origin (negative: before origin)
    data: np.ndarray  # counts / sensitivity, in m/s or m/s**2
    units: str  # "M/S" or "M/S**2"


def download(
    event: Event,
    out_dir: Path,
    max_km: float = 250.0,
    before_s: float = 60.0,
    after_s: float = 300.0,
    providers: list[str] | None = None,
) -> tuple[Path, Path]:
    """Download vertical recordings within max_km of the epicentre; returns (waveform dir, station dir)."""
    from obspy.clients.fdsn.mass_downloader import CircularDomain, MassDownloader, Restrictions

    origin = UTCDateTime(event.time)
    wave_dir, sta_dir = out_dir / event.id / "waveforms", out_dir / event.id / "stations"
    domain = CircularDomain(
        latitude=event.latitude, longitude=event.longitude, minradius=0.0, maxradius=kilometers2degrees(max_km)
    )
    restrictions = Restrictions(
        starttime=origin - before_s,
        endtime=origin + after_s,
        reject_channels_with_gaps=True,
        minimum_length=0.9,
        minimum_interstation_distance_in_m=0.0,
        channel_priorities=CHANNEL_PRIORITIES,
        location_priorities=LOCATION_PRIORITIES,
        sanitize=True,
    )
    MassDownloader(providers=providers).download(
        domain, restrictions, mseed_storage=str(wave_dir), stationxml_storage=str(sta_dir), print_report=False
    )
    return wave_dir, sta_dir


def _inventory(sta_dir: Path) -> Inventory:
    inventory = Inventory(networks=[], source="larzavan")
    for path in sorted(sta_dir.glob("*.xml")):
        inventory += read_inventory(str(path))
    return inventory


def load_records(event: Event, wave_dir: Path, sta_dir: Path, max_km: float = 250.0) -> list[StationRecord]:
    """Recordings as ground motion with flat-band gain correction, one per station, with P and S times.

    The gain correction (dividing by the overall sensitivity) is what real-time systems do; full
    response removal works in the frequency domain on the whole trace, so it would use samples
    that a real-time system has not received yet.
    """
    origin = UTCDateTime(event.time)
    inventory = _inventory(sta_dir)
    records: dict[str, StationRecord] = {}
    for path in sorted(wave_dir.glob("*.mseed")):
        for trace in read(str(path)):
            try:
                coords = inventory.get_coordinates(trace.id, trace.stats.starttime)
                sensitivity = inventory.get_response(trace.id, trace.stats.starttime).instrument_sensitivity
            except Exception:
                continue  # no usable metadata for this channel
            units = (sensitivity.input_units or "").upper()
            if units not in ("M/S", "M/S**2") or not sensitivity.value:
                continue
            distance_m, _, _ = gps2dist_azimuth(
                event.latitude, event.longitude, coords["latitude"], coords["longitude"]
            )
            distance_km = distance_m / 1000.0
            if distance_km > max_km:
                continue
            p_time, s_time = p_and_s(event.depth_km, distance_km / KM_PER_DEG)
            if p_time is None:
                continue
            station = ".".join(trace.id.split(".")[:2])
            if station in records:
                continue  # keep the first channel by priority order of the files (one per station)
            data = trace.data.astype(np.float64) / sensitivity.value
            fs, start_offset = float(trace.stats.sampling_rate), float(trace.stats.starttime - origin)
            picked = pick_p(data, fs, start_offset, p_time)
            records[station] = StationRecord(
                seed_id=trace.id,
                latitude=coords["latitude"],
                longitude=coords["longitude"],
                distance_km=distance_km,
                p_time=picked if picked is not None else p_time,
                s_time=s_time,
                p_theoretical=p_time,
                p_picked=picked is not None,
                sampling_rate=fs,
                start_offset=start_offset,
                data=data,
                units=units,
            )
    return list(records.values())
