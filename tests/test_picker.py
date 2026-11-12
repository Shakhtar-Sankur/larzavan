import numpy as np

from larzavan.picker import pick_p


def test_picks_a_clear_onset_near_the_theoretical_time():
    fs = 100.0
    rng = np.random.default_rng(0)
    t = np.arange(-60, 60, 1 / fs)
    x = 1e-6 * rng.standard_normal(len(t))
    x[t >= 21.3] += 1e-3 * np.sin(2 * np.pi * 2.0 * (t[t >= 21.3] - 21.3))
    pick = pick_p(x, fs, -60.0, theoretical_p=20.0)
    assert pick is not None and 21.3 <= pick <= 21.6


def test_no_pick_without_an_onset():
    fs = 100.0
    x = 1e-6 * np.random.default_rng(1).standard_normal(int(120 * fs))
    assert pick_p(x, fs, -60.0, theoretical_p=20.0) is None
