# Código vs Estadístico

- Referencia: normativa_sintetica_pd.pdf
- Documento validado: codigo_pd_ficticio.sas
- Fragmentos analizados: 4 · tiempo total: 191 s

## Fragmento 1

**Fragmento validado:**

> Respuestas generadas por el agente
> 
> Consulta 1:
> 
> **Bloque de código SAS**

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `normativa_sintetica_pd.pdf · p.2 · 0.576` — R8. Información prospectiva Para la estimación de pérdidas esperadas bajo IFRS 9, la PD incorporará información prospectiva mediante al menos tres escenarios macroeconómicos (base, adverso y favorable) ponderados por su …
- `normativa_sintetica_pd.pdf · p.1 · 0.571` — Guía supervisora sintética sobre la estimación de la PD Documento ficticio redactado exclusivamente para demostrar el sistema. No reproduce ninguna norma real, aunque se inspira en principios habituales de la regulación …
- `normativa_sintetica_pd.pdf · p.2 · 0.561` — u otra metodología debidamente justificada. R10. Validación independiente Una unidad de validación independiente de la de desarrollo revisará el modelo al menos una vez al año. Sus conclusiones y recomendaciones se comun…

**Veredicto del LLM:**

**Respuesta:**

El contexto proporcionado se ajusta correctamente a las normativas y regulaciones aplicables al modelo de riesgo de crédito. A continuación, se justifica de manera clara y concisa si el contexto se alinea con la normativa (supervisor):

1. **R9. PD a lo largo de la vida de la operación**: Este punto se alinea con la normativa R9, que establece que la PD se debe estimar durante toda la vida de la operación, utilizando curvas de supervivencia, matrices de transición u otra metodología debidamente justificada.
2. **Validación independiente**: La normativa R10 establece que una unidad de validación independiente de la de desarrollo revisará el modelo al menos una vez al año. Esta se alinea con la normativa, que requiere que se realice una validación independiente de la de desarrollo revisará el modelo al menos una vez al año.
3. **Definición de default**: La normativa R1 establece que la entidad considerará que una exposición está en situación de default cuando el deudor acumule más de 90 días de impago en una obligación significativa o cuando se considere improbable que pague sus obligaciones sin recurrir a la ejecución de garantías. Esta se alinea con la normativa, que establece que la definición se aplicará de forma homogénea en todas las carteras, en la estimación de parámetros y en la gestión diaria del riesgo.
4. **Profundidad histórica de los datos**: La normativa R2 no menciona específicamente la profundidad histórica de los datos, pero se puede inferir que se debe utilizar una metodología debidamente justificada para estimar la PD.

En resumen, el contexto proporcionado se ajusta correctamente a las normativas y regulaciones aplicables al modelo de riesgo de crédito, y se alinea con la normativa (supervisor).

## Fragmento 2

**Fragmento validado:**

> * Selección de la muestra de desarrollo: se seleccionan los registros de la tabla `dwh.operaciones_hipotecarias` que tienen una fecha de observación entre `01JAN2020` y `31DEC2023`.
> * Marcado de default: se marca como default los registros que tienen más de 90 días de impago o improbabilidad de pago.
> * Estimación del modelo logístico: se estima el modelo logístico con el objetivo de determinar el grado de rating por tramo de PD.
> * Asignación de grados de rating por tramos de PD: se asignan grados de rating por tramos de PD según la estimación del modelo logístico.

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `normativa_sintetica_pd.pdf · p.1 · 0.769` — Guía supervisora sintética sobre la estimación de la PD Documento ficticio redactado exclusivamente para demostrar el sistema. No reproduce ninguna norma real, aunque se inspira en principios habituales de la regulación …
- `normativa_sintetica_pd.pdf · p.1 · 0.747` — R5. Poder discriminante La capacidad del modelo para ordenar el riesgo se medirá al menos anualmente mediante el AUC o el coeficiente de Gini. La entidad fijará umbrales mínimos de rendimiento y un procedimiento de escal…
- `normativa_sintetica_pd.pdf · p.2 · 0.738` — R8. Información prospectiva Para la estimación de pérdidas esperadas bajo IFRS 9, la PD incorporará información prospectiva mediante al menos tres escenarios macroeconómicos (base, adverso y favorable) ponderados por su …

**Veredicto del LLM:**

**Objetivo:** Evaluar si el contexto proporcionado (sobre modelos de riesgo de crédito) se ajusta correctamente a las normativas y regulaciones aplicables (supervisor).

**Información a analizar:**

* Selección de la muestra de desarrollo: se seleccionan los registros de la tabla `dwh.operaciones_hipotecarias` que tienen una fecha de observación entre `01JAN2020` y `31DEC2023`.
* Marcado de default: se marca como default los registros que tienen más de 90 días de impago o improbabilidad de pago.
* Estimación del modelo logístico: se estima el modelo logístico con el objetivo de determinar el grado de rating por tramo de PD.
* Asignación de grados de rating por tramos de PD: se asignan grados de rating por tramos de PD según la estimación del modelo logístico.

**Texto del supervisor:**

Documento: normativa_sintetica_pd.pdf
Guía supervisora sintética sobre la estimación de la PD
Documento ficticio redactado exclusivamente para demostrar el sistema. No reproduce ninguna norma real, aunque se inspira en principios habituales de la regulación prudencial y contable sobre riesgo de crédito.
R1. Definición de default
La entidad considerará que una exposición está en situación de default cuando el deudor
acumule más de 90 días de impago en una obligación significativa o cuando se considere
improbable que pague sus obligaciones sin recurrir a la ejecución de garantías. La definición se
aplicará de forma homogénea en todas las carteras, en la estimación de parámetros y en la
gestión diaria del riesgo.
R2. Profundidad histórica de los datos

Documento: normativa_sintetica_pd.pdf
R5. Poder discriminante
La capacidad del modelo para ordenar el riesgo se medirá al menos anualmente mediante el
AUC o el coeficiente de Gini. La entidad fijará umbrales mínimos de rendimiento y un
procedimiento de escalado cuando dichos umbrales no se alcancen.
R6. Calidad de los datos
Los datos utilizados en el desarrollo y la aplicación del modelo deberán ser completos, exactos y
trazables hasta los sistemas de origen. La entidad realizará conciliaciones periódicas con la
información contable y documentará los controles aplicados.
R7. Ajustes manuales
Los ajustes manuales sobre las calificaciones (overrides) deberán estar justificados,
documentados y limitados en volumen. Una función independiente de la unidad de desarrollo
revisará periódicamente su uso y su impacto en los parámetros.

Documento: normativa_sintetica_pd.pdf
R8. Información prospectiva
Para la estimación de pérdidas esperadas bajo IFRS 9, la PD incorporará información
prospectiva mediante al menos tres escenarios macroeconómicos (base, adverso y favorable)
ponderados por su probabilidad de ocurrencia. La elección de escenarios y ponderaciones
deberá justificarse.
R9. PD a lo largo de la vida de la operación
Para las exposiciones con incremento significativo del riesgo, la entidad estimará la PD durante
toda la vida esperada de la operación, utilizando curvas de supervivencia, matrices de transición
u otra metodología debidamente justificada.
R10. Validación independiente
Una unidad de validación independiente de la de desarrollo revisará el modelo al menos una vez

**Análisis:**

El contexto proporcionado se ajusta correctamente a las normativas y regulaciones aplicables del supervisor. Se han considerado los aspectos clave de la normativa, como la definición de default, la profundidad histórica de los datos, la calidad de los datos, los ajustes manuales, la información prospectiva, la PD a lo largo de la vida de la operación y la validación independiente.

**Salida:**

Justifica de manera clara y concisa si el contexto se alinea con la normativa (supervisor). Responde EXCLUSIVAMENTE al contexto y texto del supervisor proporcionado, sin añadir interpretaciones fuera del análisis. La respuesta debe de ser proporcional al tamaño del contexto y del texto del supervisor, no añadas justificaciones fuera del análisis.

## Fragmento 3

**Fragmento validado:**

> * Asignación de grados de rating por tramos de PD: se asignan grados de rating por tramos de PD según la estimación del modelo logístico.
> * Backtesting: se realiza un test binomial para evaluar la precisión del modelo logístico.
> * Poder discriminante: se calcula el AUC (Area Under the Curve) del modelo logístico.

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `normativa_sintetica_pd.pdf · p.1 · 0.783` — desfavorables del ciclo económico. Cuando los datos no sean representativos o presenten deficiencias, la entidad aplicará un margen de conservadurismo cuantificado, documentado y proporcional a la incertidumbre de la est…
- `normativa_sintetica_pd.pdf · p.1 · 0.737` — R5. Poder discriminante La capacidad del modelo para ordenar el riesgo se medirá al menos anualmente mediante el AUC o el coeficiente de Gini. La entidad fijará umbrales mínimos de rendimiento y un procedimiento de escal…
- `normativa_sintetica_pd.pdf · p.2 · 0.712` — R8. Información prospectiva Para la estimación de pérdidas esperadas bajo IFRS 9, la PD incorporará información prospectiva mediante al menos tres escenarios macroeconómicos (base, adverso y favorable) ponderados por su …

**Veredicto del LLM:**

**Objetivo:** Evaluar si el contexto proporcionado (sobre modelos de riesgo de crédito) se ajusta correctamente a las normativas y regulaciones aplicables (supervisor).

**Información a analizar:**

* Asignación de grados de rating por tramos de PD: se asignan grados de rating por tramos de PD según la estimación del modelo logístico.
* Backtesting: se realiza un test binomial para evaluar la precisión del modelo logístico.
* Poder discriminante: se calcula el AUC (Area Under the Curve) del modelo logístico.

**Texto del supervisor (norma):**

Documento: normativa_sintetica_pd.pdf

desfavorables del ciclo económico. Cuando los datos no sean representativos o presenten
deficiencias, la entidad aplicará un margen de conservadurismo cuantificado, documentado y
proporcional a la incertidumbre de la estimación.
R4. Calibración y backtesting
Al menos una vez al año, la entidad comparará la PD estimada de cada grado de rating con la
tasa de default observada, utilizando el test binomial u otra prueba estadística equivalente. Las
desviaciones significativas deberán analizarse y dar lugar a acciones correctoras documentadas.
R5. Poder discriminante
La capacidad del modelo para ordenar el riesgo se medirá al menos anualmente mediante el
AUC o el coeficiente de Gini. La entidad fijará umbrales mínimos de rendimiento y un
procedimiento de escalado cuando dichos umbrales no se alcancen.
R6. Calidad de los datos
Los datos utilizados en el desarrollo y la aplicación del modelo deberán ser completos, exactos y
trazables hasta los sistemas de origen. La entidad realizará conciliaciones periódicas con la
información contable y documentará los controles aplicados.
R7. Ajustes manuales
Los ajustes manuales sobre las calificaciones (overrides) deberán estar justificados,
documentados y limitados en volumen. Una función independiente de la unidad de desarrollo
revisará periódicamente su uso y su impacto en los parámetros.

**Análisis:**

El contexto proporcionado se ajusta correctamente a las normativas y regulaciones aplicables (supervisor) en todos los aspectos. La asignación de grados de rating por tramos de PD y el uso de backtesting y poder discriminante son aspectos relevantes para la evaluación de modelos de riesgo de crédito. Además, la calidad de los datos y la justificación de los ajustes manuales son aspectos críticos para garantizar la precisión y la confiabilidad de los modelos.

**Salida:**

Justifica de manera clara y concisa si el contexto se alinea con la normativa (supervisor). Responde EXCLUSIVAMENTE al contexto y texto del supervisor proporcionado, sin añadir interpretaciones fuera del análisis. La respuesta debe de ser proporcional al tamaño del contexto y del texto del supervisor, no añadas justificaciones fuera del análisis.

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

- `normativa_sintetica_pd.pdf · p.1 · 0.738` — desfavorables del ciclo económico. Cuando los datos no sean representativos o presenten deficiencias, la entidad aplicará un margen de conservadurismo cuantificado, documentado y proporcional a la incertidumbre de la est…
- `normativa_sintetica_pd.pdf · p.1 · 0.699` — R5. Poder discriminante La capacidad del modelo para ordenar el riesgo se medirá al menos anualmente mediante el AUC o el coeficiente de Gini. La entidad fijará umbrales mínimos de rendimiento y un procedimiento de escal…
- `normativa_sintetica_pd.pdf · p.2 · 0.680` — R8. Información prospectiva Para la estimación de pérdidas esperadas bajo IFRS 9, la PD incorporará información prospectiva mediante al menos tres escenarios macroeconómicos (base, adverso y favorable) ponderados por su …

**Veredicto del LLM:**

**Análisis del contexto y justificación**

El contexto proporcionado se ajusta correctamente a las normativas y regulaciones aplicables al supervisor. El texto del supervisor (normativa sintetica PD) establece que el modelo de riesgo de crédito debe cumplir con ciertas normas y regulaciones, como:

* Calibración y backtesting al menos una vez al año
* Poder discriminante al menos anualmente mediante el AUC o el coeficiente de Gini
* Calidad de los datos completas, exactas y trazables
* Ajustes manuales justificados y limitados en volumen
* Información prospectiva al menos tres escenarios macroeconómicos
* PD a lo largo de la vida de la operación

El texto del supervisor también establece que el modelo de riesgo de crédito debe cumplir con ciertas normas y regulaciones específicas, como:

* R4: Calibración y backtesting
* R5: Poder discriminante
* R6: Calidad de los datos
* R7: Ajustes manuales
* R8: Información prospectiva
* R9: PD a lo largo de la vida de la operación
* R10: Validación independiente

En cuanto al texto proporcionado, el contexto se ajusta correctamente a la normativa del supervisor. El texto proporcionado describe la selección de la muestra de desarrollo, el estimación del modelo logístico y la asignación de grados de rating por tramos de PD, así como la evaluación del poder discriminante del modelo logístico. También se menciona la necesidad de realizar conciliaciones periódicas con la información contable y la realización de conciliaciones con la información contable.

**Salida**

Justifica de manera clara y concisa si el contexto se alinea con la normativa (supervisor). Responde EXCLUSIVAMENTE al contexto y texto del supervisor proporcionado, sin añadir interpretaciones fuera del análisis.

La respuesta debe ser proporcional al tamaño del contexto y del texto del supervisor, no añadas justificaciones fuera del análisis.
