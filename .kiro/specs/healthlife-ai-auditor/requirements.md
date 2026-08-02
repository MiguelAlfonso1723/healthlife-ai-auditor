# Requirements Document

## Introduction

El **HealthLife AI Auditor** es un sistema de Auditoría Médica Digital que valida de forma automatizada los datos de Historias Clínicas (tratamientos, procedimientos, exámenes y diagnósticos) contra la pre-factura, generando alertas preventivas de inconsistencias antes de emitir el cobro. El sistema combina un Motor de Reglas de Negocio con un Modelo de Inteligencia Artificial para reducir glosas, rechazos y fugas de ingreso en Health & Life IPS SAS.

## Glossary

- **Auditor_Digital**: Sistema compuesto por el Motor de Reglas y el Modelo de IA que ejecuta la validación cruzada entre historia clínica y pre-factura.
- **Motor_Reglas**: Componente que evalúa inconsistencias determinísticas basándose en reglas de negocio predefinidas.
- **Modelo_IA**: Modelo de clasificación basado en CNN con transfer learning que detecta patrones complejos de inconsistencia no cubiertos por el Motor de Reglas.
- **Pipeline_Datos**: Componente encargado de la ingesta, limpieza, transformación y consolidación de los datasets crudos en un Dataset Maestro.
- **Dataset_Maestro**: Tabla consolidada resultado del cruce entre pacientes, atenciones, historia clínica y pre-factura, lista para validación.
- **API_REST**: Servicio backend construido con FastAPI que expone los endpoints de validación y consulta de alertas.
- **Dashboard**: Interfaz de usuario construida con Streamlit que presenta alertas, resúmenes e indicadores al auditor humano.
- **Historia_Clínica**: Registro detallado de procedimientos, diagnósticos, exámenes y tratamientos realizados a un paciente durante una atención.
- **Pre_Factura**: Documento preliminar que lista los procedimientos y servicios que se cobrarán a la entidad pagadora.
- **Alerta**: Notificación generada por el Auditor_Digital indicando una inconsistencia detectada entre la Historia_Clínica y la Pre_Factura.
- **Glosa**: Objeción o rechazo de un cobro por parte de la entidad pagadora debido a inconsistencias documentales.
- **Inconsistencia**: Discrepancia entre lo registrado en la Historia_Clínica y lo consignado en la Pre_Factura.
- **Atención**: Evento de servicio de salud prestado a un paciente en una fecha determinada.

## Requirements

### Requirement 1: Preparación y Consolidación de Datos

**User Story:** Como científico de datos, quiero un pipeline automatizado que consolide los datasets crudos en un Dataset Maestro validado, para que el Auditor Digital tenga una fuente de datos unificada y confiable.

#### Acceptance Criteria

1. WHEN los archivos CSV (01_pacientes.csv, 02_atenciones.csv, 03_historia_clinica_detalle.csv, 04_prefactura.csv, 05_cruce_validacion.csv) son proporcionados, THE Pipeline_Datos SHALL cargar cada archivo y verificar que contiene todas las columnas requeridas según el esquema definido en la configuración del pipeline, rechazando el archivo si falta al menos una columna esperada o si el archivo está vacío (0 registros de datos).
2. WHEN un archivo CSV contiene registros con valores nulos en campos obligatorios, THE Pipeline_Datos SHALL registrar esos registros en un log de calidad indicando el archivo de origen, el número de fila y el campo nulo detectado, y excluirlos del Dataset_Maestro.
3. WHEN todos los archivos son cargados y validados, THE Pipeline_Datos SHALL cruzar los datos mediante inner join utilizando las llaves id_paciente e id_atencion, de modo que solo los registros con correspondencia en todos los datasets participantes sean incluidos en el Dataset_Maestro, y SHALL registrar en el log de calidad el conteo de registros huérfanos (sin correspondencia) por cada archivo fuente.
4. THE Pipeline_Datos SHALL generar un reporte de calidad de datos que incluya: el número total de registros cargados por archivo, el número de registros excluidos por valores nulos, el número de registros huérfanos descartados en el cruce y el número total de registros consolidados en el Dataset_Maestro.
5. IF un archivo CSV no existe o no puede ser leído, THEN THE Pipeline_Datos SHALL retornar un error indicando el nombre del archivo faltante o ilegible y detener la ejecución del pipeline sin generar el Dataset_Maestro.
6. IF un archivo CSV contiene registros duplicados por la combinación de sus llaves primarias (id_paciente, id_atencion), THEN THE Pipeline_Datos SHALL conservar únicamente la primera ocurrencia, descartar los duplicados y registrar el conteo de duplicados eliminados en el log de calidad.

---

### Requirement 2: Motor de Reglas de Negocio

**User Story:** Como auditor médico, quiero que el sistema aplique reglas de negocio predefinidas para detectar inconsistencias determinísticas entre la historia clínica y la pre-factura, para identificar errores de facturación de forma inmediata.

#### Acceptance Criteria

1. WHEN un procedimiento está registrado en la Historia_Clínica pero no aparece en la Pre_Factura para la misma Atención (comparación por código de procedimiento), THE Motor_Reglas SHALL generar una Alerta de tipo "procedimiento_no_facturado" con severidad "media".
2. WHEN un procedimiento aparece en la Pre_Factura pero no tiene soporte en la Historia_Clínica para la misma Atención (comparación por código de procedimiento), THE Motor_Reglas SHALL generar una Alerta de tipo "facturado_sin_soporte_clínico" con severidad "alta".
3. WHEN un diagnóstico registrado en la Historia_Clínica no tiene una relación válida con los procedimientos facturados según las tablas de referencia diagnóstico-procedimiento (es decir, el par diagnóstico-procedimiento no existe en la tabla de referencia), THE Motor_Reglas SHALL generar una Alerta de tipo "diagnóstico_inconsistente" con severidad "media".
4. WHEN el Motor_Reglas procesa un registro del Dataset_Maestro y detecta más de una inconsistencia, THE Motor_Reglas SHALL generar una Alerta separada por cada inconsistencia detectada, cada una con su propio tipo de alerta.
5. THE Motor_Reglas SHALL procesar el Dataset_Maestro completo y generar un listado de todas las Alertas con los campos: id_paciente, id_atención, tipo_alerta, descripción (indicando los códigos específicos de procedimiento o diagnóstico involucrados en la inconsistencia) y severidad (valores posibles: "alta", "media", "baja").
6. IF las tablas de referencia diagnóstico-procedimiento no están disponibles o no pueden ser cargadas, THEN THE Motor_Reglas SHALL omitir la regla de "diagnóstico_inconsistente", registrar el error en un log y continuar aplicando las demás reglas.
7. IF un registro del Dataset_Maestro contiene datos incompletos que impiden la evaluación de reglas (campos de código de procedimiento o diagnóstico vacíos), THEN THE Motor_Reglas SHALL clasificar el registro como "no_evaluable" y registrar la razón en el log de calidad sin generar una Alerta.

---

### Requirement 3: Modelo de Inteligencia Artificial

**User Story:** Como científico de datos, quiero un modelo de IA basado en CNN con transfer learning que complemente al Motor de Reglas detectando patrones complejos de inconsistencia, para capturar anomalías que las reglas determinísticas no pueden identificar.

#### Acceptance Criteria

1. THE Modelo_IA SHALL ser entrenado utilizando una arquitectura CNN con transfer learning según los requerimientos del curso Samsung Innovation Campus.
2. WHEN un registro del Dataset_Maestro es evaluado, THE Modelo_IA SHALL retornar una predicción binaria (consistente/inconsistente) junto con un score de confianza entre 0.0 y 1.0 en un tiempo no mayor a 500 milisegundos por registro.
3. THE Modelo_IA SHALL alcanzar un accuracy mínimo de 0.80 y un F1-score (weighted average) mínimo de 0.75 sobre un conjunto de prueba que represente al menos el 20% del Dataset_Maestro, separado mediante partición estratificada reproducible.
4. WHEN el Modelo_IA evalúa un registro y obtiene una predicción de "inconsistente" con un score de confianza mayor o igual a 0.7, THE Modelo_IA SHALL generar una Alerta de tipo "patrón_complejo_detectado".
5. WHEN el Modelo_IA evalúa un registro y obtiene un score de confianza menor a 0.7 para la clase "inconsistente", THE Modelo_IA SHALL clasificar el registro como "consistente" sin generar Alerta.
6. THE Modelo_IA SHALL ser serializado en formato joblib para su carga posterior por la API_REST.
7. WHEN el Modelo_IA es entrenado, THE Modelo_IA SHALL generar un reporte de evaluación que incluya accuracy, precision, recall, F1-score (weighted average) y matriz de confusión sobre el conjunto de prueba.
8. IF el Modelo_IA no puede generar una predicción para un registro debido a datos faltantes o error de procesamiento, THEN THE Modelo_IA SHALL clasificar el registro como "no_evaluado", registrar el error con el id_paciente y id_atención en un log de errores, y excluir el registro del conteo de métricas de rendimiento.

---

### Requirement 4: Auditor Médico Digital (Integración)

**User Story:** Como auditor médico, quiero un sistema integrado que combine las alertas del Motor de Reglas y del Modelo de IA en un resultado unificado, para tener una visión consolidada de todas las inconsistencias detectadas.

#### Acceptance Criteria

1. WHEN el Auditor_Digital recibe un Dataset_Maestro, THE Auditor_Digital SHALL ejecutar primero el Motor_Reglas y luego el Modelo_IA sobre los registros marcados como "consistente" por el Motor_Reglas.
2. THE Auditor_Digital SHALL consolidar las alertas del Motor_Reglas y del Modelo_IA en un listado único ordenado por severidad descendente, utilizando el id_atención ascendente como criterio de desempate cuando dos alertas comparten la misma severidad.
3. WHEN el Auditor_Digital finaliza la validación, THE Auditor_Digital SHALL generar un resumen con el número total de registros evaluados, registros consistentes, registros inconsistentes por tipo de alerta y el porcentaje de inconsistencia global calculado como (registros inconsistentes / registros evaluados) * 100.
4. THE Auditor_Digital SHALL asignar una severidad a cada Alerta utilizando la escala: "alta" para facturado_sin_soporte_clínico y para inconsistencias de patrón detectadas por el Modelo_IA con score mayor o igual a 0.85, "media" para procedimiento_no_facturado y para diagnóstico_inconsistente, "baja" para inconsistencias de patrón detectadas por el Modelo_IA con score mayor o igual a 0.7 y menor a 0.85.
5. IF tanto el Motor_Reglas como el Modelo_IA generan una Alerta para el mismo id_atención, THEN THE Auditor_Digital SHALL conservar únicamente la Alerta de mayor severidad y registrar ambas fuentes de detección en el campo origen de la Alerta resultante.
6. IF el Motor_Reglas o el Modelo_IA fallan durante la ejecución de la validación, THEN THE Auditor_Digital SHALL detener el proceso, registrar el componente que falló y retornar un error indicando que la validación no pudo completarse.

---

### Requirement 5: API REST

**User Story:** Como desarrollador frontend, quiero una API REST que exponga endpoints para ejecutar validaciones y consultar alertas, para que el Dashboard pueda consumir los resultados del Auditor Digital.

#### Acceptance Criteria

1. THE API_REST SHALL exponer un endpoint POST /validar que reciba un identificador de atención o un rango de fechas (máximo 90 días entre fecha inicio y fecha fin) y ejecute el Auditor_Digital sobre los registros correspondientes.
2. THE API_REST SHALL exponer un endpoint GET /alertas que retorne el listado de alertas generadas con los campos id_paciente, id_atención, tipo_alerta, descripción, severidad y fecha de detección, permitiendo filtrar por tipo de alerta, severidad y rango de fechas, con paginación de máximo 100 resultados por página.
3. THE API_REST SHALL exponer un endpoint GET /resumen que retorne las métricas consolidadas de la última validación ejecutada, incluyendo: total de registros evaluados, registros consistentes, registros inconsistentes por tipo de alerta y porcentaje de inconsistencia global.
4. WHEN una solicitud al endpoint POST /validar es procesada exitosamente, THE API_REST SHALL retornar un código HTTP 200 con el resumen de validación y el conteo de alertas generadas.
5. IF una solicitud contiene parámetros inválidos o faltantes, THEN THE API_REST SHALL retornar un código HTTP 422 con un mensaje indicando el parámetro inválido o faltante y la restricción incumplida.
6. IF ocurre un error interno durante el procesamiento, THEN THE API_REST SHALL retornar un código HTTP 500 con un identificador único de error y un mensaje genérico sin exponer detalles internos del sistema.
7. IF el endpoint GET /resumen es invocado sin que exista una validación previa ejecutada, THEN THE API_REST SHALL retornar un código HTTP 404 con un mensaje indicando que no se encontró ninguna validación previa.
8. IF el endpoint GET /alertas no encuentra alertas que coincidan con los filtros aplicados, THEN THE API_REST SHALL retornar un código HTTP 200 con un listado vacío y el campo total de resultados en cero.

---

### Requirement 6: Dashboard de Visualización

**User Story:** Como auditor médico, quiero un dashboard interactivo donde pueda visualizar las alertas, ejecutar validaciones y consultar el estado de la facturación, para tomar decisiones informadas antes de emitir cobros.

#### Acceptance Criteria

1. THE Dashboard SHALL presentar un panel principal con indicadores clave: total de atenciones validadas, porcentaje de consistencia (registros consistentes / total de registros evaluados × 100), número de alertas agrupadas por severidad (alta, media, baja) y tendencia de inconsistencias de los últimos 30 días, junto con la marca de tiempo de la última validación ejecutada.
2. WHEN el auditor selecciona ejecutar una nueva validación, THE Dashboard SHALL invocar el endpoint POST /validar de la API_REST, mostrar un indicador visual de ejecución en curso y, al completarse, actualizar los indicadores del panel principal con los nuevos resultados.
3. THE Dashboard SHALL presentar una tabla de alertas con columnas para id_paciente, id_atención, tipo_alerta, severidad y fecha, que permita filtrar por tipo, severidad, rango de fechas y paciente, con paginación de máximo 50 registros por página y ordenamiento por severidad descendente por defecto.
4. WHEN el auditor selecciona una alerta específica, THE Dashboard SHALL mostrar el detalle del registro incluyendo como mínimo: id_paciente, id_atención, fecha de atención, procedimientos de la Historia_Clínica, procedimientos de la Pre_Factura, tipo de alerta, severidad, descripción de la inconsistencia y la explicación generada por el Auditor_Digital.
5. THE Dashboard SHALL incluir un gráfico de barras con la distribución de alertas por tipo y un gráfico de líneas con la evolución temporal de inconsistencias agrupadas por semana para los últimos 90 días.
6. IF la API_REST no responde dentro de 30 segundos o retorna un error, THEN THE Dashboard SHALL mostrar un mensaje de error indicando que el servicio no está disponible y mantener visibles los últimos datos cargados previamente sin perder el estado de los filtros aplicados.
7. IF el resultado de una consulta de alertas no contiene registros, THEN THE Dashboard SHALL mostrar un mensaje indicando que no se encontraron alertas para los filtros seleccionados.

---

### Requirement 7: Protección de Datos Personales y Ética

**User Story:** Como responsable de cumplimiento, quiero que el sistema proteja los datos sensibles de salud y opere de forma transparente, para cumplir con la normativa de protección de datos personales y los estándares éticos del proyecto.

#### Acceptance Criteria

1. THE Auditor_Digital SHALL procesar datos personales de salud únicamente en el entorno local del proyecto, sin realizar conexiones de red salientes que transmitan datos de pacientes, datos clínicos o datos de facturación a servicios externos al entorno de despliegue.
2. THE Dashboard SHALL presentar datos de pacientes de forma pseudoanonimizada en todas las vistas, mostrando únicamente los últimos 4 dígitos del documento de identidad y sustituyendo el nombre completo del paciente por un identificador alfanumérico interno.
3. THE Modelo_IA SHALL incluir documentación sobre las métricas de sesgo evaluadas durante el entrenamiento, incluyendo como mínimo la tasa de falsos positivos y la tasa de falsos negativos desagregadas por cada grupo demográfico presente en el Dataset_Maestro (sexo y rango de edad como mínimo).
4. WHEN el Auditor_Digital genera una Alerta, THE Auditor_Digital SHALL incluir una explicación en texto plano de máximo 500 caracteres que indique: el campo o campos donde se detectó la discrepancia, el valor esperado según la fuente de referencia y el valor encontrado en el registro evaluado.
5. THE API_REST SHALL registrar en un log de auditoría cada solicitud de validación con la marca de tiempo en formato ISO 8601, el identificador del usuario solicitante y el número de registros procesados, sin almacenar campos de historia clínica, diagnósticos ni datos de identificación personal en los logs.
6. THE API_REST SHALL retener los registros del log de auditoría por un período mínimo de 12 meses y permitir su consulta por rango de fechas para facilitar auditorías de cumplimiento.
7. IF el Dashboard recibe datos de paciente con documento de identidad nulo o con longitud menor a 4 caracteres, THEN THE Dashboard SHALL mostrar el campo de identificación como enmascarado completamente con el texto "N/D" y registrar el evento en el log de auditoría.

---

### Requirement 8: Rendimiento y Calidad del Sistema

**User Story:** Como líder técnico, quiero que el sistema cumpla con estándares mínimos de rendimiento y calidad de código, para garantizar que el MVP sea funcional y mantenible.

#### Acceptance Criteria

1. THE Pipeline_Datos SHALL procesar los 5 archivos CSV y generar el Dataset_Maestro en un tiempo menor a 60 segundos para datasets de hasta 100,000 registros por archivo, medido en una máquina con al menos 8 GB de RAM y procesador de 4 núcleos.
2. THE API_REST SHALL responder a solicitudes individuales del endpoint GET /alertas en un tiempo menor a 2 segundos para resultados de hasta 10,000 alertas, medido sin carga concurrente adicional.
3. THE Auditor_Digital SHALL ejecutar la validación completa (Motor_Reglas + Modelo_IA) sobre un Dataset_Maestro de hasta 50,000 registros en un tiempo menor a 120 segundos, medido en las mismas condiciones de hardware definidas en el criterio 1.
4. WHEN la API_REST se inicia, THE Modelo_IA SHALL ser cargado en memoria una única vez y la API_REST SHALL estar lista para recibir solicitudes en un tiempo menor a 30 segundos, reutilizando la instancia del modelo para todas las solicitudes de validación posteriores sin recargarlo.
5. WHEN se ejecutan las pruebas automatizadas del proyecto, THE sistema SHALL alcanzar una cobertura de pruebas unitarias mínima del 70% sobre los módulos del Motor_Reglas, el Pipeline_Datos y el Auditor_Digital.
6. IF el Pipeline_Datos o el Auditor_Digital exceden su tiempo máximo de ejecución definido, THEN THE sistema SHALL registrar una advertencia en el log indicando el tiempo real de ejecución y el umbral excedido, y completar el procesamiento sin interrumpirlo.
