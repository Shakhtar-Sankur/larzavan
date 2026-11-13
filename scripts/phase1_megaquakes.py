"""Phase 1: replay every M8+ earthquake since 2000 with the classic Pd magnitude.

python scripts/phase1_megaquakes.py --data-dir data --out-dir results/phase1
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from larzavan.benchmark import score  # noqa: E402
from larzavan.catalog import fetch_events  # noqa: E402
from larzavan.replay import replay  # noqa: E402
from larzavan.report import event_chart, markdown_table, summary_chart  # noqa: E402
from larzavan.waveforms import download, load_records  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-magnitude", type=float, default=8.0)
    ap.add_argument("--start", default="2000-01-01")
    ap.add_argument("--end", default=None, help="last date to include; default: today")
    ap.add_argument("--max-km", type=float, default=250.0)
    ap.add_argument("--data-dir", type=Path, default=Path("data"))
    ap.add_argument("--out-dir", type=Path, default=Path("results/phase1"))
    ap.add_argument("--providers", nargs="*", default=None, help="FDSN data centres; default: all known")
    ap.add_argument("--only", nargs="*", default=None, help="USGS event ids to run")
    ap.add_argument("--skip-download", action="store_true")
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    events = fetch_events(args.min_magnitude, args.start, args.end)
    if args.only:
        events = [e for e in events if e.id in args.only]
    until = f" until {args.end}" if args.end else ""
    print(f"{len(events)} earthquakes of M{args.min_magnitude}+ since {args.start}{until}", flush=True)

    rows = []
    for event in events:
        label = f"{event.time:%Y-%m-%d} M{event.magnitude:.1f} {event.place}"
        print(f"\n== {label} ({event.id})", flush=True)
        try:
            wave_dir = args.data_dir / event.id / "waveforms"
            sta_dir = args.data_dir / event.id / "stations"
            if not args.skip_download:
                wave_dir, sta_dir = download(event, args.data_dir, max_km=args.max_km, providers=args.providers)
            records = load_records(event, wave_dir, sta_dir, max_km=args.max_km) if wave_dir.exists() else []
            snapshots = replay(records)
            result = score(snapshots, event.magnitude)
            error = None
        except Exception as exc:  # one failing earthquake must not stop the run
            traceback.print_exc()
            records, snapshots, result, error = [], [], score([], event.magnitude), repr(exc)
        row = {
            "id": event.id,
            "date": f"{event.time:%Y-%m-%d}",
            "place": event.place,
            "depth_km": event.depth_km,
            "n_records": len(records),
            "error": error,
            **asdict(result),
        }
        rows.append(row)
        print(json.dumps(row), flush=True)
        (args.out_dir / f"{event.id}.json").write_text(
            json.dumps(
                {
                    "event": {**row},
                    "stations": [
                        {
                            "id": r.seed_id,
                            "distance_km": round(r.distance_km, 1),
                            "p_time": round(r.p_time, 2),
                            "p_theoretical": round(r.p_theoretical, 2),
                            "p_picked": r.p_picked,
                            "channel_units": r.units,
                        }
                        for r in records
                    ],
                    "snapshots": [asdict(s) for s in snapshots],
                },
                indent=1,
            )
        )
        if snapshots:
            event_chart(
                args.out_dir / f"{event.id}.png",
                label,
                event.magnitude,
                [s.time_s for s in snapshots],
                [s.magnitude for s in snapshots],
            )

    (args.out_dir / "summary.json").write_text(json.dumps(rows, indent=1))
    (args.out_dir / "summary.md").write_text(markdown_table(rows) + "\n")
    summary_chart(args.out_dir / "summary.png", rows)
    print("\n" + markdown_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
