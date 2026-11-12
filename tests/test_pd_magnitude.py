import numpy as np

from larzavan.zelzana.pd_magnitude import displacement, magnitude_from_pd, peak_displacement_cm


def test_kuyuk_allen_relation():
    # M = 1.23 log10(Pd) + 1.38 log10(E) + 5.39, Pd in cm, E in km
    assert np.isclose(magnitude_from_pd(1.0, 10.0), 1.38 + 5.39)
    assert np.isclose(magnitude_from_pd(10.0, 100.0), 1.23 + 2 * 1.38 + 5.39)


def test_processing_is_causal():
    fs = 100.0
    x = np.zeros(2000)
    x[1500] = 1.0  # an impulse at 15 s
    for units in ("M/S", "M/S**2"):
        d = displacement(x, units, fs, pre_event_samples=1000)
        assert np.all(d[:1500] == 0.0)
        assert np.any(d[1500:] != 0.0)


def test_displacement_amplitude_of_a_sine():
    fs, f, amp_disp = 100.0, 1.0, 0.002  # 2 mm displacement at 1 Hz
    t = np.arange(0, 60, 1 / fs)
    velocity = amp_disp * 2 * np.pi * f * np.cos(2 * np.pi * f * t)
    d = displacement(velocity, "M/S", fs, pre_event_samples=0)
    late = np.max(np.abs(d[int(40 * fs) :]))
    assert abs(late - amp_disp) / amp_disp < 0.03  # 3 Hz low-pass and 0.075 Hz high-pass barely touch 1 Hz


def test_pd_window_stops_at_four_seconds_s_wave_and_now():
    fs = 10.0
    disp = np.zeros(200)
    disp[int(5 * fs)] = 0.01  # 1 cm at 5 s
    disp[int(8 * fs)] = 0.05  # 5 cm at 8 s, after the 4 s window
    common = dict(fs=fs, start_offset=0.0, p_time=3.0)
    assert peak_displacement_cm(disp, s_time=None, now=20.0, **common) == 1.0
    assert peak_displacement_cm(disp, s_time=4.5, now=20.0, **common) == 0.0  # S before the 1 cm peak
    assert peak_displacement_cm(disp, s_time=None, now=4.0, **common) == 0.0  # peak not received yet
    assert peak_displacement_cm(disp, s_time=None, now=2.0, **common) is None  # before P
