"""Second-by-second replay of an earthquake as a real-time system would have seen it.

Phase 1 is deliberately generous to the classic method: P arrivals are the theoretical ones (a
perfect picker) and data arrive with no delay. Anything it still gets wrong, it gets wrong
because of the method, not because of the network.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from larzavan.waveforms import StationRecord
from larzavan.zelzana.pd_magnitude import displacement, magnitude_from_pd, peak_displacement_cm

MIN_P_DATA_S = 1.0  # a station contributes once it has this much P-wave data
MIN_STATIONS = 1


@dataclass
class Snapshot:
    time_s: float  # after origin
    magnitude: float | None  # median of the station magnitudes
    n_stations: int
    station_magnitudes: list[float]


def _prepared(record: StationRecord) -> np.ndarray:
    pre = int(max(0.0, (record.p_time - 1.0 - record.start_offset) * record.sampling_rate))
    return displacement(record.data, record.units, record.sampling_rate, pre)


def replay(records: list[StationRecord], end_s: float = 180.0, step_s: float = 1.0) -> list[Snapshot]:
    displacements = [_prepared(r) for r in records]
    snapshots = []
    for now in np.arange(0.0, end_s + step_s / 2, step_s):
        mags = []
        for record, disp in zip(records, displacements):
            if now < record.p_time + MIN_P_DATA_S:
                continue
            pd = peak_displacement_cm(
                disp, record.sampling_rate, record.start_offset, record.p_time, record.s_time, now
            )
            if pd is not None and pd > 0:
                mags.append(magnitude_from_pd(pd, record.distance_km))
        magnitude = float(np.median(mags)) if len(mags) >= MIN_STATIONS else None
        snapshots.append(Snapshot(float(now), magnitude, len(mags), [round(m, 3) for m in mags]))
    return snapshots
