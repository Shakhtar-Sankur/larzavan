"""Second-by-second replay of the GNSS magnitude, as a real-time system would have seen it.

As in Phase 1, the replay is generous on delivery (data arrive with no delay) but strict on
information: at each second a station only contributes the displacement it has recorded so far,
and only once a wave travelling at S_SPEED_KM_S from the hypocentre could have reached it, so
pre-event noise is not mistaken for shaking.
"""

from __future__ import annotations

import numpy as np

from larzavan.gnss import GnssRecord
from larzavan.replay import Snapshot
from larzavan.zelzana.pgd_magnitude import RUHL_2019, network_magnitude, running_pgd

S_SPEED_KM_S = 3.0
MIN_PGD_M = 0.04  # the noise cutoff of Ruhl et al. (2019): smaller peaks are not counted
MIN_STATIONS = 1


def final_pgd(record: GnssRecord) -> float:
    """Peak displacement over the whole record after the S-wave arrival."""
    pgd = running_pgd(record.displacement_m)
    times = record.start_offset + np.arange(pgd.size) / record.sampling_rate
    after = times >= record.distance_km / S_SPEED_KM_S
    return float(pgd[after][-1]) if after.any() else 0.0


def replay(records: list[GnssRecord], coefficients=RUHL_2019, end_s: float = 300.0, step_s: float = 1.0):
    pgds = [running_pgd(r.displacement_m) for r in records]
    snapshots = []
    for now in np.arange(0.0, end_s + step_s / 2, step_s):
        values, distances = [], []
        for record, pgd in zip(records, pgds):
            if now < record.distance_km / S_SPEED_KM_S:
                continue
            index = int(np.floor((now - record.start_offset) * record.sampling_rate + 1e-9))
            if index < 0:
                continue
            value = float(pgd[min(index, pgd.size - 1)])
            if value >= MIN_PGD_M:
                values.append(value)
                distances.append(record.distance_km)
        magnitude = network_magnitude(values, distances, coefficients) if len(values) >= MIN_STATIONS else None
        snapshots.append(Snapshot(float(now), magnitude, len(values), []))
    return snapshots
