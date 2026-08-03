# DP-06 — Data Validation Report

| Campo | Valor |
|--------|-------|
| Fase | Data Preparation |
| Milestone | Data Preparation |
| Issue | DP-06 |
| Estado | Completed |

---

# 1. Información General

Este documento constituye el reporte oficial de validación del dataset preparado durante la fase Data Preparation del proyecto Healthcare AI Billing Auditor.

La validación fue realizada sobre el dataset generado por el pipeline automatizado (DP-05) ubicado en:

- `data/master/master_dataset_features.parquet`
- `data/master/master_dataset_features.csv`

---

# 2. Objetivo

Verificar que el dataset preparado cumple todos los requisitos funcionales, técnicos y de negocio antes de iniciar la fase de Modeling de la metodología ASUM-DM.

---

# 3. Resumen del Dataset

| Atributo | Valor |
|----------|-------|
| Registros | 3,126 |
| Columnas totales | 55 |
| Features originales (del Master Dataset) | 35 |
| Features creadas (Feature Engineering) | 20 |
| Formato CSV | ✅ Disponible |
| Formato Parquet | ✅ Disponible |
| Clave primaria | id_cruce |
| Variable objetivo | resultado (CONSISTENTE / INCONSISTENTE) |

---

# 4. Validación de Completitud

## Registros

| Métrica | Esperado | Actual | Estado |
|---------|----------|--------|--------|
| Total de registros | 3,126 | 3,126 | ✅ |
| Total de columnas | 55 | 55 | ✅ |
| Features originales | 35 | 35 | ✅ |
| Features nuevas | 20 | 20 | ✅ |

## Valores Nulos

Los nulos existentes son esperados por diseño de negocio:

| Columna | Nulos | Porcentaje | Justificación |
|---------|-------|-----------|---------------|
| id_prefactura | 152 | 4.9% | Alertas NO_FACTURADO (sin prefactura) |
| codigo_cups_facturado | 152 | 4.9% | Idem |
| descripcion_servicio_facturado | 152 | 4.9% | Idem |
| cantidad_facturada | 152 | 4.9% | Idem |
| valor_unitario | 152 | 4.9% | Idem |
| valor_total | 152 | 4.9% | Idem |
| fecha_facturacion | 152 | 4.9% | Idem |
| dias_atencion_facturacion | 152 | 4.9% | Derivado de fecha_facturacion |
| id_detalle_hc | 70 | 2.2% | Alertas SIN_SOPORTE (sin registro HC) |
| id_atencion_hc | 70 | 2.2% | Idem |
| tipo_item | 70 | 2.2% | Idem |
| codigo_cups | 70 | 2.2% | Idem |
| descripcion | 70 | 2.2% | Idem |
| cantidad_realizada | 70 | 2.2% | Idem |
| fecha_registro | 70 | 2.2% | Idem |
| soporte_clinico | 70 | 2.2% | Idem |
| profesional_responsable | 70 | 2.2% | Idem |
| hora_registro | 70 | 2.2% | Derivado de fecha_registro |

Todos los nulos están justificados. No existen valores faltantes inesperados.

---

# 5. Validación de Consistencia

| Criterio | Resultado | Estado |
|----------|-----------|--------|
| Duplicados exactos | 0 | ✅ |
| PK (id_cruce) duplicada | 0 | ✅ |
| Variable objetivo presente | Sí | ✅ |
| Clases de resultado correctas | CONSISTENTE, INCONSISTENTE | ✅ |
| Tipos de datos correctos | Sí | ✅ |
| Features numéricas coherentes | Sí | ✅ |
| Features binarias (0/1) | Sí | ✅ |
| Features temporales válidas | Sí | ✅ |

---

# 6. Validación de Relaciones

| Relación | Registros | Huérfanos | Estado |
|----------|-----------|-----------|--------|
| cruce → atenciones (id_atencion) | 3,126 | 0 | ✅ |
| atenciones → pacientes (id_paciente) | 3,126 | 0 | ✅ |
| cruce → historia_clinica (id_detalle_hc) | 3,056 | 0 | ✅ |
| cruce → prefactura (id_prefactura) | 2,974 | 0 | ✅ |

Nulos en id_detalle_hc (70) e id_prefactura (152) corresponden a registros sin relación por diseño de negocio.

No se detectó pérdida de registros durante la integración.

---

# 7. Validación de Reglas de Negocio

| Regla | Variables requeridas | Presentes | Estado |
|-------|---------------------|-----------|--------|
| BR-01 — Procedimiento no facturado | codigo_cups, codigo_cups_facturado, cups_match | ✅ | ✅ |
| BR-02 — Sin soporte clínico | soporte_clinico, tiene_soporte_clinico | ✅ | ✅ |
| BR-03 — Diagnóstico inconsistente | diagnostico_principal_cie10, codigo_cups | ✅ | ✅ |
| BR-04 — Tratamientos omitidos | tipo_item, procedimiento_no_facturado | ✅ | ✅ |
| BR-05 — Laboratorios no facturados | tipo_item, procedimiento_facturado | ✅ | ✅ |
| BR-06 — Cantidades discordantes | cantidad_realizada, cantidad_facturada, diferencia_cantidad, cantidad_coincide | ✅ | ✅ |

Todas las reglas de negocio pueden implementarse con las variables disponibles.

---

# 8. Validación para Machine Learning

## Variables Disponibles

| Categoría | Variables | Cantidad |
|-----------|-----------|----------|
| Numéricas | edad, cantidad_realizada, cantidad_facturada, valor_unitario, valor_total, len_descripcion_diagnostico, len_descripcion_hc, len_descripcion_servicio, diferencia_cantidad, dias_atencion_facturacion, anio_atencion, mes_atencion, trimestre, dia_semana, hora_registro | 15 |
| Binarias | cups_match, tiene_soporte_clinico, procedimiento_facturado, procedimiento_registrado, diagnostico_disponible, cantidad_coincide, valor_unitario_disponible, valor_total_disponible, servicio_facturado, procedimiento_no_facturado | 10 |
| Categóricas | sexo, tipo_atencion, tipo_item, tipo_afiliacion, eps, ciudad, sede | 7 |
| Textuales (CNN 1D) | descripcion_diagnostico, descripcion, descripcion_servicio_facturado | 3 |
| Objetivo | resultado | 1 |
| Multi-clase | tipo_alerta, severidad | 2 |

## Distribución de Clases

| Clase | Registros | Porcentaje |
|-------|-----------|-----------|
| CONSISTENTE | 2,477 | 79.2% |
| INCONSISTENTE | 649 | 20.8% |

## Ground Truth

El dataset contiene las etiquetas de validación provenientes de `05_cruce_validacion.csv`, preservando la distribución original sin modificaciones.

## Aptitud para CNN 1D

El dataset es apto para entrenar el modelo CNN 1D. Contiene variables numéricas, binarias, categóricas y textuales que pueden combinarse como input del modelo.

---

# 9. Validación del Pipeline

| Criterio | Estado |
|----------|--------|
| Pipeline ejecuta sin errores | ✅ |
| Pipeline es reproducible | ✅ |
| Pipeline produce 3,126 registros | ✅ |
| Pipeline produce 55 columnas | ✅ |
| Pipeline exporta CSV | ✅ |
| Pipeline exporta Parquet | ✅ |
| Pipeline incluye validación interna | ✅ |

El pipeline (`src/data/preprocessing_pipeline.py`) ejecuta las 5 etapas secuencialmente y puede reejecutarse en cualquier momento produciendo el mismo resultado.

---

# 10. Riesgos Identificados para Modeling

| Riesgo | Impacto | Fase de resolución |
|--------|---------|-------------------|
| Desbalance de clases (79/21) | Puede sesgar predicciones hacia CONSISTENTE | Modeling |
| Volumen limitado (649 registros clase positiva) | Riesgo de sobreajuste en CNN | Modeling |
| Variables categóricas requieren encoding | No pueden usarse directamente en CNN | Modeling |
| Variables numéricas requieren normalización | Escala afecta convergencia | Modeling |
| Variables textuales requieren embeddings/TF-IDF | No tokenizadas aún | Modeling |
| Subclases de tipo_alerta desbalanceadas (68-157) | Clasificación multi-clase difícil | Modeling |

---

# 11. Conclusiones

El dataset preparado durante la fase Data Preparation:

- ✅ Contiene 3,126 registros preservando el 100% del ground truth.
- ✅ Incluye 55 columnas (35 originales + 20 features derivadas).
- ✅ Mantiene integridad referencial completa.
- ✅ Contiene todas las variables necesarias para las 6 reglas de negocio.
- ✅ Contiene las variables necesarias para el modelo CNN 1D.
- ✅ Es reproducible mediante el pipeline automatizado.
- ✅ Está disponible en formatos CSV y Parquet.

**El dataset queda APROBADO para iniciar la fase de Modeling.**

---

# 12. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|--------|
| Dataset completo (3,126 registros x 55 columnas) | ✅ |
| Features consistentes y validadas | ✅ |
| Relaciones entre datasets correctas | ✅ |
| Reglas de negocio BR-01 a BR-06 satisfechas | ✅ |
| Variables para CNN 1D disponibles | ✅ |
| Variable objetivo presente | ✅ |
| Pipeline reproducible | ✅ |
| Dataset aprobado para Modeling | ✅ |

---

# 13. Relación con el siguiente Milestone

Este entregable habilita el inicio de la fase **Modeling** de la metodología ASUM-DM.

Durante Modeling se realizarán:

1. Implementación del Motor de Reglas de Negocio (BR-01 a BR-06).
2. Encoding de variables categóricas.
3. Normalización de variables numéricas.
4. Preparación de embeddings o TF-IDF para variables textuales.
5. Diseño de la arquitectura CNN 1D.
6. Entrenamiento del modelo.
7. Evaluación del desempeño.
8. Selección del enfoque definitivo (texto vs numérico).
9. Estrategia de balanceo de clases.

El dataset aprobado en este documento será la única fuente de datos utilizada durante toda la fase de Modeling.
