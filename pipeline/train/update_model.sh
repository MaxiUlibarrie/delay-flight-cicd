#!/bin/bash

dvc unprotect $MODEL_PATH

dvc add $MODEL_PATH -r $MODEL_TRACK_NAME --to-remote

dvc push $MODEL_PATH.dvc -r $MODEL_TRACK_NAME
