"""Causal P-wave picking near the theoretical arrival (recursive STA/LTA)."""

from __future__ import annotations

import numpy as np
from obspy.signal.trigger import recursive_sta_lta

STA_S, LTA_S, THRESHOLD, SEARCH_S = 0.5, 10.0, 4.0, 5.0


def pick_p(data: np.ndarray, fs: float, start_offset: float, theoretical_p: float) -> float | None:
    """First STA/LTA trigger within +-5 s of the theoretical P time, in seconds after origin.

    recursive_sta_lta is causal: the ratio at a sample uses only earlier samples.
    """
    n_lta = int(LTA_S * fs)
    if len(data) <= n_lta:
        return None
    pre = max(0, int((theoretical_p - SEARCH_S - start_offset) * fs) - n_lta)
    x = data - np.mean(data[pre : pre + n_lta])
    ratio = recursive_sta_lta(x, int(STA_S * fs), n_lta)
    t = start_offset + np.arange(len(x)) / fs
    candidates = np.where((t >= theoretical_p - SEARCH_S) & (t <= theoretical_p + SEARCH_S) & (ratio > THRESHOLD))[0]
    return float(t[candidates[0]]) if len(candidates) else None
