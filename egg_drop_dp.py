"""
Egg Dropping: programación dinámica bottom-up con tabla dp[e][f].

Evita recomputar subproblemas guardando resultados de estados ya resueltos;
complejidad polinomial frente al explosivo árbol de recursión sin memoización.
"""

from __future__ import annotations

import csv
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt

from test_cases import TEST_CASES

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def egg_drop_dp(eggs: int, floors: int) -> tuple[int, int]:
    """
    dp[e][f] = mínimo de intentos en el peor caso con e huevos y f pisos.

    Casos base en la tabla:
    - f == 0: 0 intentos
    - f == 1: 1 intento (cualquier e >= 1)
    - e == 1: f intentos (probar cada piso)

    Transición: para cada piso de prueba x en 1..f,
    peor caso = 1 + max(dp[e-1][x-1], dp[e][f-x]); minimizar sobre x.

    Retorna (resultado_óptimo, número de evaluaciones de transición en el bucle interno).
    """
    if floors == 0:
        return 0, 0
    if eggs == 0:
        return 0, 0

    # dp[i][j]: i huevos, j pisos
    dp = [[0] * (floors + 1) for _ in range(eggs + 1)]
    operations = 0

    for j in range(1, floors + 1):
        dp[1][j] = j

    for i in range(2, eggs + 1):
        dp[i][0] = 0
        dp[i][1] = 1
        for j in range(2, floors + 1):
            best = j + 1
            for x in range(1, j + 1):
                operations += 1
                worst = 1 + max(dp[i - 1][x - 1], dp[i][j - x])
                if worst < best:
                    best = worst
            dp[i][j] = best

    return dp[eggs][floors], operations


def run_benchmark(
    repetitions: int = 7,
    output_dir: Path | None = None,
    csv_name: str = "dp_results.csv",
) -> list[dict]:
    output_dir = output_dir or DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    for eggs, floors in TEST_CASES:
        egg_drop_dp(eggs, floors)

        times_ns: list[int] = []
        last_ops = 0
        optimal = 0
        for _ in range(repetitions):
            t0 = time.perf_counter_ns()
            optimal, last_ops = egg_drop_dp(eggs, floors)
            t1 = time.perf_counter_ns()
            times_ns.append(t1 - t0)

        med_ns = int(statistics.median(times_ns))
        rows.append(
            {
                "eggs": eggs,
                "floors": floors,
                "optimal_trials": optimal,
                "time_ns": med_ns,
                "time_ms": med_ns / 1_000_000.0,
                "dp_operations": last_ops,
            }
        )

    csv_path = output_dir / csv_name
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "eggs",
                "floors",
                "optimal_trials",
                "time_ns",
                "time_ms",
                "dp_operations",
            ],
        )
        w.writeheader()
        w.writerows(rows)

    return rows


def plot_results(rows: list[dict], output_dir: Path | None = None) -> None:
    output_dir = output_dir or DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    by_eggs: dict[int, list[tuple[int, float, int]]] = {2: [], 3: [], 4: []}
    for r in rows:
        e = r["eggs"]
        by_eggs[e].append((r["floors"], r["time_ms"], r["dp_operations"]))

    fig, ax = plt.subplots(figsize=(9, 5))
    for e in (2, 3, 4):
        pts = sorted(by_eggs[e], key=lambda t: t[0])
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.plot(xs, ys, marker="o", label=f"{e} huevos")
    ax.set_xlabel("Pisos")
    ax.set_ylabel("Tiempo (ms), mediana")
    ax.set_title("Egg Dropping (programación dinámica bottom-up)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "dp_timing.png", dpi=150)
    plt.close(fig)

    fig2, ax2 = plt.subplots(figsize=(9, 5))
    for e in (2, 3, 4):
        pts = sorted(by_eggs[e], key=lambda t: t[0])
        xs = [p[0] for p in pts]
        ys = [p[2] for p in pts]
        ax2.plot(xs, ys, marker="s", label=f"{e} huevos")
    ax2.set_xlabel("Pisos")
    ax2.set_ylabel("Operaciones DP (transiciones evaluadas)")
    ax2.set_title("Egg Dropping DP: conteo de operaciones")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    fig2.tight_layout()
    fig2.savefig(output_dir / "dp_operations.png", dpi=150)
    plt.close(fig2)


def main_cli(output_dir: str | None = None) -> None:
    out = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    rows = run_benchmark(output_dir=out)
    plot_results(rows, output_dir=out)
    print(f"DP: CSV -> {out / 'dp_results.csv'}")
    print(f"DP: figuras -> {out / 'dp_timing.png'}, {out / 'dp_operations.png'}")


if __name__ == "__main__":
    main_cli()
