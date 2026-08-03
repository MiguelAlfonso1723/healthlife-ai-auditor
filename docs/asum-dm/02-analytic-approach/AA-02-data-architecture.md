# AA-02 — Design Data Architecture and Relationships

| Campo | Valor |
|--------|-------|
| Fase | Analytic Approach |
| Milestone | Analytic Approach |
| Issue | AA-02 |
| Estado | Completed |

---

# 1. Objetivo

Diseñar la arquitectura de datos de la solución definiendo las relaciones entre los datasets disponibles, las claves primarias y foráneas, así como la estructura lógica del **Master Dataset** que servirá como fuente de información para el Motor de Reglas de Negocio y el Modelo de Inteligencia Artificial.

Este diseño permitirá establecer una estrategia de integración consistente para las fases posteriores de Data Understanding, Data Preparation y Modeling.

---

# 2. Descripción de los Datasets

El proyecto utiliza cinco conjuntos de datos que representan diferentes etapas del proceso de atención médica y facturación.

| Dataset | Descripción |
|----------|-------------|
| **01_pacientes.csv** | Información demográfica y administrativa de los pacientes. |
| **02_atenciones.csv** | Registro de cada atención médica realizada al paciente. |
| **03_historia_clinica_detalle.csv** | Procedimientos, consultas, tratamientos y exámenes registrados durante la atención médica. |
| **04_prefactura.csv** | Servicios incluidos en la prefactura antes de su emisión definitiva. |
| **05_cruce_validacion.csv** | Resultado histórico del proceso de validación entre Historia Clínica y Prefactura. |

---

# 3. Relaciones entre los Datasets

Los datasets presentan una estructura jerárquica donde cada paciente puede tener múltiples atenciones y cada atención puede generar múltiples registros clínicos y de facturación.

Las relaciones definidas son las siguientes:

| Dataset origen | Dataset destino | Relación |
|----------------|-----------------|----------|
| Pacientes | Atenciones | 1 : N |
| Atenciones | Historia Clínica | 1 : N |
| Atenciones | Prefactura | 1 : N |
| Historia Clínica | Cruce Validación | 1 : N |
| Prefactura | Cruce Validación | 1 : N |

Esta estructura permite reconstruir el flujo completo desde la atención médica hasta la validación final de la facturación.

---

# 4. Claves Primarias

| Dataset | Primary Key |
|----------|-------------|
| Pacientes | id_paciente |
| Atenciones | id_atencion |
| Historia Clínica | id_detalle |
| Prefactura | id_prefactura |
| Cruce Validación | id_cruce |

---

# 5. Claves Foráneas

| Dataset | Foreign Key | Referencia |
|----------|-------------|------------|
| Atenciones | id_paciente | Pacientes |
| Historia Clínica | id_atencion | Atenciones |
| Prefactura | id_atencion | Atenciones |
| Prefactura | id_paciente | Pacientes |
| Cruce Validación | id_atencion | Atenciones |
| Cruce Validación | id_prefactura | Prefactura |
| Cruce Validación | id_detalle_hc | Historia Clínica |

---

# 6. Estrategia de Integración

La integración de los datos seguirá un proceso secuencial utilizando las claves definidas anteriormente.

El flujo lógico será el siguiente:

1. Cargar el dataset de pacientes.
2. Integrar las atenciones utilizando **id_paciente**.
3. Incorporar la Historia Clínica mediante **id_atencion**.
4. Incorporar la Prefactura mediante **id_atencion**.
5. Integrar los resultados históricos de validación utilizando **id_atencion**, **id_prefactura** e **id_detalle_hc**.

Esta estrategia permitirá construir un único conjunto de datos consolidado sin perder la trazabilidad de cada registro.

---

# 7. Diseño del Master Dataset

El Master Dataset será el conjunto de datos principal utilizado durante el proyecto.

Su propósito será centralizar toda la información necesaria para:

- Ejecutar el Motor de Reglas de Negocio.
- Entrenar el modelo de Inteligencia Artificial.
- Evaluar los resultados del sistema.
- Alimentar el Dashboard y la API.

---

## 7.1 Información Demográfica

- id_paciente
- edad
- sexo
- eps
- tipo_afiliacion
- ciudad

---

## 7.2 Información de la Atención

- id_atencion
- fecha_atencion
- tipo_atencion
- diagnostico_principal_cie10
- descripcion_diagnostico
- medico_tratante
- sede

---

## 7.3 Información Clínica

- id_detalle
- tipo_item
- codigo_cups
- descripcion
- cantidad_realizada
- soporte_clinico
- profesional_responsable

---

## 7.4 Información de Facturación

- id_prefactura
- codigo_cups_facturado
- descripcion_servicio_facturado
- cantidad_facturada
- valor_unitario
- valor_total
- fecha_facturacion

---

## 7.5 Información de Validación

- resultado
- tipo_alerta
- severidad
- descripcion_alerta

---

# 8. Uso del Master Dataset

El Master Dataset será utilizado por diferentes componentes de la arquitectura.

| Componente | Uso |
|------------|-----|
| Data Processing | Integración y preparación de datos |
| Validation Rules Engine | Comparación entre Historia Clínica y Prefactura |
| AI Validation Module | Entrenamiento y evaluación del modelo CNN |
| REST API | Consulta de resultados |
| Dashboard | Visualización de alertas e indicadores |

---

# 9. Justificación del Diseño

La construcción de un Master Dataset evita realizar múltiples consultas independientes durante el proceso de validación.

Este enfoque presenta las siguientes ventajas:

- Centraliza toda la información relevante en una única estructura.
- Reduce la complejidad del procesamiento.
- Facilita la implementación del Motor de Reglas.
- Simplifica el entrenamiento del modelo de IA.
- Mantiene la trazabilidad entre todos los registros clínicos y administrativos.

Además, la separación entre los datasets originales y el Master Dataset permite conservar la integridad de las fuentes de datos mientras se dispone de un conjunto consolidado para las tareas analíticas.

---

# 10. Relación con la Arquitectura de la Solución

El Master Dataset constituye la entrada principal del componente **Data Processing** definido en la arquitectura del sistema.

A partir de este conjunto consolidado se ejecutarán:

- El Motor de Reglas de Negocio.
- El Modelo CNN con Transfer Learning.
- La generación de alertas.
- La exposición de resultados mediante la API.
- La visualización de indicadores en el Dashboard.

---

# 11. Entregables

Los entregables asociados a este Issue son:

- `docs/asum-dm/02-analytic-approach/data-architecture.md`
- `docs/diagrams/AA-02-entity-relationship-diagram.drawio`
- `docs/diagrams/AA-02-entity-relationship-diagram.png`

---

# 12. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|---------|
| Relaciones entre datasets documentadas | ✅ |
| Claves primarias identificadas | ✅ |
| Claves foráneas identificadas | ✅ |
| Diseño del Master Dataset definido | ✅ |
| Diagrama ERD completado | ✅ |