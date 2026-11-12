# Larzavan: the plan

Larzavan is an open, global early-warning system for the largest earthquakes. Zelzana is its
engine. This plan is maintained with the code; every claim in it is a target until a public run
shows it.

## 1. The limits we break, and the ones physics won't let anyone break

| We break | We respect |
|---|---|
| Magnitude stalling on giant earthquakes | Nobody can predict earthquakes, and Larzavan never claims to |
| Treating an earthquake as a point instead of a growing rupture | Right next to the epicentre, shaking arrives before any warning can |
| Country-by-country, closed systems | Public alerts come from each country's own agency |
| Results that cannot be checked | |
| One magnitude number with no uncertainty | |
| Gravity signals usable only from magnitude 8 (we will attempt to go lower) | |

## 2. Where today's systems fall short, and what Larzavan does instead

| Today | Example | Larzavan / Zelzana |
|---|---|---|
| Giant earthquakes underestimated | Japan's first estimate for Tohoku 2011 was 7.9 against a final 9.0; Google's Android system underestimated Turkey 2023 | Zelzana fuses four kinds of signal, two of which do not saturate: speed-of-light gravity signals, GNSS ground displacement, seismic shaking, fibre-optic strain |
| One country at a time | The US system covers the US West Coast | Global from day one, on every open station |
| An earthquake treated as a point | Long ruptures shake distant cities harder than a point model predicts | Live rupture tracking: length, direction, still growing |
| Methods and track records hard to inspect | No shared megaquake test | Code, data and every estimate public |
| One number, no uncertainty | Agencies guess how far to trust it | "8.6 to 9.1, 90% confidence, still growing" |
| Tsunami threat built on an underestimated magnitude | Tohoku's first tsunami warning was too low | Tsunami threat from the corrected source, computed on GPU |
| Sparse sensors in poorer regions | Large gaps in Africa, Central Asia and the Pacific islands | Citizen seismographs, low-cost sensor designs, fibre and undersea-cable partners |

## 3. What Zelzana is made of

| Layer | What it does | Advanced element |
|---|---|---|
| 1. Intake | Live (SeedLink) and archived (FDSN) data from every open station; more than 5,000 broadband stations in 217 networks through IRIS alone | Per-packet latency accounting; station health checks that reject clipped, dead or spoofed channels |
| 2. Detection and location | Machine-learning phase pickers and associators | Batched on one GPU for every station on Earth at once; handles overlapping earthquakes and aftershocks |
| 3. Seismic magnitude | Fast magnitude from the first seconds of P waves | Classic baseline (Phase 1), then learned estimators calibrated per region |
| 4. Gravity layer (Kshana) | Deep learning on prompt elasto-gravity signals, which travel at the speed of light | Trained on simulated signals with real noise; network-wide stacking to push below magnitude 8 |
| 5. GNSS layer | Real-time ground displacement, which does not saturate | Static offsets and peak displacement; also ionospheric disturbances from GNSS for tsunami confirmation |
| 6. Fibre layer | Distributed acoustic sensing on telecom and undersea cables | Strain-rate magnitude estimates where partners share data |
| 7. Rupture tracker | Length, direction and growth of the rupture | Line-source and finite-fault estimates updated every second, from seismic and GNSS data |
| 8. Fusion | One magnitude with a calibrated uncertainty | Probabilistic fusion that weights each layer by its proven reliability for that magnitude and region |
| 9. Shaking forecast | Expected shaking intensity at cities, not just a magnitude | From the rupture, not a point, so long ruptures are not underestimated far away |
| 10. Tsunami link | Arrival times and threat levels on nearby coasts | Precomputed scenarios plus a GPU shallow-water solver for the corrected source |

## 4. The Larzavan Benchmark, the largest open test of its kind

| Tier | Earthquakes since 2000 | What it tests |
|---|---|---|
| 1 | 4,001 (M6+) | Detection, location, false alarms |
| 2 | 400 (M7+) | Magnitude speed and accuracy |
| 3 | 144 (M7.5+) | Megaquake magnitude and rupture tracking |
| 4 | 28 (M8+) | Gravity signals |

Every result is published second by second. Earthquakes held back from training keep the test
fair. Results are compared with the official real-time estimates where those are public. The
benchmark is versioned and archived with a citable identifier, so other systems can be measured
against it.

## 5. Firsts we aim for, claimed only once proven

1. The first open engine combining gravity, GNSS, seismic and fibre signals.
2. The largest open benchmark for earthquake early warning.
3. Gravity signals that work below magnitude 8.
4. Every open seismic station on Earth processed live on one GPU.
5. Shaking forecasts from the growing rupture, worldwide, from open data.

## 6. Roadmap

Every phase ends in something public.

1. **Proof of the problem.** Replay the 28 M8+ earthquakes with the classic method and publish
   where it falls short. *In progress.*
2. **GNSS layer.** Show how much sooner the magnitude becomes correct.
3. **Gravity layer.** Train the model; register for free research access to Japan's NIED data;
   invite the PEGSNet authors (Géoazur, France) to collaborate.
4. **Fusion, rupture tracking, shaking forecast and tsunami link,** then the full four-tier
   benchmark.
5. **Live shadow mode, 24/7.** A public scorecard against USGS and GFZ, with no public alerts
   from Larzavan.
6. **Give it to the world.** Free feeds in the international CAP alert format for agencies in
   Peru, Indonesia, the Philippines, Chile and Central America; UNESCO's tsunami programme; a
   peer-reviewed paper.
7. **Grow the network.** Citizen seismographs, low-cost sensor designs, fibre and
   undersea-cable partners.

## 7. How "best" gets proven

Only by these numbers, on held-out earthquakes:

- seconds until the magnitude is within 0.3 of the final value;
- seconds of warning at the nearest cities;
- false and missed alarms in live shadow mode;
- results against official real-time estimates.

## 8. Rules

- No prediction, ever.
- No public alerts of its own.
- Every result reproducible from public code, public data and a public run.
- Uncertainty is always reported with a magnitude.
