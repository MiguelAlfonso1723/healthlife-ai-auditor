# BU-01 — Analyze Business Problem & Current Healthcare Billing Process

| Campo | Valor |
|--------|-------|
| Fase | Business Understanding |
| Milestone | Business Understanding |
| Issue | BU-01 |
| Estado | Completed |

---

# 1. Objetivo

Analizar y documentar el proceso empresarial actual de Health & Life IPS SAS para comprender el problema que debe resolver el proyecto.

El análisis describe el flujo de información desde la atención del paciente hasta la emisión de la factura médica, identificando los puntos donde actualmente pueden producirse inconsistencias, fugas de ingresos, glosas y procesos de auditoría manual.

Este documento constituye la base para las siguientes fases de la metodología ASUM-DM.

---

# 2. Comprensión del reto de Health & Life IPS

## Contexto

Health & Life IPS SAS plantea el desarrollo de una solución capaz de validar automáticamente la coherencia entre la información registrada en la Historia Clínica y la información incluida en la Pre-factura antes de emitir el cobro al asegurador o entidad pagadora.

Actualmente este proceso depende principalmente de revisiones manuales realizadas por auditores médicos, lo que incrementa el tiempo de validación y aumenta el riesgo de errores humanos.

La organización busca desarrollar un **Auditor Médico Digital** que permita detectar inconsistencias de manera preventiva antes de la emisión de la factura definitiva.

## Problema identificado

Actualmente no existe un mecanismo automatizado que permita verificar que:

- Todos los procedimientos realizados fueron facturados.
- Todos los procedimientos facturados poseen soporte clínico.
- Los diagnósticos son consistentes con los procedimientos realizados.
- Los tratamientos registrados coinciden con la información administrativa.
- Los exámenes realizados fueron incluidos correctamente en la pre-factura.

Como consecuencia, pueden generarse pérdidas económicas, glosas y un incremento considerable del trabajo manual de auditoría.

---

# 3. Flujo actual del proceso de facturación sanitaria

A partir de la descripción del reto, el flujo general del proceso puede resumirse de la siguiente manera.

| Etapa | Responsable | Resultado |
|--------|-------------|-----------|
| Atención del paciente | Personal asistencial | Prestación del servicio médico |
| Registro clínico | Profesional de salud | Historia Clínica actualizada |
| Consolidación administrativa | Área de facturación | Generación de la Pre-factura |
| Validación manual | Auditor médico | Comparación entre Historia Clínica y Pre-factura |
| Corrección de inconsistencias | Auditor / Facturación | Ajustes cuando existen diferencias |
| Facturación | Área administrativa | Emisión de la factura definitiva |

---

# 4. Generación de la información clínica

La información clínica se origina durante la atención del paciente y es registrada dentro de la Historia Clínica por el personal asistencial.

Entre los principales elementos registrados se encuentran:

- Diagnósticos médicos.
- Procedimientos realizados.
- Tratamientos aplicados.
- Medicamentos administrados.
- Exámenes solicitados o realizados.
- Evoluciones clínicas.

Esta información representa el soporte clínico que posteriormente debe justificar todos los servicios incluidos en la facturación.

---

# 5. Generación de la Pre-factura

La Pre-factura es elaborada por el área administrativa a partir de los servicios prestados durante la atención del paciente.

Su propósito es consolidar los procedimientos y servicios que posteriormente serán cobrados.

Antes de emitir la factura definitiva, la Pre-factura debe corresponder completamente con la información registrada en la Historia Clínica.

---

# 6. Proceso actual de validación manual

Actualmente la validación consiste en una revisión realizada por un auditor médico.

El proceso general comprende las siguientes actividades:

1. Consultar la Historia Clínica del paciente.
2. Revisar la Pre-factura generada.
3. Comparar procedimientos registrados y procedimientos facturados.
4. Verificar que los diagnósticos soporten los procedimientos cobrados.
5. Confirmar que los exámenes realizados hayan sido facturados.
6. Detectar diferencias o inconsistencias.
7. Solicitar correcciones antes de emitir la factura definitiva.

Este proceso depende principalmente de la experiencia del auditor y requiere una revisión manual de grandes volúmenes de información.

---

# 7. Puntos de dolor del negocio

Durante el análisis del reto se identifican los siguientes problemas empresariales.

| Punto de dolor | Impacto |
|----------------|---------|
| Validación manual de la información | Alto consumo de tiempo operativo |
| Alto volumen de historias clínicas | Incremento del riesgo de error humano |
| Procedimientos no facturados | Pérdida directa de ingresos |
| Procedimientos sin soporte clínico | Glosas y rechazos de facturación |
| Auditorías posteriores a la facturación | Incremento de costos operativos |
| Correcciones tardías | Retrasos en el proceso de cobro |

---

# 8. Puntos de fuga de ingresos

Las principales fuentes potenciales de pérdida económica identificadas son:

- Procedimientos registrados en la Historia Clínica que no aparecen en la Pre-factura.
- Exámenes realizados que no fueron facturados.
- Tratamientos ejecutados pero omitidos durante la facturación.
- Rechazo de cuentas médicas por falta de soporte clínico.
- Glosas ocasionadas por inconsistencias entre información clínica y administrativa.

Estas situaciones afectan directamente el flujo de ingresos de la organización.

---

# 9. Diagrama de flujo del proceso actual

El diagrama de alto nivel del proceso se encuentra en:

`docs/diagrams/BU-01-healthcare-billing-process.mmd`

---

# 10. Conclusiones

El análisis evidencia que el principal problema de Health & Life IPS SAS no corresponde a la generación de la Historia Clínica ni a la generación de la Pre-factura de manera independiente, sino a la ausencia de un mecanismo automatizado que valide la consistencia entre ambas fuentes de información antes de la emisión de la factura.

La dependencia de procesos manuales incrementa el riesgo de errores, pérdidas económicas y glosas, justificando el desarrollo de un sistema de validación automatizada que apoye el trabajo del auditor médico mediante reglas de negocio e Inteligencia Artificial.

---

# 11. Verificación de criterios de aceptación

| Criterio | Estado |
|----------|---------|
| Flujo de trabajo actual documentado | ✅ |
| Problema principal del negocio explicado | ✅ |
| Puntos de fuga de ingresos identificados | ✅ |
| Proceso actual de validación manual documentado | ✅ |

---

# 12. Relación con el siguiente Issue

Los resultados obtenidos en este análisis servirán como base para identificar los actores involucrados, definir los objetivos del negocio y establecer los indicadores que medirán el éxito del proyecto durante los siguientes Issues de la fase **Business Understanding**.