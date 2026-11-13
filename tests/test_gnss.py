import numpy as np
import pytest

from larzavan.benchmark import score
from larzavan.gnss import RUHL_EVENTS, GnssEvent, GnssRecord, hypocentral_distance_km, remove_pre_event
from larzavan.gnss_replay import MIN_PGD_M, S_SPEED_KM_S, final_pgd, replay
from larzavan.zelzana.pgd_magnitude import RUHL_2019, fit, network_magnitude, running_pgd, station_magnitude


def predicted_pgd(magnitude, distance_km, coefficients=RUHL_2019):
    a, b, c = coefficients
    return 10 ** (a + b * magnitude + c * magnitude * np.log10(distance_km))


def test_station_and_network_magnitude_invert_the_scaling_law():
    distances = np.array([50.0, 120.0, 400.0])
    pgds = predicted_pgd(8.5, distances)
    for p, d in zip(pgds, distances):
        assert station_magnitude(p, d) == pytest.approx(8.5)
    assert network_magnitude(pgds, distances) == pytest.approx(8.5)


def test_fit_recovers_known_coefficients():
    rng = np.random.default_rng(0)
    magnitude = rng.uniform(6, 9, 300)
    distance = 10 ** rng.uniform(1, 3, 300)
    pgd = predicted_pgd(magnitude, distance)
    assert fit(pgd, distance, magnitude) == pytest.approx(RUHL_2019, abs=1e-6)


def test_running_pgd_is_the_peak_so_far_of_the_three_components():
    data = np.array([[0.0, 3.0, 0.0, 0.0], [0.0, 4.0, 0.0, 6.0], [0.0, 0.0, 1.0, 0.0]])
    assert running_pgd(data).tolist() == [0.0, 5.0, 5.0, 6.0]


def test_pre_event_position_is_removed():
    data = np.array([[2.0, 2.0, 2.0, 5.0]])
    assert remove_pre_event(data, -1.0, 1.0).tolist() == [[0.0, 0.0, 0.0, 3.0]]  # samples at -1 s and 0 s
    assert remove_pre_event(data, 0.5, 1.0).tolist() == [[0.0, 0.0, 0.0, 3.0]]  # no pre-event sample: first one


def test_hypocentral_distance():
    event = GnssEvent("x", "2000-01-01T00:00:00", 0.0, 0.0, 30.0, 7.0)
    assert hypocentral_distance_km(event, 0.0, 0.0) == pytest.approx(30.0)
    assert hypocentral_distance_km(event, 0.0, 1.0) == pytest.approx(np.hypot(111.19, 30.0), rel=0.01)


def test_database_table_has_29_earthquakes():
    assert len(RUHL_EVENTS) == 29
    assert len({e.name for e in RUHL_EVENTS}) == 29
    assert max(e.magnitude for e in RUHL_EVENTS) == 9.0


def record(distance_km, final_m, rise_s=20.0, rate=1.0):
    """A station whose displacement ramps to final_m after the S wave arrives."""
    t = np.arange(-10.0, 300.0, 1.0 / rate)
    arrival = distance_km / S_SPEED_KM_S
    east = np.clip((t - arrival) / rise_s, 0.0, 1.0) * final_m
    return GnssRecord("STA", 0.0, 0.0, distance_km, -10.0, rate, np.vstack([east, 0 * t, 0 * t]))


def test_replay_reaches_the_true_magnitude_and_ignores_noise_before_the_s_wave():
    records = [record(d, predicted_pgd(8.8, d)) for d in (60.0, 150.0, 300.0)]
    snapshots = replay(records)
    assert snapshots[0].magnitude is None  # no station has seen the S wave yet
    result = score(snapshots, 8.8)
    assert result.final_estimate == pytest.approx(8.8, abs=1e-3)
    assert result.time_within_tolerance_s is not None
    assert final_pgd(records[0]) == pytest.approx(predicted_pgd(8.8, 60.0))


def test_stations_below_the_noise_cutoff_are_not_used():
    snapshots = replay([record(500.0, MIN_PGD_M / 2)])
    assert all(s.magnitude is None for s in snapshots)
