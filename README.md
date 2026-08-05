### HealthLife AI Auditor

# Description

**HealthLife AI Auditor** es una solución de Auditoría Médica Digital desarrollada para **Health & Life IPS SAS**. El sistema combina un **Motor de Reglas de Negocio** con técnicas de **Inteligencia Artificial** para validar automáticamente la consistencia entre la Historia Clínica y la Pre-facturación antes de la emisión de la factura, generando alertas preventivas sobre inconsistencias clínicas y administrativas.

---

# Live Demo

## REST API

https://healthlife-api.onrender.com


---

## Project Resources

Google Drive (documentation, reports, presentation and deliverables)

https://drive.google.com/drive/folders/1DNaGulYBbmoAVqPRwV3Fr4ee65qnVQrT?usp=sharing

---

# Business Problem

Actualmente, las inconsistencias entre la Historia Clínica y la Pre-facturación suelen detectarse durante auditorías posteriores a la facturación, generando:

- Glosas y rechazos.
- Retrabajos administrativos.
- Pérdidas económicas.
- Incremento del tiempo de auditoría.

Este proyecto propone un sistema híbrido que permita detectar dichas inconsistencias de forma automática antes de emitir la factura.

---

# Objectives

- Integrar y preparar la información proveniente de historias clínicas y pre-facturas.
- Desarrollar un modelo de Inteligencia Artificial para detectar inconsistencias clínicas y de facturación.
- Implementar un motor de reglas de negocio para validar automáticamente la información.
- Generar alertas preventivas antes del proceso de facturación.
- Evaluar el desempeño del sistema mediante métricas técnicas y de negocio.

---

# Project Architecture

```
                CSV Files
                     │
                     ▼
             Data Preparation
                     │
                     ▼
              Master Dataset
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
Business Rules Engine          AI Validation Model
 (BR-01, BR-02, BR-03...)      (XGBoost Hybrid Model)
      │                             │
      └──────────────┬──────────────┘
                     ▼
            Medical Digital Auditor
                     │
                     ▼
                 REST API 
                     │
                     ▼
             Streamlit Dashboard             
```

See the complete architecture in **ARCHITECTURE.md**.

---

# Repository Structure

```
data/
├── raw/
├── processed/
└── master/

docs/

models/

notebooks/

src/


tests/

dashboard/


requirements.txt

README.md
```

---

# Tech Stack

- Python
- Pandas
- NumPy
- Scikit-Learn
- TensorFlow / Keras
- XGBoost
- LightGBM
- SentenceTransformers
- FastAPI
- Streamlit
- Pytest
- GitHub Actions

---

# Dataset

El proyecto utiliza cinco fuentes principales de información proporcionadas por **Health & Life IPS SAS**.

| Dataset | Descripción |
|----------|-------------|
| 01_pacientes.csv | Información demográfica del paciente |
| 02_atenciones.csv | Información de las atenciones médicas |
| 03_historia_clinica_detalle.csv | Procedimientos, tratamientos y exámenes registrados |
| 04_prefactura.csv | Servicios incluidos en la pre-factura |
| 05_cruce_validacion.csv | Ground Truth utilizado para entrenamiento y evaluación |

El proceso de preparación integra estas fuentes para construir un **Master Dataset** utilizado por el Motor de Reglas y los modelos de Inteligencia Artificial.

---

# Methodology

El proyecto sigue la metodología **ASUM-DM**.

```
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

# Team

**Predictors Team** — Samsung Innovation Campus 2025

| Member | Role |
|----------|----------------|
| David Antonio García Contreras | Team Leader / Business Understanding |
| Miguel Ángel Alfonso Saavedra | Data Understanding |
| Yineth Daniela Botina Puerres | Data Preparation |
| Diego Alejandro Bejarano Prada | Modeling |
| Johann Smith Rivera Montoya | Evaluation & Dashboard |

---

# Installation

```bash
git clone <repository-url>

cd healthlife-ai-auditor

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```
---

# Deployment

The production REST API is deployed on Render.

Platform:

- Render

Production endpoint:

https://healthlife-api.onrender.com

Documentation:

https://healthlife-api.onrender.com/docs


---

# Usage

Entrenar y comparar los modelos implementados:

```bash
python 
```

Ejecutar las pruebas:

```bash
pytest
```

La API REST y el Dashboard pueden ejecutarse siguiendo la documentación incluida en las carpetas correspondientes.

---

# License

Proyecto académico desarrollado dentro del programa **Samsung Innovation Campus 2025**, en colaboración con **Health & Life IPS SAS**.

---

# Project Status

**Current Version:** 1.0

**Status:** ✅ Completed

The project has successfully completed all phases of the ASUM-DM methodology:

- Business Understanding
- Analytic Approach
- Data Understanding
- Data Preparation
- Modeling
- Evaluation
- Deployment

The REST API has been deployed in production using Render and the project is ready for demonstration.

---
# Project Progress
## ✅ Business Understanding (Completed)

- Business Problem Analysis
- Functional & Non-Functional Requirements
- Medical Billing Business Rules
- Project KPIs
- Business Understanding Review

## ✅ Analytic Approach (Completed)

- Solution Architecture
- Data Architecture & Entity Relationship Diagram (ERD)
- Automated Validation Strategy
- Analytical Techniques & AI Approach
- Technical Stack & Development Strategy
- Analytic Approach Review

## ✅ Data Understanding (Completed)
- Source Dataset Analysis
- Data Dictionary
- Data Quality Assessment
- Dataset Relationships
- Exploratory Data Analysis (EDA)
- Data Understanding Review

## ✅ Data Preparation (Completed)

- Data Cleaning and Standardization
- Healthcare Dataset Integration
- Master Dataset Construction
- Feature Engineering
- Automated Preprocessing Pipeline
- Prepared Dataset Validation
- Production-Ready Dataset Export

## ✅ Modeling

### Business Rules Engine

- BR-01: Detects **NO_FACTURADO** and **CODIGO_NO_COINCIDE**.
- BR-02: Detects missing clinical support.
- BR-03: Validates Diagnosis–Procedure consistency using an explicit matrix.

### Machine Learning Models

The official training pipeline compares the following models:

- Random Forest
- Logistic Regression + TF-IDF
- SVM + TF-IDF
- SentenceTransformer + Logistic Regression
- SentenceTransformer + SVM
- MLP Hybrid
- CNN 1D
- XGBoost Hybrid
- LightGBM Hybrid

### Selected Model

**XGBoost Hybrid Sentence**

| Metric | Value |
|---------|-------|
| Accuracy | 0.7652 |
| Balanced Accuracy | 0.7585 |
| Macro-F1 | 0.7347 |
| Recall (Inconsistencies) | 0.7385 |
| Selection Score | 0.7408 |



### Testing

- ✅ 13/13 tests passed.


## ✅ Evaluation (Completed)

- Medical Business Rules Validation
- End-to-End Validation
- Business KPI Validation
- Final Evaluation Report

## ✅ Deployment (Completed)

- REST API
- Interactive Dashboard
- Production Deployment
- Final Documentation

---

## Final Results

The implemented solution integrates:

- Business Rules Engine (BR-01 to BR-06)
- Hybrid XGBoost AI Model
- REST API developed with FastAPI
- Interactive Dashboard built with Streamlit
- Automated Alert Generation
- End-to-End Medical Billing Validation Workflow

Main achievements:

- Accuracy: 76.52%
- Balanced Accuracy: 75.85%
- Macro-F1: 73.47%
- Inconsistency Recall: 73.85%
- Complete ASUM-DM implementation
- Production deployment completed
  
---
