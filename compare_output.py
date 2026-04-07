"""
Gráficas comparativas DaC vs DP a partir de filas de benchmark (mismos casos de prueba).
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


def plot_dac_vs_dp_time(
    dac_rows: list[dict],
    dp_rows: list[dict],
    output_dir: Path,
    filename: str = "dac_vs_dp_timing.png",
) -> Path:
    """
    Tres paneles (2, 3 y 4 huevos): tiempo mediano (ms) vs pisos, DaC vs DP.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharey=True)
    for idx, e in enumerate((2, 3, 4)):
        ax = axes[idx]
        dac_pts = sorted(
            [(r["floors"], r["time_ms"]) for r in dac_rows if r["eggs"] == e],
            key=lambda t: t[0],
        )
        dp_pts = sorted(
            [(r["floors"], r["time_ms"]) for r in dp_rows if r["eggs"] == e],
            key=lambda t: t[0],
        )
        ax.plot(
            [p[0] for p in dac_pts],
            [p[1] for p in dac_pts],
            marker="o",
            label="DaC (recursivo, sin memo)",
            color="C0",
        )
        ax.plot(
            [p[0] for p in dp_pts],
            [p[1] for p in dp_pts],
            marker="s",
            label="DP (bottom-up)",
            color="C1",
        )
        ax.set_title(f"{e} huevos")
        ax.set_xlabel("Pisos")
        if idx == 0:
            ax.set_ylabel("Tiempo (ms), mediana")
        ax.legend(fontsize=8, loc="best")
        ax.grid(True, alpha=0.3)

    fig.suptitle("Comparación empírica: tiempo de ejecución DaC vs DP")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def plot_from_csvs(
    dac_csv: Path,
    dp_csv: Path,
    output_dir: Path,
    filename: str = "dac_vs_dp_timing.png",
) -> Path:
    """Genera la misma figura leyendo los CSV ya exportados."""
    def load(path: Path) -> list[dict]:
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    dac_raw = load(dac_csv)
    dp_raw = load(dp_csv)
    dac_rows = [
        {
            "eggs": int(r["eggs"]),
            "floors": int(r["floors"]),
            "time_ms": float(r["time_ms"]),
        }
        for r in dac_raw
    ]
    dp_rows = [
        {
            "eggs": int(r["eggs"]),
            "floors": int(r["floors"]),
            "time_ms": float(r["time_ms"]),
        }
        for r in dp_raw
    ]
    return plot_dac_vs_dp_time(dac_rows, dp_rows, output_dir, filename=filename)
