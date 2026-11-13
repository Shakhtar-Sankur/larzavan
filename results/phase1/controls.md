# Phase 1 controls: earthquakes where the classic magnitude is known to work

The same replay as for the M8+ earthquakes, on recordings within 150 km.

- Code: commit `1365eca`
- Run: https://www.kaggle.com/code/sankurkundu/notebookcf5db34abd
- Data: FDSN data centres NCEDC, SCEDC and IRIS

| Earthquake | USGS M | Stations | First estimate | Final estimate | Underestimate | Within 0.3 from |
|---|---|---|---|---|---|---|
| 2014-08-24 South Napa, California | 6.0 | 212 | 5.90 at 4 s | 5.918 | 0.102 | 4 s |
| 2019-07-04 Ridgecrest, California (foreshock) | 6.4 | 86 | 2.93 at 2 s | 6.198 | 0.202 | 26 s |
| 2019-07-06 Ridgecrest, California (mainshock) | 7.1 | 78 | 3.35 at 2 s | 6.455 | 0.645 | – |

## What it shows

- **The pipeline is right:** on South Napa (magnitude 6.0) the estimate is within 0.3 from 4 seconds
  after the origin and stays there; on the Ridgecrest foreshock (magnitude 6.4) it ends within 0.2.
- **The stall already starts at magnitude 7:** with 78 stations, the Ridgecrest mainshock (magnitude
  7.1) ends at 6.46 and is never within 0.3.
- The first estimates, from the first second of P waves at the nearest stations, are low on every
  earthquake; that is expected, and why the estimate is updated every second.
