import { useState } from 'react'
import './App.css'
import { calcularPotencialIngresos } from './api'
import DesglosePotencial from './components/DesglosePotencial'
import FormularioRepartidor from './components/FormularioRepartidor'

export default function App() {
  const [resultado, setResultado] = useState(null)
  const [error, setError] = useState(null)
  const [cargando, setCargando] = useState(false)

  async function handleSubmit(datos) {
    setCargando(true)
    setError(null)
    setResultado(null)
    try {
      const data = await calcularPotencialIngresos(datos)
      setResultado(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setCargando(false)
    }
  }

  return (
    <main className="app">
      <h1>Potencial de ingresos</h1>
      <p className="subtitulo">
        Según tu vehículo, tu ubicación, el clima actual y cuántos repartidores están activos ahora
        mismo.
      </p>

      <FormularioRepartidor onSubmit={handleSubmit} cargando={cargando} />

      {error && <p className="error">Ocurrió un error: {error}</p>}
      {resultado && <DesglosePotencial resultado={resultado} />}
    </main>
  )
}
