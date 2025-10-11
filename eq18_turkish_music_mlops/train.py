import argparse
import json
import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


def get_model_and_params(model_name):
    """Retorna el modelo y su grid de hiperparámetros correspondiente."""
    if model_name == "logistic":
        model = LogisticRegression(
            multi_class="multinomial",
            solver="lbfgs",
            max_iter=1000,
            random_state=1,
        )
        param_grid = {
            "C": [0.01, 0.1, 1, 10],
            "class_weight": [None, "balanced"],
            "fit_intercept": [True, False],
        }

    elif model_name == "randomforest":
        model = RandomForestClassifier(random_state=1)
        param_grid = {
            "n_estimators": [100, 200, 300],
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
        }

    elif model_name == "xgboost":
        model = XGBClassifier(
            objective="multi:softmax",
            num_class=4,
            eval_metric="mlogloss",
            random_state=1,
            use_label_encoder=False,
        )
        param_grid = {
            "n_estimators": [100, 200],
            "learning_rate": [0.01, 0.1],
            "max_depth": [3, 5, 7],
            "subsample": [0.8, 1.0],
        }

    else:
        raise ValueError(f"Modelo '{model_name}' no soportado")

    return model, param_grid


def main(model_name):
    # --- Configuración de rutas ---
    data_dir = Path("data/processed")
    models_dir = Path("models")
    reports_dir = Path("reports")

    models_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)

    # --- Cargar datos de entrenamiento ---
    print("📥 Cargando datos de entrenamiento...")
    train = pd.read_csv(data_dir / "train.csv")

    X_train, y_train = train.drop(columns=["Class"]), train["Class"]

    # --- Cargar preprocessor (solo referencia) ---
    preprocessor_path = models_dir / "preprocessor.pkl"
    if preprocessor_path.exists():
        print("🔗 Cargando preprocessor (solo referencia)...")
        preprocessor = joblib.load(preprocessor_path)
    else:
        print("⚠️ Advertencia: preprocessor.pkl no encontrado, continuaré sin él.")

    # --- Seleccionar modelo y grid ---
    print(f"⚙️ Entrenando modelo: {model_name}")
    model, param_grid = get_model_and_params(model_name)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
    grid = GridSearchCV(model, param_grid, cv=cv, scoring="accuracy", n_jobs=-1)

    # --- Entrenamiento + validación cruzada ---
    grid.fit(X_train, y_train)

    print(f"✅ Mejor modelo encontrado: {grid.best_params_}")
    print(f"📊 Accuracy CV promedio: {grid.best_score_:.4f}")

    # --- Reentrenar con todos los datos de entrenamiento ---
    best_model = grid.best_estimator_
    best_model.fit(X_train, y_train)

    # --- Guardar modelo ---
    model_path = models_dir / f"model_{model_name}.pkl"
    joblib.dump(best_model, model_path)

    # --- Guardar resultados ---
    results = {
        "model": model_name,
        "best_params": grid.best_params_,
        "cv_accuracy": grid.best_score_,
    }

    with open(reports_dir / f"train_results_{model_name}.json", "w") as f:
        json.dump(results, f, indent=4)

    print(f"💾 Modelo guardado en: {model_path}")
    print(f"📝 Reporte guardado en: {reports_dir}/train_results_{model_name}.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Entrenamiento de modelos de clasificación de emociones musicales")
    parser.add_argument(
        "--model",
        type=str,
        choices=["logistic", "randomforest", "xgboost"],
        required=True,
        help="Modelo a entrenar (logistic, randomforest, xgboost)",
    )
    args = parser.parse_args()

    main(args.model)