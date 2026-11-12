# Larzavan

**Open, global earthquake early warning for the largest earthquakes.**

Its magnitude engine is **Zelzana**.

Early-warning systems measure an earthquake in its first seconds. For the largest earthquakes,
the ones that cause tsunamis, those first seconds are not enough: the rupture is still growing,
and the magnitude estimate stalls far below the true size. Japan's first estimate for the 2011
Tohoku earthquake was 7.9; it was a 9.0. Larzavan is being built to give a correct magnitude, with
an honest uncertainty, for earthquakes of magnitude 7.5 to 9 and above, worldwide, from open data.

## Status: Phase 1, measuring the problem

Phase 1 replays every magnitude 8+ earthquake since 2000 (28 in the USGS catalogue) second by
second, with the classic early-warning magnitude (peak P-wave displacement, Kuyuk & Allen 2013),
using open recordings within 250 km. The replay is generous to the classic method: P waves are
picked near their theoretical arrival and data arrive with no delay.

First result, the 2015 Illapel, Chile earthquake (USGS magnitude 8.3), five stations within 250 km:
the classic estimate stays near magnitude 6.0 throughout. Results for all 28 earthquakes will be
published in `results/phase1/` from a public Kaggle run.

## What Larzavan will not do

- **No prediction.** Larzavan describes an earthquake that has already started.
- **No public alerts of its own.** Alerts reach people through each country's agency; Larzavan
  publishes research estimates and a public scorecard.
- **No unverifiable claims.** Every number comes from public code, public data and a public run.

## Run it

```bash
pip install -e ".[dev]"
pytest
python scripts/phase1_megaquakes.py --data-dir data --out-dir results/phase1
python scripts/phase1_megaquakes.py --only us20003k7a --providers IRIS   # one earthquake
```

Data come from the open FDSN data centres (IRIS/EarthScope, GEOFON, ORFEUS, RESIF, INGV and
others) through ObsPy, and the catalogue from the USGS.

## Plan

See [docs/PLAN.md](docs/PLAN.md).

## Licence

MIT. Author: Sankur Kundu.
