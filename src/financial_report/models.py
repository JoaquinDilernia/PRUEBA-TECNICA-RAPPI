"""Estructuras de datos compartidas entre los módulos del reporte."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ExchangeRatesSnapshot:
    """Tasas de cambio normalizadas, independientes del shape del proveedor.

    Desacopla al resto de la app de los nombres de campo específicos de
    la API (ej. `base_code` vs `base`, `time_last_update_unix` vs `date`),
    para que un cambio de proveedor solo impacte en `api_client.py`.
    """

    base: str
    rates: dict[str, float]
    source_updated_at: datetime | None


@dataclass(frozen=True)
class CurrencyRow:
    """Una fila del reporte: una moneda LATAM con su valor y variación del día."""

    moneda: str
    valor: float
    variacion: float
    fecha: str

    def to_dict(self) -> dict[str, str | float]:
        return {
            "moneda": self.moneda,
            "valor": round(self.valor, 4),
            "variacion": round(self.variacion, 6),
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CurrencyRow":
        return cls(
            moneda=data["moneda"],
            valor=float(data["valor"]),
            variacion=float(data["variacion"]),
            fecha=data["fecha"],
        )


@dataclass(frozen=True)
class RunResult:
    """Resultado completo de una corrida del reporte."""

    source: str  # "live" o "fallback"
    rows: list[CurrencyRow]
    most_devalued: CurrencyRow
    most_stable: CurrencyRow
    csv_path: str
    timestamp: str
