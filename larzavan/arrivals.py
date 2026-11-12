"""Theoretical P and S arrival times (IASP91), standing in for a perfect phase picker."""

from __future__ import annotations

from functools import lru_cache

from obspy.taup import TauPyModel

P_PHASES = ["P", "p", "Pn", "Pg", "Pdiff"]
S_PHASES = ["S", "s", "Sn", "Sg", "Sdiff"]


@lru_cache(maxsize=1)
def _model() -> TauPyModel:
    return TauPyModel(model="iasp91")


def first_arrival(depth_km: float, distance_deg: float, phases: list[str]) -> float | None:
    """Seconds after the origin time of the first of the given phases, or None if none arrives."""
    arrivals = _model().get_travel_times(
        source_depth_in_km=max(depth_km, 0.0), distance_in_degree=distance_deg, phase_list=phases
    )
    return min(a.time for a in arrivals) if arrivals else None


def p_and_s(depth_km: float, distance_deg: float) -> tuple[float | None, float | None]:
    return first_arrival(depth_km, distance_deg, P_PHASES), first_arrival(depth_km, distance_deg, S_PHASES)
