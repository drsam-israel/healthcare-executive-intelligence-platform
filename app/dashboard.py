import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

from auth import login, check_authentication

if not check_authentication():
    login()
    st.stop()
st.set_page_config(
    page_title="Healthcare Executive Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>

    /* MAIN APP */
    .stApp {
        background-color: #F4F7FB;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #06152B 0%,
            #081F3F 100%
        );
        border-right: 1px solid #102C54;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white !important;
    }

    section[data-testid="stSidebar"] input {
        background-color: white !important;
        color: black !important;
        border-radius: 10px !important;
    }

    /* KPI CARDS */
    .metric-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.08);
        border-left: 6px solid #2563EB;
        margin-bottom: 20px;
    }

    /* EXECUTIVE CONTAINERS */
    .executive-container {
        background: white;
        padding: 28px;
        border-radius: 22px;
        box-shadow: 0px 6px 24px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }

    /* TITLES */
    h1 {
        color: #0F172A;
        font-weight: 800;
        letter-spacing: -1px;
    }

    h2, h3 {
        color: #1E293B;
        font-weight: 700;
    }

    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(
            90deg,
            #2563EB,
            #1D4ED8
        );
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.7rem 1.4rem;
        font-weight: 600;
        transition: 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        background: linear-gradient(
            90deg,
            #1D4ED8,
            #1E40AF
        );
    }

    /* DATAFRAME */
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
    }

    /* PLOTLY CONTAINER */
    .js-plotly-plot {
        border-radius: 20px;
        overflow: hidden;
    }

    /* METRICS */
    [data-testid="metric-container"] {
        background: white;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0px 4px 16px rgba(0,0,0,0.08);
        border-left: 5px solid #2563EB;
    }

    /* DIVIDER */
    hr {
        border: none;
        height: 1px;
        background: #DCE3F0;
        margin-top: 25px;
        margin-bottom: 25px;
    }

    /* PAGE SPACING */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# AUTHENTICATION
# ==========================================

USERS = {
    "executive": {
        "password": "exec123",
        "role": "Executive"
    },
    "operations": {
        "password": "ops123",
        "role": "Operations Manager"
    },
    "clinical": {
        "password": "clinical123",
        "role": "Clinical AI Lead"
    },
    "admin": {
        "password": "admin123",
        "role": "Data Science Admin"
    }
}


def login():
    st.sidebar.markdown("## 🔐 Enterprise Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = USERS[username]["role"]
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password")


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


if not st.session_state["authenticated"]:
    st.title("🏥 Healthcare Executive Intelligence & Predictive AI Platform")
    st.caption(
        "Enterprise healthcare command center for operations intelligence, predictive AI, bed occupancy, financial analytics, and executive strategy."
    )
    st.warning("Please log in to access the platform.")

    login()

    st.info(
        """
        Demo Login Accounts:

        Executive: executive / exec123  
        Operations Manager: operations / ops123  
        Clinical AI Lead: clinical / clinical123  
        Data Science Admin: admin / admin123
        """
    )

    st.stop()


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/diabetic_data.csv")
    df = df.replace("?", np.nan)
    return df


df = load_data()

MODEL_PATH = "models/predictive/readmission_model.pkl"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model_package = load_model()
readmission_model = model_package["model"]
model_features = model_package["features"]

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.markdown("## 🏥 Healthcare Executive Dashboard")
st.sidebar.success(f"Logged in as: {st.session_state['role']}")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()


role = st.session_state["role"]


if role == "Executive":
    pages = [
        "📊 Executive Command Center",
        "💰 Financial Performance Analytics",
        "📈 Operational Forecasting",
        "📘 Executive Insights & Strategy"
    ]

elif role == "Operations Manager":
    pages = [
        "📊 Executive Command Center",
        "🏥 Operations Intelligence",
        "🛏️ Bed Occupancy Intelligence",
        "📈 Operational Forecasting"
    ]

elif role == "Clinical AI Lead":
    pages = [
        "⚠️ Quality & Risk Intelligence",
        "🧠 Predictive Clinical AI",
        "🔍 Explainable AI Intelligence",
        "📘 Executive Insights & Strategy"
    ]

else:
    pages = [
        "📊 Executive Command Center",
        "🏥 Operations Intelligence",
        "🛏️ Bed Occupancy Intelligence",
        "⚠️ Quality & Risk Intelligence",
        "💰 Financial Performance Analytics",
        "🧠 Predictive Clinical AI",
        "🔍 Explainable AI Intelligence",
        "📈 Operational Forecasting",
        "📘 Executive Insights & Strategy",
        "📂 Enterprise Data Explorer"
    ]


page = st.sidebar.radio(
    "Executive Navigation",
    pages,
    key="main_navigation"
)


# ==========================================
# ENTERPRISE FILTERS
# ==========================================

st.sidebar.markdown("---")
st.sidebar.markdown("## 🎛️ Enterprise Filters")

filtered_df = df.copy()

age_filter = st.sidebar.multiselect(
    "Age Group",
    options=sorted(df["age"].dropna().unique()),
    default=[],
    key="age_filter"
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["gender"].dropna().unique()),
    default=[],
    key="gender_filter"
)

race_filter = st.sidebar.multiselect(
    "Race",
    options=sorted(df["race"].dropna().unique()),
    default=[],
    key="race_filter"
)

specialty_filter = st.sidebar.multiselect(
    "Medical Specialty",
    options=sorted(df["medical_specialty"].dropna().unique()),
    default=[],
    key="specialty_filter"
)

readmission_filter = st.sidebar.multiselect(
    "Readmission Status",
    options=sorted(df["readmitted"].dropna().unique()),
    default=[],
    key="readmission_filter"
)

if age_filter:
    filtered_df = filtered_df[filtered_df["age"].isin(age_filter)]

if gender_filter:
    filtered_df = filtered_df[filtered_df["gender"].isin(gender_filter)]

if race_filter:
    filtered_df = filtered_df[filtered_df["race"].isin(race_filter)]

if specialty_filter:
    filtered_df = filtered_df[filtered_df["medical_specialty"].isin(specialty_filter)]

if readmission_filter:
    filtered_df = filtered_df[filtered_df["readmitted"].isin(readmission_filter)]


# ==========================================
# FILTERED KPI ENGINE
# ==========================================

total_admissions = len(filtered_df)

if total_admissions == 0:
    st.warning("No records match the selected filters. Please adjust the sidebar filters.")
    st.stop()

readmission_rate = (filtered_df["readmitted"] != "NO").mean() * 100
average_los = filtered_df["time_in_hospital"].mean()
average_medications = filtered_df["num_medications"].mean()
emergency_admissions = filtered_df["admission_type_id"].isin([1, 2, 7]).sum()
emergency_rate = (emergency_admissions / total_admissions) * 100
bed_occupancy_rate = min(95, round((average_los / 5.5) * 100, 1))
icu_occupancy_rate = min(99, round(bed_occupancy_rate + 8, 1))
estimated_cost = total_admissions * 8500


# ==========================================
# EXECUTIVE COMMAND CENTER
# ==========================================

if page == "📊 Executive Command Center":

    st.title("🏥 Healthcare Executive Intelligence Dashboard")

    st.caption(
        "Enterprise command center for hospital operations, utilization, bed occupancy, predictive AI, and executive decision support."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Filtered Admissions", f"{total_admissions:,}")
    col2.metric("Average LOS", f"{average_los:.2f} days")
    col3.metric("Readmission Rate", f"{readmission_rate:.2f}%")

    col4, col5, col6 = st.columns(3)

    col4.metric("ED Admission Rate", f"{emergency_rate:.2f}%")
    col5.metric("Bed Occupancy", f"{bed_occupancy_rate:.1f}%")
    col6.metric("ICU Occupancy", f"{icu_occupancy_rate:.1f}%")

    st.divider()

    st.subheader("Executive Intelligence Summary")

    st.write(
        f"""
        - The selected cohort contains approximately {total_admissions:,} diabetic admissions.
        - The readmission burden is approximately {readmission_rate:.2f}%.
        - Average hospital length of stay is approximately {average_los:.2f} days.
        - Emergency-related admissions account for approximately {emergency_rate:.2f}% of the selected cohort.
        - Estimated bed occupancy pressure is approximately {bed_occupancy_rate:.1f}%.
        """
    )


# ==========================================
# OPERATIONS INTELLIGENCE
# ==========================================

elif page == "🏥 Operations Intelligence":

    st.title("🏥 Operations Intelligence")

    st.caption(
        "Enterprise operational intelligence for admissions, utilization, LOS burden, and readmission analytics."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Filtered Admissions", f"{total_admissions:,}")
    col2.metric("Average LOS", f"{average_los:.2f} days")
    col3.metric("Average Medications", f"{average_medications:.2f}")

    st.divider()

    readmit_chart = filtered_df["readmitted"].value_counts().reset_index()
    readmit_chart.columns = ["Readmission Status", "Count"]

    fig_readmit = px.bar(
        readmit_chart,
        x="Readmission Status",
        y="Count",
        color="Readmission Status",
        title="Readmission Distribution"
    )

    st.plotly_chart(fig_readmit, use_container_width=True)

    los_chart = (
        filtered_df.groupby("readmitted")["time_in_hospital"]
        .mean()
        .reset_index()
    )

    fig_los = px.bar(
        los_chart,
        x="readmitted",
        y="time_in_hospital",
        color="readmitted",
        title="Average Length of Stay by Readmission Status"
    )

    st.plotly_chart(fig_los, use_container_width=True)

    age_chart = filtered_df["age"].value_counts().reset_index()
    age_chart.columns = ["Age Group", "Count"]

    fig_age = px.bar(
        age_chart,
        x="Age Group",
        y="Count",
        color="Count",
        title="Patient Age Distribution"
    )

    st.plotly_chart(fig_age, use_container_width=True)


# ==========================================
# BED OCCUPANCY INTELLIGENCE
# ==========================================

elif page == "🛏️ Bed Occupancy Intelligence":

    st.title("🛏️ Bed Occupancy Intelligence")

    st.caption(
        "Executive inpatient capacity, occupancy pressure, and operational throughput intelligence."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Estimated Bed Occupancy", f"{bed_occupancy_rate:.1f}%")
    col2.metric("Estimated ICU Occupancy", f"{icu_occupancy_rate:.1f}%")
    col3.metric("Average LOS", f"{average_los:.2f} days")

    st.divider()

    fig_bed = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=bed_occupancy_rate,
            title={"text": "Hospital Bed Occupancy"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, 70], "color": "lightgreen"},
                    {"range": [70, 85], "color": "gold"},
                    {"range": [85, 100], "color": "red"}
                ]
            }
        )
    )

    st.plotly_chart(fig_bed, use_container_width=True)

    fig_icu = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=icu_occupancy_rate,
            title={"text": "ICU Occupancy Pressure"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "crimson"},
                "steps": [
                    {"range": [0, 70], "color": "lightgreen"},
                    {"range": [70, 85], "color": "gold"},
                    {"range": [85, 100], "color": "red"}
                ]
            }
        )
    )

    st.plotly_chart(fig_icu, use_container_width=True)


# ==========================================
# QUALITY & RISK
# ==========================================

elif page == "⚠️ Quality & Risk Intelligence":

    st.title("⚠️ Quality & Risk Intelligence")

    st.caption("Readmission burden, utilization risk, and patient safety intelligence.")

    col1, col2 = st.columns(2)

    col1.metric("Readmission Rate", f"{readmission_rate:.2f}%")
    col2.metric("Emergency Admissions", f"{emergency_admissions:,}")

    st.divider()

    readmission_counts = filtered_df["readmitted"].value_counts().reset_index()
    readmission_counts.columns = ["Readmission Status", "Count"]

    fig_quality = px.bar(
        readmission_counts,
        x="Readmission Status",
        y="Count",
        color="Readmission Status",
        title="Readmission Risk Distribution"
    )

    st.plotly_chart(fig_quality, use_container_width=True)


# ==========================================
# FINANCIAL PERFORMANCE
# ==========================================

elif page == "💰 Financial Performance Analytics":

    st.title("💰 Financial Performance Analytics")

    st.caption(
        "Executive financial intelligence for utilization cost, readmission burden, and LOS-driven operational cost exposure."
    )

    avg_cost_per_admission = 8500
    avg_readmission_cost = 12000
    los_cost_per_day = 1800

    total_operational_cost = total_admissions * avg_cost_per_admission
    readmitted_cases = (filtered_df["readmitted"] != "NO").sum()
    estimated_readmission_cost = readmitted_cases * avg_readmission_cost
    los_cost_burden = filtered_df["time_in_hospital"].sum() * los_cost_per_day
    avoidable_readmission_savings = estimated_readmission_cost * 0.20

    col1, col2, col3 = st.columns(3)

    col1.metric("Estimated Total Cost", f"${total_operational_cost:,.0f}")
    col2.metric("Readmission Cost Burden", f"${estimated_readmission_cost:,.0f}")
    col3.metric("LOS Cost Burden", f"${los_cost_burden:,.0f}")

    col4, col5 = st.columns(2)

    col4.metric("Potential 20% Readmission Savings", f"${avoidable_readmission_savings:,.0f}")
    col5.metric("Avg Cost per Admission", f"${avg_cost_per_admission:,.0f}")

    st.divider()

    financial_df = pd.DataFrame({
        "Cost Category": [
            "Total Operational Cost",
            "Readmission Cost Burden",
            "LOS Cost Burden",
            "Potential 20% Readmission Savings"
        ],
        "Estimated Cost": [
            total_operational_cost,
            estimated_readmission_cost,
            los_cost_burden,
            avoidable_readmission_savings
        ]
    })

    fig_financial = px.bar(
        financial_df,
        x="Cost Category",
        y="Estimated Cost",
        color="Cost Category",
        title="Estimated Financial Burden by Cost Category"
    )

    st.plotly_chart(fig_financial, use_container_width=True)


# ==========================================
# PREDICTIVE CLINICAL AI
# ==========================================
elif page == "🧠 Predictive Clinical AI":

    st.title("🧠 Predictive Clinical AI")

    st.caption(
        "Real machine learning engine for diabetic 30-day readmission risk prediction."
    )

    st.markdown("## 🏥 Patient Clinical Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        race = st.selectbox(
            "Race",
            sorted(df["race"].dropna().unique()),
            key="ml_race"
        )

        gender = st.selectbox(
            "Gender",
            sorted(df["gender"].dropna().unique()),
            key="ml_gender"
        )

        age = st.selectbox(
            "Age Group",
            sorted(df["age"].dropna().unique()),
            key="ml_age"
        )

        admission_type_id = st.selectbox(
            "Admission Type ID",
            sorted(df["admission_type_id"].dropna().unique()),
            key="ml_admission_type"
        )

        discharge_disposition_id = st.selectbox(
            "Discharge Disposition ID",
            sorted(df["discharge_disposition_id"].dropna().unique()),
            key="ml_discharge"
        )

        admission_source_id = st.selectbox(
            "Admission Source ID",
            sorted(df["admission_source_id"].dropna().unique()),
            key="ml_admission_source"
        )

    with col2:
        time_in_hospital = st.slider(
            "Hospital Length of Stay",
            1,
            14,
            5,
            key="ml_los"
        )

        num_lab_procedures = st.slider(
            "Lab Procedures",
            1,
            120,
            45,
            key="ml_lab"
        )

        num_procedures = st.slider(
            "Procedures",
            0,
            6,
            1,
            key="ml_procedures"
        )

        num_medications = st.slider(
            "Number of Medications",
            1,
            80,
            15,
            key="ml_meds"
        )

        number_outpatient = st.slider(
            "Outpatient Visits",
            0,
            40,
            1,
            key="ml_outpatient"
        )

        number_emergency = st.slider(
            "Emergency Visits",
            0,
            20,
            0,
            key="ml_emergency"
        )

    with col3:
        number_inpatient = st.slider(
            "Previous Inpatient Visits",
            0,
            20,
            1,
            key="ml_inpatient"
        )

        number_diagnoses = st.slider(
            "Number of Diagnoses",
            1,
            16,
            8,
            key="ml_diagnoses"
        )

        max_glu_serum = st.selectbox(
            "Max Glucose Serum",
            sorted(df["max_glu_serum"].dropna().unique()),
            key="ml_glucose"
        )

        A1Cresult = st.selectbox(
            "A1C Result",
            sorted(df["A1Cresult"].dropna().unique()),
            key="ml_a1c"
        )

        insulin = st.selectbox(
            "Insulin Usage",
            sorted(df["insulin"].dropna().unique()),
            key="ml_insulin"
        )

        change = st.selectbox(
            "Medication Change",
            sorted(df["change"].dropna().unique()),
            key="ml_change"
        )

        diabetesMed = st.selectbox(
            "Diabetes Medication",
            sorted(df["diabetesMed"].dropna().unique()),
            key="ml_diabetesmed"
        )

    st.divider()

    if st.button("Generate ML Readmission Prediction"):

        input_data = pd.DataFrame([{
            "race": race,
            "gender": gender,
            "age": age,
            "admission_type_id": admission_type_id,
            "discharge_disposition_id": discharge_disposition_id,
            "admission_source_id": admission_source_id,
            "time_in_hospital": time_in_hospital,
            "num_lab_procedures": num_lab_procedures,
            "num_procedures": num_procedures,
            "num_medications": num_medications,
            "number_outpatient": number_outpatient,
            "number_emergency": number_emergency,
            "number_inpatient": number_inpatient,
            "number_diagnoses": number_diagnoses,
            "max_glu_serum": max_glu_serum,
            "A1Cresult": A1Cresult,
            "insulin": insulin,
            "change": change,
            "diabetesMed": diabetesMed
        }])

        for col in input_data.select_dtypes(include=["object"]).columns:
            input_data[col] = input_data[col].astype("category").cat.codes

        input_data = input_data[model_features]

        prediction_probability = readmission_model.predict_proba(input_data)[0][1]

        risk_score = round(prediction_probability * 100, 2)

        st.markdown("## 📊 Real ML Readmission Risk Result")

        col4, col5 = st.columns([1, 2])

        with col4:
            st.metric(
                "Predicted 30-Day Readmission Risk",
                f"{risk_score}%"
            )

        with col5:
            if risk_score < 30:
                st.success("🟢 LOW READMISSION RISK")
            elif risk_score < 70:
                st.warning("🟠 MODERATE READMISSION RISK")
            else:
                st.error("🔴 HIGH READMISSION RISK")

        fig_risk = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=risk_score,
                title={"text": "ML Readmission Risk Probability"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {"range": [0, 30], "color": "lightgreen"},
                        {"range": [30, 70], "color": "gold"},
                        {"range": [70, 100], "color": "red"}
                    ]
                }
            )
        )

        st.plotly_chart(fig_risk, use_container_width=True)

        st.subheader("Executive ML Interpretation")

        st.write(
            f"""
            - The trained machine learning model estimates a {risk_score}% probability of 30-day diabetic readmission.
            - This prediction is generated from the saved production model: models/predictive/readmission_model.pkl.
            - Inputs include demographic, admission, utilization, medication, laboratory, and diabetes management variables.
            - The output should support clinical review, discharge planning, and operational risk stratification.
            """
        )


# ==========================================
# EXPLAINABLE AI
# ==========================================

elif page == "🔍 Explainable AI Intelligence":

    st.title("🔍 Explainable AI Intelligence")

    st.caption(
        "Enterprise Explainable AI engine using SHAP interpretability and feature attribution analytics."
    )

    feature_importance_path = "reports/executive/feature_importance.csv"
    shap_image_path = "reports/figures/shap_summary.png"

    try:
        feature_df = pd.read_csv(feature_importance_path)

        col1, col2, col3 = st.columns(3)

        col1.metric("Features Analyzed", len(feature_df))
        col2.metric("Top Predictor", feature_df.iloc[0]["feature"])
        col3.metric("Explainability Engine", "SHAP + Random Forest")

        st.divider()

        st.subheader("📊 AI Feature Importance Rankings")

        st.dataframe(feature_df, use_container_width=True)

        fig_importance = px.bar(
            feature_df.head(10),
            x="feature",
            y="importance",
            color="importance",
            title="Top 10 AI Feature Importance Drivers"
        )

        st.plotly_chart(fig_importance, use_container_width=True)

        st.subheader("🧠 Explainable AI: SHAP Summary")

        st.image(shap_image_path, use_container_width=True)

    except Exception:
        st.warning("Explainability outputs not found yet. Run shap_engine.py first.")


# ==========================================
# FORECASTING
# ==========================================

elif page == "📈 Operational Forecasting":

    st.title("📈 Operational Forecasting")

    current_weekly_admissions = max(1, int(total_admissions / 12))
    projected_growth_rates = [1.00, 1.04, 1.08, 1.12]

    forecast_df = pd.DataFrame({
        "Forecast Period": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "Projected Admissions": [
            int(current_weekly_admissions * rate)
            for rate in projected_growth_rates
        ]
    })

    forecast_df["Projected Readmissions"] = (
        forecast_df["Projected Admissions"] * (readmission_rate / 100)
    ).round(0).astype(int)

    forecast_df["Projected Bed Occupancy (%)"] = [
        min(99, round(bed_occupancy_rate * rate, 1))
        for rate in [1.00, 1.03, 1.06, 1.09]
    ]

    forecast_df["Projected ICU Occupancy (%)"] = [
        min(99, round(icu_occupancy_rate * rate, 1))
        for rate in [1.00, 1.03, 1.06, 1.09]
    ]

    forecast_df["Capacity Risk Level"] = forecast_df["Projected Bed Occupancy (%)"].apply(
        lambda x: "High" if x >= 85 else "Moderate" if x >= 75 else "Stable"
    )

    st.dataframe(forecast_df, use_container_width=True)

    fig_forecast = px.line(
        forecast_df,
        x="Forecast Period",
        y=["Projected Bed Occupancy (%)", "Projected ICU Occupancy (%)"],
        markers=True,
        title="Projected Bed & ICU Occupancy Pressure"
    )

    st.plotly_chart(fig_forecast, use_container_width=True)


# ==========================================
# EXECUTIVE INSIGHTS
# ==========================================

elif page == "📘 Executive Insights & Strategy":

    st.title("📘 Executive Insights & Strategy")

    st.write(
        f"""
        - The selected cohort contains approximately {total_admissions:,} diabetic admissions.
        - The readmission burden is approximately {readmission_rate:.2f}%.
        - Average hospital LOS is approximately {average_los:.2f} days.
        - Emergency admissions account for approximately {emergency_rate:.2f}% of this cohort.
        - Estimated bed occupancy pressure is approximately {bed_occupancy_rate:.1f}%.
        """
    )


# ==========================================
# DATA EXPLORER
# ==========================================

elif page == "📂 Enterprise Data Explorer":

    st.title("📂 Enterprise Data Explorer")

    st.dataframe(filtered_df.head(500), use_container_width=True)
