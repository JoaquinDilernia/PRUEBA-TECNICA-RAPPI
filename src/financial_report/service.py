"""Orquesta una corrida completa del reporte financiero LATAM.

Usado tanto por el CLI como por la API web, para que ambas interfaces
compartan exactamente la misma lógica de negocio.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from financial_report.analysis import most_devalued, most_stable
from financial_report.api_client import ExchangeAPIError, fetch_rates
from financial_report.console import print_summary
from financial_report.currencies import LATAM_CURRENCIES
from financial_report.history import DEFAULT_HISTORY_PATH, append_run, get_last_rates
from financial_report.models import RunResult
from financial_report.report import build_rows, write_csv

DEFAULT_REPORTS_DIR = Path("data/reports")


def run_report(
    history_path: Path = DEFAULT_HISTORY_PATH,
    reports_dir: Path = DEFAULT_REPORTS_DIR,
) -> RunResult:
    """Ejecuta el flujo completo: obtener tasas (o fallback), simular, reportar y persistir."""
    now = datetime.now()
    fecha = now.strftime("%Y-%m-%d")
    timestamp = now.isoformat(timespec="seconds")

    try:
        rates = fetch_rates()
        source = "live"
    except ExchangeAPIError as exc:
        fallback_rates = get_last_rates(history_path)
        if fallback_rates is None:
            raise ExchangeAPIError(
                f"La API falló y no hay historial previo para usar como fallback: {exc}"
            ) from exc
        rates = fallback_rates
        source = "fallback"

    rows = build_rows(rates, fecha)
    if not rows:
        raise ExchangeAPIError("Ninguna moneda LATAM está presente en las tasas obtenidas")

    devalued = most_devalued(rows)
    stable = most_stable(rows)

    print_summary(rows, devalued, stable, source)

    csv_filename = f"reporte_{now.strftime('%Y%m%d_%H%M%S')}.csv"
    csv_path = write_csv(rows, reports_dir / csv_filename).as_posix()

    latam_rates_used = {code: rates[code] for code in LATAM_CURRENCIES if code in rates}
    append_run(
        {
            "timestamp": timestamp,
            "fecha": fecha,
            "source": source,
            "rates": latam_rates_used,
            "rows": [row.to_dict() for row in rows],
            "csv_path": str(csv_path),
        },
        history_path,
    )

    return RunResult(
        source=source,
        rows=rows,
        most_devalued=devalued,
        most_stable=stable,
        csv_path=str(csv_path),
        timestamp=timestamp,
    )
