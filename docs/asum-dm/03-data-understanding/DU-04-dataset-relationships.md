# DU-04 — Análisis de Relaciones entre los Conjuntos de Datos

| Campo | Valor |
|--------|-------|
| Fase | Data Understanding |
| Milestone | Data Understanding |
| Issue | DU-04 |
| Estado | Completed |

---

# 1. Objetivo

Analizar las relaciones existentes entre los cinco conjuntos de datos del proyecto y validar cómo pueden integrarse para soportar el proceso automatizado de validación entre la Historia Clínica y la Pre-factura.

Este análisis confirma la arquitectura de datos definida durante la fase **Analytic Approach** y establece la estrategia de uniones (*Join Strategy*) que será utilizada posteriormente para construir el **Master Dataset** durante la fase de **Data Preparation**.

---

# 2. Conjuntos de Datos Analizados

| Dataset | Identificador Principal |
|----------|-------------------------|
| 01_pacientes | id_paciente |
| 02_atenciones | id_atencion |
| 03_historia_clinica_detalle | id_detalle |
| 04_prefactura | id_prefactura |
| 05_cruce_validacion | id_cruce |

---

# 3. Relaciones entre los Datasets

Las relaciones propuestas durante el diseño de la arquitectura de datos fueron verificadas utilizando los datos reales.

| Dataset Padre | Dataset Hijo | Relación | Campo de Unión |
|---------------|--------------|----------|----------------|
| Pacientes | Atenciones | 1 : N | id_paciente |
| Atenciones | Historia Clínica | 1 : N | id_atencion |
| Atenciones | Pre-factura | 1 : N | id_atencion |
| Atenciones | Cruce de Validación | 1 : N | id_atencion |
| Historia Clínica | Cruce de Validación | 1 : N | id_detalle |
| Pre-factura | Cruce de Validación | 1 : N | id_prefactura |

Estas relaciones garantizan la trazabilidad entre la información clínica y administrativa utilizada por el Motor de Validación.

---

# 4. Validación de Integridad Referencial

Se verificó la integridad de todas las relaciones definidas mediante claves foráneas.

## Resultados

| Validación | Resultado |
|------------|-----------|
| Llaves foráneas inválidas | No se encontraron |
| Registros huérfanos | No se encontraron |
| Relaciones rotas | No se encontraron |

Los cinco datasets presentan una integridad referencial completa.

---

# 5. Análisis de Cardinalidad

El análisis de cardinalidad confirmó el comportamiento esperado del proceso de facturación médica.

| Relación | Cardinalidad |
|-----------|--------------|
| Paciente → Atención | Uno a Muchos |
| Atención → Historia Clínica | Uno a Muchos |
| Atención → Pre-factura | Uno a Muchos |
| Atención → Cruce de Validación | Uno a Muchos |
| Historia Clínica → Cruce de Validación | Uno a Muchos |
| Pre-factura → Cruce de Validación | Uno a Muchos |

Las cardinalidades observadas son consistentes con el modelo de datos definido durante el Issue **AA-02**.

---

# 6. Estrategia de Uniones (Join Strategy)

Con base en el análisis realizado, se propone la siguiente estrategia para construir el **Master Dataset**.

## Paso 1

Utilizar **05_cruce_validacion** como dataset base, ya que contiene el resultado histórico de la validación (`resultado`), el cual será utilizado como variable objetivo durante el entrenamiento del modelo de Inteligencia Artificial.

## Paso 2

Realizar un **INNER JOIN** con **02_atenciones** utilizando el campo:

```
id_atencion
```

Esto garantiza que cada registro de validación esté asociado con la atención médica correspondiente.

## Paso 3

Realizar **LEFT JOIN** con los siguientes datasets:

- 01_pacientes
- 03_historia_clinica_detalle
- 04_prefactura

Esta estrategia permite conservar todos los registros históricos de validación mientras se incorpora la información clínica, administrativa y del paciente.

## Estrategia Final

```
05_cruce_validacion
        │
INNER JOIN
        │
02_atenciones
        │
 ├── LEFT JOIN → 01_pacientes
 ├── LEFT JOIN → 03_historia_clinica_detalle
 └── LEFT JOIN → 04_prefactura
```

---

# 7. Cobertura de las Relaciones

La estrategia de uniones fue validada utilizando los cinco datasets.

## Resultados

- Cobertura completa de las atenciones médicas.
- No se detectó pérdida de información durante las uniones.
- Todos los registros de validación pueden relacionarse correctamente con su atención correspondiente.

Lo anterior confirma que la estrategia propuesta es adecuada para la construcción del Master Dataset.

---

# 8. Relaciones Críticas del Sistema

Las siguientes relaciones son indispensables para cada componente de la solución.

| Componente | Relaciones Necesarias |
|------------|----------------------|
| Motor de Reglas | Atenciones ↔ Historia Clínica ↔ Pre-factura |
| Modelo CNN 1D | Cruce de Validación + Historia Clínica + Pre-factura |
| API REST | Master Dataset |
| Dashboard | Master Dataset |

---

# 9. Preparación del Master Dataset

El análisis permitió identificar los atributos necesarios para construir el conjunto de datos integrado.

Resumen del análisis:

- Aproximadamente **28 columnas** deben conservarse.
- **4 columnas** presentan información redundante y podrán consolidarse.
- **3 columnas** pueden eliminarse por duplicidad de información.
- **2 columnas** deberán evaluarse durante la fase de Data Preparation antes de tomar una decisión definitiva.

La selección final de variables será realizada durante la construcción del Master Dataset.

---

# 10. Principales Hallazgos

## Fortalezas

- Integridad referencial completa.
- No existen registros huérfanos.
- Relaciones Uno a Muchos consistentes.
- Cobertura total de las uniones.
- Identificadores únicos correctamente definidos.

## Riesgos

No se identificaron problemas críticos relacionados con la estructura relacional de los datos.

El principal desafío para las siguientes fases será seleccionar las variables más relevantes para el entrenamiento del modelo de Inteligencia Artificial.

---

# 11. Conclusiones

Los cinco datasets presentan una estructura relacional sólida y consistente para soportar el proceso automatizado de auditoría médica.

La estrategia de uniones propuesta garantiza la trazabilidad completa entre pacientes, atenciones, historia clínica, pre-factura y resultados históricos de validación.

Asimismo, el análisis confirma que la arquitectura de datos definida durante **Analytic Approach** se encuentra completamente respaldada por los datos reales del proyecto.

En consecuencia, el proyecto se encuentra preparado para iniciar la construcción del **Master Dataset** durante la fase de **Data Preparation**.

---

# 12. Verificación de los Criterios de Aceptación

| Criterio | Estado |
|-----------|--------|
| Relaciones entre datasets documentadas | ✅ |
| Claves de unión validadas | ✅ |
| Diagrama de relaciones completado | ✅ |

---

# 13. Relación con el Siguiente Issue

La estrategia de uniones documentada en este entregable servirá como base para construir el **Master Dataset**, el cual será utilizado por el Motor de Reglas y el modelo CNN 1D durante las fases de **Data Preparation** y **Modeling**.