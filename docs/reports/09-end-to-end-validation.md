# EV-03 — End-to-End Validation Report

| Campo | Valor |
|-------|-------|
| Fase | Evaluation |
| Milestone | Evaluation |
| Issue | EV-03 |
| Estado | Completed |
| Fecha | 2026-08-04 |

---

## 1. Objetivo

Validar el flujo completo del sistema Medical Digital Auditor, desde la ingesta de registros del Master Dataset hasta la generación de alertas, verificando que todos los componentes integrados funcionan correctamente de forma conjunta utilizando el modelo oficial `xgboost_hybrid_sentence`.

---

## 2. Componentes Utilizados

| Componente | Ubicación | Descripción |
|---|---|---|
| `MedicalAuditorPredictor` | `src/ai/inference.py` | Wrapper de inferencia: carga el registry, construye la matriz híbrida y sirve predicciones |
| `MedicalValidationEngine` | `src/backend/validation_engine/engine.py` | Motor de reglas de negocio BR-01 a BR-06 |
| `xgboost_hybrid_sentence` | `models/artifacts/xgboost_hybrid_sentence.joblib` | Modelo XGBoost ganador (1,388,164 bytes) |
| `SentenceTransformer` local | `models/artifacts/sentence_transformer_model/` | Embeddings semánticos multilingüe (`paraphrase-multilingual-MiniLM-L12-v2`) |
| `hybrid_feature_builder` | `models/artifacts/hybrid_feature_builder.joblib` | Preprocessor tabular (ColumnTransformer) + fuente de embeddings |
| `alert_label_encoder` | `models/artifacts/alert_label_encoder.joblib` | LabelEncoder para decodificar predicciones enteras a strings |
| `model_registry.json` | `models/model_registry.json` | Registro oficial del modelo ganador (6,426 bytes) |
| REST API | `src/backend/api.py` | FastAPI — `GET /health` y `POST /predict` |
| Master Dataset | `data/master/master_dataset_features.csv` | Dataset oficial de features (3,126 registros × 55 columnas) |

---

## 3. Flujo de Ejecución Validado

```
Registro del Master Dataset (CSV)
            │
            ▼
  Leakage columns dropped
  (resultado, tipo_alerta, severidad, descripcion_alerta)
            │
   ┌─────────────────┐
   │                 │
   ▼                 ▼
MedicalValidationEngine    MedicalAuditorPredictor
(BR-01 a BR-06)            │
   │                       ├─ build_text()
   │                       │   (descripcion_diagnostico |
   │                       │    descripcion |
   │                       │    descripcion_servicio_facturado)
   │                       │
   │                       ├─ ColumnTransformer
   │                       │   (25 numeric + 12 categorical cols definidas en config)
   │                       │
   │                       ├─ SentenceTransformer local
   │                       │   (embeddings 384-dim)
   │                       │
   │                       ├─ np.hstack([tabular, embeddings])
   │                       │
   │                       └─ XGBClassifier.predict_proba()
   │                           → LabelEncoder.inverse_transform()
   │
   └──────────── Resultado combinado ──────────────────────┐
                                                           │
                                                           ▼
                                              REST API POST /predict
                                              → JSON Response
                                              {predicted_alert,
                                               predicted_status,
                                               confidence,
                                               probabilities,
                                               model}
```

---

## 4. Verificación de Artefactos (Step 0)

Todos los artefactos verificados presentes antes de ejecutar el flujo:

| Artefacto | Ruta | Tamaño | Estado |
|---|---|---|---|
| `model_registry.json` | `models/model_registry.json` | 6,426 bytes | OK |
| `xgboost_hybrid_sentence.joblib` | `models/artifacts/xgboost_hybrid_sentence.joblib` | 1,388,164 bytes | OK |
| `hybrid_feature_builder.joblib` | `models/artifacts/hybrid_feature_builder.joblib` | 9,242 bytes | OK |
| `alert_label_encoder.joblib` | `models/artifacts/alert_label_encoder.joblib` | 597 bytes | OK |
| `sentence_transformer_model/` | `models/artifacts/sentence_transformer_model/` | directorio | OK |
| `master_dataset_features.csv` | `data/master/master_dataset_features.csv` | 1,449,949 bytes | OK |

---

## 5. Dataset Cargado (Step 1)

| Parámetro | Valor |
|---|---|
| Filas | 3,126 |
| Columnas | 55 |
| Tiempo de carga | 135.10 ms |
| Columna target | `tipo_alerta` |

**Distribución de clases:**

| Clase | Registros | % |
|---|---|---|
| `CONSISTENTE` | 2,477 | 79.2% |
| `SIN_SOPORTE_CLINICO` | 157 | 5.0% |
| `DIAGNOSTICO_NO_RELACIONADO` | 152 | 4.9% |
| `NO_FACTURADO` | 152 | 4.9% |
| `CODIGO_NO_COINCIDE` | 120 | 3.8% |
| `CANTIDAD_DISCORDANTE` | 68 | 2.2% |

---

## 6. Inicialización de Componentes (Steps 2–3)

### MedicalAuditorPredictor

| Parámetro | Valor |
|---|---|
| Modelo cargado | `xgboost_hybrid_sentence` |
| Ruta del modelo | `models/artifacts/xgboost_hybrid_sentence.joblib` |
| Fuente de embeddings | `sentence-transformer-local:models/artifacts/sentence_transformer_model` |
| Clases del registry | `CANTIDAD_DISCORDANTE`, `CODIGO_NO_COINCIDE`, `CONSISTENTE`, `DIAGNOSTICO_NO_RELACIONADO`, `NO_FACTURADO`, `SIN_SOPORTE_CLINICO` |
| Tiempo de inicialización | 103.65 ms |

### MedicalValidationEngine

| Parámetro | Valor |
|---|---|
| Reglas registradas | 6 (BR-01 a BR-06) |
| Tiempo de inicialización | 0.03 ms |

---

## 7. Ejecución E2E por Clase — Resultados Individuales (Steps 4–5)

Se seleccionó un registro real del dataset por cada clase. Los resultados provienen de la ejecución directa de ambos componentes sobre esos registros.

| true_label | id_cruce | Rules Engine | Rules Alerts | AI predicted | AI conf | Final status |
|---|---|---|---|---|---|---|
| `CONSISTENTE` | CRZ-0000004 | CONSISTENTE | — | `DIAGNOSTICO_NO_RELACIONADO` | 0.6876 | INCONSISTENTE |
| `SIN_SOPORTE_CLINICO` | CRZ-0000021 | CONSISTENTE | — | `CONSISTENTE` | 0.9090 | CONSISTENTE |
| `DIAGNOSTICO_NO_RELACIONADO` | CRZ-0000001 | CONSISTENTE | — | `DIAGNOSTICO_NO_RELACIONADO` | 0.6868 | INCONSISTENTE |
| `NO_FACTURADO` | CRZ-0000003 | INCONSISTENTE | BR-01 `NO_FACTURADO` (ALTA), BR-04 `NO_FACTURADO` (MEDIA) | `NO_FACTURADO` | 0.9983 | INCONSISTENTE |
| `CODIGO_NO_COINCIDE` | CRZ-0000044 | INCONSISTENTE | BR-01 `CODIGO_NO_COINCIDE` (ALTA) | `CODIGO_NO_COINCIDE` | 0.9967 | INCONSISTENTE |
| `CANTIDAD_DISCORDANTE` | CRZ-0000012 | INCONSISTENTE | BR-06 `CANTIDAD_DISCORDANTE` (MEDIA) | `CANTIDAD_DISCORDANTE` | 0.9959 | INCONSISTENTE |

**Tiempos de ejecución por registro (warm run):**

| true_label | Rules Engine (ms) | AI model (ms) |
|---|---|---|
| `CONSISTENTE` | 0.0974 | 34,876.35 *(cold start — primer encoding SentenceTransformer)* |
| `SIN_SOPORTE_CLINICO` | 0.1644 | 196.83 |
| `DIAGNOSTICO_NO_RELACIONADO` | 0.1436 | 130.92 |
| `NO_FACTURADO` | 0.1441 | 238.88 |
| `CODIGO_NO_COINCIDE` | 0.1645 | 182.64 |
| `CANTIDAD_DISCORDANTE` | 0.1025 | 124.42 |

> El tiempo de 34,876 ms en el primer registro corresponde al cold start del `SentenceTransformer`: carga del modelo de embeddings desde disco y primera codificación. Las ejecuciones posteriores son todas < 240 ms por registro.

---

## 8. Validación en Lote — 48 Registros Estratificados (Step 6)

Muestra balanceada de 48 registros (8 por clase, `random_state=42`), ejecutada sobre ambos componentes.

### Resultados del Motor de Reglas

| Parámetro | Valor |
|---|---|
| Registros procesados | 48 |
| INCONSISTENTE detectados | 26/48 (54.2%) |
| CONSISTENTE | 22/48 (45.8%) |
| Tiempo total | 1.05 ms |
| Tiempo por registro | 0.022 ms |

### Resultados del Modelo AI

| Parámetro | Valor |
|---|---|
| Registros procesados | 48 |
| Accuracy sobre muestra balanceada | **87.5% (42/48)** |
| AI INCONSISTENTE | 40/48 (83.3%) |
| AI CONSISTENTE | 8/48 (16.7%) |
| Tiempo total | 981.82 ms |
| Tiempo por registro | 20.45 ms |

**Distribución de predicciones del modelo vs. distribución real:**

| Clase | Real | AI pred |
|---|---|---|
| `CANTIDAD_DISCORDANTE` | 8 | 8 |
| `CODIGO_NO_COINCIDE` | 8 | 8 |
| `CONSISTENTE` | 8 | 8 |
| `DIAGNOSTICO_NO_RELACIONADO` | 8 | 10 |
| `NO_FACTURADO` | 8 | 8 |
| `SIN_SOPORTE_CLINICO` | 8 | 6 |

> El modelo sobre-predice `DIAGNOSTICO_NO_RELACIONADO` (+2) y sub-predice `SIN_SOPORTE_CLINICO` (-2) en esta muestra balanceada, consistente con las métricas de EV-01 (precisión baja en ambas clases).

---

## 9. Verificación del Contrato de la API (Step 7)

### GET /health

```json
Status: 200 OK
Body: {"status": "ok", "model": "xgboost_hybrid_sentence"}
Tiempo: 25.46 ms
```

### POST /predict — Un registro por clase

Todos los requests retornaron HTTP 200. Los campos `predicted_alert`, `predicted_status`, `confidence`, `probabilities` (6 clases) y `model` están presentes en todas las respuestas.

| true_label | predicted_alert | predicted_status | confidence | HTTP | Tiempo (ms) |
|---|---|---|---|---|---|
| `CONSISTENTE` | `DIAGNOSTICO_NO_RELACIONADO` | INCONSISTENTE | 0.6876 | 200 | 85.79 |
| `SIN_SOPORTE_CLINICO` | `CONSISTENTE` | CONSISTENTE | 0.9090 | 200 | 107.99 |
| `DIAGNOSTICO_NO_RELACIONADO` | `DIAGNOSTICO_NO_RELACIONADO` | INCONSISTENTE | 0.6868 | 200 | 127.14 |
| `NO_FACTURADO` | `NO_FACTURADO` | INCONSISTENTE | 0.9983 | 200 | 207.18 |
| `CODIGO_NO_COINCIDE` | `CODIGO_NO_COINCIDE` | INCONSISTENTE | 0.9967 | 200 | 107.08 |
| `CANTIDAD_DISCORDANTE` | `CANTIDAD_DISCORDANTE` | INCONSISTENTE | 0.9959 | 200 | 100.69 |

---

## 10. Verificación de Probabilidades (Step 8)

| Verificación | Resultado |
|---|---|
| Clases en output == clases del registry | ✅ |
| Suma de probabilidades | 1.000000 (≈ 1.0) |
| Todos los valores en [0,1] | ✅ |
| Campo `model` contiene nombre correcto | ✅ `xgboost_hybrid_sentence` |
| Campo `predicted_status` presente | ✅ |
| Campo `confidence` == max(probabilities) | ✅ |

---

## 11. Alineación de Tipos de Alerta — Rules Engine vs. AI (Step 9)

| Componente | Tipos de salida |
|---|---|
| Rules Engine (+ CONSISTENTE) | `CANTIDAD_DISCORDANTE`, `CODIGO_NO_COINCIDE`, `CONSISTENTE`, `DIAGNOSTICO_NO_RELACIONADO`, `NO_FACTURADO`, `SIN_SOPORTE_CLINICO` |
| AI model classes | `CANTIDAD_DISCORDANTE`, `CODIGO_NO_COINCIDE`, `CONSISTENTE`, `DIAGNOSTICO_NO_RELACIONADO`, `NO_FACTURADO`, `SIN_SOPORTE_CLINICO` |
| **Alineación perfecta** | ✅ |

Los 6 tipos de alerta del Motor de Reglas corresponden exactamente a las 6 clases del modelo `xgboost_hybrid_sentence`. La integración semántica entre ambas capas es completa.

---

## 12. Errores de Integración Encontrados

### ERROR-01: sklearn InconsistentVersionWarning (no bloqueante)

**Descripción:** El artefacto `hybrid_feature_builder.joblib` fue serializado con `scikit-learn==1.9.0` y el entorno de ejecución tiene `scikit-learn==1.7.2`. sklearn emite un `InconsistentVersionWarning` en cada deserialización.

**Impacto:** No bloqueante. El pipeline funcionó correctamente y produjo predicciones válidas. sklearn garantiza compatibilidad de lectura entre versiones menores en la mayoría de los estimators (SimpleImputer, StandardScaler, Pipeline, OneHotEncoder, ColumnTransformer, LabelEncoder).

**Recomendación:** Re-serializar los artefactos con la versión de sklearn del entorno de ejecución destino para eliminar el warning en producción.

### ERROR-02: NaN en campos del dataset no serializable por TestClient (no bloqueante)

**Descripción:** Los registros del Master Dataset contienen valores `NaN` en campos opcionales. El cliente HTTP (TestClient/httpx) no puede serializar `NaN` como JSON válido (`allow_nan=False`).

**Impacto:** No bloqueante en producción. Un cliente HTTP real (browser, curl, otro servicio) enviaría `null` en lugar de `NaN`. El predictor maneja `None`/`null` correctamente a través del `SimpleImputer` del pipeline.

**Recomendación:** La API debería documentar que `null` es el valor esperado para campos ausentes, no `NaN`.

### Comportamiento de la primera llamada al SentenceTransformer (no es error)

La primera invocación del `SentenceTransformer.encode()` tomó ~34,876 ms porque carga los pesos del modelo local desde disco (`sentence_transformer_model/`). Las llamadas posteriores tomaron entre 124–238 ms. Este es el comportamiento esperado de cold start de un modelo de embeddings.

---

## 13. Análisis de Predicciones Incorrectas

### Caso CRZ-0000004 (true_label=CONSISTENTE, predicted=DIAGNOSTICO_NO_RELACIONADO)

El Motor de Reglas clasificó el registro como CONSISTENTE (ninguna regla disparó). El modelo AI predijo `DIAGNOSTICO_NO_RELACIONADO` con confianza 0.6876 — relativamente baja, lo que indica incertidumbre del modelo. Este es un caso de falso positivo del modelo AI. Consistente con la precision de DIAGNOSTICO_NO_RELACIONADO en EV-01 (0.099), que es la clase con mayor tasa de error del sistema.

### Caso CRZ-0000021 (true_label=SIN_SOPORTE_CLINICO, predicted=CONSISTENTE)

El Motor de Reglas no detectó la inconsistencia (el registro no tiene los campos determinísticos que activan BR-02 de forma directa). El modelo AI predijo `CONSISTENTE` con confianza 0.909 — un falso negativo de alta confianza. Consistente con el recall de SIN_SOPORTE_CLINICO en EV-01 (0.4375), que es la segunda clase más difícil de detectar.

---

## 14. Resumen de Tiempos de Ejecución

Todos los tiempos provienen de mediciones reales durante la ejecución.

| Operación | Tiempo |
|---|---|
| Carga del dataset (3,126 × 55) | 135.10 ms |
| Inicialización de MedicalAuditorPredictor | 103.65 ms |
| Inicialización de MedicalValidationEngine | 0.03 ms |
| Primer inference AI (cold start — SentenceTransformer) | ~34,876 ms |
| Inference AI subsiguiente (warm) | 124–238 ms/registro |
| Rules Engine por registro | 0.10–0.16 ms |
| Rules Engine batch (48 registros) | 1.05 ms total / 0.022 ms por registro |
| AI model batch (48 registros) | 981.82 ms total / 20.45 ms por registro |
| API GET /health | 25.46 ms |
| API POST /predict (warm) | 86–207 ms |

---

## 15. Limitaciones Encontradas

| ID | Limitación | Impacto | Contexto |
|---|---|---|---|
| L-01 | Cold start del SentenceTransformer (~35 s) en primera llamada por proceso. | Medio — solo afecta el arranque del servidor. | Una vez inicializado, el modelo queda en memoria y las llamadas subsiguientes son rápidas. |
| L-02 | sklearn version mismatch entre entorno de serialización (1.9.0) y entorno de ejecución (1.7.2). | Bajo — warnings no bloqueantes, resultados correctos. | Requiere re-serialización en entorno homogéneo para producción. |
| L-03 | La API no maneja explícitamente la conversión de `NaN` a `null`. Los clientes deben enviar `null` para campos ausentes. | Bajo — comportamiento estándar de JSON. | El pipeline interno (SimpleImputer) maneja `None` correctamente. |
| L-04 | El modelo `xgboost_hybrid_sentence` tiene baja precisión en `DIAGNOSTICO_NO_RELACIONADO` (0.099) y `SIN_SOPORTE_CLINICO` (recall 0.4375), tal como se documentó en EV-01. | Medio — estas dos clases son las más difíciles. | Conocido desde EV-01. La arquitectura híbrida es la mitigación actual. |
| L-05 | No existe un componente de fusión formal entre los resultados del Motor de Reglas y el modelo AI. La lógica de decisión combinada está en el cliente/orquestador. | Bajo para MVP. | Diseño intencional: el Motor de Reglas y el modelo AI son capas independientes y complementarias. |

---

## 16. Conclusiones

1. **El flujo end-to-end funciona correctamente.** Todos los componentes se cargan, inicializan y ejecutan sin errores bloqueantes. La cadena completa `dataset → preprocessing → SentenceTransformer → XGBoost → predicción → API` opera de principio a fin.

2. **La integración entre el Motor de Reglas y el modelo AI es semánticamente consistente.** Los 6 tipos de alerta producidos por las reglas determinísticas corresponden exactamente a las 6 clases del modelo `xgboost_hybrid_sentence`. No existe conflicto de vocabulario entre ambas capas.

3. **La API REST responde correctamente.** `GET /health` retorna el modelo activo con HTTP 200. `POST /predict` retorna las 6 predicciones requeridas con HTTP 200, incluyendo `predicted_alert`, `predicted_status`, `confidence`, `probabilities` y `model` en todas las respuestas.

4. **El modelo produce predicciones válidas.** La suma de probabilidades es exactamente 1.0, todos los valores están en [0,1], y los 4 de 6 registros representativos son predichos correctamente. En la muestra balanceada de 48 registros, la accuracy es 87.5% (42/48).

5. **Los errores encontrados son no bloqueantes.** El warning de versión de sklearn y el comportamiento de NaN no impiden el funcionamiento del sistema y están mitigados por el pipeline de preprocesamiento.

6. **Las limitaciones conocidas de EV-01 se confirman en el contexto E2E.** `DIAGNOSTICO_NO_RELACIONADO` y `SIN_SOPORTE_CLINICO` son las clases con mayor tasa de error, tanto en el Motor de Reglas (limitación de la matriz BR-03) como en el modelo AI (métricas EV-01).

---

## 17. Verificación de Criterios de Aceptación

| Criterio | Estado |
|---|---|
| Flujo completo E2E ejecutado con datos reales | ✅ |
| Pipeline de preprocesamiento verificado | ✅ |
| Motor de Reglas verificado | ✅ |
| Modelo `xgboost_hybrid_sentence` produce predicciones válidas | ✅ |
| Alertas corresponden con la predicción | ✅ |
| API responde correctamente en todos los endpoints | ✅ |
| Sin errores de integración bloqueantes | ✅ |
| Tiempos provienen de mediciones reales | ✅ |
| Limitaciones documentadas | ✅ |
| Sin información del modelo anterior (CNN 1D) | ✅ |
| Sin modificaciones a componentes existentes | ✅ |

---

## 18. Relación con los siguientes Issues

- **EV-04** — Business Validation: contrastará los KPIs de negocio de BU-04 contra los resultados obtenidos en el flujo E2E validado en este reporte.
- **EV-05** — Final Evaluation Report: consolidará EV-01, EV-02, EV-03 y EV-04 en el reporte final de evaluación de la fase.
