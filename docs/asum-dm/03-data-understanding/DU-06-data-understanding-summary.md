# DU-06 — Data Understanding Summary

| Campo | Valor |
|--------|-------|
| Fase | Data Understanding |
| Milestone | Data Understanding |
| Issue | DU-06 |
| Estado | Completed |

---

# 1. Objetivo

Este documento resume los resultados obtenidos durante toda la fase **Data Understanding** del proyecto Healthcare AI Billing Auditor y valida que los cinco datasets fuente han sido comprendidos en su estructura, calidad, relaciones y contenido.

El propósito es confirmar que el equipo dispone de suficiente conocimiento sobre los datos para iniciar la fase **Data Preparation** de la metodología ASUM-DM.

---

# 2. Resumen de los Issues Completados

## DU-01 — Analyze Source Datasets Structure

**Objetivo:** Analizar la estructura de los cinco datasets para comprender su propósito, atributos y tipos de datos.

**Resultado:** Se identificaron 43 columnas distribuidas en 5 datasets (300 a 3,126 registros). Se documentaron llaves primarias, foráneas y la función de cada dataset dentro del sistema.

---

## DU-02 — Create the Data Dictionary

**Objetivo:** Crear un diccionario de datos completo que documente todos los atributos.

**Resultado:** Se generó `docs/data-dictionary.xlsx` con 43 atributos documentados incluyendo tipo de dato, nullable, llave y significado de negocio.

---

## DU-03 — Perform Data Quality Assessment

**Objetivo:** Evaluar la calidad de los datos para identificar problemas que afecten al Motor de Reglas y al modelo de IA.

**Resultado:** Se determinó que los datos tienen alta calidad estructural (0 duplicados, integridad referencial perfecta, formatos correctos). Se identificó desbalance de clases (79/21) y volumen limitado (3,126 registros) como riesgos principales.

---

## DU-04 — Analyze Relationships Between Datasets

**Objetivo:** Analizar las relaciones entre datasets y definir la estrategia de JOIN para el Master Dataset.

**Resultado:** Se verificó integridad referencial completa. Se definió una estrategia de 4 pasos usando cruce_validacion como base con INNER JOIN a atenciones y LEFT JOIN a pacientes, historia_clinica y prefactura.

---

## DU-05 — Perform Exploratory Data Analysis

**Objetivo:** Comprender distribuciones, detectar anomalías y descubrir patrones relevantes para el Motor de Reglas y el modelo CNN 1D.

**Resultado:** Se generaron 20 visualizaciones. Se identificaron patrones de inconsistencia por EPS, diagnóstico y tipo de atención. Se determinaron variables candidatas para el modelo y variables críticas para las reglas de negocio.

---

# 3. Comprensión de los Datos

## Estructura de los Datasets

| Dataset | Registros | Columnas | PK |
|---------|-----------|----------|----|
| 01_pacientes | 300 | 7 | id_paciente |
| 02_atenciones | 1,200 | 9 | id_atencion |
| 03_historia_clinica_detalle | 3,056 | 9 | id_detalle |
| 04_prefactura | 2,974 | 10 | id_prefactura |
| 05_cruce_validacion | 3,126 | 8 | id_cruce |

## Identificadores Principales

- `id_paciente` — Identifica al paciente.
- `id_atencion` — Identifica cada evento de atención médica (tabla pivote).
- `id_detalle` — Identifica cada registro clínico individual.
- `id_prefactura` — Identifica cada servicio en la pre-factura.
- `id_cruce` — Identifica cada resultado de validación.

## Claves Foráneas

- `atenciones.id_paciente` → `pacientes.id_paciente`
- `historia_clinica.id_atencion` → `atenciones.id_atencion`
- `prefactura.id_atencion` → `atenciones.id_atencion`
- `cruce_validacion.id_atencion` → `atenciones.id_atencion`
- `cruce_validacion.id_prefactura` → `prefactura.id_prefactura`
- `cruce_validacion.id_detalle_hc` → `historia_clinica.id_detalle`

## Master Dataset Propuesto

El Master Dataset se construirá usando `cruce_validacion` como tabla base (contiene el ground truth), enriquecido con información de atenciones, pacientes, historia clínica y prefactura.

## Estrategia de JOIN

```
cruce_validacion
  INNER JOIN atenciones        ON id_atencion
  LEFT JOIN  pacientes         ON id_paciente (via atenciones)
  LEFT JOIN  historia_clinica  ON id_detalle_hc = id_detalle
  LEFT JOIN  prefactura        ON id_prefactura
```

Resultado esperado: 3,126 registros con aproximadamente 28 columnas útiles.

---

# 4. Calidad de los Datos

## Valores Faltantes

- Solo `cruce_validacion` presenta nulos: `id_prefactura` (152 nulos, 4.86%) e `id_detalle_hc` (70 nulos, 2.24%).
- Estos nulos son esperados por diseño de negocio (alertas de tipo NO_FACTURADO no tienen prefactura, alertas sin HC).
- Los demás datasets tienen 0% de nulos.

## Duplicados

- No se detectaron filas duplicadas en ningún dataset.
- No se detectaron llaves primarias duplicadas.

## Integridad Referencial

- Todas las FK apuntan a registros existentes en sus tablas padre.
- 0 registros huérfanos detectados en todas las relaciones verificadas.

## Formatos

- IDs siguen patrones regex válidos (PAC-XXXXX, ATN-XXXXXX, etc.).
- Fechas son parseables correctamente.
- Códigos CUPS cumplen formato de 5-6 dígitos.
- Códigos CIE-10 cumplen patrón válido.

## Calidad General

La calidad general de los datos es **alta**. No se detectaron problemas críticos que impidan continuar. La completitud global supera el 99%.

---

# 5. Hallazgos del EDA

## Principales Patrones

- La tasa de inconsistencia varía significativamente entre EPS.
- Ciertos diagnósticos CIE-10 presentan tasas de inconsistencia mucho mayores que el promedio.
- `SIN_SOPORTE_CLINICO` y `DIAGNOSTICO_NO_RELACIONADO` son los tipos de alerta más frecuentes.
- Los servicios de mayor valor económico tienden a generar alertas de mayor severidad.
- La distribución de resultado es 79.2% CONSISTENTE vs 20.8% INCONSISTENTE.

## Variables Candidatas para IA (CNN 1D)

- **Textuales:** `descripcion_diagnostico`, `descripcion`, `descripcion_servicio_facturado`
- **Categóricas:** `tipo_atencion`, `tipo_item`, `eps`, `tipo_afiliacion`
- **Numéricas:** `edad`, `valor_total`, `cantidad_realizada`, `cantidad_facturada`
- **Derivadas (a crear):** `cups_match`, `diferencia_cantidad`

## Variables para el Motor de Reglas

| Regla | Variables |
|-------|-----------|
| BR-01 | `codigo_cups` vs `codigo_cups_facturado` |
| BR-02 | `soporte_clinico` |
| BR-03 | `diagnostico_principal_cie10` vs `codigo_cups` |
| BR-04 | `tipo_item` (tratamientos) |
| BR-05 | `tipo_item` (laboratorios/exámenes) |
| BR-06 | `cantidad_realizada` vs `cantidad_facturada` |

## Tipos de Alerta Identificados

| Tipo | Frecuencia |
|------|-----------|
| CONSISTENTE | 2,477 |
| SIN_SOPORTE_CLINICO | 157 |
| DIAGNOSTICO_NO_RELACIONADO | 152 |
| NO_FACTURADO | 152 |
| CODIGO_NO_COINCIDE | 120 |
| CANTIDAD_DISCORDANTE | 68 |

---

# 6. Preparación para Data Preparation

Las siguientes actividades pueden comenzar inmediatamente:

## Construcción del Master Dataset

- Estrategia de JOIN definida y simulada exitosamente.
- Resultado esperado: 3,126 registros con 28 columnas útiles.
- Columnas redundantes identificadas para eliminación.

## Feature Engineering

- Features derivadas diseñadas: `cups_match`, `diferencia_cantidad`.
- Variables categóricas identificadas para codificación.
- Variables numéricas identificadas para normalización.

## Codificación de Variables

- Categóricas de baja cardinalidad (sexo, tipo_atencion, tipo_item): One-Hot Encoding.
- Categóricas de alta cardinalidad (eps, ciudad, sede): Label Encoding o Target Encoding.
- Textuales: Embeddings o TF-IDF (decisión en Modeling).

## Preparación para CNN 1D

- Se evaluará si el input será texto (embeddings) o vector numérico de features.
- La decisión dependerá de la calidad observada en los campos textuales.
- Ambas opciones son viables según el análisis realizado.

---

# 7. Riesgos Identificados

| Riesgo | Impacto | Fase de Resolución |
|--------|---------|-------------------|
| Selección definitiva del input de la CNN (texto vs numérico) | Alto | Data Preparation / Modeling |
| Volumen limitado para Deep Learning (3,126 registros, 649 de clase positiva) | Alto | Modeling |
| Desbalance de clases (79/21) puede sesgar predicciones | Alto | Data Preparation / Modeling |
| Subclases de tipo_alerta con pocas muestras (CANTIDAD_DISCORDANTE: 68) | Medio | Modeling |
| Nulos en id_prefactura e id_detalle_hc requieren tratamiento adecuado | Medio | Data Preparation |

---

# 8. Conclusión

## ¿Los datasets fueron comprendidos?

**Sí.** Se analizó la estructura, tipos de datos, identificadores, cardinalidad y distribuciones de los 5 datasets. Se documentaron 43 atributos en el diccionario de datos.

## ¿Se conoce la calidad de los datos?

**Sí.** La calidad es alta: sin duplicados, integridad referencial perfecta, formatos válidos y completitud superior al 99%. Los únicos nulos son esperados por diseño de negocio.

## ¿La estrategia de integración está validada?

**Sí.** La estrategia de JOIN fue simulada exitosamente, produciendo 3,126 registros sin pérdida de datos del ground truth.

## ¿Puede comenzar Data Preparation?

**Sí.** El equipo dispone de toda la información necesaria para construir el Master Dataset, realizar feature engineering y preparar los datos para el Motor de Reglas y el modelo CNN 1D.

**El milestone Data Understanding puede darse por finalizado.**

---

# 9. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|--------|
| Estructura de datasets analizada | ✅ |
| Diccionario de datos creado | ✅ |
| Calidad de datos evaluada | ✅ |
| Relaciones entre datasets validadas | ✅ |
| EDA completado | ✅ |
| Estrategia de JOIN definida | ✅ |
| Variables para Motor de Reglas identificadas | ✅ |
| Variables candidatas para IA identificadas | ✅ |
| Riesgos documentados | ✅ |
| Equipo listo para Data Preparation | ✅ |

---

# 10. Relación con el siguiente Milestone

El siguiente milestone será **Data Preparation**, donde se realizarán las siguientes actividades:

1. Construcción del Master Dataset utilizando la estrategia de JOIN definida.
2. Limpieza de datos (tratamiento de nulos, conversión de fechas).
3. Feature Engineering (creación de variables derivadas).
4. Codificación de variables categóricas.
5. Normalización de variables numéricas.
6. Preparación del dataset de entrenamiento para el modelo CNN 1D.
7. Estrategia de balanceo de clases.
8. División en conjuntos de entrenamiento, validación y prueba.

Toda la información recopilada durante Data Understanding será utilizada como guía para estas actividades.
