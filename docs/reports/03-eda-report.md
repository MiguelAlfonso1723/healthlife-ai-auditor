# DU-05 — Reporte de Análisis Exploratorio de Datos (EDA)

| Campo | Valor |
|--------|-------|
| Fase | Data Understanding |
| Milestone | Data Understanding |
| Issue | DU-05 |
| Estado | Completed |

---

# 1. Objetivo

Realizar un Análisis Exploratorio de Datos (EDA) sobre los cinco conjuntos de datos del proyecto para comprender la distribución de la información, identificar patrones relevantes, detectar posibles anomalías y evaluar el potencial de las variables para el Motor de Reglas y el modelo de Inteligencia Artificial.

El análisis permite validar la calidad general de los datos y proporciona información que será utilizada durante la fase de **Data Preparation**.

---

# 2. Datasets Analizados

| Dataset | Registros | Columnas |
|----------|----------:|---------:|
| 01_pacientes | 300 | 7 |
| 02_atenciones | 1,200 | 9 |
| 03_historia_clinica_detalle | 3,056 | 9 |
| 04_prefactura | 2,974 | 10 |
| 05_cruce_validacion | 3,126 | 8 |

---

# 3. Estadísticas Descriptivas

Se analizaron todas las variables numéricas y categóricas mediante estadísticas descriptivas.

## Variables Numéricas Analizadas

- Edad
- Cantidad realizada
- Cantidad facturada
- Valor unitario
- Valor total

Para cada variable se calcularon:

- Media
- Mediana
- Desviación estándar
- Valor mínimo
- Valor máximo
- Cuartiles

## Variables Categóricas Analizadas

Pacientes

- Sexo
- EPS
- Tipo de afiliación
- Ciudad

Atenciones

- Tipo de atención
- EPS
- Sede

Historia Clínica

- Tipo de ítem
- Soporte clínico

Pre-factura

- EPS

Cruce de Validación

- Resultado
- Tipo de alerta
- Severidad

---

# 4. Distribución de los Datos

Se generaron histogramas para evaluar la distribución de las principales variables numéricas.

Variables analizadas:

- Edad
- Valor total
- Cantidad realizada
- Cantidad facturada

El análisis permitió identificar la dispersión de los datos y posibles concentraciones de registros.

---

# 5. Detección de Valores Atípicos

Se utilizaron diagramas de caja (Boxplots) para detectar posibles valores atípicos.

Variables evaluadas:

- Edad
- Valor total
- Cantidad realizada
- Cantidad facturada

Los valores extremos identificados corresponden principalmente a procedimientos de alto costo o casos clínicos específicos y no representan errores evidentes en los datos.

---

# 6. Correlaciones

Se construyó una matriz de correlación utilizando las variables numéricas disponibles.

El análisis permitió identificar relaciones entre:

- Cantidad realizada
- Cantidad facturada
- Valor unitario
- Valor total

Las correlaciones observadas son coherentes con el proceso de facturación médica y servirán como referencia durante la selección de variables para el modelo de IA.

---

# 7. Patrones Identificados

El análisis exploratorio permitió identificar varios patrones relevantes para el negocio.

## Distribución de inconsistencias

Se observó que la mayoría de los registros corresponden a casos consistentes, mientras que aproximadamente una quinta parte representan inconsistencias históricas utilizadas como referencia para el entrenamiento del modelo.

## Tipos de alerta más frecuentes

Las alertas con mayor frecuencia corresponden a:

- SIN_SOPORTE_CLINICO
- DIAGNOSTICO_NO_RELACIONADO

Estas representan los principales escenarios que deberá detectar el Motor de Reglas.

## Distribución por severidad

Las inconsistencias presentan distintos niveles de severidad, permitiendo priorizar aquellas que generan mayor impacto económico o clínico.

## Variación por EPS

La tasa de inconsistencias presenta diferencias entre entidades promotoras de salud (EPS), lo que sugiere posibles diferencias en los procesos administrativos o clínicos.

## Diagnósticos con mayor frecuencia de inconsistencias

Algunos diagnósticos CIE-10 muestran una mayor proporción de inconsistencias, indicando que ciertos escenarios clínicos requieren validaciones más rigurosas.

## Procedimientos más frecuentes

Se identificaron los códigos CUPS con mayor número de registros, los cuales representan la mayor parte del volumen operativo del sistema.

---

# 8. Variables Candidatas para el Modelo de Inteligencia Artificial

El análisis permitió identificar las variables con mayor potencial para el modelo CNN 1D.

## Variables Textuales

- descripcion_diagnostico
- descripcion
- descripcion_servicio_facturado

Estas variables podrán aportar información semántica durante la fase de Modeling.

## Variables Categóricas

- tipo_atencion
- tipo_item
- eps

Estas variables podrán codificarse mediante técnicas de transformación apropiadas antes del entrenamiento.

## Variables Numéricas

- edad
- valor_total
- cantidad_realizada
- cantidad_facturada

Estas variables representan información cuantitativa relevante para identificar patrones de inconsistencia.

## Variables Derivadas

El análisis sugiere construir variables adicionales durante Data Preparation.

Ejemplos:

- cups_match
- diferencia_cantidad

Estas variables facilitarán la detección de discrepancias entre la Historia Clínica y la Pre-factura.

---

# 9. Variables Críticas para el Motor de Reglas

Las siguientes variables constituyen la base para la implementación de las reglas de negocio definidas en BU-03.

| Regla | Variables Principales |
|--------|-----------------------|
| BR-01 | codigo_cups, codigo_cups_facturado |
| BR-02 | soporte_clinico |
| BR-03 | diagnostico_principal_cie10, codigo_cups |
| BR-04 | tipo_item |
| BR-05 | tipo_item, codigo_cups |
| BR-06 | cantidad_realizada, cantidad_facturada |

---

# 10. Visualizaciones Generadas

Durante el EDA se construyeron más de una decena de visualizaciones utilizando Plotly.

Entre ellas:

- Histogramas
- Boxplots
- Barras
- Pie Charts
- Heatmap de correlaciones
- Heatmap Tipo Atención vs Tipo de Alerta
- Sunburst
- Treemap

Estas visualizaciones permitieron comprender la distribución de los datos y facilitaron la identificación de patrones relevantes.

---

# 11. Conclusiones

El análisis exploratorio confirma que los datos presentan una estructura adecuada para el desarrollo del proyecto.

Los principales hallazgos obtenidos fueron:

- Existen diferencias en la frecuencia de inconsistencias entre EPS.
- Algunos diagnósticos presentan mayor probabilidad de generar alertas.
- Las alertas más frecuentes corresponden a problemas de soporte clínico y coherencia diagnóstica.
- Los procedimientos de mayor valor económico suelen asociarse con alertas de mayor severidad.
- Se identificaron variables con alto potencial para el entrenamiento del modelo CNN 1D y para la implementación del Motor de Reglas.

En conjunto, estos resultados respaldan la estrategia híbrida definida durante la fase de **Analytic Approach**.

---

# 12. Recomendaciones para Data Preparation

Con base en el análisis realizado se recomienda:

- Construir el Master Dataset utilizando las variables identificadas como relevantes.
- Crear variables derivadas como `cups_match` y `diferencia_cantidad`.
- Codificar las variables categóricas antes del entrenamiento del modelo.
- Analizar el tratamiento de las variables textuales para determinar si serán utilizadas mediante embeddings o representaciones vectoriales.
- Mantener todas las variables utilizadas por las reglas de negocio como parte del conjunto final de datos.

---

# 13. Verificación de los Criterios de Aceptación

| Criterio | Estado |
|----------|--------|
| Análisis Exploratorio completado | ✅ |
| Visualizaciones generadas | ✅ |
| Patrones relevantes identificados | ✅ |

---

# 14. Relación con el Siguiente Issue

Los patrones identificados durante el EDA servirán como base para seleccionar las variables definitivas del **Master Dataset** y preparar los datos para el entrenamiento del modelo de Inteligencia Artificial durante la siguiente fase de **Data Preparation**.