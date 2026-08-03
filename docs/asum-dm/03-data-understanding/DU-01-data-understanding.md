# DU-01 — Analyze Source Datasets Structure

| Campo | Valor |
|--------|-------|
| Fase | Data Understanding |
| Milestone | Data Understanding |
| Issue | DU-01 |
| Estado | Completed |

---

# 1. Objetivo

Analizar la estructura de los datasets fuente utilizados por el sistema de validación automática de facturación médica para comprender su contenido, atributos, tipos de datos y función dentro del proceso analítico.

Este análisis constituye el primer paso de la fase **Data Understanding** de la metodología **ASUM-DM** y proporciona la base para las siguientes actividades de evaluación de calidad, preparación de datos y modelado.

---

# 2. Datasets Analizados

El proyecto utiliza cinco conjuntos de datos que representan las diferentes etapas del proceso de atención médica y facturación dentro de una IPS.

| Dataset | Registros | Columnas | Descripción |
|----------|----------:|---------:|-------------|
| 01_pacientes.csv | 300 | 7 | Información demográfica y administrativa de los pacientes. |
| 02_atenciones.csv | 1,200 | 9 | Información general de las atenciones médicas realizadas. |
| 03_historia_clinica_detalle.csv | 3,056 | 9 | Procedimientos, consultas, tratamientos y exámenes registrados durante cada atención. |
| 04_prefactura.csv | 2,974 | 10 | Servicios registrados para el proceso de facturación. |
| 05_cruce_validacion.csv | 3,126 | 8 | Resultados históricos del proceso de validación entre Historia Clínica y Pre-factura. |

---

# 3. Objetivo de cada Dataset

## 3.1 01_pacientes.csv

Contiene la información básica del paciente.

Información disponible:

- Identificador del paciente
- Tipo de documento
- Edad
- Sexo
- EPS
- Tipo de afiliación
- Ciudad

**Rol dentro del proyecto**

Representa la entidad principal sobre la cual se relacionan las diferentes atenciones médicas.

---

## 3.2 02_atenciones.csv

Registra cada atención realizada dentro de la IPS.

Información disponible:

- Identificador de atención
- Paciente asociado
- Fecha
- Tipo de atención
- Diagnóstico principal (CIE-10)
- Descripción del diagnóstico
- Médico tratante
- Sede
- EPS

**Rol dentro del proyecto**

Actúa como eje central que conecta la información clínica con la información administrativa.

---

## 3.3 03_historia_clinica_detalle.csv

Contiene el detalle clínico registrado durante cada atención.

Información disponible:

- Código CUPS
- Tipo de procedimiento
- Descripción
- Cantidad realizada
- Fecha de registro
- Soporte clínico
- Profesional responsable

**Rol dentro del proyecto**

Representa la evidencia clínica utilizada por el Motor de Reglas para validar la facturación.

---

## 3.4 04_prefactura.csv

Contiene los servicios registrados para ser facturados.

Información disponible:

- Código CUPS facturado
- Descripción del servicio
- Cantidad facturada
- Valor unitario
- Valor total
- Fecha de facturación
- EPS

**Rol dentro del proyecto**

Representa la información administrativa que será comparada con la Historia Clínica para detectar inconsistencias.

---

## 3.5 05_cruce_validacion.csv

Contiene el resultado histórico del proceso de validación.

Información disponible:

- Resultado de validación
- Tipo de alerta
- Severidad
- Descripción de la alerta

**Rol dentro del proyecto**

Proporciona el histórico de validaciones realizadas y será evaluado en fases posteriores como posible fuente de etiquetas (*ground truth*) para el entrenamiento y evaluación del modelo de Inteligencia Artificial.

---

# 4. Identificadores Principales

Durante el análisis estructural se identificaron los siguientes identificadores principales.

| Dataset | Llave Primaria |
|----------|----------------|
| 01_pacientes | id_paciente |
| 02_atenciones | id_atencion |
| 03_historia_clinica_detalle | id_detalle |
| 04_prefactura | id_prefactura |
| 05_cruce_validacion | id_cruce |

También se identificaron las siguientes relaciones mediante llaves foráneas.

| Dataset | Llaves Foráneas |
|----------|-----------------|
| 02_atenciones | id_paciente |
| 03_historia_clinica_detalle | id_atencion |
| 04_prefactura | id_atencion, id_paciente |
| 05_cruce_validacion | id_atencion, id_prefactura, id_detalle_hc |

---

# 5. Relación entre los Datasets

La estructura observada confirma el modelo de datos definido durante la fase **Analytic Approach**.

Las relaciones principales son:

- Pacientes → Atenciones
- Atenciones → Historia Clínica
- Atenciones → Pre-factura
- Historia Clínica → Cruce de Validación
- Pre-factura → Cruce de Validación

Estas relaciones permiten reconstruir completamente el flujo de información desde el registro clínico hasta la validación final de la facturación.

---

# 6. Análisis Estructural Realizado

El notebook **01_data_understanding.ipynb** ejecuta automáticamente el análisis estructural de cada dataset.

Las actividades realizadas incluyen:

- Carga automática de los cinco datasets.
- Identificación del número de registros y columnas.
- Inspección de tipos de datos.
- Identificación de posibles llaves primarias.
- Identificación de posibles llaves foráneas.
- Análisis de valores nulos.
- Análisis de valores únicos.
- Detección de registros duplicados.
- Cálculo del uso de memoria.
- Generación de un resumen consolidado de cada dataset.

Este análisis constituye la línea base para las actividades posteriores de evaluación de calidad y preparación de datos.

---

# 7. Hallazgos Iniciales

El análisis estructural permitió identificar las siguientes características generales:

- Los cinco datasets presentan una estructura claramente definida y consistente con el proceso de negocio documentado durante Business Understanding.
- Cada conjunto de datos posee un identificador principal que facilita su integración dentro del modelo relacional.
- Existen relaciones lógicas entre los datasets mediante identificadores compartidos (`id_paciente`, `id_atencion`, `id_prefactura` e `id_detalle_hc`).
- El volumen de información disponible es suficiente para iniciar el análisis exploratorio y las siguientes fases del proyecto.
- El dataset **05_cruce_validacion.csv** representa un candidato importante para actuar como fuente de etiquetas históricas durante la fase de Modeling, aspecto que será evaluado en mayor profundidad en los siguientes issues de Data Understanding.

---

# 8. Conclusiones

El análisis confirma que la estructura de los cinco datasets es coherente con la arquitectura de datos diseñada durante la fase **Analytic Approach**.

La información disponible permite reconstruir el proceso completo de atención médica, documentar la evidencia clínica, relacionarla con la información de facturación y conocer el resultado histórico de las validaciones.

Estos resultados proporcionan una base sólida para continuar con la evaluación de calidad de los datos, la identificación de inconsistencias y la preparación del Master Dataset que será utilizado durante las fases posteriores del proyecto.

---

# 9. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|---------|
| Todos los datasets cargados correctamente | ✅ |
| Estructura de los datasets documentada | ✅ |
| Identificadores principales identificados | ✅ |
| Resumen estructural completado | ✅ |

---

# 10. Relación con el siguiente Issue

La información obtenida en este análisis será utilizada en el siguiente issue de **Data Understanding** para evaluar la calidad de los datos, identificar valores faltantes, registros duplicados, inconsistencias y otros aspectos que puedan afectar el desempeño del sistema de validación automática y del modelo de Inteligencia Artificial.