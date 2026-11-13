"""Magnitude from GNSS peak ground displacement (PGD).

log10(PGD) = A + B * M + C * M * log10(R), with PGD in metres and R the hypocentral distance in km
(Crowell et al. 2013; coefficients of Ruhl et al. 2019 by default). Unlike the peak P-wave
displacement of the first seconds, PGD keeps growing for as long as the rupture does, so it does
not stall on the largest earthquakes.
"""

from __future__ import annotations

import numpy as np

RUHL_2019 = (-5.919, 1.009, -0.145)


def running_pgd(displacement_m: np.ndarray) -> np.ndarray:
    """Peak three-component displacement so far, sample by sample, from (3, n) east/north/up."""
    return np.maximum.accumulate(np.sqrt((displacement_m**2).sum(axis=0)))


def station_magnitude(pgd_m: float, distance_km: float, coefficients=RUHL_2019) -> float:
    a, b, c = coefficients
    return (np.log10(pgd_m) - a) / (b + c * np.log10(distance_km))


def network_magnitude(pgd_m, distance_km, coefficients=RUHL_2019) -> float:
    """Least-squares magnitude for several stations: minimises the misfit in log10(PGD)."""
    a, b, c = coefficients
    y = np.log10(np.asarray(pgd_m, dtype=float)) - a
    g = b + c * np.log10(np.asarray(distance_km, dtype=float))
    return float((g * y).sum() / (g * g).sum())


def fit(pgd_m, distance_km, magnitude, weights=None) -> tuple[float, float, float]:
    """Weighted least-squares A, B, C from recordings of known magnitude."""
    pgd_m, distance_km, magnitude = (np.asarray(x, dtype=float) for x in (pgd_m, distance_km, magnitude))
    w = np.ones_like(pgd_m) if weights is None else np.asarray(weights, dtype=float)
    design = np.column_stack([np.ones_like(magnitude), magnitude, magnitude * np.log10(distance_km)])
    sw = np.sqrt(w)
    solution, *_ = np.linalg.lstsq(design * sw[:, None], np.log10(pgd_m) * sw, rcond=None)
    return tuple(float(x) for x in solution)
