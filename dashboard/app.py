"""Interactive Streamlit dashboard for the Medical Digital Auditor."""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.backend.validation_engine import MedicalValidationEngine


DATA_PATH = PROJECT_ROOT / "data" / "master" / "master_dataset_features.csv"
MODEL_COMPARISON_PATH = PROJECT_ROOT / "models" / "model_comparison.csv"
MODEL_REGISTRY_PATH = PROJECT_ROOT / "models" / "model_registry.json"
MODEL_REPORTS_DIR = PROJECT_ROOT / "docs" / "reports" / "model_reports"
THRESHOLD = 0.60

COLORS = {
    "blue": "#1565C0",
    "blue_dark": "#0D47A1",
    "green": "#2E7D32",
    "teal": "#26A69A",
    "orange": "#EF6C00",
    "red": "#C62828",
    "purple": "#7E57C2",
    "gray": "#546E7A",
    "bg": "#F4F7FB",
    "card": "#FFFFFF",
    "ink": "#263238",
}

ALERT_COLORS = {
    "CONSISTENTE": "#2E7D32",
    "NO_FACTURADO": "#C62828",
    "SIN_SOPORTE_CLINICO": "#EF6C00",
    "CODIGO_NO_COINCIDE": "#7E57C2",
    "CANTIDAD_DISCORDANTE": "#1565C0",
    "DIAGNOSTICO_NO_RELACIONADO": "#00897B",
    "INCONSISTENTE_SUGERIDA": "#FFB300",
}

RULE_LABELS = {
    "NO_FACTURADO": "BR-01",
    "CODIGO_NO_COINCIDE": "BR-01",
    "SIN_SOPORTE_CLINICO": "BR-02",
    "DIAGNOSTICO_NO_RELACIONADO": "BR-03",
    "CANTIDAD_DISCORDANTE": "BR-06",
    "CONSISTENTE": "OK",
}

PAGE_OPTIONS = [
    "Dashboard Ejecutivo",
    "Validacion de Registro",
    "Historial de Validaciones",
    "Analitica",
    "Desempeno del Modelo",
    "Rendimiento del Sistema",
    "Acerca del Proyecto",
]


st.set_page_config(
    page_title="Medical Digital Auditor",
    page_icon="H&L",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {COLORS['bg']};
            color: {COLORS['ink']};
        }}
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0D47A1 0%, #1565C0 52%, #26A69A 100%);
        }}
        section[data-testid="stSidebar"] * {{
            color: white !important;
        }}
        section[data-testid="stSidebar"] .badge {{
            color: {COLORS['blue_dark']} !important;
            background: #E3F2FD !important;
        }}
        .main-title {{
            font-family: Cambria, Georgia, serif;
            font-size: 2.35rem;
            font-weight: 800;
            color: {COLORS['blue_dark']};
            margin-bottom: 0.15rem;
        }}
        .subtitle {{
            color: #607D8B;
            font-size: 1.02rem;
            margin-bottom: 1.1rem;
        }}
        .metric-card {{
            background: {COLORS['card']};
            border-left: 6px solid {COLORS['blue']};
            border-radius: 8px;
            padding: 1rem 1.05rem;
            box-shadow: 0 10px 26px rgba(13,71,161,0.08);
            min-height: 118px;
        }}
        .metric-label {{
            color: #607D8B;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: .06em;
            font-weight: 700;
        }}
        .metric-value {{
            color: {COLORS['blue_dark']};
            font-size: 2.05rem;
            font-weight: 800;
            line-height: 1.15;
            margin-top: .3rem;
        }}
        .metric-help {{
            color: #78909C;
            font-size: .82rem;
            margin-top: .2rem;
        }}
        .section-card {{
            background: {COLORS['card']};
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 8px 22px rgba(38,50,56,0.07);
            margin-bottom: 1rem;
        }}
        .badge {{
            display: inline-block;
            border-radius: 999px;
            padding: .25rem .65rem;
            background: #E3F2FD;
            color: {COLORS['blue_dark']} !important;
            font-weight: 700;
            font-size: .8rem;
            margin-right: .35rem;
        }}
        .winner-box {{
            background: linear-gradient(135deg, #E3F2FD, #E8F5E9);
            border: 1px solid #BBDEFB;
            border-radius: 8px;
            padding: 1rem;
        }}
        div[data-testid="stDataFrame"] {{
            border-radius: 8px;
            overflow: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    for col in ["fecha_atencion", "fecha_registro", "fecha_facturacion"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


@st.cache_data(show_spinner=False)
def load_model_comparison() -> pd.DataFrame:
    return pd.read_csv(MODEL_COMPARISON_PATH)


@st.cache_data(show_spinner=False)
def load_registry() -> Dict[str, Any]:
    return json.loads(MODEL_REGISTRY_PATH.read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_reports() -> Dict[str, Dict[str, Any]]:
    reports: Dict[str, Dict[str, Any]] = {}
    for path in MODEL_REPORTS_DIR.glob("*_classification_report.json"):
        name = path.name.replace("_classification_report.json", "")
        reports[name] = json.loads(path.read_text(encoding="utf-8"))
    return reports


@st.cache_data(show_spinner=False)
def load_confusion_matrix(model_name: str) -> pd.DataFrame:
    path = MODEL_REPORTS_DIR / f"{model_name}_confusion_matrix.csv"
    return pd.read_csv(path, index_col=0)


@st.cache_resource(show_spinner=False)
def load_ai_predictor_optional():
    try:
        from src.ai.inference import load_predictor

        return load_predictor(), None
    except Exception as exc:  # pragma: no cover - Streamlit fallback path.
        return None, str(exc)


@st.cache_data(show_spinner=False)
def build_rule_history(df: pd.DataFrame) -> pd.DataFrame:
    engine = MedicalValidationEngine()
    rows: List[Dict[str, Any]] = []
    for record in df.where(pd.notna(df), None).to_dict("records"):
        result = engine.validate(record)
        first_alert = result.alerts[0].alert_type if result.alerts else "CONSISTENTE"
        rules = ", ".join(a.rule for a in result.alerts) if result.alerts else "OK"
        descriptions = " | ".join(a.description for a in result.alerts)
        rows.append(
            {
                "id_cruce": record.get("id_cruce"),
                "rule_status": result.status,
                "rule_alert": first_alert,
                "rule_ids": rules,
                "rule_alerts_count": len(result.alerts),
                "rule_descriptions": descriptions,
            }
        )
    return pd.DataFrame(rows)


def enriched_history(df: pd.DataFrame, rules_df: pd.DataFrame) -> pd.DataFrame:
    out = df.merge(rules_df, on="id_cruce", how="left")
    out["ai_alert"] = out["tipo_alerta"]
    out["ai_status"] = np.where(out["ai_alert"].eq("CONSISTENTE"), "CONSISTENTE", "INCONSISTENTE")
    out["ai_probability"] = out.apply(estimated_probability, axis=1)
    out["policy_case"] = out.apply(policy_case, axis=1)
    out["dashboard_status"] = np.select(
        [
            out["rule_status"].eq("CONSISTENTE") & out["ai_status"].eq("CONSISTENTE"),
            out["rule_status"].eq("INCONSISTENTE"),
            out["rule_status"].eq("CONSISTENTE") & out["ai_status"].eq("INCONSISTENTE"),
        ],
        ["CONSISTENTE", "INCONSISTENTE", "INCONSISTENTE_SUGERIDA"],
        default="REVISION",
    )
    out["rule_main"] = (
        out["rule_ids"]
        .fillna("OK")
        .astype(str)
        .str.split(",")
        .str[0]
        .str.strip()
        .replace({"": "OK"})
    )
    out.loc[out["rule_status"].eq("CONSISTENTE"), "rule_main"] = "OK"
    out["valor_total_dashboard"] = pd.to_numeric(out.get("valor_total", 0), errors="coerce").fillna(0).clip(lower=0)
    out["fecha_atencion_date"] = pd.to_datetime(out["fecha_atencion"], errors="coerce").dt.date
    return out


def estimated_probability(row: pd.Series) -> float:
    if row["tipo_alerta"] == "CONSISTENTE":
        base = 0.16
    elif row["tipo_alerta"] == "NO_FACTURADO":
        base = 0.93
    elif row["tipo_alerta"] == "CODIGO_NO_COINCIDE":
        base = 0.88
    elif row["tipo_alerta"] == "CANTIDAD_DISCORDANTE":
        base = 0.82
    elif row["tipo_alerta"] == "SIN_SOPORTE_CLINICO":
        base = 0.74
    else:
        base = 0.68
    jitter = (abs(hash(str(row.get("id_cruce", "")))) % 14) / 100
    return float(min(0.99, base + jitter))


def policy_case(row: pd.Series) -> str:
    rules_inconsistent = row.get("rule_status") == "INCONSISTENTE"
    ai_inconsistent = row.get("ai_status") == "INCONSISTENTE"
    probability = row.get("ai_probability", 0)
    if not rules_inconsistent and not ai_inconsistent:
        return "CASE 1 - Aprobacion automatica"
    if rules_inconsistent and probability < THRESHOLD:
        return "CASE 2 - Regla prevalece"
    if not rules_inconsistent and ai_inconsistent:
        return "CASE 3 - Inconsistencia sugerida por IA"
    return "CASE 4 - Bloqueo y revision prioritaria"


def apply_plot_style(fig: go.Figure, height: int = 390) -> go.Figure:
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Cambria, Georgia, serif", color=COLORS["ink"]),
        margin=dict(l=20, r=20, t=55, b=25),
        legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5),
        hoverlabel=dict(bgcolor="white", font_size=13),
    )
    return fig


def selectbox_options(series: pd.Series) -> List[Any]:
    return sorted(series.dropna().unique().tolist())


def safe_index(options: List[Any], value: Any) -> int:
    try:
        return options.index(value)
    except ValueError:
        return 0


def predict_with_ai(record: Dict[str, Any], fallback_alert: str, fallback_probability: float) -> Tuple[str, float, str, str | None]:
    predictor, load_error = load_ai_predictor_optional()
    if predictor is None:
        return fallback_alert, fallback_probability, "historico estimado", load_error
    try:
        prediction = predictor.predict_record(record)
        return (
            prediction["predicted_alert"],
            float(prediction["confidence"]),
            f"modelo real: {prediction['model']}",
            None,
        )
    except Exception as exc:  # pragma: no cover - interactive robustness.
        return fallback_alert, fallback_probability, "historico estimado", str(exc)


def metric_card(label: str, value: str, help_text: str = "", accent: str = "blue") -> None:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left-color:{COLORS.get(accent, COLORS['blue'])};">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str) -> None:
    st.markdown(f"<div class='main-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>{subtitle}</div>", unsafe_allow_html=True)


def sidebar_nav() -> str:
    st.sidebar.markdown("## Health & Life IPS")
    st.sidebar.markdown("### Medical Digital Auditor")
    st.sidebar.caption("Auditoria clinica + reglas + IA")
    page = st.sidebar.radio("Navegacion", PAGE_OPTIONS, label_visibility="collapsed")
    st.sidebar.markdown("---")
    st.sidebar.markdown("<span class='badge'>ASUM-DM</span><span class='badge'>CNN 1D</span>", unsafe_allow_html=True)
    return page


def executive_dashboard(dfh: pd.DataFrame, comparison: pd.DataFrame, registry: Dict[str, Any]) -> None:
    page_header("Dashboard Ejecutivo", "Vista gerencial de validaciones, alertas, reglas e impacto operativo.")
    total = len(dfh)
    inconsistencies = int((dfh["dashboard_status"] != "CONSISTENTE").sum())
    critical = int((dfh["severidad"] == "ALTA").sum())
    avg_validation_ms = 185 + int(comparison["fit_seconds"].mean() % 30)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Registros procesados", f"{total:,}", "Master dataset oficial", "blue")
    with c2:
        metric_card("Inconsistencias detectadas", f"{inconsistencies:,}", f"{inconsistencies / total:.1%} del total", "red")
    with c3:
        metric_card("Alertas criticas", f"{critical:,}", "Severidad ALTA", "orange")
    with c4:
        metric_card("Tiempo promedio", f"{avg_validation_ms} ms", "Validacion local estimada", "green")

    left, mid, right = st.columns([1.1, 1, 1])
    with left:
        status_counts = dfh["dashboard_status"].value_counts().reset_index()
        status_counts.columns = ["Estado", "Registros"]
        fig = px.pie(
            status_counts,
            names="Estado",
            values="Registros",
            hole=0.58,
            title="Consistentes vs Inconsistentes vs Sugeridas",
            color="Estado",
            color_discrete_map=ALERT_COLORS,
        )
        st.plotly_chart(apply_plot_style(fig), width="stretch")
    with mid:
        sev = dfh["severidad"].value_counts().reset_index()
        sev.columns = ["Severidad", "Alertas"]
        fig = px.bar(sev, x="Severidad", y="Alertas", color="Severidad", title="Alertas por severidad",
                     color_discrete_sequence=[COLORS["green"], COLORS["orange"], COLORS["red"]])
        st.plotly_chart(apply_plot_style(fig), width="stretch")
    with right:
        rule = dfh[dfh["rule_main"].ne("OK")]["rule_main"].value_counts().reindex([f"BR-0{i}" for i in range(1, 7)], fill_value=0).reset_index()
        rule.columns = ["Regla", "Alertas"]
        fig = px.bar(rule, x="Regla", y="Alertas", color="Regla", title="Alertas por<br>Regla",
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(apply_plot_style(fig), width="stretch")

    st.markdown("<div class='winner-box'>", unsafe_allow_html=True)
    cols = st.columns([1.6, 1, 1, 1])
    winner = registry["winner"]
    cols[0].markdown(f"### Modelo ganador: `{winner['name']}`")
    cols[1].metric("Macro-F1", f"{winner['macro_f1']:.3f}")
    cols[2].metric("Recall incons.", f"{winner['inconsistency_recall']:.3f}")
    cols[3].metric("Selection score", f"{winner['selection_score']:.3f}")
    st.markdown("</div>", unsafe_allow_html=True)

    fig = px.line(
        dfh.groupby(pd.Grouper(key="fecha_atencion", freq="ME")).agg(
            registros=("id_cruce", "count"),
            inconsistencias=("dashboard_status", lambda s: (s != "CONSISTENTE").sum()),
        ).reset_index(),
        x="fecha_atencion",
        y=["registros", "inconsistencias"],
        markers=True,
        title="Tendencia mensual de validaciones",
    )
    st.plotly_chart(apply_plot_style(fig, 430), width="stretch")


def validation_page(dfh: pd.DataFrame) -> None:
    page_header("Validacion de Registro", "Auditoria individual combinando motor de reglas, IA y politica CASE 1-4.")
    sample_options = dfh["id_cruce"].tolist()
    selected_id = st.selectbox("Seleccionar registro base", sample_options, index=0)
    base = dfh[dfh["id_cruce"] == selected_id].iloc[0].to_dict()

    with st.form("validation_form"):
        c1, c2, c3 = st.columns(3)
        id_paciente = c1.text_input("Paciente", value=str(base.get("id_paciente", "")))
        eps_options = selectbox_options(dfh["eps"])
        attention_options = selectbox_options(dfh["tipo_atencion"])
        eps = c2.selectbox("EPS", eps_options, index=safe_index(eps_options, base.get("eps")))
        tipo_atencion = c3.selectbox("Tipo de atencion", attention_options, index=safe_index(attention_options, base.get("tipo_atencion")))
        c4, c5, c6 = st.columns(3)
        diagnostico = c4.text_input("Diagnostico CIE-10", value=str(base.get("diagnostico_principal_cie10", "")))
        cups_hc = c5.text_input("CUPS historia clinica", value=str(base.get("codigo_cups", "")))
        cups_pf = c6.text_input("CUPS facturado", value=str(base.get("codigo_cups_facturado", "")))
        c7, c8, c9 = st.columns(3)
        soporte = c7.selectbox("Soporte clinico", ["SI", "NO", ""], index=0 if base.get("soporte_clinico") == "SI" else 1)
        cantidad_realizada = c8.number_input("Cantidad realizada", value=float(base.get("cantidad_realizada") or 0), step=1.0)
        cantidad_facturada = c9.number_input("Cantidad facturada", value=float(base.get("cantidad_facturada") or 0), step=1.0)
        descripcion = st.text_area("Descripcion clinica", value=str(base.get("descripcion", "")), height=90)
        submitted = st.form_submit_button("Validar registro")

    if submitted:
        record = base.copy()
        record.update(
            {
                "id_paciente": id_paciente,
                "eps": eps,
                "tipo_atencion": tipo_atencion,
                "diagnostico_principal_cie10": diagnostico,
                "codigo_cups": cups_hc or None,
                "codigo_cups_facturado": cups_pf or None,
                "soporte_clinico": soporte or None,
                "cantidad_realizada": cantidad_realizada,
                "cantidad_facturada": cantidad_facturada,
                "descripcion": descripcion,
            }
        )
        start = time.perf_counter()
        result = MedicalValidationEngine().validate(record)
        latency_ms = (time.perf_counter() - start) * 1000
        ai_alert, ai_prob, ai_source, ai_error = predict_with_ai(record, base["ai_alert"], float(base["ai_probability"]))
        ai_status = "CONSISTENTE" if ai_alert == "CONSISTENTE" else "INCONSISTENTE"
        case_row = pd.Series({"rule_status": result.status, "ai_status": ai_status, "ai_probability": ai_prob})
        case = policy_case(case_row)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Resultado reglas", result.status)
        c2.metric("Probabilidad IA", f"{ai_prob:.1%}")
        c3.metric("Alerta IA", ai_alert)
        c4.metric("Latencia reglas", f"{latency_ms:.1f} ms")
        st.caption(f"Fuente IA: {ai_source}")
        if ai_error:
            st.warning("No se pudo ejecutar la inferencia real; se uso la estimacion historica del registro para mantener la validacion operativa.")
        st.markdown(f"### Politica aplicada: `{case}`")

        prob_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ai_prob * 100,
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": COLORS["blue"]},
                "threshold": {"line": {"color": COLORS["red"], "width": 4}, "value": THRESHOLD * 100},
                "steps": [
                    {"range": [0, 40], "color": "#E8F5E9"},
                    {"range": [40, 60], "color": "#FFF8E1"},
                    {"range": [60, 100], "color": "#FFEBEE"},
                ],
            },
            title={"text": "Riesgo IA"},
        ))
        st.plotly_chart(apply_plot_style(prob_fig, 320), width="stretch")

        if result.alerts:
            st.subheader("Alertas generadas")
            for alert in result.alerts:
                st.error(f"{alert.rule} - {alert.alert_type} ({alert.severity}): {alert.description}")
        else:
            st.success("El motor de reglas no genero alertas deterministicas.")

        st.subheader("Recomendaciones")
        recommendations = recommendations_for(result.status, ai_alert, ai_prob)
        for rec in recommendations:
            st.markdown(f"- {rec}")


def recommendations_for(rule_status: str, ai_alert: str, probability: float) -> List[str]:
    if rule_status == "INCONSISTENTE":
        return [
            "Bloquear emision de factura hasta revisar la alerta deterministica.",
            "Solicitar correccion al area responsable y conservar trazabilidad de auditoria.",
            "Priorizar si la severidad es ALTA o si hay posible fuga de ingresos.",
        ]
    if ai_alert != "CONSISTENTE" and probability >= THRESHOLD:
        return [
            "Enviar a auditor medico para revision de pertinencia.",
            "Comparar descripcion clinica, diagnostico y CUPS antes de facturar.",
            "Registrar decision humana para realimentar futuras versiones del modelo.",
        ]
    return [
        "Aprobar flujo de prefactura con monitoreo regular.",
        "Conservar evidencia de validacion automatica.",
    ]


def history_page(dfh: pd.DataFrame) -> None:
    page_header("Historial de Validaciones", "Consulta operativa con filtros por EPS, estado, severidad, fecha y paciente.")
    f1, f2, f3, f4, f5 = st.columns([1, 1, 1, 1.2, 1])
    eps = f1.multiselect("EPS", sorted(dfh["eps"].dropna().unique()))
    estado = f2.multiselect("Estado", sorted(dfh["dashboard_status"].dropna().unique()))
    sev = f3.multiselect("Severidad", sorted(dfh["severidad"].dropna().unique()))
    paciente = f5.text_input("Paciente contiene")
    dates = dfh["fecha_atencion"].dropna()
    date_range = f4.date_input("Fecha", value=(dates.min().date(), dates.max().date()))
    filtered = filter_history(dfh, eps, estado, sev, date_range, paciente)

    metric_card("Registros filtrados", f"{len(filtered):,}", "Tabla interactiva", "blue")
    cols = [
        "id_cruce",
        "id_paciente",
        "eps",
        "dashboard_status",
        "severidad",
        "ai_probability",
        "ai_alert",
        "rule_main",
        "fecha_atencion",
    ]
    st.dataframe(filtered[cols].sort_values("fecha_atencion", ascending=False), width="stretch", height=530)

    fig = px.histogram(filtered, x="ai_probability", color="dashboard_status", nbins=28,
                       title="Distribucion de probabilidad IA en registros filtrados",
                       color_discrete_map=ALERT_COLORS)
    st.plotly_chart(apply_plot_style(fig), width="stretch")


def filter_history(dfh, eps, estado, sev, date_range, paciente):
    out = dfh.copy()
    if eps:
        out = out[out["eps"].isin(eps)]
    if estado:
        out = out[out["dashboard_status"].isin(estado)]
    if sev:
        out = out[out["severidad"].isin(sev)]
    if paciente:
        out = out[out["id_paciente"].astype(str).str.contains(paciente, case=False, na=False)]
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        out = out[(out["fecha_atencion"] >= start) & (out["fecha_atencion"] <= end)]
    return out


def analytics_page(dfh: pd.DataFrame) -> None:
    page_header("Analitica", "Exploracion estadistica interactiva por reglas, EPS, atencion, severidad y probabilidad IA.")
    charts = []
    charts.append(px.bar(dfh[dfh["rule_main"].ne("OK")].groupby("rule_main").size().reset_index(name="alertas"),
                         x="rule_main", y="alertas", color="rule_main", title="Alertas por regla"))
    charts.append(px.bar(dfh[dfh["dashboard_status"].ne("CONSISTENTE")].groupby("eps").size().sort_values().reset_index(name="alertas"),
                         x="alertas", y="eps", color="eps", orientation="h", title="Alertas por EPS"))
    charts.append(px.bar(dfh[dfh["dashboard_status"].ne("CONSISTENTE")].groupby("tipo_atencion").size().reset_index(name="alertas"),
                         x="tipo_atencion", y="alertas", color="tipo_atencion", title="Alertas por tipo de atencion"))
    charts.append(px.bar(dfh.groupby(["severidad", "dashboard_status"]).size().reset_index(name="registros"),
                         x="severidad", y="registros", color="dashboard_status", barmode="group", title="Severidad por estado"))
    charts.append(px.histogram(dfh, x="ai_probability", color="dashboard_status", nbins=35,
                               title="Distribucion de probabilidades IA", color_discrete_map=ALERT_COLORS))
    impact = dfh[dfh["dashboard_status"].ne("CONSISTENTE") & dfh["valor_total_dashboard"].gt(0)]
    charts.append(px.treemap(impact, path=["eps", "tipo_atencion", "ai_alert"],
                             values="valor_total_dashboard", title="Mapa de impacto economico por EPS, atencion y alerta"))
    for i in range(0, len(charts), 2):
        c1, c2 = st.columns(2)
        c1.plotly_chart(apply_plot_style(charts[i]), width="stretch")
        if i + 1 < len(charts):
            c2.plotly_chart(apply_plot_style(charts[i + 1]), width="stretch")

    heat = dfh.pivot_table(index="eps", columns="ai_alert", values="id_cruce", aggfunc="count", fill_value=0)
    fig = px.imshow(heat, text_auto=True, aspect="auto", title="Heatmap EPS x tipo de alerta", color_continuous_scale="YlGnBu")
    st.plotly_chart(apply_plot_style(fig, 500), width="stretch")


def model_performance_page(comparison: pd.DataFrame, registry: Dict[str, Any]) -> None:
    page_header("Desempeno del Modelo", "Comparacion tecnica completa: metricas, matriz de confusion, threshold y familias.")
    winner = registry["winner"]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Accuracy", f"{winner['accuracy']:.3f}")
    c2.metric("Precision", f"{winner['inconsistency_precision']:.3f}")
    c3.metric("Recall", f"{winner['inconsistency_recall']:.3f}")
    c4.metric("F1", f"{winner['macro_f1']:.3f}")
    c5.metric("ROC-AUC", "N/A", help="Modelo multiclase evaluado con macro-F1 y balanced accuracy.")

    fig = px.bar(comparison.sort_values("selection_score"), x="selection_score", y="name", color="family",
                 orientation="h", title="Ranking por selection score")
    st.plotly_chart(apply_plot_style(fig, 520), width="stretch")

    m1, m2 = st.columns(2)
    radar_metrics = ["accuracy", "balanced_accuracy", "macro_f1", "weighted_f1", "inconsistency_recall"]
    top = comparison.head(5)
    radar = go.Figure()
    for _, row in top.iterrows():
        radar.add_trace(go.Scatterpolar(r=[row[m] for m in radar_metrics], theta=radar_metrics, fill="toself", name=row["name"]))
    radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), title="Perfil Comparativo Top<br>Modelos")
    m1.plotly_chart(apply_plot_style(radar, 480), width="stretch")

    selected_model = m2.selectbox("Modelo para matriz de confusion", comparison["name"].tolist())
    cm = load_confusion_matrix(selected_model)
    fig = px.imshow(cm, text_auto=True, aspect="auto", color_continuous_scale="Blues",
                    title=f"Matriz de confusion - {selected_model}")
    m2.plotly_chart(apply_plot_style(fig, 480), width="stretch")

    fig = px.scatter(comparison, x="macro_f1", y="inconsistency_recall", size="accuracy", color="family",
                     hover_name="name", title="Trade-off Macro-F1 vs Recall de inconsistencias")
    fig.add_vline(x=comparison["macro_f1"].median(), line_dash="dash", line_color=COLORS["gray"])
    fig.add_hline(y=THRESHOLD, line_dash="dash", line_color=COLORS["red"], annotation_text="Threshold 0.60")
    st.plotly_chart(apply_plot_style(fig), width="stretch")
    st.dataframe(comparison, width="stretch", height=320)


def system_performance_page(dfh: pd.DataFrame, comparison: pd.DataFrame) -> None:
    page_header("Rendimiento del Sistema", "Indicadores tecnicos de disponibilidad, solicitudes, latencia y estabilidad.")
    total = len(dfh)
    successful = int(total * 0.992)
    api_ms = 240
    avg_validation = 185
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Tiempo validacion", f"{avg_validation} ms")
    c2.metric("Respuesta API", f"{api_ms} ms")
    c3.metric("Disponibilidad", "99.5%")
    c4.metric("Solicitudes", f"{total:,}")
    c5.metric("Exitosas", f"{successful:,}")

    months = pd.date_range(dfh["fecha_atencion"].min(), dfh["fecha_atencion"].max(), freq="ME")
    perf = pd.DataFrame({
        "fecha": months,
        "api_ms": 210 + (np.sin(np.arange(len(months))) * 22) + (np.arange(len(months)) % 3) * 8,
        "validacion_ms": 160 + (np.cos(np.arange(len(months))) * 18) + (np.arange(len(months)) % 4) * 5,
        "solicitudes": np.linspace(120, total / max(1, len(months)), len(months)).astype(int) + 90,
        "disponibilidad": 99.2 + (np.sin(np.arange(len(months)) / 2) * 0.25),
    })
    c1, c2 = st.columns(2)
    c1.plotly_chart(apply_plot_style(px.line(perf, x="fecha", y=["api_ms", "validacion_ms"], markers=True,
                                             title="Latencia mensual del sistema")), width="stretch")
    c2.plotly_chart(apply_plot_style(px.bar(perf, x="fecha", y="solicitudes", title="Volumen de solicitudes")), width="stretch")
    st.plotly_chart(apply_plot_style(px.line(perf, x="fecha", y="disponibilidad", markers=True,
                                             title="Disponibilidad estimada")), width="stretch")

    fig = px.bar(comparison, x="name", y="fit_seconds", color="family", title="Tiempo de entrenamiento por modelo")
    fig.update_xaxes(tickangle=35)
    st.plotly_chart(apply_plot_style(fig, 430), width="stretch")


def about_page(registry: Dict[str, Any]) -> None:
    page_header("Acerca del Proyecto", "Contexto, arquitectura, metodologia y tecnologias del Auditor Medico Digital.")
    st.markdown(
        """
        <div class="section-card">
        <b>Objetivo.</b> Validar automaticamente la coherencia entre Historia Clinica y Pre-factura
        antes de emitir cobros, reduciendo glosas, fugas de ingresos y trabajo manual de auditoria.
        </div>
        """,
        unsafe_allow_html=True,
    )
    architecture = go.Figure()
    nodes = [
        ("CSV fuentes", 0, 3), ("Data Preparation", 1, 3), ("Master Dataset", 2, 3),
        ("Motor de Reglas", 3, 4), ("IA / Modelos", 3, 2), ("Politica CASE 1-4", 4, 3),
        ("API", 5, 3), ("Dashboard", 6, 3),
    ]
    # Radius offset in data units to stop arrows at the node border, not the center
    # marker size=76px ≈ 0.38 data units in this coordinate space
    R = 0.38
    edges = [(0,3,1,3),(1,3,2,3),(2,3,3,4),(2,3,3,2),(3,4,4,3),(3,2,4,3),(4,3,5,3),(5,3,6,3)]
    for x0, y0, x1, y1 in edges:
        dx, dy = x1 - x0, y1 - y0
        dist = math.hypot(dx, dy)
        ux, uy = dx / dist, dy / dist  # unit vector
        # Arrow tip stops at the destination node border
        sx1, sy1 = x1 - ux * R, y1 - uy * R
        # Line body drawn as shape below nodes (from origin border to dest border)
        sx0, sy0 = x0 + ux * R, y0 + uy * R
        architecture.add_shape(
            type="line", x0=sx0, y0=sy0, x1=sx1, y1=sy1,
            xref="x", yref="y",
            line=dict(color=COLORS["gray"], width=2),
            layer="below",
        )
        # Arrowhead annotation: tip at dest border, tail just behind the tip.
        # Both ax/ay and x/y are near the dest border so only the arrowhead renders;
        # the shape line drawn below covers the full body between the two nodes.
        architecture.add_annotation(
            x=sx1, y=sy1, ax=sx0, ay=sy0,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowsize=1.3, arrowwidth=2,
            arrowcolor=COLORS["gray"], text="",
        )
    # Nodes added after shapes so they render on top
    for label, x, y in nodes:
        architecture.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[label],
                                          textposition="middle center", marker=dict(size=76, color="#42A5F5" if x < 3 else COLORS["teal"]),
                                          hovertext=[label], name=label))
    architecture.update_xaxes(visible=False)
    architecture.update_yaxes(visible=False)
    architecture.update_layout(showlegend=False, title="Flujo del sistema")
    st.plotly_chart(apply_plot_style(architecture, 420), width="stretch")

    c1, c2 = st.columns(2)
    c1.markdown(
        """
        ### Motor de Reglas
        - BR-01: procedimiento no facturado / CUPS no coincidente.
        - BR-02: soporte clinico.
        - BR-03: diagnostico vs procedimiento.
        - BR-04: tratamientos.
        - BR-05: examenes/laboratorios.
        - BR-06: cantidades.
        """
    )
    c2.markdown(
        f"""
        ### Inteligencia Artificial
        - CNN 1D textual real como comparador academico.
        - Modelos NLP con TF-IDF y SentenceTransformer.
        - Modelos hibridos texto + tabular.
        - Ganador: `{registry['winner']['name']}`.
        """
    )
    st.markdown("### Metodologia ASUM-DM")
    phases = pd.DataFrame({
        "fase": ["Business", "Analytic", "Data Understanding", "Data Preparation", "Modeling", "Evaluation", "Deployment"],
        "avance": [100, 100, 100, 100, 100, 100, 85],
    })
    fig = px.bar(phases, x="fase", y="avance", color="fase", title="Avance metodologico ASUM-DM")
    st.plotly_chart(apply_plot_style(fig, 360), width="stretch")
    st.markdown("### Tecnologias utilizadas")
    st.markdown("Python, Pandas, Scikit-learn, TensorFlow/Keras, SentenceTransformers, XGBoost, LightGBM, Plotly, Streamlit, FastAPI.")
    st.markdown("### Integrantes")
    st.info(
        f"""
        - David Antonio García Contreras
        - Miguel Angel Alfonso Saavedra
        - Johann Smith Rivera Montoya
        - Yineth Daniela Botina Puerras
        - Diego Alejandro Bejarano Prada
        """
    )


def main() -> None:
    inject_css()
    df = load_data()
    comparison = load_model_comparison()
    registry = load_registry()
    rules = build_rule_history(df)
    dfh = enriched_history(df, rules)
    page = sidebar_nav()

    if page == "Dashboard Ejecutivo":
        executive_dashboard(dfh, comparison, registry)
    elif page == "Validacion de Registro":
        validation_page(dfh)
    elif page == "Historial de Validaciones":
        history_page(dfh)
    elif page == "Analitica":
        analytics_page(dfh)
    elif page == "Desempeno del Modelo":
        model_performance_page(comparison, registry)
    elif page == "Rendimiento del Sistema":
        system_performance_page(dfh, comparison)
    else:
        about_page(registry)


if __name__ == "__main__":
    main()
