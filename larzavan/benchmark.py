"""Scores for one replayed earthquake."""

from __future__ import annotations

from dataclasses import dataclass

from larzavan.replay import Snapshot

TOLERANCE = 0.3


@dataclass
class Score:
    true_magnitude: float
    first_estimate_s: float | None  # first time any estimate exists
    first_estimate: float | None
    final_estimate: float | None  # at the end of the replay
    final_error: float | None  # true minus final estimate (positive = underestimate)
    time_within_tolerance_s: float | None  # first time the estimate stays within +-0.3 to the end
    n_stations_final: int


def score(snapshots: list[Snapshot], true_magnitude: float) -> Score:
    with_estimate = [s for s in snapshots if s.magnitude is not None]
    if not with_estimate:
        return Score(true_magnitude, None, None, None, None, None, 0)
    first, last = with_estimate[0], with_estimate[-1]
    settled = None
    for s in reversed(with_estimate):
        if abs(s.magnitude - true_magnitude) <= TOLERANCE:
            settled = s.time_s
        else:
            break
    return Score(
        true_magnitude,
        first.time_s,
        round(first.magnitude, 3),
        round(last.magnitude, 3),
        round(true_magnitude - last.magnitude, 3),
        settled,
        last.n_stations,
    )
