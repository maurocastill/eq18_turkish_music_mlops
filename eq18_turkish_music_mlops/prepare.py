"""
prepare.py

Preprocesamiento completo del dataset Turkish Music Emotion.
Lee el dataset crudo, realiza limpieza determinística, divide en train/test
y aplica pipeline de transformación con:
 - Detección/reemplazo de outliers (IQR)
 - Imputación por mediana
 - Transformación Yeo-Johnson
 - Escalado estándar

Guarda:
 - data/processed/train.csv
 - data/processed/test.csv
 - models/preprocessor.pkl
 - models/label_encoder.pkl
 - reports/outlier_report.json
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import PowerTransformer, StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


# =========================
# Parámetros generales
# =========================
RAW_DATA_PATH = "../data/raw/turkish_music_emotion_modified.csv"
PROCESSED_DIR = "../data/processed"
MODELS_DIR = "../models"
REPORTS_DIR = "../reports"

TEST_SIZE = 0.2
RANDOM_STATE = 42
IQR_FACTOR = 1.5


# =========================
# Clase para detección y reemplazo de outliers
# =========================
class OutlierIQRTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, factor=1.5):
        self.factor = factor
        self.bounds_ = {}
        self.outlier_counts_ = {}

    def fit(self, X, y=None):
        X_df = pd.DataFrame(X)
        for col in X_df.columns:
            q1 = X_df[col].quantile(0.25)
            q3 = X_df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - self.factor * iqr
            upper = q3 + self.factor * iqr
            self.bounds_[col] = (lower, upper)
            self.outlier_counts_[col] = int(((X_df[col] < lower) | (X_df[col] > upper)).sum())
        return self

    def transform(self, X):
        X_df = pd.DataFrame(X).copy()
        for col in X_df.columns:
            lower, upper = self.bounds_[col]
            X_df.loc[(X_df[col] < lower) | (X_df[col] > upper), col] = np.nan
        return X_df.values  # devolver como array para compatibilidad con sklearn


# =========================
# Función principal
# =========================
def main():
    # --- 1. Cargar datos crudos ---
    df = pd.read_csv(RAW_DATA_PATH)

    # --- 2. Limpieza determinística ---
    df.columns = df.columns.str.strip()
    df["Class"] = df["Class"].str.strip().str.lower()
    df = df[df["Class"].isin(["happy", "sad", "angry", "relax"])]

    # Reemplazar comas por puntos y limpiar objetos numéricos
    for col in df.select_dtypes(include="object").columns:
        if col != "Class":
            df[col] = (
                df[col].astype(str)
                .str.replace(",", ".")
                .str.replace(" ", "")
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Eliminar columnas irrelevantes
    if "mixed_type_col" in df.columns:
        df = df.drop(columns=["mixed_type_col"])

    # Eliminar duplicados
    df = df.drop_duplicates()

    # --- 3. Separar features y target ---
    X = df.drop(columns=["Class"])
    y = df["Class"]

    # --- 4. Codificar y ---
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # --- 5. Dividir en train/test antes de transformaciones ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=TEST_SIZE,
        stratify=y_encoded,
        random_state=RANDOM_STATE
    )

    # --- 6. Pipeline de preprocesamiento ---
    numeric_cols = X_train.select_dtypes(include=["number"]).columns.tolist()
    numeric_pipeline = Pipeline(steps=[
        ("outlier", OutlierIQRTransformer(factor=IQR_FACTOR)),
        ("imputer", SimpleImputer(strategy="median")),
        ("power", PowerTransformer(method="yeo-johnson")),
        ("scaler", StandardScaler())
    ])
    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_pipeline, numeric_cols)
    ])

    # --- 7. Ajustar pipeline (solo con train) ---
    preprocessor.fit(X_train)

    # --- 8. Transformar train/test ---
    X_train_t = preprocessor.transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    X_train_t = pd.DataFrame(X_train_t, columns=numeric_cols)
    X_test_t = pd.DataFrame(X_test_t, columns=numeric_cols)
    X_train_t["Class"] = y_train
    X_test_t["Class"] = y_test

    # --- 9. Guardar resultados ---
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    X_train_t.to_csv(os.path.join(PROCESSED_DIR, "train.csv"), index=False)
    X_test_t.to_csv(os.path.join(PROCESSED_DIR, "test.csv"), index=False)

    joblib.dump(preprocessor, os.path.join(MODELS_DIR, "preprocessor.pkl"))
    joblib.dump(label_encoder, os.path.join(MODELS_DIR, "label_encoder.pkl"))

    # --- 10. Guardar informe de outliers ---
    outlier_report_path = os.path.join(REPORTS_DIR, "outlier_report.json")
    with open(outlier_report_path, "w") as f:
        json.dump(preprocessor.named_transformers_["num"]
                  .named_steps["outlier"].outlier_counts_, f, indent=4)

    print("✅ Preparación completada con éxito.")
    print(f"Train shape: {X_train_t.shape}, Test shape: {X_test_t.shape}")
    print(f"Outlier report guardado en: {outlier_report_path}")


if __name__ == "__main__":
    main()