"""Charts and a markdown summary of a replay run."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def event_chart(path: Path, title: str, true_magnitude: float, times: list[float], magnitudes: list[float | None]):
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.axhline(true_magnitude, color="#222222", lw=1.2, label=f"USGS magnitude {true_magnitude:.1f}")
    ax.axhspan(true_magnitude - 0.3, true_magnitude + 0.3, color="#cccccc", alpha=0.5, label="within 0.3")
    pts = [(t, m) for t, m in zip(times, magnitudes) if m is not None]
    if pts:
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color="#c0392b", lw=1.6, label="classic Pd magnitude")
    ax.set_xlabel("seconds after origin")
    ax.set_ylabel("magnitude")
    ax.set_title(title, fontsize=10)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def summary_chart(path: Path, rows: list[dict]):
    pts = [(r["true_magnitude"], r["final_estimate"]) for r in rows if r["final_estimate"] is not None]
    fig, ax = plt.subplots(figsize=(5, 5))
    if pts:
        ax.scatter([p[0] for p in pts], [p[1] for p in pts], color="#c0392b", zorder=3)
    lo, hi = 7.5, 9.3
    ax.plot([lo, hi], [lo, hi], color="#222222", lw=1, label="estimate = true magnitude")
    ax.set_xlim(lo, hi)
    ax.set_ylim(5.5, hi)
    ax.set_xlabel("USGS magnitude")
    ax.set_ylabel("classic Pd magnitude, end of replay")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def markdown_table(rows: list[dict]) -> str:
    lines = [
        "| Earthquake | USGS M | Stations | First estimate | Final estimate | Underestimate | Within 0.3 from |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:

        def fmt(v, suffix=""):
            return "–" if v is None else f"{v}{suffix}"

        first = "–" if r["first_estimate"] is None else f"{r['first_estimate']:.2f} at {r['first_estimate_s']:.0f} s"
        lines.append(
            f"| {r['date']} {r['place']} | {r['true_magnitude']:.1f} | {r['n_stations_final']} | {first} | "
            f"{fmt(r['final_estimate'])} | {fmt(r['final_error'])} | {fmt(r['time_within_tolerance_s'], ' s')} |"
        )
    return "\n".join(lines)
