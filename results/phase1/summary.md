# Phase 1 results: the classic magnitude on every M8+ earthquake since 2000

The classic early-warning magnitude (peak P-wave displacement, Kuyuk & Allen 2013), replayed second
by second on open recordings within 250 km, for the 28 earthquakes of magnitude 8 and above in the
USGS catalogue since 2000.

- Code: commit `d9f94cf`
- Run: https://www.kaggle.com/code/sankurkundu/notebook3f9c3c9150
- Data: FDSN data centres IRIS, GEOFON, ORFEUS, RESIF, INGV, ETH, GEONET, AUSPASS, USP, KOERI,
  NOA, BGR, NCEDC, SCEDC and Raspberry Shake

"Within 0.3 from" is the first second after which the estimate stays within 0.3 of the USGS
magnitude; "–" means never.

| Earthquake | USGS M | Stations | First estimate | Final estimate | Underestimate | Within 0.3 from |
|---|---|---|---|---|---|---|
| 2000-11-16 2000 New Ireland Earthquake | 8.0 | 0 | – | – | – | – |
| 2001-06-23 6 km SSW of Atico, Peru | 8.4 | 0 | – | – | – | – |
| 2003-09-25 2003 Tokachi-Oki Earthquake | 8.2 | 0 | – | – | – | – |
| 2004-12-23 2004 Tasman Sea Earthquake | 8.1 | 0 | – | – | – | – |
| 2004-12-26 2004 Sumatra - Andaman Islands Earthquake | 9.1 | 0 | – | – | – | – |
| 2005-03-28 78 km WSW of Singkil, Indonesia | 8.6 | 1 | 5.28 at 35 s | 5.85 | 2.75 | – |
| 2006-05-03 2006 Tonga Earthquake | 8.0 | 0 | – | – | – | – |
| 2006-11-15 2006 Kuril Islands Earthquake | 8.3 | 0 | – | – | – | – |
| 2007-01-13 2007 Kuril Islands Earthquake | 8.1 | 0 | – | – | – | – |
| 2007-04-01 2007 Solomon Islands Earthquake | 8.1 | 0 | – | – | – | – |
| 2007-08-15 41 km SW of San Vicente de Cañete, Peru | 8.0 | 0 | – | – | – | – |
| 2007-09-12 122 km SW of Bengkulu, Indonesia | 8.4 | 1 | 6.04 at 27 s | 6.268 | 2.132 | – |
| 2009-09-29 2009 Samoa Earthquake | 8.1 | 2 | 7.15 at 26 s | 5.504 | 2.596 | – |
| 2010-02-27 2010 Maule, Chile Earthquake | 8.8 | 0 | – | – | – | – |
| 2011-03-11 2011 Great Tohoku Earthquake, Japan | 9.1 | 0 | – | – | – | – |
| 2012-04-11 2012 Wharton Basin Earthquake | 8.6 | 0 | – | – | – | – |
| 2012-04-11 2012 Wharton Basin Aftershock | 8.2 | 0 | – | – | – | – |
| 2013-02-06 2013 Santa Cruz Islands Earthquake | 8.0 | 0 | – | – | – | – |
| 2013-05-24 2013 Sea of Okhotsk Earthquake | 8.3 | 0 | – | – | – | – |
| 2014-04-01 93 km NW of Iquique, Chile | 8.2 | 20 | 4.62 at 13 s | 5.972 | 2.228 | – |
| 2015-09-16 48 km W of Illapel, Chile | 8.3 | 5 | 6.28 at 21 s | 6.211 | 2.089 | – |
| 2017-09-08 2017 Tehuantepec, Mexico Earthquake | 8.2 | 1 | 6.47 at 36 s | 6.588 | 1.612 | – |
| 2018-08-19 2018 Fiji Earthquake | 8.2 | 0 | – | – | – | – |
| 2019-05-26 78 km NE of Navarro, Peru | 8.0 | 0 | – | – | – | – |
| 2021-03-04 2021 Kermadec Islands, New Zealand Earthquake | 8.1 | 0 | – | – | – | – |
| 2021-07-29 2021 Chignik, Alaska Earthquake | 8.2 | 7 | 6.05 at 18 s | 6.705 | 1.495 | – |
| 2021-08-12 2021 South Sandwich Islands Earthquake | 8.1 | 0 | – | – | – | – |
| 2025-07-29 2025 Kamchatka Peninsula, Russia Earthquake | 8.8 | 1 | 6.92 at 22 s | 6.918 | 1.882 | – |

## What it shows

- **Only 8 of the 28 earthquakes have any open recording within 250 km.** Sumatra 2004, Maule
  2010 and Tohoku 2011 have none.
- **On all 8, the classic magnitude stays far too low:** final estimates between 5.5 and 6.9 for
  earthquakes of magnitude 8.1 to 8.8, underestimates of 1.5 to 2.75. It is never within 0.3.
- With 20 stations, Iquique 2014 (magnitude 8.2) ends at 5.97. More stations do not fix the
  method: this is its known saturation, because the first seconds of P waves do not yet carry
  the size of a rupture that is still growing.
