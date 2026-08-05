# BU-04 — Define Business KPIs and Project Success Metrics

| Campo | Valor |
|--------|-------|
| Fase | Business Understanding |
| Milestone | Business Understanding |
| Issue | BU-04 |
| Estado | Completed |

---

# 1. Objetivo

Definir los indicadores clave de desempeño (KPIs) y las métricas de éxito que permitirán evaluar el impacto del sistema de validación automatizada de Health & Life IPS SAS.

Estos indicadores servirán para medir el desempeño del modelo de Inteligencia Artificial, la eficiencia del motor de validación y el impacto esperado sobre el proceso de facturación médica.

---

# 2. KPIs de Negocio

Los siguientes indicadores permitirán medir el impacto del sistema desde la perspectiva del negocio.

| ID | KPI | Descripción | Objetivo |
|----|-----|-------------|----------|
| BKPI-01 | Revenue Leakage Detection Rate | Porcentaje de procedimientos no facturados detectados automáticamente. | Maximizar |
| BKPI-02 | Billing Consistency Rate | Porcentaje de registros clínicos consistentes con la Pre-factura. | Maximizar |
| BKPI-03 | Inconsistency Detection Rate | Porcentaje de inconsistencias identificadas antes de emitir la factura. | Maximizar |
| BKPI-04 | Manual Audit Reduction | Reducción estimada de revisiones manuales requeridas por el auditor. | Maximizar |
| BKPI-05 | Billing Validation Coverage | Porcentaje de atenciones procesadas automáticamente por el sistema. | Maximizar |

---

# 3. KPIs Técnicos

Estos indicadores evaluarán el rendimiento técnico de la solución.

| ID | KPI | Descripción | Objetivo |
|----|-----|-------------|----------|
| TKPI-01 | Validation Execution Time | Tiempo requerido para validar una atención médica. | Minimizar |
| TKPI-02 | Processing Throughput | Número de registros procesados por minuto. | Maximizar |
| TKPI-03 | API Response Time | Tiempo promedio de respuesta de la API. | Minimizar |
| TKPI-04 | Validation Success Rate | Porcentaje de validaciones ejecutadas sin errores. | Maximizar |
| TKPI-05 | Dashboard Availability | Disponibilidad del módulo de visualización durante las pruebas. | Maximizar |

---

# 4. Métricas de Evaluación del Modelo

El desempeño del modelo de Inteligencia Artificial será evaluado utilizando métricas estándar de clasificación.

| Métrica | Descripción | Objetivo |
|----------|-------------|----------|
| Accuracy | Proporción de predicciones correctas sobre el total de casos. | Maximizar |
| Precision | Proporción de inconsistencias detectadas que realmente son inconsistencias. | Maximizar |
| Recall | Capacidad del modelo para detectar todas las inconsistencias existentes. | Maximizar |
| F1 Score | Media armónica entre Precision y Recall. | Maximizar |

Estas métricas permitirán comparar diferentes modelos durante la fase de Modeling y seleccionar la alternativa con mejor desempeño.

---

# 5. Impacto Esperado del Proyecto

Se espera que la solución contribuya a mejorar el proceso de validación médica mediante:

- Detección temprana de inconsistencias entre Historia Clínica y Pre-factura.
- Reducción de posibles fugas de ingresos ocasionadas por procedimientos no facturados.
- Disminución del tiempo dedicado a auditorías manuales.
- Mayor consistencia entre la información clínica y administrativa.
- Apoyo al auditor médico mediante alertas preventivas antes de la emisión de la factura.

---

# 6. Relación entre KPIs y Requisitos del Proyecto

| KPI | Requisitos relacionados |
|-----|--------------------------|
| Revenue Leakage Detection Rate | FR-05, FR-08 |
| Billing Consistency Rate | FR-04 |
| Inconsistency Detection Rate | FR-08, FR-09 |
| Validation Execution Time | NFR-01, NFR-07 |
| Accuracy | FR-09 |
| Precision | FR-09 |
| Recall | FR-09 |
| F1 Score | FR-09 |

---

# 7. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|---------|
| Accuracy documentado | ✅ |
| Precision documentado | ✅ |
| Recall documentado | ✅ |
| F1 Score documentado | ✅ |
| Revenue Leakage Detection documentado | ✅ |
| Validation Execution Time documentado | ✅ |

---

# 8. Relación con el siguiente Issue

Los KPIs definidos en este documento servirán como criterios de evaluación durante las fases de **Modeling** y **Evaluation**, permitiendo medir objetivamente el desempeño del sistema desarrollado y verificar el cumplimiento de los objetivos del proyecto.