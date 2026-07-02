const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function calcularPotencialIngresos({ ingresoBase, vehiculo, lat, lon }) {
  const response = await fetch(`${API_URL}/potencial-ingresos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ingreso_base: ingresoBase,
      vehiculo,
      lat,
      lon,
    }),
  })

  if (!response.ok) {
    const detalle = await response.json().catch(() => null)
    throw new Error(detalle?.detail ? JSON.stringify(detalle.detail) : `Error ${response.status}`)
  }

  return response.json()
}
