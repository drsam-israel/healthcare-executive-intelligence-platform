from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

import shap


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "diabetic_data.csv"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
EXECUTIVE_REPORTS_DIR = BASE_DIR / "reports" / "executive"


def load_data():
    df = pd.read_csv(RAW_DATA_PATH, low_memory=False)
    df = df.replace("?", pd.NA)
    return df


def prepare_data(df):
    df = df.copy()

    df["readmitted_30"] = df["readmitted"].apply(
        lambda x: 1 if x == "<30" else 0
    )

    selected_features = [
        "race",
        "gender",
        "age",
        "admission_type_id",
        "discharge_disposition_id",
        "admission_source_id",
        "time_in_hospital",
        "num_lab_procedures",
        "num_procedures",
        "num_medications",
        "number_outpatient",
        "number_emergency",
        "number_inpatient",
        "number_diagnoses",
        "max_glu_serum",
        "A1Cresult",
        "insulin",
        "change",
        "diabetesMed",
    ]

    X = df[selected_features].copy()
    y = df["readmitted_30"]

    for col in X.select_dtypes(include=["object"]).columns:
        encoder = LabelEncoder()
        X[col] = X[col].astype(str)
        X[col] = encoder.fit_transform(X[col])

    return X, y


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
        max_depth=8
    )

    model.fit(X_train, y_train)

    return model, X_test


def generate_shap_outputs(model, X_test):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    EXECUTIVE_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    sample_X = X_test.sample(
        n=min(1000, len(X_test)),
        random_state=42
    )

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(sample_X)

    if isinstance(shap_values, list):
        shap_values_for_class = shap_values[1]
    else:
        shap_values_for_class = shap_values

    plt.figure()

    shap.summary_plot(
        shap_values_for_class,
        sample_X,
        show=False
    )

    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / "shap_summary.png",
        bbox_inches="tight"
    )

    plt.close()

    importances = model.feature_importances_

    feature_importance = pd.DataFrame({
        "feature": sample_X.columns,
        "importance": importances
    })

    feature_importance = feature_importance.sort_values(
        by="importance",
        ascending=False
    )

    feature_importance.to_csv(
        EXECUTIVE_REPORTS_DIR / "feature_importance.csv",
        index=False
    )

    print("SHAP summary image saved.")
    print("Feature importance CSV saved.")


if __name__ == "__main__":
    print("Loading data...")
    df = load_data()

    print("Preparing data...")
    X, y = prepare_data(df)

    print("Training explainability model...")
    model, X_test = train_model(X, y)

    print("Generating SHAP outputs...")
    generate_shap_outputs(model, X_test)

    print("Explainable AI engine completed successfully.")