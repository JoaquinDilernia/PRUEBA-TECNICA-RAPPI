from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .calculator import compute_ingreso_estimado, compute_señal
from .demand import simulate_demand
from .models import (
    ClimaDesglose,
    DemandaDesglose,
    PotencialIngresosRequest,
    PotencialIngresosResponse,
)
from .weather import classify_weather, compute_factor_climatico, fetch_current_weather

app = FastAPI(title="Potencial de Ingresos - Repartidores")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/potencial-ingresos", response_model=PotencialIngresosResponse)
async def potencial_ingresos(request: PotencialIngresosRequest) -> PotencialIngresosResponse:
    raw = await fetch_current_weather(request.lat, request.lon)
    current = raw["current"]
    condition_text = current["condition"]["text"]
    temp_c = current["temp_c"]

    categoria = classify_weather(
        condition_text=condition_text,
        temp_c=temp_c,
        wind_kph=current["wind_kph"],
        precip_mm=current["precip_mm"],
    )
    demand_shift, operability_mod, factor_climatico = compute_factor_climatico(
        categoria, request.vehiculo
    )

    nivel, activos, factor_demanda = simulate_demand()

    ingreso_estimado, multiplicador_total = compute_ingreso_estimado(
        request.ingreso_base, factor_climatico, factor_demanda
    )
    señal = compute_señal(multiplicador_total)

    return PotencialIngresosResponse(
        ingreso_base=request.ingreso_base,
        vehiculo=request.vehiculo,
        clima=ClimaDesglose(
            categoria=categoria,
            condition_text=condition_text,
            temp_c=temp_c,
            demand_shift=demand_shift,
            operability_mod=operability_mod,
            factor_climatico=factor_climatico,
        ),
        demanda=DemandaDesglose(
            nivel=nivel,
            activos=activos,
            tipico=100,
            factor_demanda=factor_demanda,
        ),
        ingreso_estimado=round(ingreso_estimado, 2),
        multiplicador_total=round(multiplicador_total, 4),
        señal=señal,
    )
