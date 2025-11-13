#!/usr/bin/env python3
"""
Run the dashboard (replacement for run_dashboard.sh)

Usage: python scripts/run_dashboard.py
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
env = os.environ.copy()
env['PYTHONPATH'] = str(ROOT)

def main():
    print('Starting dashboard...')
    cmd = [sys.executable, '-m', 'Sevidor.server_dashboard']
    subprocess.run(cmd, cwd=str(ROOT), env=env)

if __name__ == '__main__':
    main()
