# Turkish Music Emotion

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>
Clasificación de Emociones en Música Turca Usando Machine Learning

## Equipo 18
- Ali Mateo Campos Martínez / A01796071 / a1licampos
- Mario Fonseca Martínez / A01795228 / mariofmtz15
- Miguel Ángel Hernández Núñez / A01795751 / mickyhn
- Jonatan Israel Meza Mendoza / A01275322 / Jonatana01275322
- Eder Mauricio Castillo Galindo / A01795453 / maurocastill

## Resumen del proyecto

**Nombre:** Clasificación de Emociones en Música Turca
**Propósito:** pendiente*.
Estructura basada en **Cookiecutter Data Science**. Control de código con **Git**, control de datos con **DVC**, y almacenamiento remoto de datos en **Azure Blob Storage**.

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         eq18_turkish_music_mlops and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── eq18_turkish_music_mlops   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes eq18_turkish_music_mlops a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

## Estructura clave del repo

* `data/raw/` — datasets originales (versionados con DVC).
* `notebooks/` — notebooks para EDA y modelado.
* `eq18_turkish_music_mlops/` — código fuente del proyecto.
* `.dvc/` — metadata de DVC (versionada).
* `dvc.yaml` / `dvc.lock` — (si aplican) pipelines DVC.
* `requirements.txt` — dependencias Python.
* `README.md` — este archivo.

## Requisitos

* Python 3.13
* virtualenv
* Git
* `dvc[azure]` instalado
* `ACCOUNT_KEY` de la cuenta de Azure Storage (compartida por otro medio)
* Nota: Este README muestra comandos para Windows

## Pasos para clonar y obtener datos

Este repositorio es **privado**, por lo que cada integrante debe autenticarse en GitHub antes de poder clonarlo.

### 1. Generar un Personal Access Token (PAT) en GitHub

1. Entra a [GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)](https://github.com/settings/tokens).
2. Haz clic en **Generate new token (classic)**.
3. Asigna un nombre (ej. `eq18_turkish_music_mlops`).
4. Selecciona al menos el permiso **repo**.
5. Crea el token y **cópialo** (se muestra solo una vez).

> ⚠️ Guarda tu PAT en un lugar seguro. Este token reemplaza tu contraseña en Git.

---

### 2. Clonar el repositorio

En una terminal (PowerShell o CMD):

```bash
git clone https://github.com/maurocastill/eq18_turkish_music_mlops.git
cd eq18_turkish_music_mlops
```

Cuando se pida usuario/contraseña:

* **Usuario** = tu nombre de usuario de GitHub.
* **Contraseña** = pega el PAT que generaste.

---

### 3. Configurar credenciales para no ingresarlas siempre (Windows recomendado)

Ejecuta una vez:

```bash
git config --global credential.helper manager
```

Esto guarda tu usuario y PAT en el **Administrador de Credenciales de Windows**.
De ahora en adelante, `git push` y `git pull` no volverán a pedir tu token.

---

### 4. Preparar entorno Python

1. Activa el entorno virtual compartido `env-mlops-313` (o crea uno nuevo con Python 3.13).
2. Instala dependencias:

```bash
pip install -r requirements.txt
```

---

### 5. Configurar acceso a datos en Azure

Cada integrante debe configurar la `ACCOUNT_KEY` localmente.

```bash
dvc remote modify azure-storage account_key "AZURE_KEY" --local
```

---

### 6. Descargar los datos con DVC

Ejecuta:

```bash
dvc pull
```

Al terminar verás `data/raw/*.csv` descargados desde Azure.

--------