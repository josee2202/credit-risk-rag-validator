# Funcional vs Técnico

- Referencia: metodologia_banco_ficticio.docx
- Documento validado: tecnico_banco_ficticio.docx
- Fragmentos analizados: 3 · tiempo total: 5 s

## Fragmento 1

**Fragmento validado:**

> Documento técnico de implementación del modelo de PD de hipotecas - Banco Ficticio S.A.
> 
> Documento ficticio redactado para demostrar el sistema. Describe la implementación en SAS.
> 
> 1. Fuentes de datos
> 
> Las operaciones se extraen mensualmente de las tablas del almacén corporativo. Antes de cada ejecución se concilian los saldos con la contabilidad y se registran los controles de completitud.
> 
> 2. Construcción de la muestra
> 
> La muestra de desarrollo incluye las operaciones hipotecarias observadas entre enero de 2020 y diciembre de 2023.
> 
> 3. Marca de default

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `metodologia_banco_ficticio.docx · 0.863` — Documento metodológico del modelo de PD de hipotecas - Banco Ficticio S.A.  Documento ficticio redactado para demostrar el sistema. Banco Ficticio S.A. no existe.  1. Definición de default  El modelo considera en default…
- `metodologia_banco_ficticio.docx · 0.668` — 2. Muestra de desarrollo  La tasa media de default a largo plazo se ha calculado con la muestra disponible entre enero de 2021 y diciembre de 2023, es decir, tres años de observación. Los años anteriores se han descartad…
- `metodologia_banco_ficticio.docx · 0.667` — 6. Escenarios prospectivos  Para el cálculo de la pérdida esperada bajo IFRS 9 se utiliza un único escenario macroeconómico, el escenario base publicado por el servicio de estudios, sin escenarios alternativos ni pondera…

## Fragmento 2

**Fragmento validado:**

> 2. Construcción de la muestra
> 
> La muestra de desarrollo incluye las operaciones hipotecarias observadas entre enero de 2020 y diciembre de 2023.
> 
> 3. Marca de default
> 
> La variable de default se activa cuando la operación supera los 90 días de impago o cuando está marcada con improbabilidad de pago.
> 
> 4. Estimación del modelo
> 
> La PD se estima con una regresión logística (PROC LOGISTIC) con selección stepwise sobre el LTV, la antigüedad de la operación y el ratio de esfuerzo. Después se asignan cinco grados de rating por tramos de PD.
> 
> 5. Backtesting

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `metodologia_banco_ficticio.docx · 0.795` — 4. Calibración  Cada año se compara la PD asignada a cada grado de rating con la tasa de default observada mediante el test binomial con un nivel de confianza del 95%. Las desviaciones significativas se analizan en el co…
- `metodologia_banco_ficticio.docx · 0.769` — 2. Muestra de desarrollo  La tasa media de default a largo plazo se ha calculado con la muestra disponible entre enero de 2021 y diciembre de 2023, es decir, tres años de observación. Los años anteriores se han descartad…
- `metodologia_banco_ficticio.docx · 0.738` — 6. Escenarios prospectivos  Para el cálculo de la pérdida esperada bajo IFRS 9 se utiliza un único escenario macroeconómico, el escenario base publicado por el servicio de estudios, sin escenarios alternativos ni pondera…

## Fragmento 3

**Fragmento validado:**

> 5. Backtesting
> 
> Para cada grado se calcula el límite superior del número de defaults con el test binomial al 95% y se marca el grado como rechazado si los defaults observados lo superan. El AUC se obtiene con la instrucción ROC de PROC LOGISTIC.
> 
> 6. Ajustes manuales
> 
> La herramienta de admisión permite ajustes manuales del rating hasta un máximo del 10% de las operaciones.
> 
> 7. Escenarios macroeconómicos
> 
> La PD prospectiva se calcula con tres escenarios (base, adverso y favorable) ponderados al 60%, 25% y 15%.

**Evidencias recuperadas (fuente · página · similitud coseno):**

- `metodologia_banco_ficticio.docx · 0.864` — 4. Calibración  Cada año se compara la PD asignada a cada grado de rating con la tasa de default observada mediante el test binomial con un nivel de confianza del 95%. Las desviaciones significativas se analizan en el co…
- `metodologia_banco_ficticio.docx · 0.818` — 6. Escenarios prospectivos  Para el cálculo de la pérdida esperada bajo IFRS 9 se utiliza un único escenario macroeconómico, el escenario base publicado por el servicio de estudios, sin escenarios alternativos ni pondera…
- `metodologia_banco_ficticio.docx · 0.732` — 2. Muestra de desarrollo  La tasa media de default a largo plazo se ha calculado con la muestra disponible entre enero de 2021 y diciembre de 2023, es decir, tres años de observación. Los años anteriores se han descartad…
