# Phase 2 results: the GNSS magnitude on 29 earthquakes, each one held out

The magnitude from GNSS peak ground displacement (PGD), log10(PGD) = A + B·M + C·M·log10(R),
replayed second by second on the 29 earthquakes (Mw 6.0 to 9.0) of the Ruhl et al. (2019)
high-rate GNSS database. Every earthquake is scored with coefficients refitted on the other 28
only, so the method never sees the earthquake it is tested on.

- Code: commit `954698b`
- Run: https://www.kaggle.com/code/sankurkundu/notebooka5bbb87656
- Data: Ruhl et al. (2019), https://doi.org/10.5281/zenodo.1434374 (CC BY-SA 4.0); origin times,
  hypocentres and Global CMT moment magnitudes from Table 1 of the paper
- Rules: hypocentral distance up to 1,000 km; a station counts once a 3 km/s wave from the
  hypocentre could have reached it and its PGD reaches 4 cm, the paper's noise cutoff; refit with
  equal weight for each occupied cell of a 20 × 20 grid in log distance and log PGD, in the spirit
  of the paper's weighting

"Within 0.3 from" is the first second after which the estimate stays within 0.3 of Mw; "–" means
never. "Error" is Mw minus the final estimate (positive = underestimate).

| Earthquake | Mw | GNSS stations | First estimate | At 60 s | Final | Error | Within 0.3 from |
|---|---|---|---|---|---|---|---|
| 2011-03-11 Tohoku2011 | 9.0 | 811 | 6.21 at 41 s | 7.32 | 8.82 | 0.18 | 126 s |
| 2010-02-27 Maule2010 | 8.8 | 20 | 6.27 at 28 s | 8.95 | 8.80 | 0.00 | 172 s |
| 2015-09-16 Illapel2015 | 8.3 | 38 | 6.02 at 14 s | 7.79 | 7.54 | 0.76 | – |
| 2003-09-25 Tokachi2003 | 8.3 | 343 | 6.28 at 25 s | 7.55 | 7.66 | 0.64 | – |
| 2017-09-08 Tehuantepec2017 | 8.2 | 7 | 8.26 at 97 s | – | 7.97 | 0.23 | 246 s |
| 2014-04-01 Iquique2014 | 8.1 | 23 | 6.74 at 25 s | 7.60 | 7.54 | 0.56 | – |
| 2016-04-16 Ecuador2016 | 7.8 | 21 | 5.72 at 10 s | 7.29 | 7.47 | 0.33 | – |
| 2016-11-13 Kaikoura2016 | 7.8 | 36 | 6.65 at 10 s | 7.14 | 7.69 | 0.11 | 104 s |
| 2015-04-25 Nepal2015 | 7.8 | 7 | 6.05 at 20 s | 8.74 | 8.43 | -0.62 | – |
| 2011-03-11 Ibaraki2011 | 7.7 | 645 | 6.05 at 37 s | 7.45 | 7.29 | 0.41 | – |
| 2014-04-03 Iquique_aftershock2014 | 7.7 | 12 | 6.01 at 14 s | 7.21 | 7.14 | 0.56 | – |
| 2010-10-25 Mentawai2010 | 7.7 | 12 | 5.97 at 26 s | 6.92 | 7.08 | 0.62 | – |
| 2011-03-11 N.Honshu2011 | 7.7 | 128 | 6.98 at 109 s | – | 7.29 | 0.41 | – |
| 2016-12-25 Melinka2016 | 7.6 | 7 | 7.69 at 27 s | 7.46 | 7.35 | 0.25 | 289 s |
| 2012-09-05 Nicoya2012 | 7.6 | 9 | 7.02 at 14 s | 7.59 | 7.59 | 0.01 | 20 s |
| 2011-03-11 Iwate2011 | 7.4 | 173 | 6.26 at 31 s | 6.82 | 7.08 | 0.32 | – |
| 2011-03-09 Miyagi2011A | 7.3 | 160 | 6.50 at 56 s | 6.55 | 7.09 | 0.21 | 207 s |
| 2012-12-07 N.Honshu2012 | 7.3 | 90 | 7.23 at 117 s | – | 7.35 | -0.05 | 117 s |
| 2015-05-12 Nepal_aftershock2015 | 7.3 | 5 | 6.50 at 19 s | 6.78 | 6.81 | 0.49 | – |
| 2010-04-04 ElMayor2010 | 7.2 | 93 | 6.24 at 26 s | 7.12 | 7.16 | 0.04 | 40 s |
| 2011-04-07 Miyagi2011B | 7.1 | 167 | 6.26 at 37 s | 6.64 | 7.16 | -0.06 | 129 s |
| 2013-10-25 N.Honshu2013 | 7.1 | 9 | 6.90 at 145 s | – | 7.24 | -0.14 | 145 s |
| 2017-09-19 Puebla2017 | 7.1 | 5 | 6.29 at 35 s | 6.45 | 6.57 | 0.54 | – |
| 2016-04-15 Kumamoto2016 | 7.0 | 224 | 5.69 at 23 s | 6.80 | 6.84 | 0.16 | 35 s |
| 2014-05-24 Aegean2014 | 6.9 | 4 | 5.98 at 22 s | 6.42 | 6.42 | 0.48 | – |
| 2011-04-11 E.Fukushima2011 | 6.6 | 84 | 5.69 at 16 s | 6.21 | 6.86 | -0.26 | 87 s |
| 2015-11-17 Lefkada2015 | 6.5 | 5 | 6.48 at 4 s | 6.54 | 6.64 | -0.14 | 4 s |
| 2014-08-24 Napa2014 | 6.1 | 67 | 5.71 at 6 s | 6.26 | 6.56 | -0.46 | – |
| 2004-09-28 Parkfield2004 | 6.0 | 12 | 5.56 at 6 s | 5.81 | 5.94 | 0.06 | 7 s |

| Coefficients | Within 0.3 by the end | Mean final error | Mean absolute final error |
|---|---|---|---|
| Refitted without the earthquake, distance and PGD bins equal (main result) | 15 of 29 | +0.19 | 0.31 |
| Refitted without the earthquake, every recording equal | 17 of 29 | +0.01 | 0.34 |
| Refitted without the earthquake, every earthquake equal | 13 of 29 | +0.04 | 0.36 |
| Published Ruhl et al. (2019), fitted with the earthquake | 15 of 29 | +0.13 | 0.29 |

## What it shows

- **GNSS does not stall on the largest earthquakes.** Held out, Tohoku 2011 (Mw 9.0) ends at 8.82
  and Maule 2010 (Mw 8.8) at 8.80, both within 0.3 after two to three minutes. Neither had an
  open seismic station within 250 km in Phase 1.
- **On the same M8 earthquakes, it closes most of the classic method's gap:**

  | Earthquake | Mw | Classic seismic, final (Phase 1) | GNSS, final (held out) |
  |---|---|---|---|
  | Tohoku 2011 | 9.0 | no open station | 8.82 |
  | Maule 2010 | 8.8 | no open station | 8.80 |
  | Illapel 2015 | 8.3 | 6.21 | 7.54 |
  | Tehuantepec 2017 | 8.2 | 6.59 | 7.97 |
  | Iquique 2014 | 8.1 | 5.97 | 7.54 |

- **It is not enough on its own.** Illapel, Tokachi-oki and Iquique still end 0.5 to 0.8 low; Nepal
  2015, whose rupture drove towards the nearby stations, ends 0.6 high; on Napa 2014 (Mw 6.1) the
  classic seismic method is within 0.3 from 4 seconds while GNSS ends 0.46 high. GNSS is also
  slow: one to four minutes to settle. Fusing the two, in Phase 5, is the point.
- **The weighting of the refit matters most for the largest earthquake.** With every recording
  weighted equally, Japan's thousands of recordings of magnitude 7 earthquakes decide the fit, and
  Tohoku held out is overestimated (10.5). The binned weighting is the main result for that reason;
  the other weightings are shown above so the choice is visible.
- **Holding each earthquake out costs little:** mean absolute error 0.31, against 0.29 for the
  published coefficients, which were fitted with the earthquake they are scored on.
- **Generous to GNSS in one respect:** the database holds post-processed displacements, so the
  replay has research-grade positions and no transmission delay. Real-time positioning is noisier.
