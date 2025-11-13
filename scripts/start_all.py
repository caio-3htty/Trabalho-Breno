#!/usr/bin/env python3
"""
Start all services (server gRPC, dashboard, GUI) similar to run_all.sh

Usage: python scripts/start_all.py
"""
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGDIR = ROOT / 'logs'
LOGDIR.mkdir(exist_ok=True)

PY = os.environ.get('PYTHON', 'python')
env = os.environ.copy()
env['PYTHONPATH'] = str(ROOT)

def start_process(cmd, logfile):
    with open(logfile, 'ab') as out:
        p = subprocess.Popen(cmd, cwd=str(ROOT), env=env, stdout=out, stderr=subprocess.STDOUT)
    print(f"Started: {' '.join(cmd)} (pid={p.pid}) -> {logfile}")
    return p

def main():
    print('Starting services...')
    # Start gRPC server
    server_log = LOGDIR / 'server.log'
    start_process([PY, '-m', 'Sevidor.Servidor'], str(server_log))
    time.sleep(0.3)

    # Start dashboard
    dashboard_log = LOGDIR / 'dashboard.log'
    start_process([PY, '-m', 'Sevidor.server_dashboard'], str(dashboard_log))
    time.sleep(0.3)

    # Start GUI
    gui_log = LOGDIR / 'gui.log'
    start_process([PY, 'Cliente/gui.py', '--host', '0.0.0.0', '--port', '5000'], str(gui_log))

    print('All start commands issued. Check logs in:', LOGDIR)

if __name__ == '__main__':
    main()
