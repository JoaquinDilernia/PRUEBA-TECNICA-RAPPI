## Contexto

Trabajas en una plataforma de delivery. El equipo de producto identificó el siguiente insight:
>*Los repartidores toman decisiones subóptimas sobre cuándo trabajar porque no entienden cómo varía su potencial de ingresos a lo largo del día."*
Cada repartidor tiene un **ingreso base** — pero eso no es lo que realmente gana. Sus ingresos reales fluctúan por factores que el repartidor no puede ver fácilmente.

---

## API CLIMA
Weather API

## El Problema

El **potencial de ingresos real** de un repartidor está afectado por al menos tres variables:

1. **Su vehículo** — el tipo impacta capacidad, velocidad y operabilidad bajo ciertas condiciones
2. **Las condiciones climáticas** — lluvia, calor, viento, nieve afectan la demanda y la eficiencia operativa
3. **La dinámica de oferta/demanda** — cuántos otros repartidores están activos en este momento y zona

Hoy, los repartidores simplemente adivinan. No saben si conectarse a las 18:00 vs las 20:00 vale la pena. No saben si la lluvia les beneficia o perjudica. No saben cómo la competencia de otros repartidores afecta su porción de la demanda.

---

## Tu Misión

Construir un **MVP** de una herramienta de asesoría que le diga al repartidor:
> *Ddo tu vehículo, tu ubicación, el clima actual y cuántos repartidores están activos ahora mismo — este es tu potencial de ingresos estimado."*

a herramienta también debe entregar una **señal clara** sobre si este es un buen momento para estar trabajando.
---

## Requerimientos

### Obligatorio (MVP)
- Elepartidor puede **configurar** su ingreso base y tipo de vehículo
- Elistema **obtiene el clima automáticamente** según la ubicación del repartidor
- Elistema **calcula el potencial de ingresos ajustado** según vehículo + clima + demanda
- Elesultado **muestra el desglose** de factores (no solo el número final)
- Laógica de cálculo está **documentada en un spec antes de escribir código**


### Fuera de Alcance
- Aunticación / login
- Ba de datos en producción (en memoria está bien)
- Pudo visual del UI

---
## Un Ejemplo Concreto (Para Orientarte)

Supón:
- Ineso base del repartidor: **$20/orden**
- Veculo: **moto**
- Cla: **lluvia**
- Rertidores activos en la zona: **60** (de un típico de 100)

Tu herramienta debería poder producir algo como:

```
eso base:             $20.00
Factor climático:         +20%  (la lluvia incrementa la demanda)
Factor de demanda:        +67%  (menos repartidores de lo usual)
─────────────────────────────────────
Ingreso estimado:         $40.08 / orden
Señal:                    ⬆ Ventana de alta oportunidad
```