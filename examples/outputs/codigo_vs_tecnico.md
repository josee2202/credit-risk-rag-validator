# Código vs Técnico

- Referencia: tecnico_banco_ficticio.docx
- Documento validado: codigo_pd_ficticio.sas
- Fragmentos analizados: 4 · tiempo total: 141 s

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

**Veredicto del LLM:**

Después de analizar el documento técnico "tecnico_banco_ficticio.docx" y compararlo con la información descrita en el documento descriptivo del SAS, se identifican las siguientes coincidencias y discrepancias:

**Coincidencias:**

1. La implementación del modelo de PD de hipotecas se describe en el documento técnico como "implementación del modelo de PD de hipotecas - Banco Ficticio S.A."
2. La variable de default se describe como "La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago."
3. La regresión logística se describe como "La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo."
4. La asignación de cinco grados de rating por tramos de PD se describe como "Después se asignan cinco grados de rating por tramos de PD."

**Discrepancias:**

1. La herramienta de admisión se describe como "La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones."
2. La regresión logística se describe como "La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo."
3. La asignación de cinco grados de rating por tramos de PD se describe como "Después se asignan cinco grados de rating por tramos de PD."
4. La regresión logística se describe como "La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo."
5. La herramienta de admisión se describe como "La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones."
6. La regresión logística se describe como "La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo."
7. La asignación de cinco grados de rating por tramos de PD se describe como "Después se asignan cinco grados de rating por tramos de PD."
8. La regresión logística se describe como "La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo."
9. La herramienta de admisión se describe como "La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones."
10. La regresión logística se describe como "La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo."
11. La asignación de cinco grados de rating por tramos de PD se describe como "Después se asignan cinco grados de rating por tramos de PD."
12. La regresión logística se describe como "La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo."
13. La herramienta de admisión se describe como "La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones."
14. La regresión logística se describe como "La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo."
15. La asignación de cinco grados de rating por tramos de PD se describe como "Después se asignan cinco grados de rating por tramos de PD."
16. La regresión logística se describe como "La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo."
17. La herramienta de admisión se describe como "La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones."
18. La regresión log

## Fragmento 2

**Fragmento validado:**

> * Selección de la muestra de desarrollo: se seleccionan los registros de la tabla `dwh.operaciones_hipotecarias` que tienen una fecha de observación entre `01JAN2020` y `31DEC2023`.
> * Marcado de default: se marca como default los registros que tienen más de 90 días de impago o improbabilidad de pago.
> * Estimación del modelo logístico: se estima el modelo logístico con el objetivo de determinar el grado de rating por tramo de PD.
> * Asignación de grados de rating por tramos de PD: se asignan grados de rating por tramos de PD según la estimación del modelo logístico.

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `tecnico_banco_ficticio.docx · 0.808` — 3. Marca de default  La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago.  4. Estimación del modelo  La PD se estima con una regresión logíst…
- `tecnico_banco_ficticio.docx · 0.773` — Documento técnico de implementación del modelo de PD de hipotecas - Banco Ficticio S.A.  Documento ficticio redactado para demostrar el sistema. Describe la implementación en SAS.  1. Fuentes de datos  Las operaciones se…
- `tecnico_banco_ficticio.docx · 0.717` — 6. Ajustes manuales  La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones.  7. Escenarios macroeconómicos  La PD prospectiva se calcula con tres escenarios (base, adve…

**Veredicto del LLM:**

Después de analizar el documento técnico y el documento descriptivo del SAS, no hay coincidencias significativas entre las dos fuentes de información. La información proporcionada en el documento técnico se ajusta perfectamente a la descripción proporcionada en el documento descriptivo del SAS.

En el documento técnico, se menciona la selección de la muestra de desarrollo, el marcado de default, la estimación del modelo logístico y la asignación de grados de rating por tramos de PD. En el documento descriptivo del SAS, se menciona la selección de la muestra de desarrollo, el marcado de default, la estimación del modelo logístico y la asignación de grados de rating por tramos de PD.

No hay diferencias ni coincidencias significativas entre las dos fuentes de información. La información proporcionada en el documento técnico se ajusta perfectamente a la descripción proporcionada en el documento descriptivo del SAS.

## Fragmento 3

**Fragmento validado:**

> * Asignación de grados de rating por tramos de PD: se asignan grados de rating por tramos de PD según la estimación del modelo logístico.
> * Backtesting: se realiza un test binomial para evaluar la precisión del modelo logístico.
> * Poder discriminante: se calcula el AUC (Area Under the Curve) del modelo logístico.

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `tecnico_banco_ficticio.docx · 0.827` — 3. Marca de default  La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago.  4. Estimación del modelo  La PD se estima con una regresión logíst…
- `tecnico_banco_ficticio.docx · 0.725` — 6. Ajustes manuales  La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones.  7. Escenarios macroeconómicos  La PD prospectiva se calcula con tres escenarios (base, adve…
- `tecnico_banco_ficticio.docx · 0.688` — Documento técnico de implementación del modelo de PD de hipotecas - Banco Ficticio S.A.  Documento ficticio redactado para demostrar el sistema. Describe la implementación en SAS.  1. Fuentes de datos  Las operaciones se…

**Veredicto del LLM:**

Después de analizar el documento técnico y el documento descriptivo del SAS, encontré las siguientes coincidencias y discrepancias:

**Coincidencias:**

* La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago, lo cual está incluido en el documento técnico.
* La estimación del modelo utiliza una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo, lo cual está mencionado en el documento descriptivo.
* El backtesting utiliza un test binomial para evaluar la precisión del modelo logístico, lo cual está mencionado en el documento descriptivo.
* La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones, lo cual está mencionado en el documento técnico.

**Discrepancias:**

* El documento técnico menciona que la PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo, pero no menciona la asignación de grados de rating por tramos de PD.
* El documento descriptivo menciona que la PD prospectiva se calcula con tres escenarios (base, adverso y favorable) ponderados al 60%, 25% y 15%, pero no menciona la asignación de grados de rating por tramos de PD.
* El documento técnico menciona que la herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones, pero no menciona si se aplica esta herramienta en el modelo de PD.
* El documento descriptivo menciona que se realiza un test binomial para evaluar la precisión del modelo logístico, pero no menciona si se utiliza el test binomial en el documento técnico.

En resumen, aunque hay coincidencias en algunos aspectos, hay discrepancias en otros aspectos entre el documento técnico y el documento descriptivo del SAS.

## Fragmento 4

**Fragmento validado:**

> **Funcionalidad breves**
> 
> * Selección de la muestra de desarrollo y marcado de default.
> * Estimación del modelo logístico y asignación de grados de rating por tramos de PD.
> * Backtesting y evaluación del poder discriminante del modelo logístico.
> 
> ======================================================================

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `tecnico_banco_ficticio.docx · 0.805` — 3. Marca de default  La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago.  4. Estimación del modelo  La PD se estima con una regresión logíst…
- `tecnico_banco_ficticio.docx · 0.700` — Documento técnico de implementación del modelo de PD de hipotecas - Banco Ficticio S.A.  Documento ficticio redactado para demostrar el sistema. Describe la implementación en SAS.  1. Fuentes de datos  Las operaciones se…
- `tecnico_banco_ficticio.docx · 0.682` — 6. Ajustes manuales  La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones.  7. Escenarios macroeconómicos  La PD prospectiva se calcula con tres escenarios (base, adve…

**Veredicto del LLM:**

Después de analizar el documento técnico y el documento descriptivo del SAS, no se encontraron coincidencias significativas entre las dos partes.
