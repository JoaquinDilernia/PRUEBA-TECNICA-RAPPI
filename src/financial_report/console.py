"""Resumen del reporte impreso en consola."""

from __future__ import annotations

from financial_report.currencies import LATAM_CURRENCIES
from financial_report.models import CurrencyRow


def _format_pct(variation: float) -> str:
    sign = "+" if variation >= 0 else ""
    return f"{sign}{variation * 100:.2f}%"


def print_summary(
    rows: list[CurrencyRow],
    devalued: CurrencyRow,
    stable: CurrencyRow,
    source: str,
) -> None:
    """Imprime el resumen del día: moneda más devaluada, más estable y la tabla completa."""
    origin_label = "datos en vivo" if source == "live" else "fallback (último historial guardado)"
    print()
    print(f"=== Reporte Financiero LATAM — fuente: {origin_label} ===")
    print()
    print(f"Moneda más devaluada del día: {devalued.moneda} ({_format_pct(devalued.variacion)})")
    print(f"Moneda más estable del día:   {stable.moneda} ({_format_pct(stable.variacion)})")
    print()

    header = f"{'Moneda':<8}{'Nombre':<22}{'Valor (USD)':<15}{'Variación':<12}{'Fecha':<12}"
    print(header)
    print("-" * len(header))
    for row in sorted(rows, key=lambda r: r.moneda):
        nombre = LATAM_CURRENCIES.get(row.moneda, "")
        print(
            f"{row.moneda:<8}{nombre:<22}{row.valor:<15.4f}{_format_pct(row.variacion):<12}{row.fecha:<12}"
        )
    print()
