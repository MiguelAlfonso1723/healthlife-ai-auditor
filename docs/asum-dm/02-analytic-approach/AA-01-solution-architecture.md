# AA-01 — Design the Solution Architecture

| Campo | Valor |
|--------|-------|
| Fase | Analytic Approach |
| Milestone | Analytic Approach |
| Issue | AA-01 |
| Estado | Completed |

---

# 1. Objetivo

Diseñar la arquitectura de alto nivel del sistema de validación automatizada para Health & Life IPS SAS, definiendo los componentes principales, sus responsabilidades y el flujo completo de información desde los datos de entrada hasta la generación de alertas de validación.

La arquitectura debe satisfacer tanto los requisitos funcionales del proyecto como los lineamientos académicos del Capstone relacionados con el uso de modelos CNN preentrenados.

---

# 2. Arquitectura General

La solución adopta una arquitectura híbrida compuesta por dos mecanismos de validación complementarios:

- Motor de Reglas de Negocio.
- Modelo de Inteligencia Artificial basado en CNN + Transfer Learning.

Las reglas determinísticas serán resueltas mediante lógica de negocio, mientras que las inconsistencias que requieran interpretación clínica serán evaluadas mediante el modelo de IA.

---

# 3. Componentes del Sistema

## 3.1 Data Sources

Responsabilidad

Proveer la información necesaria para el proceso de validación.

Fuentes de datos

- 01_pacientes.csv
- 02_atenciones.csv
- 03_historia_clinica_detalle.csv
- 04_prefactura.csv
- 05_cruce_validacion.csv

Entradas

Información clínica y administrativa.

Salida

Datos preparados para el proceso ETL.

---

## 3.2 Data Processing

Responsabilidad

Realizar el proceso ETL.

Actividades

- Integración de datasets.
- Limpieza de datos.
- Tratamiento de valores nulos.
- Validación de tipos.
- Ingeniería de características.
- Preparación del conjunto de entrenamiento.

Salida

Dataset consolidado.

---

## 3.3 Validation Rules Engine

Responsabilidad

Ejecutar todas las reglas de negocio definidas durante Business Understanding.

Reglas implementadas

- BR-01
- BR-02
- BR-03
- BR-04
- BR-05
- BR-06

Validaciones realizadas

- Comparación de códigos CUPS.
- Comparación de cantidades.
- Verificación de soporte clínico.
- Validación de tratamientos.
- Validación de laboratorios.
- Generación de alertas determinísticas.

Salida

Alertas preliminares.

---

## 3.4 AI Model

Responsabilidad

Analizar inconsistencias que requieren interpretación clínica utilizando Inteligencia Artificial.

Modelo propuesto

CNN preentrenada utilizando Transfer Learning.

Entrada

Información textual proveniente de:

- descripcion_diagnostico
- descripcion
- descripcion_servicio_facturado

Proceso

1. Tokenización.
2. Embeddings.
3. CNN 1D preentrenada.
4. Fine Tuning mediante Transfer Learning.
5. Clasificación.

Salida

Clasificación de la consistencia clínica.

Clases esperadas

- CONSISTENTE
- NO_FACTURADO
- DIAGNOSTICO_NO_RELACIONADO
- SOPORTE_INSUFICIENTE
- Otras inconsistencias identificadas.

Justificación

El uso de CNN permite analizar relaciones semánticas entre diagnósticos y procedimientos clínicos, complementando las validaciones determinísticas realizadas por el Motor de Reglas.

---

## 3.5 REST API

Tecnología

FastAPI

Responsabilidad

Exponer los servicios del sistema.

Endpoints principales

- Validar atención médica.
- Obtener resultado de validación.
- Consultar alertas.
- Consultar estadísticas.

Salida

Respuestas JSON.

---

## 3.6 Dashboard

Tecnología

Streamlit

Responsabilidad

Visualizar resultados del proceso de validación.

Funciones

- Alertas detectadas.
- Indicadores del proyecto.
- Estadísticas.
- Historial de validaciones.

---

# 4. Flujo General del Sistema

1. Los archivos CSV son cargados desde el repositorio.

2. El módulo ETL integra toda la información.

3. Se generan las características necesarias.

4. El Motor de Reglas ejecuta las validaciones determinísticas.

5. Cuando una validación requiere interpretación clínica, los datos son enviados al modelo CNN.

6. La CNN determina si existe una inconsistencia clínica.

7. Los resultados son consolidados.

8. FastAPI expone los resultados.

9. Streamlit presenta la información al usuario.

---

# 5. Responsabilidades por Componente

| Componente | Responsabilidad |
|------------|-----------------|
| Data Sources | Proveer información clínica y administrativa |
| Data Processing | Integrar, limpiar y transformar datos |
| Validation Rules Engine | Ejecutar reglas de negocio |
| AI Model | Clasificar inconsistencias clínicas |
| REST API | Exponer servicios |
| Dashboard | Visualizar resultados |

---

# 6. Justificación Arquitectónica

Se adopta una arquitectura híbrida debido a que el problema presenta dos tipos de validaciones:

## Validaciones determinísticas

Son aquellas que pueden resolverse mediante reglas de negocio, por ejemplo:

- Comparación de códigos CUPS.
- Comparación de cantidades.
- Existencia de soporte clínico.

Estas validaciones ofrecen alta precisión y no requieren modelos de IA.

## Validaciones semánticas

Existen casos donde la consistencia entre un diagnóstico y un procedimiento no puede determinarse únicamente mediante comparaciones exactas.

Para estos escenarios se incorpora un modelo CNN preentrenado con Transfer Learning, encargado de analizar la relación semántica entre las descripciones clínicas.

Esta aproximación permite cumplir los requisitos académicos del Capstone sin sustituir las reglas de negocio que forman parte del dominio del problema.

---

# 7. Cumplimiento de Requisitos

| Requisito | Cumplimiento |
|------------|--------------|
| Data Sources | ✅ |
| Data Processing | ✅ |
| Validation Engine | ✅ |
| AI Model | ✅ |
| REST API | ✅ |
| Dashboard | ✅ |

---

# 8. Relación con la siguiente fase

La arquitectura definida servirá como base para la fase Data Understanding, donde se analizará la calidad de los datasets, las relaciones entre tablas y la viabilidad de las características necesarias para implementar el Motor de Reglas y el Modelo CNN.

---

# 9. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|---------|
| Diagrama de arquitectura definido | ✅ |
| Responsabilidades documentadas | ✅ |
| Flujo de datos documentado | ✅ |
| Arquitectura alineada con los requisitos | ✅ |