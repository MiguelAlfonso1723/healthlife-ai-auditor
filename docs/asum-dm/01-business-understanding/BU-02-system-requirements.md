# BU-02 — Define Functional and Non-Functional Requirements

| Campo | Valor |
|--------|-------|
| Fase | Business Understanding |
| Milestone | Business Understanding |
| Issue | BU-02 |
| Estado | Completed |

---

# 1. Objetivo

Definir los requisitos funcionales y no funcionales del sistema de validación automatizada de Health & Life IPS SAS, estableciendo el alcance del proyecto, sus restricciones, supuestos y las salidas esperadas.

Estos requisitos servirán como base para el diseño de la arquitectura y el desarrollo de la solución durante las siguientes fases de la metodología ASUM-DM.

---

# 2. Requisitos Funcionales

El sistema deberá ser capaz de realizar las siguientes funciones:

| ID | Requisito |
|----|-----------|
| FR-01 | Cargar los datos provenientes de la Historia Clínica. |
| FR-02 | Cargar los datos correspondientes a la Pre-factura. |
| FR-03 | Integrar la información clínica y administrativa para su validación. |
| FR-04 | Validar automáticamente la consistencia entre la Historia Clínica y la Pre-factura. |
| FR-05 | Detectar procedimientos registrados que no fueron incluidos en la Pre-factura. |
| FR-06 | Detectar procedimientos facturados que no cuentan con soporte clínico. |
| FR-07 | Identificar inconsistencias entre diagnósticos y procedimientos registrados. |
| FR-08 | Generar alertas preventivas para cada inconsistencia detectada. |
| FR-09 | Clasificar las inconsistencias según su tipo y nivel de impacto. |
| FR-10 | Permitir la consulta de los resultados de validación mediante una interfaz visual. |
| FR-11 | Exponer los resultados del proceso mediante una API REST. |
| FR-12 | Generar reportes con el resumen de inconsistencias detectadas. |

---

# 3. Requisitos No Funcionales

El sistema deberá cumplir los siguientes atributos de calidad.

| ID | Requisito |
|----|-----------|
| NFR-01 | Mantener una arquitectura modular que facilite el mantenimiento y la escalabilidad. |
| NFR-02 | Ser fácilmente extensible para incorporar nuevas reglas de validación. |
| NFR-03 | Mantener una separación clara entre procesamiento de datos, lógica de negocio y presentación. |
| NFR-04 | Proporcionar resultados consistentes para una misma entrada de datos. |
| NFR-05 | Generar mensajes de error claros durante el proceso de validación. |
| NFR-06 | Permitir la reutilización de componentes del sistema. |
| NFR-07 | Mantener una estructura organizada del código siguiendo buenas prácticas de desarrollo. |
| NFR-08 | Facilitar la integración con futuras fuentes de datos o sistemas externos. |

---

# 4. Alcance del Proyecto

El proyecto contempla el desarrollo de un Producto Mínimo Viable (MVP) capaz de validar automáticamente la consistencia entre la Historia Clínica y la Pre-factura utilizando reglas de negocio y técnicas de Inteligencia Artificial.

El alcance incluye:

- Integración de los conjuntos de datos suministrados.
- Preparación y limpieza de los datos.
- Implementación del motor de validación.
- Desarrollo de un modelo de Inteligencia Artificial para apoyar la detección de inconsistencias.
- Desarrollo de una API REST para consultar los resultados.
- Desarrollo de un Dashboard para visualizar alertas e indicadores.
- Generación de reportes de inconsistencias.

No hacen parte del alcance:

- Integración con sistemas hospitalarios reales (HIS o ERP).
- Facturación electrónica en producción.
- Actualización en tiempo real de Historias Clínicas.
- Despliegue en infraestructura hospitalaria.

---

# 5. Restricciones del Proyecto

Durante el desarrollo deberán considerarse las siguientes restricciones:

- El proyecto utilizará únicamente las bases de datos suministradas para el Capstone.
- El desarrollo seguirá estrictamente la metodología ASUM-DM.
- El tiempo de desarrollo está limitado al cronograma establecido para el curso.
- La solución se implementará como un MVP funcional.
- No se realizarán integraciones con servicios externos de producción.
- Las reglas de negocio se construirán a partir de la información disponible en el reto y los datos suministrados.

---

# 6. Supuestos

Para el desarrollo del proyecto se asumen las siguientes condiciones:

- Las bases de datos representan correctamente el proceso de negocio.
- La información suministrada posee la calidad suficiente para entrenar y validar el sistema.
- La Historia Clínica y la Pre-factura contienen identificadores que permiten relacionar ambos conjuntos de datos.
- Las inconsistencias presentes en los datos representan casos reales de validación.
- El Auditor Médico Digital actuará como herramienta de apoyo y no reemplazará completamente la revisión humana.

---

# 7. Salidas Esperadas del Sistema

Al finalizar el proceso de validación, el sistema deberá generar como mínimo:

- Alertas de inconsistencias detectadas.
- Listado de procedimientos sin soporte clínico.
- Listado de procedimientos registrados pero no facturados.
- Resumen estadístico de inconsistencias.
- Indicadores para el Dashboard.
- Respuesta estructurada de la API REST.
- Reportes de validación para consulta del auditor.

---

# 8. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|---------|
| Requisitos funcionales documentados | ✅ |
| Requisitos no funcionales documentados | ✅ |
| Alcance del proyecto definido | ✅ |
| Restricciones identificadas | ✅ |

---

# 9. Relación con el siguiente Issue

Los requisitos definidos en este documento servirán como entrada para el diseño de la arquitectura analítica y la selección de las técnicas de Inteligencia Artificial durante la fase **Analytic Approach**.