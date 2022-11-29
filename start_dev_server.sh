#! /bin/bash

#tenta criar o ambiente. vai falhar se ja existir
set +e
python -m venv venv
set -e

source venv/bin/activate

pip install -r requirements.txt

uvicorn api:app --host 0.0.0.0 --port 80 --reload