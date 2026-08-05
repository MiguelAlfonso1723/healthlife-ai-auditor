# Medical Digital Auditor Dashboard

Dashboard Streamlit interactivo para el proyecto Capstone Health & Life IPS.

## Ejecutar

```powershell
.\.venv\Scripts\streamlit.exe run dashboard\app.py
```

URL local por defecto: http://localhost:8501

## Paginas

1. Dashboard Ejecutivo
2. Validacion de Registro
3. Historial de Validaciones
4. Analitica
5. Desempeno del Modelo
6. Rendimiento del Sistema
7. Acerca del Proyecto

## Cobertura funcional

- Todas las graficas se renderizan con Plotly y son interactivas.
- La pagina de validacion ejecuta el motor de reglas deterministico y, si los artefactos estan disponibles, usa el predictor real empaquetado en `src.ai.inference`.
- Si falta algun artefacto pesado del modelo, la validacion conserva una estimacion historica para que el dashboard siga operativo y avise al usuario.
- El dashboard consume `data/master/master_dataset_features.csv`, `models/model_comparison.csv`, `models/model_registry.json` y los reportes de `docs/reports/model_reports`.
