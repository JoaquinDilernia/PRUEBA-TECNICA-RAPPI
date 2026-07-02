function formatPorcentaje(valor) {
  const signo = valor >= 0 ? '+' : ''
  return `${signo}${(valor * 100).toFixed(0)}%`
}

function formatMoneda(valor) {
  return `$${valor.toFixed(2)}`
}

const CATEGORIA_LABELS = {
  despejado: 'Despejado',
  lluvia: 'Lluvia',
  tormenta_nieve: 'Tormenta / nieve',
  viento_fuerte: 'Viento fuerte',
  calor_extremo: 'Calor extremo',
  frio_extremo: 'Frío extremo',
}

const NIVEL_LABELS = {
  alta: 'Alta demanda',
  media: 'Demanda media',
  baja: 'Baja demanda',
}

export default function DesglosePotencial({ resultado }) {
  const { clima, demanda } = resultado

  return (
    <div className="desglose">
      <div className="linea">
        <span>Ingreso base</span>
        <span>{formatMoneda(resultado.ingreso_base)}</span>
      </div>

      <div className="linea">
        <span>
          Factor climático — {CATEGORIA_LABELS[clima.categoria] ?? clima.categoria} (
          {clima.condition_text}, {clima.temp_c}°C)
        </span>
        <span>{formatPorcentaje(clima.factor_climatico)}</span>
      </div>

      <div className="linea">
        <span>
          Factor de demanda — {NIVEL_LABELS[demanda.nivel] ?? demanda.nivel} ({demanda.activos} de un
          típico de {demanda.tipico})
        </span>
        <span>{formatPorcentaje(demanda.factor_demanda)}</span>
      </div>

      <hr />

      <div className="linea linea-total">
        <span>Ingreso estimado</span>
        <span>{formatMoneda(resultado.ingreso_estimado)} / orden</span>
      </div>

      <div className="señal">{resultado.señal}</div>
    </div>
  )
}
