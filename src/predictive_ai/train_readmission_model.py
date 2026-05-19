from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "diabetic_data.csv"
MODEL_OUTPUT_PATH = BASE_DIR / "models" / "predictive" / "readmission_model.pkl"


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

    return X, y, selected_features


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print("Model Training Completed")
    print("\nROC-AUC Score:")
    print(round(roc_auc_score(y_test, probabilities), 4))

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    return model


if __name__ == "__main__":
    print("Loading dataset...")
    df = load_data()

    print("Preparing features...")
    X, y, selected_features = prepare_data(df)

    print("Training readmission model...")
    model = train_model(X, y)

    MODEL_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    model_package = {
        "model": model,
        "features": selected_features
    }

    joblib.dump(model_package, MODEL_OUTPUT_PATH)

    print(f"\nModel saved successfully to: {MODEL_OUTPUT_PATH}")