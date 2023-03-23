#!/bin/bash

python common/credential_decode.py

dvc pull --remote $MODEL_TRACK_NAME

uvicorn pipeline.backend.main:app --host 0.0.0.0 --port 8000
