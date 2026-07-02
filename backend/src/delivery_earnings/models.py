from enum import Enum

from pydantic import BaseModel, Field


class Vehiculo(str, Enum):
    moto = "moto"
    bici = "bici"
    auto = "auto"


class PotencialIngresosRequest(BaseModel):
    ingreso_base: float = Field(gt=0)
    vehiculo: Vehiculo
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)


class ClimaDesglose(BaseModel):
    categoria: str
    condition_text: str
    temp_c: float
    demand_shift: float
    operability_mod: float
    factor_climatico: float


class DemandaDesglose(BaseModel):
    nivel: str
    activos: int
    tipico: int
    factor_demanda: float


class PotencialIngresosResponse(BaseModel):
    ingreso_base: float
    vehiculo: Vehiculo
    clima: ClimaDesglose
    demanda: DemandaDesglose
    ingreso_estimado: float
    multiplicador_total: float
    señal: str
