# AA-04 — Select Analytical Techniques and AI Approach

| Campo | Valor |
|--------|-------|
| Fase | Analytic Approach |
| Milestone | Analytic Approach |
| Issue | AA-04 |
| Estado | Completed |

---

# 1. Objetivo

Seleccionar y justificar el enfoque analítico que será utilizado para detectar inconsistencias entre la Historia Clínica y la Pre-factura, considerando las características de los datos disponibles, los objetivos del proyecto y los lineamientos establecidos para el Capstone.

El enfoque seleccionado deberá proporcionar una solución explicable, escalable y capaz de asistir al auditor médico durante el proceso de validación.

---

# 2. Análisis del Problema

El proceso de auditoría médica presenta dos características principales:

- Existen reglas de negocio claramente definidas que determinan cuándo una facturación es inconsistente.
- También existen patrones complejos difíciles de identificar mediante reglas estáticas, especialmente cuando múltiples variables interactúan entre sí.

Por esta razón, una única técnica analítica no resulta suficiente para resolver completamente el problema.

Se requiere una estrategia híbrida que combine validaciones determinísticas con modelos de Inteligencia Artificial.

---

# 3. Evaluación de Alternativas Analíticas

Se evaluaron diferentes enfoques considerando:

- Naturaleza de los datos.
- Interpretabilidad.
- Facilidad de implementación.
- Escalabilidad.
- Compatibilidad con los requisitos del proyecto.

## 3.1 Validación Basada en Reglas

### Descripción

Consiste en implementar reglas determinísticas derivadas del conocimiento del dominio médico.

### Ventajas

- Totalmente explicable.
- Alta trazabilidad.
- Fácil mantenimiento.
- Resultados reproducibles.

### Desventajas

- No aprende nuevos patrones.
- Requiere actualización manual cuando cambian las reglas del negocio.

**Resultado**

✅ Seleccionada como primera capa de validación.

---

## 3.2 Árboles de Decisión

### Ventajas

- Interpretables.
- Simples de entrenar.

### Desventajas

- Limitados para relaciones complejas.
- Riesgo de sobreajuste.

**Resultado**

❌ No seleccionado.

---

## 3.3 Random Forest

### Ventajas

- Buen desempeño en datos tabulares.
- Reduce el sobreajuste.

### Desventajas

- Menor interpretabilidad.
- Mayor complejidad computacional.

**Resultado**

❌ No seleccionado.

---

## 3.4 XGBoost

### Ventajas

- Excelente desempeño en problemas tabulares.
- Alta precisión.

### Desventajas

- No cumple con el enfoque de Deep Learning requerido por el Capstone.
- Reduce la interpretabilidad del proceso de validación.

**Resultado**

❌ No seleccionado.

---

## 3.5 Redes Neuronales Multicapa (MLP)

### Ventajas

- Aprende relaciones no lineales.
- Flexible para distintos tipos de datos.

### Desventajas

- No aprovecha relaciones locales entre variables.
- Menor capacidad para extraer patrones estructurados.

**Resultado**

❌ No seleccionado.

---

## 3.6 CNN 1D con Transfer Learning

### Descripción

Cada registro del Master Dataset será transformado en un vector numérico de características mediante procesos de codificación y preprocesamiento.

Este vector será utilizado como entrada para una red convolucional unidimensional (1D-CNN), permitiendo aprender patrones locales entre variables relacionadas.

### Ventajas

- Compatible con TensorFlow/Keras.
- Cumple los lineamientos del Capstone.
- Aprende relaciones complejas entre variables.
- Escalable para futuras ampliaciones.

### Desventajas

- Mayor complejidad de entrenamiento.
- Requiere un proceso adecuado de preparación de datos.

**Resultado**

✅ Seleccionada.

---

# 4. Comparación de Alternativas

| Técnica | Interpretabilidad | Precisión Esperada | Escalabilidad | Seleccionada |
|----------|------------------|-------------------|---------------|--------------|
| Rule-Based | Alta | Alta | Alta | ✅ |
| Decision Tree | Alta | Media | Media | ❌ |
| Random Forest | Media | Alta | Alta | ❌ |
| XGBoost | Baja | Muy Alta | Alta | ❌ |
| MLP | Media | Alta | Alta | ❌ |
| CNN 1D + Transfer Learning | Media | Alta | Muy Alta | ✅ |

---

# 5. Enfoque Analítico Seleccionado

El proyecto implementará una estrategia híbrida compuesta por dos componentes complementarios.

## 5.1 Motor de Reglas de Negocio

Responsable de ejecutar las reglas definidas durante la fase Business Understanding.

Estas reglas permiten detectar inconsistencias objetivas entre la Historia Clínica y la Pre-factura.

Las reglas implementadas corresponden a:

- BR-01
- BR-02
- BR-03
- BR-04
- BR-05
- BR-06

---

## 5.2 Modelo de Inteligencia Artificial

Una vez detectadas las inconsistencias mediante el Motor de Reglas, el modelo CNN con Transfer Learning realizará un análisis complementario.

El modelo tendrá como objetivo:

- Clasificar inconsistencias.
- Priorizar alertas.
- Estimar niveles de severidad.
- Identificar patrones históricos similares.
- Apoyar la toma de decisiones del auditor.

La Inteligencia Artificial no reemplaza las reglas de negocio.

Las reglas identifican las inconsistencias.

La IA ayuda a interpretar su importancia.

---

# 6. Arquitectura Analítica

El flujo analítico será el siguiente:

```text
Datasets Fuente

        │

        ▼

Master Dataset

        │

        ▼

Preprocesamiento

        │

        ▼

Motor de Reglas

(BR-01 ... BR-06)

        │

        ▼

¿Existe inconsistencia?

      ┌─────────────┐
      │             │
     NO            SI

      │             │

      ▼             ▼

 Registro      CNN + Transfer Learning

                     │

                     ▼

      Clasificación de Alertas

                     │

                     ▼

      Dashboard + REST API
```

---

# 7. Estrategia de Transfer Learning

El proyecto utilizará TensorFlow/Keras para implementar una arquitectura CNN unidimensional.

La estrategia de Transfer Learning será definida durante la fase de Modeling. Se evaluará el uso de pesos preentrenados o estrategias de reutilización de conocimiento compatibles con arquitecturas CNN 1D implementadas en TensorFlow/Keras, de acuerdo con las características finales del conjunto de datos y los requerimientos del proyecto.

La decisión específica sobre la estrategia de entrenamiento será tomada durante la fase de Modeling, una vez finalizada la preparación de los datos.

---

# 8. Métricas de Evaluación

El desempeño del modelo será evaluado utilizando métricas de clasificación.

## Métricas del Modelo

| Métrica | Objetivo |
|----------|----------|
| Accuracy | Maximizar |
| Precision | Maximizar |
| Recall | Maximizar |
| F1-Score | Maximizar |

---

## Métricas del Sistema

| Métrica | Objetivo |
|----------|----------|
| Validation Execution Time | Minimizar |
| Revenue Leakage Detection Rate | Maximizar |
| False Positive Rate | Minimizar |
| False Negative Rate | Minimizar |

Estas métricas mantienen trazabilidad con los KPIs definidos durante Business Understanding.

---

# 9. Justificación del Enfoque Seleccionado

La estrategia híbrida proporciona un equilibrio entre interpretabilidad y capacidad predictiva.

El Motor de Reglas garantiza que todas las decisiones sean trazables y explicables conforme a las reglas de negocio definidas por la IPS.

La CNN con Transfer Learning permite analizar patrones complejos presentes en los datos históricos que no pueden modelarse fácilmente mediante reglas estáticas.

Este enfoque facilita la incorporación de nuevos criterios de validación sin modificar la arquitectura general del sistema.

Además, satisface los lineamientos académicos establecidos para el Capstone al incorporar técnicas de Deep Learning basadas en CNN.

---

# 10. Trazabilidad

| Documento | Relación |
|------------|----------|
| BU-02 Functional Requirements | Define los requisitos funcionales implementados por el sistema. |
| BU-03 Business Rules | Proporciona las reglas ejecutadas por el Motor de Validación. |
| BU-04 Project KPIs | Define las métricas de evaluación. |
| AA-01 Solution Architecture | Define la arquitectura general del sistema. |
| AA-02 Data Architecture | Define la estructura del Master Dataset. |
| AA-03 Validation Strategy | Define el flujo de validación que implementará este enfoque analítico. |

---

# 11. Beneficios del Enfoque Seleccionado

La estrategia propuesta ofrece los siguientes beneficios:

- Combina reglas de negocio con técnicas de Inteligencia Artificial.
- Mantiene interpretabilidad y trazabilidad en las decisiones.
- Reduce el riesgo de inconsistencias en la facturación médica.
- Permite priorizar automáticamente las alertas generadas.
- Facilita la escalabilidad del sistema mediante nuevos modelos o reglas.
- Cumple con los lineamientos del Capstone respecto al uso de modelos CNN y Transfer Learning.

---

# 12. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|--------|
| Enfoque analítico seleccionado | ✅ |
| Estrategia de IA documentada | ✅ |
| Métricas de evaluación definidas | ✅ |
| Justificación técnica documentada | ✅ |

---

# 13. Relación con el siguiente Issue

El enfoque analítico definido servirá como base para la selección de tecnologías, herramientas y frameworks que serán utilizados durante la implementación del sistema en el siguiente entregable de la fase **Analytic Approach**.