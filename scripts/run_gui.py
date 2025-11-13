#!/usr/bin/env python3
"""
Run the GUI (replacement for run_gui.sh)

Usage: python scripts/run_gui.py [--host HOST] [--port PORT]
"""
import os
import subprocess
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
env = os.environ.copy()
env['PYTHONPATH'] = str(ROOT)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    print(f'Starting GUI on http://{args.host}:{args.port} ...')
    cmd = [sys.executable, 'Cliente/gui.py', '--host', args.host, '--port', str(args.port)]
    subprocess.run(cmd, cwd=str(ROOT), env=env)

if __name__ == '__main__':
    main()
