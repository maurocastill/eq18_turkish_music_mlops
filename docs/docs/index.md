# eq18_turkish_music_mlops documentation!

## Description

Clasificación de Emociones en Música Turca Usando Machine Learning

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `az storage blob upload-batch -d` to recursively sync files in `data/` up to `dvc-remote/data/`.
* `make sync_data_down` will use `az storage blob upload-batch -d` to recursively sync files from `dvc-remote/data/` to `data/`.


