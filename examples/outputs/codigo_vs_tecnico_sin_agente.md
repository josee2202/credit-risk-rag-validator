# Código vs Técnico

- Referencia: tecnico_banco_ficticio.docx
- Documento validado: codigo_pd_ficticio.sas
- Fragmentos analizados: 4 · tiempo total: 103 s

## Fragmento 1

**Fragmento validado:**

> Respuestas generadas por el agente
> 
> Consulta 1:
> 
> **Bloque de código SAS**

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `tecnico_banco_ficticio.docx · 0.634` — Documento técnico de implementación del modelo de PD de hipotecas - Banco Ficticio S.A.  Documento ficticio redactado para demostrar el sistema. Describe la implementación en SAS.  1. Fuentes de datos  Las operaciones se…
- `tecnico_banco_ficticio.docx · 0.587` — 6. Ajustes manuales  La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones.  7. Escenarios macroeconómicos  La PD prospectiva se calcula con tres escenarios (base, adve…
- `tecnico_banco_ficticio.docx · 0.581` — 3. Marca de default  La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago.  4. Estimación del modelo  La PD se estima con una regresión logíst…

## Fragmento 2

**Fragmento validado:**

> * Selección de la muestra de desarrollo: se seleccionan los registros de la tabla `dwh.operaciones_hipotecarias` que tienen una fecha de observación entre `01JAN2020` y `31DEC2023`.
> * Marcado de default: se marca como default los registros con más de 90 días de impago o con probabilidad de pago improbable.
> * Estimación del modelo logístico: se estima el modelo logístico con la variable `default_flag` como predictor y se selecciona el tramo de PD según la media estimada.

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `tecnico_banco_ficticio.docx · 0.783` — 3. Marca de default  La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago.  4. Estimación del modelo  La PD se estima con una regresión logíst…
- `tecnico_banco_ficticio.docx · 0.760` — Documento técnico de implementación del modelo de PD de hipotecas - Banco Ficticio S.A.  Documento ficticio redactado para demostrar el sistema. Describe la implementación en SAS.  1. Fuentes de datos  Las operaciones se…
- `tecnico_banco_ficticio.docx · 0.673` — 6. Ajustes manuales  La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones.  7. Escenarios macroeconómicos  La PD prospectiva se calcula con tres escenarios (base, adve…

## Fragmento 3

**Fragmento validado:**

> * Estimación del modelo logístico: se estima el modelo logístico con la variable `default_flag` como predictor y se selecciona el tramo de PD según la media estimada.
> * Asignación de grados de rating por tramos de PD: se asignan grados de rating según la media estimada del modelo logístico.
> * Backtesting: se realiza un test binomial para evaluar la precisión del modelo logístico según la probabilidad de éxito (95%).
> * Poder discriminante: se calcula el área bajo la curva ROC (Receiver Operating Characteristic) para evaluar la precisión del modelo logístico.

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `tecnico_banco_ficticio.docx · 0.850` — 3. Marca de default  La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago.  4. Estimación del modelo  La PD se estima con una regresión logíst…
- `tecnico_banco_ficticio.docx · 0.716` — Documento técnico de implementación del modelo de PD de hipotecas - Banco Ficticio S.A.  Documento ficticio redactado para demostrar el sistema. Describe la implementación en SAS.  1. Fuentes de datos  Las operaciones se…
- `tecnico_banco_ficticio.docx · 0.695` — 6. Ajustes manuales  La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones.  7. Escenarios macroeconómicos  La PD prospectiva se calcula con tres escenarios (base, adve…

## Fragmento 4

**Fragmento validado:**

> **Funcionalidad breves**
> 
> * Selección de la muestra de desarrollo y marcado de default.
> * Estimación del modelo logístico con grados de rating por tramos de PD.
> * Backtesting del modelo logístico para evaluar su precisión.
> * Calculo del poder discriminante para evaluar la precisión del modelo logístico.
> 
> ======================================================================

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `tecnico_banco_ficticio.docx · 0.824` — 3. Marca de default  La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago.  4. Estimación del modelo  La PD se estima con una regresión logíst…
- `tecnico_banco_ficticio.docx · 0.701` — Documento técnico de implementación del modelo de PD de hipotecas - Banco Ficticio S.A.  Documento ficticio redactado para demostrar el sistema. Describe la implementación en SAS.  1. Fuentes de datos  Las operaciones se…
- `tecnico_banco_ficticio.docx · 0.693` — 6. Ajustes manuales  La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones.  7. Escenarios macroeconómicos  La PD prospectiva se calcula con tres escenarios (base, adve…
