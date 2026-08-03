# AA-05 — Define Technical Stack and Development Strategy

| Campo | Valor |
|--------|-------|
| Fase | Analytic Approach |
| Milestone | Analytic Approach |
| Issue | AA-05 |
| Estado | Completed |

---

# 1. Objetivo

Definir el stack tecnológico y la estrategia de desarrollo que serán utilizados durante todo el proyecto, estableciendo una referencia técnica común para garantizar consistencia en la implementación, integración y despliegue del sistema.

Este documento servirá como guía para el equipo de desarrollo durante las fases de Data Understanding, Data Preparation, Modeling, Evaluation y Deployment.

---

# 2. Principios Tecnológicos

La selección de tecnologías se realizó considerando los siguientes criterios:

- Compatibilidad con modelos de Inteligencia Artificial.
- Facilidad de integración entre componentes.
- Escalabilidad.
- Comunidad y documentación.
- Compatibilidad con el ecosistema Python.
- Cumplimiento de los lineamientos del Capstone.

---

# 3. Lenguaje de Programación

## Python

Python será utilizado como lenguaje principal para todo el proyecto.

### Justificación

- Amplio ecosistema para Ciencia de Datos.
- Excelente soporte para IA.
- Integración sencilla con APIs REST.
- Compatible con TensorFlow y FastAPI.
- Alta productividad durante el desarrollo.

---

# 4. Librerías de Ciencia de Datos

## Pandas

Responsabilidad

- Lectura de archivos CSV.
- Integración de datasets.
- Limpieza de datos.
- Transformación del Master Dataset.

---

## NumPy

Responsabilidad

- Operaciones matriciales.
- Manipulación eficiente de arreglos.
- Preparación de datos para Deep Learning.

---

## Scikit-learn

Responsabilidad

- Codificación de variables.
- Normalización.
- División entrenamiento/prueba.
- Métricas de evaluación.
- Pipeline de preprocesamiento.

---

## TensorFlow / Keras

Responsabilidad

Implementación del modelo CNN 1D con Transfer Learning definido durante Analytic Approach.

Será el framework principal de Inteligencia Artificial del proyecto.

---

# 5. Backend

## FastAPI

Responsabilidad

- Exponer servicios REST.
- Ejecutar el motor de validación.
- Invocar el modelo de IA.
- Enviar resultados al Dashboard.

### Justificación

- Alto rendimiento.
- Documentación automática.
- Fácil integración con Python.
- Excelente soporte para Machine Learning.

---

# 6. Dashboard

## Streamlit

Responsabilidad

- Visualización de resultados.
- Consulta de alertas.
- Indicadores de desempeño.
- Estadísticas del proceso de auditoría.

### Justificación

- Desarrollo rápido.
- Integración directa con Python.
- Ideal para aplicaciones analíticas.

---

# 7. Control de Versiones

## Git

Responsabilidad

- Control de cambios.
- Versionamiento del proyecto.
- Trabajo colaborativo.

---

## GitHub

Responsabilidad

- Repositorio central.
- Gestión de Issues.
- Pull Requests.
- Milestones.
- Documentación.

---

# 8. Herramientas de Desarrollo

| Herramienta | Uso |
|-------------|-----|
| VS Code | Desarrollo principal |
| GitHub Desktop | Gestión de commits |
| Draw.io | Diagramas |
| Mermaid | Diagramas en documentación |
| Markdown | Documentación técnica |

---

# 9. Estructura del Repositorio

```text
healthcare-ai-auditor/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── docs/
│   ├── architecture/
│   ├── asum-dm/
│   ├── diagrams/
│   ├── presentation/
│   ├── references/
│   └── reports/
│
├── notebooks/
│
├── src/
│   ├── api/
│   ├── dashboard/
│   ├── data/
│   ├── models/
│   ├── rules/
│   ├── services/
│   └── utils/
│
├── tests/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 10. Estrategia de Desarrollo

El proyecto seguirá un desarrollo incremental basado en ASUM-DM.

Cada fase generará entregables independientes antes de avanzar a la siguiente.

La implementación seguirá el siguiente flujo:

```text
Business Understanding

↓

Analytic Approach

↓

Data Understanding

↓

Data Preparation

↓

Modeling

↓

Evaluation

↓

Deployment
```

---

# 11. Flujo de Trabajo de Desarrollo

Para cada funcionalidad se seguirá el siguiente proceso:

```text
GitHub Issue

↓

Análisis

↓

Diseño

↓

Implementación

↓

Pruebas

↓

Documentación

↓

Commit

↓

Pull Request

↓

Merge
```

---

# 12. Estrategia de Integración

Los componentes se desarrollarán de forma modular.

Cada módulo tendrá responsabilidades claramente definidas.

- Data Layer
- Validation Layer
- AI Layer
- API Layer
- Presentation Layer

La comunicación entre módulos se realizará mediante interfaces bien definidas para facilitar futuras ampliaciones.

---

# 13. Tecnologías Seleccionadas

| Categoría | Tecnología |
|------------|------------|
| Lenguaje | Python |
| Manipulación de datos | Pandas |
| Computación numérica | NumPy |
| Machine Learning | Scikit-learn |
| Deep Learning | TensorFlow / Keras |
| Backend | FastAPI |
| Dashboard | Streamlit |
| API | REST |
| Control de versiones | Git |
| Repositorio | GitHub |
| Diagramas | Draw.io |
| Documentación | Markdown |

---

# 14. Justificación del Stack

El stack seleccionado ofrece un equilibrio entre rendimiento, mantenibilidad y facilidad de desarrollo.

Todas las herramientas pertenecen al ecosistema Python, reduciendo la complejidad de integración.

La combinación de FastAPI, TensorFlow, Pandas y Streamlit permite construir una solución completa para la validación automática de facturación médica, desde la preparación de datos hasta la visualización de resultados.

Además, el uso de TensorFlow/Keras asegura el cumplimiento del requisito del Capstone relacionado con la implementación de modelos CNN.

---

# 15. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|--------|
| Stack tecnológico aprobado | ✅ |
| Flujo de desarrollo documentado | ✅ |
| Estrategia del repositorio validada | ✅ |

---

# 16. Relación con la siguiente fase

La información definida en este documento servirá como base para iniciar la fase **Data Understanding**, donde se realizará el análisis exploratorio de los datasets, la validación de su calidad y la comprensión de las variables que alimentarán el Motor de Validación y el modelo de Inteligencia Artificial.