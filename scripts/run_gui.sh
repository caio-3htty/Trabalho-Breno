#!/usr/bin/env bash
set -e
export PYTHONPATH=.
echo "Abrindo GUI em http://localhost:5000"
python Cliente/gui.py --host 0.0.0.0 --port 5000
