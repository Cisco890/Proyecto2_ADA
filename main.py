"""
Punto de entrada: ejecutar benchmarks y gráficas de DaC y/o DP.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import compare_output
import egg_drop_dac
import egg_drop_dp


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Egg Dropping: Divide and Conquer (recursivo) vs Programación Dinámica.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    out_help = "Carpeta para CSV e imágenes (por defecto: ./outputs en la raíz del proyecto)"

    dac_p = sub.add_parser(
        "dac",
        help="Solo algoritmo recursivo DaC (sin memoización): CSV + gráficas.",
    )
    dac_p.add_argument("-o", "--output-dir", type=str, default=None, help=out_help)

    dp_p = sub.add_parser(
        "dp",
        help="Solo programación dinámica bottom-up: CSV + gráficas.",
    )
    dp_p.add_argument("-o", "--output-dir", type=str, default=None, help=out_help)

    all_p = sub.add_parser(
        "all",
        help="Ejecutar DaC y DP, gráficas individuales y comparativa de tiempos.",
    )
    all_p.add_argument("-o", "--output-dir", type=str, default=None, help=out_help)

    cmp_p = sub.add_parser(
        "compare",
        help="Solo gráfica comparativa a partir de dac_results.csv y dp_results.csv (misma carpeta).",
    )
    cmp_p.add_argument("-o", "--output-dir", type=str, default=None, help=out_help)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    out = Path(args.output_dir).resolve() if args.output_dir else None

    if args.command == "dac":
        egg_drop_dac.main_cli(output_dir=str(out) if out else None)
    elif args.command == "dp":
        egg_drop_dp.main_cli(output_dir=str(out) if out else None)
    elif args.command == "compare":
        out_path = out.resolve() if out else Path(egg_drop_dac.DEFAULT_OUTPUT_DIR)
        dac_csv = out_path / "dac_results.csv"
        dp_csv = out_path / "dp_results.csv"
        if not dac_csv.is_file() or not dp_csv.is_file():
            print(
                "Faltan CSV: ejecuta antes `python main.py all` (o dac y dp) en la misma carpeta.",
                file=sys.stderr,
            )
            sys.exit(1)
        p = compare_output.plot_from_csvs(dac_csv, dp_csv, out_path)
        print(f"Comparativa -> {p}")
    else:
        out_path = out.resolve() if out else Path(egg_drop_dac.DEFAULT_OUTPUT_DIR)
        out_path.mkdir(parents=True, exist_ok=True)

        dac_rows = egg_drop_dac.run_benchmark(output_dir=out_path)
        egg_drop_dac.plot_results(dac_rows, output_dir=out_path)
        print(f"DaC: CSV -> {out_path / 'dac_results.csv'}")
        print(
            f"DaC: figuras -> {out_path / 'dac_timing.png'}, "
            f"{out_path / 'dac_recursive_calls.png'}"
        )

        dp_rows = egg_drop_dp.run_benchmark(output_dir=out_path)
        egg_drop_dp.plot_results(dp_rows, output_dir=out_path)
        print(f"DP: CSV -> {out_path / 'dp_results.csv'}")
        print(
            f"DP: figuras -> {out_path / 'dp_timing.png'}, "
            f"{out_path / 'dp_operations.png'}"
        )

        cmp_path = compare_output.plot_dac_vs_dp_time(dac_rows, dp_rows, out_path)
        print(f"Comparativa -> {cmp_path}")


if __name__ == "__main__":
    main()
