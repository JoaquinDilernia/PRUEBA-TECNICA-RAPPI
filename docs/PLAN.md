# Plan — Reporte Financiero LATAM

## Enunciado (resumen)
Sistema de automatización financiera que:
1. Se conecta a `https://api.exchangerate-api.com/v4/latest/USD`.
2. Filtra monedas LATAM: ARS, BRL, CLP, COP, MXN, PEN, UYU.
3. Simula variación diaria random entre -2% y +2% por moneda.
4. Genera un CSV con: moneda, valor, variación, fecha.
5. Muestra en consola: moneda más devaluada, moneda más estable, tabla completa.
6. Guarda historial de ejecuciones en JSON local.
7. Bonus: si la API falla, usa como fallback la última corrida guardada en el historial.

## Decisiones de diseño

- **Definición de métricas**: "más devaluada" = variación más negativa (mínimo). "Más estable" = variación con menor valor absoluto (más cercana a 0).
- **`valor` del CSV**: tasa USD→moneda obtenida de la API, ajustada por la variación simulada: `valor = rate * (1 + variacion)`. La `variacion` queda además como columna separada en %.
- **Fallback**: cualquier error de red, timeout o respuesta de error/JSON inválido (tras reintentos) dispara el fallback a la última entrada de `data/history.json`, reusando esas tasas base para simular una nueva variación del día. Si no hay historial previo y la API falla, se informa el error explícitamente (no hay con qué generar el reporte) y el CLI termina con exit code 1.
- **Gestión de dependencias**: `uv` (ya configurado en el entorno) en lugar de pip/venv manual — más rápido, `pyproject.toml` como fuente de verdad.
- **Interfaz**: además del requisito literal de consola, se agrega una interfaz web local simple (FastAPI + HTML/CSS/JS vanilla, sin build step) para poder demostrar el flujo de forma visual. La lógica de negocio vive en módulos puros de Python, independientes de CLI y web, para que ambas interfaces reutilicen el mismo core y sea testeable sin necesidad de levantar un server.
- **Proveedor de tipos de cambio**: se usa el endpoint abierto v6 (`https://open.er-api.com/v6/latest/USD`, sin API key) en lugar del v4 legacy del enunciado original (`api.exchangerate-api.com/v4`), que la propia API marca como deprecado (`WARNING_UPGRADE_TO_V6`). El shape de la respuesta es distinto (`result`, `base_code`, `time_last_update_unix`, etc.), por lo que `api_client.fetch_rates()` normaliza todo a un `ExchangeRatesSnapshot` propio — si el proveedor cambia de nuevo, solo se toca ese módulo.
- **Configuración centralizada** en `config.py`, sobreescribible por variables de entorno (`EXCHANGE_RATE_API_URL`, timeouts, reintentos, directorio de datos) para no hardcodear valores en cada módulo y facilitar correr en distintos entornos.
- **Resiliencia de red**: `api_client` reintenta automáticamente (backoff exponencial) ante timeouts o errores 5xx antes de propagar el fallo al `service`, que recién ahí recurre al fallback del historial.
- **Observabilidad**: se usa `logging` (a stderr) para warnings/errores internos (fallos de API, uso de fallback), separado del resumen de negocio que imprime `console.py` (a stdout) — así no se mezclan logs técnicos con el resultado que pide el enunciado.
- **Historial**: además de las filas del reporte, cada corrida guarda `source` (`live`/`fallback`) y `source_updated_at` (cuándo el proveedor actualizó esas tasas), visible también en el resumen de consola.

## Arquitectura

```
src/financial_report/
├── currencies.py     # constante LATAM_CURRENCIES
├── api_client.py     # fetch_rates(): llama a la API, lanza ExchangeAPIError en fallos
├── simulator.py      # random_variation(), apply_variation()
├── analysis.py       # most_devalued(), most_stable()
├── history.py        # load_history(), append_run(), get_last_run()
├── report.py         # build_rows(), write_csv()
├── console.py        # print_summary(): imprime resumen + tabla
├── service.py        # run_report(): orquesta todo el flujo (fetch → filtrar → simular → analizar → csv → consola → historial)
├── cli.py             # entry point: `python -m financial_report.cli`
└── web/
    ├── app.py         # FastAPI: GET / , POST /api/run , GET /api/history , GET /api/latest
    └── static/        # index.html, styles.css, app.js

data/
├── history.json       # historial de corridas (fecha, fuente live/fallback, filas, ruta del csv)
└── reports/           # CSVs generados por corrida

tests/                 # pytest, cubre módulos core + service (con API mockeada)
```

## Flujo de una corrida (`service.run_report`)

1. Intentar `api_client.fetch_rates()`.
   - Éxito → `source = "live"`.
   - Falla → buscar `history.get_last_run()`. Si existe, `source = "fallback"` y se reusan esas tasas. Si no existe, se propaga el error.
2. Filtrar solo `LATAM_CURRENCIES`.
3. Por cada moneda: generar variación random (-2%, +2%) y calcular `valor`.
4. Armar filas `{moneda, valor, variacion, fecha}`.
5. Calcular más devaluada / más estable.
6. Imprimir resumen en consola (se ve tanto en CLI como en la consola donde corre el server web).
7. Escribir CSV en `data/reports/`.
8. Agregar la corrida a `data/history.json`.
9. Devolver un resultado estructurado (usado por CLI y por la API).

## Cómo se ejecuta

- CLI: `uv run python -m financial_report.cli`
- Web: `uv run uvicorn financial_report.web.app:app --reload` → abrir `http://localhost:8000`
- Tests: `uv run pytest`
