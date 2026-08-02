# BU-03 — Define Medical Billing Validation Business Rules

| Campo | Valor |
|--------|-------|
| Fase | Business Understanding |
| Milestone | Business Understanding |
| Issue | BU-03 |
| Estado | Completed |

---

# 1. Objetivo

Definir las reglas de negocio que utilizará el Motor de Validación para comparar la información registrada en la Historia Clínica con la información contenida en la Pre-factura.

Estas reglas representan la lógica central del Auditor Médico Digital y servirán como base para la implementación del motor de validación durante las fases posteriores del proyecto.

---

# 2. Relación con los Requisitos Funcionales

| Regla | Requisito |
|--------|-----------|
| BR-01 | FR-04 |
| BR-02 | FR-05 |
| BR-03 | FR-06 |
| BR-04 | FR-07 |
| BR-05 | FR-08 |
| BR-06 | FR-09 |

---

# 3. Reglas de Negocio

---

## BR-01 — Validación de Procedimientos Facturados

**Objetivo**

Garantizar que todos los procedimientos registrados clínicamente sean facturados.

**Campos involucrados**

- id_atencion
- codigo_cups
- codigo_cups_facturado

**Descripción**

Para una misma atención (`id_atencion`), todo procedimiento registrado en la Historia Clínica (`codigo_cups`) debe existir en la Pre-factura (`codigo_cups_facturado`).

**Escenario válido**

Todos los códigos CUPS registrados aparecen en la Pre-factura.

**Escenario de inconsistencia**

Existe al menos un código CUPS registrado que no fue facturado.

**Resultado esperado**

Generar una alerta de posible fuga de ingresos.

**Prioridad**

Alta

---

## BR-02 — Validación de Soporte Clínico

**Objetivo**

Garantizar que todo procedimiento facturado tenga respaldo clínico.

**Campos involucrados**

- soporte_clinico
- codigo_cups_facturado

**Descripción**

Todo procedimiento incluido en la Pre-factura debe contar con un soporte clínico registrado en la Historia Clínica.

**Escenario válido**

Existe soporte clínico para todos los procedimientos facturados.

**Escenario de inconsistencia**

Un procedimiento facturado no posee evidencia clínica.

**Resultado esperado**

Generar alerta por posible glosa.

**Prioridad**

Crítica

---

## BR-03 — Validación de Diagnósticos

**Objetivo**

Verificar la consistencia entre diagnósticos y procedimientos.

**Campos involucrados**

- diagnostico
- codigo_cups

> **Nota:** Esta regla depende de la disponibilidad de los campos de diagnóstico en los datos clínicos. Si dichos campos se encuentran en otro conjunto de datos, la implementación deberá integrarlos durante la fase de Data Preparation.

**Descripción**

Los procedimientos registrados deben ser coherentes con el diagnóstico asociado.

**Escenario válido**

El procedimiento corresponde al diagnóstico registrado.

**Escenario de inconsistencia**

Procedimiento incompatible con el diagnóstico.

**Resultado esperado**

Generar alerta para revisión médica.

**Prioridad**

Alta

---

## BR-04 — Validación de Tratamientos

**Objetivo**

Verificar que los tratamientos realizados sean considerados durante la facturación.

**Campos involucrados**

- tipo_item
- codigo_cups

**Descripción**

Todo tratamiento registrado en la Historia Clínica deberá reflejarse en la información administrativa correspondiente.

**Escenario válido**

Todos los tratamientos aparecen registrados para facturación.

**Escenario de inconsistencia**

Tratamientos registrados que no generan cobro.

**Resultado esperado**

Generar alerta de posible pérdida económica.

**Prioridad**

Media

---

## BR-05 — Validación de Laboratorios y Procedimientos

**Objetivo**

Detectar exámenes realizados que no fueron facturados.

**Campos involucrados**

- tipo_item
- codigo_cups
- codigo_cups_facturado

**Descripción**

Cuando `tipo_item` corresponda a un examen o procedimiento, deberá existir un servicio equivalente en la Pre-factura.

**Escenario válido**

Todos los laboratorios realizados fueron facturados.

**Escenario de inconsistencia**

Existe un examen realizado que no aparece en la Pre-factura.

**Resultado esperado**

Generar alerta por procedimiento omitido.

**Prioridad**

Alta

---

## BR-06 — Validación de Cantidades

**Objetivo**

Validar que la cantidad registrada clínicamente coincida con la cantidad facturada.

**Campos involucrados**

- cantidad_realizada
- cantidad_facturada

**Descripción**

Para cada procedimiento, la cantidad realizada deberá coincidir con la cantidad facturada.

**Escenario válido**

Las cantidades son iguales.

**Escenario de inconsistencia**

Las cantidades difieren.

**Resultado esperado**

Generar alerta por inconsistencia de facturación.

**Prioridad**

Media

---

# 4. Escenarios de Inconsistencia

| ID | Escenario | Regla |
|----|-----------|--------|
| INC-01 | Procedimiento registrado sin facturación | BR-01 |
| INC-02 | Procedimiento facturado sin soporte clínico | BR-02 |
| INC-03 | Diagnóstico incompatible | BR-03 |
| INC-04 | Tratamiento omitido en facturación | BR-04 |
| INC-05 | Laboratorio no facturado | BR-05 |
| INC-06 | Cantidades inconsistentes | BR-06 |

---

# 5. Trazabilidad

| Requisito | Regla | Campos involucrados |
|------------|-------|--------------------|
| FR-04 | BR-01 | id_atencion, codigo_cups, codigo_cups_facturado |
| FR-05 | BR-01 | codigo_cups |
| FR-06 | BR-02 | soporte_clinico |
| FR-07 | BR-03 | diagnostico |
| FR-08 | BR-05 | tipo_item |
| FR-09 | BR-06 | cantidad_realizada, cantidad_facturada |

---

# 6. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|---------|
| Reglas de negocio documentadas | ✅ |
| Escenarios de validación identificados | ✅ |
| Reglas trazables a requisitos del negocio | ✅ |

---

# 7. Relación con el siguiente Issue

Las reglas documentadas en este entregable serán utilizadas durante la fase **Analytic Approach** para diseñar el Motor de Validación y definir la arquitectura lógica del sistema.