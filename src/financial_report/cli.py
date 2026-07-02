"""Entry point de línea de comandos: `python -m financial_report.cli`."""

from __future__ import annotations

import logging
import sys

from financial_report.api_client import ExchangeAPIError
from financial_report.service import run_report


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    try:
        run_report()
    except ExchangeAPIError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
