# AA-03 — Define the Automated Validation Strategy

| Campo | Valor |
|--------|-------|
| Fase | Analytic Approach |
| Milestone | Analytic Approach |
| Issue | AA-03 |
| Estado | Completed |

---

# 1. Objetivo

Definir la estrategia completa de validación automatizada que utilizará el sistema para comparar la información registrada en la Historia Clínica con la Pre-factura, detectar inconsistencias antes del proceso de facturación y generar alertas que apoyen la auditoría médica.

Esta estrategia establece el comportamiento funcional del Motor de Validación y servirá como guía para su implementación durante las fases posteriores del proyecto.

---

# 2. Propósito de la Estrategia de Validación

La validación automatizada tiene como objetivo reducir las inconsistencias presentes en el proceso de facturación médica mediante un enfoque híbrido que combine:

- Reglas de negocio completamente trazables.
- Inteligencia Artificial como mecanismo de apoyo a la decisión.

El sistema no reemplaza al auditor médico; actúa como una herramienta de apoyo que automatiza la detección de inconsistencias y prioriza aquellas que requieren revisión.

---

# 3. Estrategia Híbrida de Validación

La solución estará compuesta por dos capas complementarias.

## 3.1 Capa de Reglas de Negocio

La primera capa ejecuta validaciones determinísticas utilizando las reglas definidas durante la fase **Business Understanding** (BU-03).

Estas reglas permiten detectar inconsistencias objetivas y completamente explicables entre la Historia Clínica y la Pre-factura.

Las reglas implementadas serán:

| Regla | Objetivo |
|--------|----------|
| BR-01 | Validar que todos los procedimientos registrados hayan sido facturados. |
| BR-02 | Verificar que toda facturación tenga soporte clínico. |
| BR-03 | Validar la coherencia entre diagnóstico y procedimiento realizado. |
| BR-04 | Verificar que los tratamientos registrados sean considerados para facturación. |
| BR-05 | Detectar laboratorios o procedimientos realizados que no fueron facturados. |
| BR-06 | Comparar la cantidad realizada contra la cantidad facturada. |

Cada regla genera un resultado completamente trazable y explicable.

---

## 3.2 Capa de Inteligencia Artificial

Una vez ejecutadas las reglas determinísticas, únicamente los casos que presenten inconsistencias serán enviados al componente de Inteligencia Artificial.

El modelo basado en **CNN con Transfer Learning** tendrá como objetivo complementar el proceso de auditoría mediante:

- Clasificación de inconsistencias.
- Priorización automática de alertas.
- Identificación de patrones repetitivos.
- Estimación de severidad.
- Apoyo a la toma de decisiones del auditor.

La IA no reemplaza las reglas de negocio.

Las reglas determinan **qué ocurrió**.

La IA ayuda a determinar **qué tan importante es actuar sobre dicha inconsistencia**.

---

# 4. Flujo General de Validación

El proceso completo de validación seguirá las siguientes etapas:

1. Recepción de la atención médica.
2. Integración de los cinco conjuntos de datos.
3. Construcción del Master Dataset.
4. Preprocesamiento de la información.
5. Ejecución de las reglas de negocio.
6. Identificación de inconsistencias.
7. Análisis complementario mediante Inteligencia Artificial.
8. Clasificación de severidad.
9. Generación de alertas.
10. Publicación de resultados mediante la API y el Dashboard.

---

# 5. Flujo del Motor de Validación

```text
                Datasets Fuente

01 Pacientes
02 Atenciones
03 Historia Clínica
04 Pre-factura
05 Cruce Validación

            │
            ▼

Integración de Datos

            │
            ▼

Construcción del Master Dataset

            │
            ▼

Preprocesamiento

            │
            ▼

Motor de Reglas de Negocio

BR-01
BR-02
BR-03
BR-04
BR-05
BR-06

            │
            ▼

¿Existe alguna inconsistencia?

      ┌──────────────┐
      │              │
     NO             SI

      │              │
      ▼              ▼

Registro        Modelo CNN
Consistente   + Transfer Learning

                    │
                    ▼

      Clasificación y Priorización

                    │
                    ▼

        Generación de Alertas

                    │
                    ▼

          REST API + Dashboard
```

---

# 6. Flujo de Decisión

La estrategia de decisión utilizada por el sistema será la siguiente:

## Paso 1

Construcción del Master Dataset utilizando la integración de los cinco datasets definidos durante el diseño de la arquitectura de datos.

## Paso 2

Aplicación de todas las reglas de negocio definidas en BU-03.

## Paso 3

Si ninguna regla detecta inconsistencias:

- El registro será clasificado como **CONSISTENTE**.

## Paso 4

Si una o más reglas detectan inconsistencias:

- El registro será enviado al modelo de Inteligencia Artificial.

## Paso 5

La IA clasificará:

- Tipo de inconsistencia.
- Nivel de severidad.
- Prioridad de atención.

## Paso 6

El sistema generará la alerta correspondiente y la enviará al Dashboard para revisión del auditor médico.

---

# 7. Categorías de Alertas

Las alertas generadas corresponden directamente a las reglas de negocio documentadas durante Business Understanding.

| Regla | Tipo de Alerta |
|--------|----------------|
| BR-01 | Missing Billed Procedure |
| BR-02 | Unsupported Billed Procedure |
| BR-03 | Missing / Inconsistent Diagnosis |
| BR-04 | Inconsistent Treatment |
| BR-05 | Unsupported Laboratory Exam |
| BR-06 | Quantity Mismatch |

Cada alerta incluirá una descripción detallada y un nivel de severidad.

---

# 8. Niveles de Severidad

Las alertas serán clasificadas según su impacto potencial sobre el proceso de facturación.

| Severidad | Descripción |
|------------|-------------|
| Alta | Posible fuga de ingresos o glosa crítica. |
| Media | Inconsistencia clínica o administrativa que requiere revisión. |
| Baja | Diferencias menores que no afectan significativamente la facturación. |
| Ninguna | Registro consistente. |

---

# 9. Salidas del Motor de Validación

Cada ejecución del proceso producirá un resultado estructurado compuesto por la siguiente información.

| Campo | Origen |
|--------|---------|
| id_atencion | 02_atenciones |
| id_prefactura | 04_prefactura |
| id_detalle_hc | 03_historia_clinica_detalle |
| resultado | Motor de Validación |
| tipo_alerta | Motor de Validación |
| severidad | Motor de Validación |
| descripcion_alerta | Motor de Validación |
| regla_aplicada | Motor de Validación |
| confianza_modelo | Modelo de IA |

---

# 10. Trazabilidad

La estrategia de validación mantiene consistencia con todos los artefactos desarrollados previamente.

| Documento | Relación |
|------------|----------|
| BU-02 Functional Requirements | Define los requisitos funcionales implementados por el Motor de Validación. |
| BU-03 Business Rules | Proporciona las reglas de negocio ejecutadas por el sistema. |
| BU-04 Project KPIs | Define las métricas utilizadas para evaluar el desempeño del proceso de validación. |
| AA-01 Solution Architecture | Define los componentes que ejecutan el proceso de validación. |
| AA-02 Data Architecture | Define la estructura del Master Dataset utilizado durante la validación. |

---

# 11. Beneficios de la Estrategia

La estrategia híbrida propuesta proporciona las siguientes ventajas:

- Automatiza el proceso de auditoría previo a la facturación.
- Reduce el riesgo de glosas por inconsistencias clínicas.
- Detecta procedimientos realizados que no fueron facturados.
- Prioriza automáticamente los casos de mayor impacto económico.
- Mantiene trazabilidad completa de todas las decisiones tomadas.
- Permite incorporar nuevas reglas de negocio sin modificar la arquitectura general.
- Complementa las reglas determinísticas mediante Inteligencia Artificial sin perder interpretabilidad.

---

# 12. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|--------|
| Flujo de validación documentado | ✅ |
| Estrategia basada en reglas definida | ✅ |
| Estrategia asistida por IA documentada | ✅ |
| Tipos de alertas definidos | ✅ |
| Salidas del proceso documentadas | ✅ |
| Estrategia lista para implementación | ✅ |

---

# 13. Relación con el siguiente Issue

La estrategia definida en este documento servirá como base para seleccionar y justificar el enfoque de Inteligencia Artificial que será utilizado durante la fase **AA-04**, donde se diseñará la arquitectura del modelo CNN con Transfer Learning y su integración con el Motor de Validación.