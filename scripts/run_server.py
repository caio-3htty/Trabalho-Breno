#!/usr/bin/env python3
"""
Run the gRPC server (replacement for run_server.sh)

Usage: python scripts/run_server.py
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
env = os.environ.copy()
env['PYTHONPATH'] = str(ROOT)

def main():
    print('Starting gRPC server...')
    cmd = [sys.executable, '-m', 'Sevidor.Servidor']
    subprocess.run(cmd, cwd=str(ROOT), env=env)

if __name__ == '__main__':
    main()
