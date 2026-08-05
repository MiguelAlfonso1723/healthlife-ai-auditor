# DP-07 — Export Production-Ready Dataset

| Campo | Valor |
|--------|-------|
| Fase | Data Preparation |
| Milestone | Data Preparation |
| Issue | DP-07 |
| Estado | Completed |

---

# 1. Información General

Este documento registra la publicación oficial del Master Dataset preparado durante la fase Data Preparation del proyecto Healthcare AI Billing Auditor.

El dataset fue validado y aprobado durante el Issue DP-06 y constituye la versión definitiva que será utilizada durante las fases de Modeling, Evaluation y Deployment.

---

# 2. Objetivo

Publicar el Master Dataset aprobado como el dataset oficial de producción para la fase de Modeling, garantizando que:

- Se preserva la integridad del dataset validado.
- Se genera una copia oficial en `data/final/`.
- Se documenta la estructura y propósito del dataset.
- Se establece el versionado oficial del entregable.

---

# 3. Descripción del Master Dataset

| Atributo | Valor |
|----------|-------|
| Registros | 3,126 |
| Columnas totales | 55 |
| Features originales | 35 |
| Features generadas | 20 |
| Variable objetivo (binaria) | resultado |
| Variable objetivo (multi-clase) | tipo_alerta |
| Variable objetivo (ordinal) | severidad |
| Clave primaria | id_cruce |

---

# 4. Estructura General

## Variables de Validación (Ground Truth)

- id_cruce
- resultado
- tipo_alerta
- severidad
- descripcion_alerta

## Variables de Atención

- id_atencion
- fecha_atencion
- tipo_atencion
- diagnostico_principal_cie10
- descripcion_diagnostico
- medico_tratante
- sede
- eps

## Variables del Paciente

- id_paciente
- edad
- sexo
- tipo_documento
- tipo_afiliacion
- ciudad

## Variables de Historia Clínica

- id_detalle_hc
- id_atencion_hc
- tipo_item
- codigo_cups
- descripcion
- cantidad_realizada
- fecha_registro
- soporte_clinico
- profesional_responsable

## Variables de Prefactura

- id_prefactura
- codigo_cups_facturado
- descripcion_servicio_facturado
- cantidad_facturada
- valor_unitario
- valor_total
- fecha_facturacion

## Features Clínicas (DP-04)

- cups_match
- tiene_soporte_clinico
- procedimiento_facturado
- procedimiento_registrado
- diagnostico_disponible
- len_descripcion_diagnostico
- len_descripcion_hc
- len_descripcion_servicio

## Features de Facturación (DP-04)

- diferencia_cantidad
- cantidad_coincide
- valor_unitario_disponible
- valor_total_disponible
- servicio_facturado
- procedimiento_no_facturado

## Features Temporales (DP-04)

- anio_atencion
- mes_atencion
- trimestre
- dia_semana
- hora_registro
- dias_atencion_facturacion

---

# 5. Archivos Exportados

| Archivo | Formato | Ubicación | Propósito |
|---------|---------|-----------|-----------|
| master_dataset.csv | CSV | data/final/ | Compatibilidad general, inspección manual |
| master_dataset.parquet | Parquet | data/final/ | Carga eficiente para entrenamiento y producción |

### Tamaños

| Archivo | Tamaño |
|---------|--------|
| master_dataset.csv | 1,416 KB |
| master_dataset.parquet | 211 KB |

---

# 6. Validación de Integridad

| Criterio | Estado |
|----------|--------|
| Registros: 3,126 | ✅ |
| Columnas: 55 | ✅ |
| Duplicados: 0 | ✅ |
| PK (id_cruce) única | ✅ |
| Idéntico al dataset aprobado en DP-06 | ✅ |
| CSV exportado correctamente | ✅ |
| Parquet exportado correctamente | ✅ |

Se verificó que los archivos en `data/final/` son idénticos byte a byte al dataset aprobado durante DP-06.

---

# 7. Uso durante Modeling

Este dataset será utilizado como fuente única durante:

| Componente | Uso |
|-----------|-----|
| Entrenamiento CNN 1D | Preparación de features, encoding, normalización y entrenamiento |
| Motor de Reglas | Implementación de BR-01 a BR-06 |
| Evaluación | Métricas de desempeño (Accuracy, F1, Precision, Recall) |
| Inferencia | Input del modelo durante la ejecución del Auditor Médico Digital |
| Dashboard | Visualización de alertas e indicadores |
| API REST | Consulta de resultados de validación |

---

# 8. Versionado

| Atributo | Valor |
|----------|-------|
| Versión | 1.0 |
| Fecha de generación | Fase Data Preparation |
| Generado por | Pipeline DP-05 |
| Aprobado en | DP-06 |
| Publicado en | DP-07 |
| Estado | Oficial |

Esta versión corresponde al cierre de la fase Data Preparation y constituye la fuente oficial para todas las fases posteriores del proyecto.

Cualquier modificación futura al dataset deberá generar una nueva versión documentada.

---

# 9. Verificación de Criterios de Aceptación

| Criterio | Estado |
|----------|--------|
| Dataset exportado a data/final/ | ✅ |
| CSV generado correctamente | ✅ |
| Parquet generado correctamente | ✅ |
| Integridad verificada respecto a DP-06 | ✅ |
| Documentación actualizada | ✅ |
| Dataset listo para Modeling | ✅ |

---

# 10. Relación con el siguiente Issue

Este dataset será la entrada oficial para la fase **Modeling** de la metodología ASUM-DM.

Durante Modeling se utilizará este dataset para:

1. Implementar el Motor de Reglas de Negocio (BR-01 a BR-06).
2. Preparar el input del modelo CNN 1D (encoding, normalización, embeddings).
3. Entrenar y evaluar el modelo de Inteligencia Artificial.
4. Integrar ambos componentes en el Auditor Médico Digital.

El dataset NO será modificado durante Modeling. Todas las transformaciones de encoding y normalización se realizarán como parte del pipeline de entrenamiento sin alterar los archivos en `data/final/`.
