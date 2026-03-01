# How to create a new project


## Required Environment

  - Python 3.14 or later
  - uv

## Setup project

for Windows
```shell
python -m venv .venv
./venv/Script/Activate.ps1

uv sync
```

## Run server

```shell
uv run uvicorn src.main:app --host <IP Address> --port <Port> [--reload]
```

## Build container
```shell
uv export --no-dev --no-annotate --no-hashes --format requirements.txt > .\requirements.txt
docker build -t <name> .
```
