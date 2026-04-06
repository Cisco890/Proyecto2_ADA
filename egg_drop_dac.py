"""
Egg Dropping: enfoque recursivo tipo Divide and Conquer SIN memoización.

La recurrencia descompone el problema en subproblemas más pequejos (menos huevos
o menos pisos), pero los mismos pares (e, f) pueden aparecer muchas veces, por
lo que hay subproblemas traslapados; esta versión los recalcula a propósito para
contrastar con la solución por programación dinámica.
"""

from __future__ import annotations

import csv
import os
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt

from test_cases import TEST_CASES

# Directorio por defecto para CSV y figuras
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def egg_drop_dac(eggs: int, floors: int) -> tuple[int, int]:
    """
    Mínimo de intentos en el peor caso con `eggs` huevos y `floors` pisos.
    Retorna (resultado_óptimo, número_de_llamadas_recursivas_a_solve).
    Sin memoización ni caché.
    """
    calls = [0]

    def solve(e: int, f: int) -> int:
        calls[0] += 1
        # 0 o 1 pisos: respuesta directa
        if f == 0:
            return 0
        if f == 1:
            return 1
        # Un solo huevo: hay que subir piso a piso en el peor caso
        if e == 1:
            return f

        best = floors + 1  # cota superior trivial
        for x in range(1, f + 1):
            # Rompe en x: subproblema (e-1, x-1). No rompe: (e, f-x)
            worst = 1 + max(solve(e - 1, x - 1), solve(e, f - x))
            if worst < best:
                best = worst
        return best

    result = solve(eggs, floors)
    return result, calls[0]


def run_benchmark(
    repetitions: int = 7,
    output_dir: Path | None = None,
    csv_name: str = "dac_results.csv",
) -> list[dict]:
    """
    Ejecuta todos los TEST_CASES varias veces; reporta mediana de tiempo (ns).
    Incluye una corrida de calentamiento por caso antes de medir.
    """
    output_dir = output_dir or DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    for eggs, floors in TEST_CASES:
        # Calentamiento (descarta tiempo de arranque de Python/interpreter en la primera pasada)
        egg_drop_dac(eggs, floors)

        times_ns: list[int] = []
        last_calls = 0
        optimal = 0
        for _ in range(repetitions):
            t0 = time.perf_counter_ns()
            optimal, last_calls = egg_drop_dac(eggs, floors)
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
                "recursive_calls": last_calls,
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
                "recursive_calls",
            ],
        )
        w.writeheader()
        w.writerows(rows)

    return rows


def plot_results(rows: list[dict], output_dir: Path | None = None) -> None:
    """
    Gráfica: eje X = pisos, eje Y = tiempo (ms), series por número de huevos (2, 3, 4).
    Gráfica adicional: llamadas recursivas vs pisos.
    """
    output_dir = output_dir or DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    by_eggs: dict[int, list[tuple[int, float, int]]] = {2: [], 3: [], 4: []}
    for r in rows:
        e = r["eggs"]
        by_eggs[e].append((r["floors"], r["time_ms"], r["recursive_calls"]))

    fig, ax = plt.subplots(figsize=(9, 5))
    for e in (2, 3, 4):
        pts = sorted(by_eggs[e], key=lambda t: t[0])
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.plot(xs, ys, marker="o", label=f"{e} huevos")
    ax.set_xlabel("Pisos")
    ax.set_ylabel("Tiempo (ms), mediana")
    ax.set_title("Egg Dropping (DaC recursivo, sin memoización)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "dac_timing.png", dpi=150)
    plt.close(fig)

    fig2, ax2 = plt.subplots(figsize=(9, 5))
    for e in (2, 3, 4):
        pts = sorted(by_eggs[e], key=lambda t: t[0])
        xs = [p[0] for p in pts]
        ys = [p[2] for p in pts]
        ax2.plot(xs, ys, marker="s", label=f"{e} huevos")
    ax2.set_xlabel("Pisos")
    ax2.set_ylabel("Llamadas recursivas")
    ax2.set_title("Egg Dropping DaC: volumen de llamadas recursivas")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    fig2.tight_layout()
    fig2.savefig(output_dir / "dac_recursive_calls.png", dpi=150)
    plt.close(fig2)


def main_cli(output_dir: str | None = None) -> None:
    out = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    rows = run_benchmark(output_dir=out)
    plot_results(rows, output_dir=out)
    print(f"DaC: CSV -> {out / 'dac_results.csv'}")
    print(f"DaC: figuras -> {out / 'dac_timing.png'}, {out / 'dac_recursive_calls.png'}")


if __name__ == "__main__":
    main_cli()
