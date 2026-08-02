# 🏥 System Architecture

## Project

Health & Life IPS - Medical Digital Auditor

---

# Objective

Develop an AI-powered Medical Digital Auditor capable of validating Clinical History records against Pre-Invoice data before billing.

---

# High-Level Architecture

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

---

# Main Components

## Data Layer

Input datasets:

- Patients
- Healthcare Encounters
- Clinical History
- Pre-Invoice
- Validation Data

Output:

Master Dataset

---

## AI Layer

Responsible for:

- Prediction
- Pattern Detection
- Anomaly Detection

---

## Business Rules Layer

Responsible for:

- Clinical validations
- Billing validations
- Diagnosis validations
- Treatment validations

---

## Backend Layer

Technology

FastAPI

Responsibilities

- Receive requests
- Execute Medical Auditor
- Return alerts

---

## Dashboard

Technology

Streamlit

Responsibilities

- Display alerts
- Execute validations
- Show patient summary
- Show inconsistencies

---

# Folder Responsibilities

data/

Raw datasets

notebooks/

EDA

Training

Experiments

src/backend/

Business logic

src/ai/

Machine Learning

dashboard/

User Interface

reports/

Generated reports

docs/

Documentation

---

# Data Flow

CSV

↓

Cleaning

↓

Master Dataset

↓

Rules Engine

↓

AI Model

↓

Medical Auditor

↓

REST API

↓

Dashboard

---

# Technology Stack

Python

Pandas

Scikit-Learn

FastAPI

Streamlit

GitHub

GitHub Actions

Docker (optional)

---

# Future Improvements

- Real-time integration with HIS
- Cloud deployment
- Authentication
- Multi-hospital support
- Continuous model retraining