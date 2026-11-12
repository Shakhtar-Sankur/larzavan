# Larzavan: the plan

Larzavan is an open, global early-warning system for every damaging earthquake, from magnitude 5
to 9 and above, with a capability today's systems lack for the largest ones. Zelzana is its engine.

For magnitude 5 to 7 the magnitude methods already work; warnings are limited by speed, by the
blind zone near the epicentre and by sensor density near cities. For magnitude 7.5 and above the
magnitude itself stalls. Larzavan addresses both.

This plan is maintained with the code. Every capability in it is a target until a public run
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
| Too few real megaquakes to learn from (we train on physics simulations too) | |

## 2. Where today's systems fall short, and what Larzavan does instead

| Today | Example | Larzavan / Zelzana |
|---|---|---|
| Giant earthquakes underestimated | Japan's first estimate for Tohoku 2011 was 7.9 against a final 9.0; Google's Android system underestimated Turkey 2023 | Zelzana fuses gravity, GNSS, seismic and fibre signals; two of them do not saturate |
| One country at a time | The US system covers the US West Coast | Global from day one, on every open station |
| An earthquake treated as a point | Long ruptures shake distant cities harder than a point model predicts | Live rupture tracking: length, direction, slip, still growing |
| Methods and track records hard to inspect | No shared megaquake test | Code, data, models and every estimate public |
| One number, no uncertainty | Agencies guess how far to trust it | Calibrated intervals with a coverage guarantee: "8.6 to 9.1, 90%, still growing" |
| Tsunami threat built on an underestimated magnitude | Tohoku's first tsunami warning was too low | Tsunami threat from the corrected source, updated by ocean-bottom pressure data |
| Moderate earthquakes under cities leave little or no warning | Bam 2003 (M6.6), Christchurch 2011 (M6.2) | Fastest detection, on-site warning, dense low-cost sensors near cities |
| Sparse sensors in poorer regions | Large gaps in Africa, Central Asia and the Pacific islands | An open low-cost sensor node, citizen seismographs, fibre and undersea-cable partners |

## 3. Architecture: sense, understand, decide, deliver

### 3.1 Sense: every signal the Earth gives in the first minutes

| Source | What it gives | High-tech element |
|---|---|---|
| Open seismic networks | Live (SeedLink) and archived (FDSN) waveforms; more than 5,000 broadband stations in 217 networks through IRIS alone, plus GEOFON, ORFEUS and others | Per-packet latency accounting; automatic rejection of clipped, dead, drifting or spoofed channels |
| Strong-motion accelerometers | Unclipped shaking close to large earthquakes | Preferred near the source, where broadband sensors saturate |
| High-rate GNSS | Real-time ground displacement, which does not saturate | Precise point positioning at 1 to 10 samples per second; static offsets for finite-fault inversion |
| Prompt elasto-gravity signals | Gravity changes that travel at the speed of light, ahead of every seismic wave | Read from broadband seismometers and gravimeters by a network-wide deep model (Kshana) |
| Fibre-optic cables (DAS) | Thousands of strain sensors per cable, on land and under the sea | Through telecom and undersea "SMART" cable partners |
| Ocean-bottom pressure sensors | Direct tsunami measurement offshore (for example NOAA's open DART data) | Assimilated into the tsunami forecast as the wave crosses them |
| GNSS ionospheric sounding | Disturbances in the upper atmosphere caused by a tsunami | An independent confirmation of a tsunami, from the same GNSS receivers |
| Larzavan sensor node | An open, low-cost node: MEMS accelerometer, GNSS timing, a small processor | Runs P-wave detection on the device for on-site warning, and streams to the network; designs published openly |
| Citizen seismographs | Raspberry Shake and similar open networks | Dense coverage near cities at very low cost |

### 3.2 Understand: Zelzana

| Component | What it does | High-tech element |
|---|---|---|
| Seismic foundation model | One model pretrained on decades of open continuous waveforms | Self-supervised pretraining; fine-tuned for picking, magnitude, location and ground motion |
| Network transformer | Treats every station as a token and the whole network as one input | Attention across stations and signal types (building on transformer alerting models such as TEAM, Münchmeyer et al. 2021) |
| Detection and association | Picks, associates and locates earthquakes, including overlapping ones and aftershocks | Batched on one GPU for every station on Earth at once |
| On-site warning | Each sensor warns its own location from the first seconds of P waves | Shrinks the blind zone for moderate earthquakes under cities |
| Seismic magnitude | Fast magnitude from the first seconds | Classic baseline (Phase 1), then learned, region-calibrated estimators |
| Gravity layer (Kshana) | Magnitude and growth from speed-of-light gravity signals | Trained on simulated signals with real noise; network stacking to push below magnitude 8 |
| GNSS layer | Magnitude from peak ground displacement; slip from static offsets | Real-time finite-fault inversion on GPU |
| Fibre layer | Strain-rate magnitude and detection along cables | Learned directly from raw DAS strain |
| Rupture tracker | Length, direction, slip distribution and growth of the rupture | Physics-informed: a learned model constrained by elasticity, updated every second |

### 3.3 Decide: from measurements to consequences

| Component | What it does | High-tech element |
|---|---|---|
| Fusion | One magnitude and rupture with a calibrated uncertainty | Bayesian fusion that weights each layer by its proven reliability; conformal prediction for intervals with a guaranteed coverage rate |
| Shaking forecast | Expected shaking intensity at every city | From the rupture, not a point, with local site amplification from global soil maps |
| Tsunami forecast | Arrival times, wave heights and threat levels on coasts | Precomputed scenario bank plus a GPU shallow-water solver for the corrected source, updated with ocean-bottom pressure data |
| Impact estimate | People exposed to each level of shaking within minutes | Shaking forecast combined with open population maps |
| Aftershock outlook | Probabilities of strong aftershocks in the following days | Statistical aftershock models of the kind agencies already publish; a probability, never a prediction |

### 3.4 Deliver: to agencies, never around them

- Free feeds in the international CAP alert format, plus QuakeML and a streaming API.
- Every message signed, so agencies can verify it came from Larzavan unchanged.
- Agency dashboards with the live estimate, its uncertainty and the reason behind it.
- Public research estimates and a public scorecard, clearly labelled as not an alert.

## 4. Training data: more megaquakes than nature has given us

- **Real archives:** decades of open continuous waveforms, GNSS records (such as the Ruhl et al.
  2019 global high-rate GNSS database, 3,433 recordings from 29 earthquakes) and catalogues.
- **Synthetic megaquakes:** thousands of physically realistic ruptures from magnitude 7 to 9.5,
  generated with open stochastic rupture tools (such as FakeQuakes in MudPy), with matching
  seismic, GNSS and gravity signals and real recorded noise.
- **Gravity-signal synthetics** for every station geometry Larzavan uses.
- **Fair testing:** earthquakes used to test are never used to train; held-out sets are fixed and
  published before results.
- **Versioned data:** every dataset and model has a version and a fingerprint, so any result can
  be reproduced exactly.

## 5. Performance engineering

| Target | Value to reach |
|---|---|
| Processing time per update, all open stations on Earth | under 1 second on one GPU |
| Update rate of the estimate | every second |
| First estimate after the P wave reaches the nearest stations | a few seconds |
| Bit-identical results on GPU and CPU | yes, for every published number |

Batched GPU inference, fused kernels for filtering and feature extraction, and deterministic
arithmetic, so a replay gives the same answer on any machine.

## 6. Reliability and security

- **Digital twin:** a simulated global network that replays real and synthetic earthquakes with
  realistic delays, dropped stations and faulty sensors, used to test every release.
- **Bad-data defence:** detection of clipped, dead, drifting, duplicated or spoofed streams before
  they reach the estimate.
- **Fail-safe decisions:** the alert logic is specified in writing and tested property by property;
  when the data disagree, Larzavan reports more uncertainty, never false confidence.
- **Redundancy:** independent processing in separate regions, so one outage does not stop it.

## 7. The Larzavan Benchmark, the largest open test of its kind

| Tier | Earthquakes since 2000 | What it tests |
|---|---|---|
| 0 | 44,290 (M5 to 6) | Detection speed, location, false alarms, on-site warning |
| 1 | 4,001 (M6+) | Detection, location, false alarms |
| 2 | 400 (M7+) | Magnitude speed and accuracy, shaking forecasts |
| 3 | 144 (M7.5+) | Megaquake magnitude, rupture tracking, tsunami forecasts |
| 4 | 28 (M8+) | Gravity signals |
| Live | every earthquake from launch | The public scorecard |

Every result is published second by second. Results are compared with the official real-time
estimates where those are public. The benchmark is versioned and archived with a citable
identifier, so other systems can be measured against it.

## 8. Firsts we aim for, claimed only once proven

1. The first open engine combining gravity, GNSS, seismic and fibre signals.
2. The largest open benchmark for earthquake early warning.
3. Gravity signals that work below magnitude 8.
4. Every open seismic station on Earth processed live on one GPU, in under a second.
5. Shaking forecasts from the growing rupture, worldwide, from open data.
6. Magnitude intervals with a guaranteed coverage rate.
7. An open, low-cost sensor node with on-device warning.

## 9. Roadmap

Every phase ends in something public.

1. **Proof of the problem.** Replay the 28 M8+ earthquakes with the classic method and publish
   where it falls short. *In progress.*
2. **GNSS layer.** Peak-displacement magnitude on the 29 earthquakes of the Ruhl et al. database,
   with coefficients refitted without each earthquake in turn; show how much sooner the
   magnitude becomes correct.
3. **Synthetic megaquakes.** Generate the training set of simulated ruptures and signals.
4. **Gravity layer (Kshana).** Train the model; register for free research access to Japan's NIED
   data; invite the PEGSNet authors (Géoazur, France) to collaborate.
5. **Network transformer and fusion,** with calibrated intervals.
6. **Rupture tracking, shaking forecast, tsunami forecast and impact estimate.**
7. **The full benchmark,** tiers 0 to 4.
8. **Live shadow mode, 24/7,** with a public scorecard against USGS and GFZ and no public alerts
   from Larzavan.
9. **Give it to the world.** Free signed feeds for agencies in Peru, Indonesia, the Philippines,
   Chile and Central America; UNESCO's tsunami programme; peer-reviewed papers.
10. **Grow the network.** The open sensor node, citizen seismographs, fibre and undersea-cable
    partners.

## 10. How "best" gets proven

Only by these numbers, on held-out earthquakes:

- seconds until the magnitude is within 0.3 of the final value;
- seconds of warning at the nearest cities;
- false and missed alarms in live shadow mode;
- how often the true magnitude falls inside the stated interval;
- results against official real-time estimates.

## 11. Rules

- No prediction, ever.
- No public alerts of its own.
- Every result reproducible from public code, public data and a public run.
- Uncertainty is always reported with a magnitude.
