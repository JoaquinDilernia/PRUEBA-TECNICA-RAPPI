# Potencial de Ingresos — Repartidores

MVP que le muestra a un repartidor su potencial de ingresos ajustado según su vehículo,
el clima actual de su ubicación y la dinámica de oferta/demanda simulada, con el
desglose completo de factores y una señal de oportunidad.

- Contexto del desafío: [`info.md`](info.md)
- Spec de la lógica de cálculo (escrita antes de codear): [`docs/SPEC.md`](docs/SPEC.md)

## Estructura

- `backend/` — API FastAPI (Python, gestionado con `uv`)
- `frontend/` — React + Vite (JSX/CSS)

## Cómo correrlo

### Backend

```bash
cd backend
uv run uvicorn delivery_earnings.api:app --app-dir src --port 8000
```

Requiere `WEATHER_API_KEY` en un `.env` en la raíz del repo (WeatherAPI.com).

Tests: `cd backend && uv run pytest`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Sirve en `http://localhost:5173` y consume el backend en `http://localhost:8000`
(configurable con `VITE_API_URL`).

## Fuera de alcance (según el enunciado)

Autenticación/login, base de datos en producción, pulido visual del UI.
