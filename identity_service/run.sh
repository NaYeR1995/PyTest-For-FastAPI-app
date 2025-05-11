#!/bin/bash
py clean.py
clear
export PYTHONPATH=$(pwd)/..
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug