"""
Punto de entrada: ejecutar benchmarks y gráficas de DaC y/o DP.
"""

from __future__ import annotations

import argparse
from pathlib import Path

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

    all_p = sub.add_parser("all", help="Ejecutar DaC y DP en secuencia.")
    all_p.add_argument("-o", "--output-dir", type=str, default=None, help=out_help)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    out = Path(args.output_dir).resolve() if args.output_dir else None

    if args.command == "dac":
        egg_drop_dac.main_cli(output_dir=str(out) if out else None)
    elif args.command == "dp":
        egg_drop_dp.main_cli(output_dir=str(out) if out else None)
    else:
        egg_drop_dac.main_cli(output_dir=str(out) if out else None)
        egg_drop_dp.main_cli(output_dir=str(out) if out else None)


if __name__ == "__main__":
    main()
