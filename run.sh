#!/bin/bash

source set_pythonpath.sh

uvicorn $1.app.main:app --host 0.0.0.0 --port 8000 --reload
