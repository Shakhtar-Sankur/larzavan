import numpy as np

from larzavan.benchmark import score
from larzavan.replay import Snapshot, replay
from larzavan.waveforms import StationRecord


def _record(p_time, distance_km=100.0):
    fs = 100.0
    t = np.arange(-60, 120, 1 / fs)
    v = np.where(t >= p_time, 0.01 * np.sin(2 * np.pi * 1.0 * (t - p_time)), 0.0)
    return StationRecord("XX.STA..HHZ", 0, 0, distance_km, p_time, None, p_time, False, fs, -60.0, v, "M/S")


def test_station_counts_only_after_its_p_wave():
    snaps = replay([_record(10.0), _record(30.0)], end_s=60)
    by_t = {s.time_s: s.n_stations for s in snaps}
    assert by_t[10.0] == 0 and by_t[11.0] == 1 and by_t[30.0] == 1 and by_t[31.0] == 2


def test_score_reports_underestimate_and_settling_time():
    snaps = [Snapshot(t, m, 3, []) for t, m in [(0, None), (1, 7.0), (2, 8.6), (3, 8.7), (4, 8.75)]]
    s = score(snaps, 8.8)
    assert s.first_estimate_s == 1 and s.final_estimate == 8.75
    assert np.isclose(s.final_error, 0.05) and s.time_within_tolerance_s == 2
    assert score(snaps[:2], 8.8).time_within_tolerance_s is None
