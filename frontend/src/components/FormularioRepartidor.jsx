import { useState } from 'react'

const VEHICULOS = [
  { value: 'moto', label: 'Moto' },
  { value: 'bici', label: 'Bici' },
  { value: 'auto', label: 'Auto' },
]

export default function FormularioRepartidor({ onSubmit, cargando }) {
  const [ingresoBase, setIngresoBase] = useState('20')
  const [vehiculo, setVehiculo] = useState('moto')
  const [lat, setLat] = useState('-34.6037')
  const [lon, setLon] = useState('-58.3816')

  function handleSubmit(event) {
    event.preventDefault()
    onSubmit({
      ingresoBase: Number(ingresoBase),
      vehiculo,
      lat: Number(lat),
      lon: Number(lon),
    })
  }

  return (
    <form className="formulario" onSubmit={handleSubmit}>
      <label>
        Ingreso base ($/orden)
        <input
          type="number"
          min="0"
          step="0.01"
          value={ingresoBase}
          onChange={(e) => setIngresoBase(e.target.value)}
          required
        />
      </label>

      <label>
        Vehículo
        <select value={vehiculo} onChange={(e) => setVehiculo(e.target.value)}>
          {VEHICULOS.map((v) => (
            <option key={v.value} value={v.value}>
              {v.label}
            </option>
          ))}
        </select>
      </label>

      <div className="fila-coordenadas">
        <label>
          Latitud
          <input
            type="text"
            inputMode="decimal"
            value={lat}
            onChange={(e) => setLat(e.target.value)}
            required
          />
        </label>

        <label>
          Longitud
          <input
            type="text"
            inputMode="decimal"
            value={lon}
            onChange={(e) => setLon(e.target.value)}
            required
          />
        </label>
      </div>

      <button type="submit" disabled={cargando}>
        {cargando ? 'Calculando…' : 'Calcular potencial de ingresos'}
      </button>
    </form>
  )
}
