# Larzavan

**Larzavan** is an open, global earthquake early-warning system for every damaging earthquake,
from magnitude 5 to 9 and above. Its engine is **Zelzana**, which estimates how big an earthquake
is, second by second, while it is still happening.

## Early warning, not prediction

Nobody can predict earthquakes: no method has ever reliably forecast one, and Larzavan does not
try. Larzavan starts the moment an earthquake begins. The earthquake's waves travel through the ground at a few
kilometres per second, while a warning travels at the speed of light. That gap saves lives in
three ways:

1. **Seconds before the shaking.** Cities tens to hundreds of kilometres away can get several to
   tens of seconds of warning: enough to stop trains and lifts, halt surgery, shut gas valves and
   get people under tables. Japan's warning system slows its bullet trains this way.
2. **Minutes before a tsunami, the biggest life-saver.** Tsunami waves often reach the nearest
   coasts 15 to 40 minutes after a great earthquake. How big the warning is, and how many people
   are told to leave, depends on getting the magnitude right in the first minutes.
3. **The first hour after.** Knowing where the shaking was worst sends rescuers to the right
   places first.

## Every damaging earthquake

Moderate earthquakes cause havoc too, and they are far more frequent: the 2003 Bam earthquake
(magnitude 6.6) killed about 26,000 people, and the 2011 Christchurch earthquake (6.2) killed 185.
Since 2000 the USGS has recorded 44,290 earthquakes of magnitude 5 to 6, 3,601 of 6 to 7 and 400
of 7 and above. For magnitude 5 to 7, today's magnitude methods work well; what limits warnings is
speed, the blind zone close to the epicentre where shaking arrives before any alert, and too few
sensors near cities. Larzavan answers with the fastest possible detection, dense low-cost and
citizen sensors near cities, on-site warning (each sensor warns its own location from the first
P wave), and shaking forecasts for each city.

## The problem only Larzavan takes on: the largest earthquakes

Early-warning systems measure an earthquake in its first seconds. For the largest earthquakes,
the ones that cause tsunamis, those first seconds are not enough: the rupture is still growing,
and the magnitude estimate stalls far below the true size. Japan's first estimate for the 2011
Tohoku earthquake was 7.9; it was a 9.0, so the first tsunami warning was too low. Zelzana is
being built to give a correct magnitude, with an honest uncertainty, for earthquakes of magnitude
7.5 to 9 and above, worldwide, from open data.

## Status: Phase 1, measuring the problem

Phase 1 replays every magnitude 8+ earthquake since 2000 (28 in the USGS catalogue) second by
second, with the classic early-warning magnitude (peak P-wave displacement, Kuyuk & Allen 2013),
using open recordings within 250 km. The replay is generous to the classic method: P waves are
picked near their theoretical arrival and data arrive with no delay.

Control: on the 2014 South Napa, California earthquake (magnitude 6.0), where the classic method is
known to work, it gives 5.9 four seconds after the origin and 5.95 at the end, within 0.3
throughout. On the 2015 Illapel, Chile earthquake (magnitude 8.3), it stays near 6.2. Results for
all 28 earthquakes and the control earthquakes will be published in `results/phase1/` from a
public Kaggle run.

## What Larzavan will not do

- **No prediction.** Larzavan warns about an earthquake that has already started.
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
