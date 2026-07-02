# Spec: Cálculo de Potencial de Ingresos

Este documento define la lógica de cálculo **antes** de implementarla, según lo pedido en `info.md`.

## 1. Entradas

| Campo | Tipo | Descripción |
|---|---|---|
| `ingreso_base` | float | Ingreso base por orden configurado por el repartidor ($/orden) |
| `vehiculo` | enum | `moto` \| `bici` \| `auto` |
| `lat`, `lon` | float | Ubicación del repartidor (texto libre en el form, se valida como coordenadas) |

## 2. Clima (WeatherAPI.com)

Se consulta `GET https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={lat},{lon}` y se extrae:
- `condition.text` (texto de condición, ej. "Rain", "Snow", "Clear")
- `temp_c`
- `wind_kph`
- `precip_mm`

### 2.1 Clasificación en categorías climáticas

Se evalúa en este orden de prioridad (la primera que matchee gana):

| Categoría | Condición de detección |
|---|---|
| `tormenta_nieve` | `condition.text` contiene "snow", "sleet", "blizzard", "thunder" o `precip_mm > 10` |
| `lluvia` | `condition.text` contiene "rain", "drizzle", "shower" o `precip_mm > 0.5` |
| `viento_fuerte` | `wind_kph > 40` (y no cae en las anteriores) |
| `calor_extremo` | `temp_c > 35` |
| `frio_extremo` | `temp_c < 5` |
| `despejado` | cualquier otro caso (baseline) |

### 2.2 Demand shift base por categoría (efecto sobre demanda de pedidos, aplica a todos los vehículos)

| Categoría | demand_shift |
|---|---|
| despejado | 0% |
| lluvia | +20% |
| tormenta_nieve | +30% |
| viento_fuerte | +10% |
| calor_extremo | +10% |
| frio_extremo | +15% |

### 2.3 Modificador de operatividad por vehículo (capacidad/velocidad bajo esa condición)

| Categoría | moto | bici | auto |
|---|---|---|---|
| despejado | 0% | 0% | 0% |
| lluvia | 0% | -10% | +5% |
| tormenta_nieve | -25% | -40% | -10% |
| viento_fuerte | -10% | -20% | 0% |
| calor_extremo | -15% | -15% | -5% |
| frio_extremo | -10% | -20% | 0% |

### 2.4 Factor climático final

```
factor_climatico = demand_shift(categoria) + operability_mod(vehiculo, categoria)
```

Ejemplo de validación (del `info.md`): moto + lluvia → `0.20 + 0.00 = +20%` ✅ coincide con el ejemplo dado.

## 3. Demanda (simulada, sin datos reales)

No hay fuente real de "repartidores activos", así que se simula un nivel de demanda al azar en cada request, dentro de 3 niveles:

| Nivel | Probabilidad | Ratio activos/típico (se sortea uniforme dentro del rango) |
|---|---|---|
| `alta` (pocos repartidores activos) | 33% | activos = 55%–80% del típico |
| `media` | 34% | activos = 90%–110% del típico |
| `baja` (saturación) | 33% | activos = 120%–170% del típico |

Se fija `típico = 100` (constante del MVP, representa la oferta de referencia de la zona).
Se sortea `activos` dentro del rango del nivel elegido, y:

```
factor_demanda = (típico / activos) - 1
```

Esto reproduce el ejemplo del info.md: activos=60, típico=100 → `100/60 - 1 = +67%`.

## 4. Fórmula final de ingreso ajustado

```
ingreso_ajustado = ingreso_base × (1 + factor_climatico) × (1 + factor_demanda)
```

Validación con el ejemplo: `20 × 1.20 × 1.67 = 40.08` ✅ coincide exactamente con el info.md.

## 5. Señal de oportunidad

Se calcula sobre el multiplicador total `M = (1 + factor_climatico) × (1 + factor_demanda)`:

| Rango de M | Señal |
|---|---|
| M ≥ 1.5 | ⬆ Ventana de alta oportunidad |
| 1.1 ≤ M < 1.5 | ↗ Buen momento para conectarte |
| 0.9 ≤ M < 1.1 | → Momento neutro |
| M < 0.9 | ↓ Baja oportunidad, considera esperar |

## 6. Respuesta del endpoint (desglose completo)

```json
{
  "ingreso_base": 20.0,
  "vehiculo": "moto",
  "clima": {
    "categoria": "lluvia",
    "condition_text": "Patchy rain nearby",
    "temp_c": 18.0,
    "demand_shift": 0.20,
    "operability_mod": 0.0,
    "factor_climatico": 0.20
  },
  "demanda": {
    "nivel": "alta",
    "activos": 60,
    "tipico": 100,
    "factor_demanda": 0.67
  },
  "ingreso_estimado": 40.08,
  "multiplicador_total": 2.004,
  "señal": "⬆ Ventana de alta oportunidad"
}
```

## 7. Fuera de alcance (según info.md)
- Autenticación/login
- Persistencia en base de datos real (todo en memoria/stateless por request)
- Pulido visual del frontend
