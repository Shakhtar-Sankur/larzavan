"""The classic early-warning magnitude: peak P-wave displacement (Pd), Kuyuk & Allen (2013).

Kuyuk, H. S. and Allen, R. M. (2013), A global approach to provide magnitude estimates for
earthquake early warning alerts, Geophys. Res. Lett., 40, 6329-6333:

    M = 1.23 log10(Pd) + 1.38 log10(E) + 5.39

with Pd the peak absolute vertical displacement in cm within 4 s of the P arrival (only up to the
S arrival if it comes sooner), after a causal two-pole 3 Hz low-pass Butterworth filter, and E the
epicentral distance in km (stations up to 250 km). Displacement is obtained causally from velocity
or acceleration, with a causal 0.075 Hz high-pass after each integration to remove drift, as in
the ElarmS processing this relation was calibrated with.

Every filter here is causal (scipy.signal.sosfilt), so a value at time t uses only samples up to
t, as in a real-time system.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfilt

PD_WINDOW_S = 4.0
LOWPASS_HZ = 3.0
HIGHPASS_HZ = 0.075


def magnitude_from_pd(pd_cm: float, epicentral_km: float) -> float:
    return 1.23 * np.log10(pd_cm) + 1.38 * np.log10(max(epicentral_km, 1.0)) + 5.39


def _highpass(x: np.ndarray, fs: float) -> np.ndarray:
    return sosfilt(butter(2, HIGHPASS_HZ, btype="highpass", fs=fs, output="sos"), x)


def _integrate(x: np.ndarray, fs: float) -> np.ndarray:
    return np.cumsum(x) / fs


def displacement(data: np.ndarray, units: str, fs: float, pre_event_samples: int) -> np.ndarray:
    """Causal displacement in metres from velocity (M/S) or acceleration (M/S**2).

    The offset is removed with the mean of the samples before the P arrival only.
    """
    x = data - (np.mean(data[:pre_event_samples]) if pre_event_samples > 0 else data[0])
    if units == "M/S**2":
        x = _highpass(_integrate(x, fs), fs)
    elif units != "M/S":
        raise ValueError(f"unsupported units {units!r}")
    x = _highpass(_integrate(x, fs), fs)
    nyquist = fs / 2.0
    if LOWPASS_HZ < nyquist:
        x = sosfilt(butter(2, LOWPASS_HZ, btype="lowpass", fs=fs, output="sos"), x)
    return x


def peak_displacement_cm(
    disp_m: np.ndarray, fs: float, start_offset: float, p_time: float, s_time: float | None, now: float
) -> float | None:
    """Pd in cm over [P, min(P + 4 s, S, now)], or None if no sample of that window has arrived."""
    end = min(p_time + PD_WINDOW_S, now, s_time if s_time is not None else np.inf)
    i0 = int(np.ceil((p_time - start_offset) * fs))
    i1 = int(np.floor((end - start_offset) * fs)) + 1
    i0, i1 = max(i0, 0), min(i1, len(disp_m))
    if i1 <= i0:
        return None
    return float(np.max(np.abs(disp_m[i0:i1]))) * 100.0
