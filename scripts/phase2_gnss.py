"""Phase 2: the GNSS peak-displacement magnitude on the 29 earthquakes of the Ruhl et al. database.

Every earthquake is replayed second by second with coefficients refitted on the other 28 only
(leave one earthquake out): the honest test of how the method would do on an earthquake it has
never seen. For reference, the published Ruhl et al. (2019) coefficients, fitted on all 29
including the one replayed, are scored too, as are two other weightings of the refit; without
the paper's weighting, holding out Tohoku leaves the fit to the magnitude 7 earthquakes and the
magnitude 9 is overestimated.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from larzavan import gnss  # noqa: E402
from larzavan.benchmark import score  # noqa: E402
from larzavan.gnss_replay import MIN_PGD_M, final_pgd, replay  # noqa: E402
from larzavan.report import event_chart, summary_chart  # noqa: E402
from larzavan.zelzana.pgd_magnitude import RUHL_2019, fit  # noqa: E402

WEIGHTINGS = ("bins", "none", "per_earthquake")
MAIN = "bins"


def weights(kind: str, names: np.ndarray, pgd: np.ndarray, dist: np.ndarray) -> np.ndarray:
    """bins (the main result): every occupied cell of a 20 x 20 grid in log distance and log PGD
    counts the same, in the spirit of Ruhl et al. (2019), so the thousands of Japanese recordings
    of magnitude 7 earthquakes do not decide the fit alone; none: every recording counts the same;
    per_earthquake: every earthquake counts the same."""
    if kind == "none":
        return np.ones(names.size)
    if kind == "per_earthquake":
        counts = {name: int((names == name).sum()) for name in set(names)}
        return np.array([1.0 / counts[name] for name in names])
    cells = []
    for values in (np.log10(dist), np.log10(pgd)):
        scaled = (values - values.min()) / (np.ptp(values) or 1.0)
        cells.append(np.clip((scaled * 20).astype(int), 0, 19))
    cell = cells[0] * 20 + cells[1]
    return 1.0 / np.bincount(cell, minlength=400)[cell]


def fmt(value, digits=2, suffix=""):
    return "–" if value is None else f"{value:.{digits}f}{suffix}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--out-dir", type=Path, default=Path("results/phase2"))
    ap.add_argument("--max-km", type=float, default=1000.0)
    ap.add_argument("--end-s", type=float, default=300.0)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    root = gnss.download(args.data_dir)
    events = gnss.RUHL_EVENTS
    records, fit_rows = {}, []  # fit_rows: (earthquake, final PGD, distance, magnitude)
    for event in events:
        records[event.name] = gnss.load_event(root, event, args.max_km)
        for r in records[event.name]:
            value = final_pgd(r)
            if value >= MIN_PGD_M:
                fit_rows.append((event.name, value, r.distance_km, event.magnitude))
        print(f"{event.name}: {len(records[event.name])} stations within {args.max_km:.0f} km", flush=True)

    names = np.array([row[0] for row in fit_rows])
    pgd, dist, mag = (np.array([row[i] for row in fit_rows], dtype=float) for i in (1, 2, 3))
    print(f"\n{len(fit_rows)} recordings with PGD >= {MIN_PGD_M} m")

    rows, comparison = [], {kind: [] for kind in (*WEIGHTINGS, "published")}
    for event in events:
        keep = names != event.name
        recs = records[event.name]
        coefficients = {
            kind: fit(pgd[keep], dist[keep], mag[keep], weights(kind, names[keep], pgd[keep], dist[keep]))
            for kind in WEIGHTINGS
        }
        coefficients["published"] = RUHL_2019
        scores = {}
        for kind, coeffs in coefficients.items():
            snapshots = replay(recs, coeffs, args.end_s)
            scores[kind] = score(snapshots, event.magnitude)
            comparison[kind].append(scores[kind])
            if kind == MAIN:
                main_snapshots = snapshots
        at60 = next((s.magnitude for s in main_snapshots if s.time_s == 60.0), None)
        row = {
            "name": event.name,
            "date": event.origin[:10],
            "magnitude": event.magnitude,
            "n_stations": len(recs),
            "coefficients": [round(x, 4) for x in coefficients[MAIN]],
            "at_60_s": None if at60 is None else round(at60, 3),
            **{kind: asdict(s) for kind, s in scores.items()},
        }
        rows.append(row)
        print(json.dumps({k: row[k] for k in ("name", "magnitude", "n_stations", "at_60_s")} | row[MAIN]), flush=True)
        (args.out_dir / f"{event.name}.json").write_text(
            json.dumps({**row, "snapshots": [asdict(s) for s in main_snapshots]}, indent=1)
        )
        event_chart(
            args.out_dir / f"{event.name}.png",
            f"{event.origin[:10]} {event.name} M{event.magnitude} (GNSS, held out)",
            event.magnitude,
            [s.time_s for s in main_snapshots],
            [s.magnitude for s in main_snapshots],
            label="GNSS PGD magnitude",
        )

    lines = [
        "| Earthquake | Mw | GNSS stations | First estimate | At 60 s | Final | Error | Within 0.3 from |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        h = r[MAIN]
        first = "–" if h["first_estimate"] is None else f"{h['first_estimate']:.2f} at {h['first_estimate_s']:.0f} s"
        lines.append(
            f"| {r['date']} {r['name']} | {r['magnitude']} | {r['n_stations']} | {first} | {fmt(r['at_60_s'])} | "
            f"{fmt(h['final_estimate'])} | {fmt(h['final_error'])} | {fmt(h['time_within_tolerance_s'], 0, ' s')} |"
        )
    lines += [
        "",
        "| Coefficients | Within 0.3 by the end | Mean final error | Mean absolute final error |",
        "|---|---|---|---|",
    ]
    labels = {
        "bins": "Refitted without the earthquake, distance and PGD bins equal (main result)",
        "none": "Refitted without the earthquake, every recording equal",
        "per_earthquake": "Refitted without the earthquake, every earthquake equal",
        "published": "Published Ruhl et al. (2019), fitted with the earthquake",
    }
    for kind, scores in comparison.items():
        errors = np.array([s.final_error for s in scores if s.final_error is not None])
        settled = sum(s.time_within_tolerance_s is not None for s in scores)
        lines.append(
            f"| {labels[kind]} | {settled} of {len(scores)} | {errors.mean():+.2f} | {np.abs(errors).mean():.2f} |"
        )
    table = "\n".join(lines)
    (args.out_dir / "summary.json").write_text(json.dumps(rows, indent=1))
    (args.out_dir / "summary.md").write_text(table + "\n")
    summary_chart(
        args.out_dir / "summary.png",
        [{"true_magnitude": r["magnitude"], "final_estimate": r[MAIN]["final_estimate"]} for r in rows],
        limits=(5.8, 9.4, 5.8),
        ylabel="GNSS PGD magnitude, end of replay (held out)",
    )
    print("\n" + table)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
