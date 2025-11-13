#!/usr/bin/env python3
"""
Start all services (server gRPC, dashboard, GUI) similar to run_all.sh

Usage: python scripts/start_all.py
"""
import argparse
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


def wait_grpc_ready(target='localhost:50052', timeout=5.0):
    try:
        import grpc
        ch = grpc.insecure_channel(target)
        grpc.channel_ready_future(ch).result(timeout=timeout)
        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-gui', action='store_true', help='Do not start the GUI')
    parser.add_argument('--no-dashboard', action='store_true', help='Do not start the dashboard')
    parser.add_argument('--wait-timeout', type=float, default=5.0, help='gRPC ready timeout in seconds')
    args = parser.parse_args()

    print('Starting services...')
    # Start gRPC server
    server_log = LOGDIR / 'server.log'
    start_process([PY, '-m', 'Sevidor.Servidor'], str(server_log))
    time.sleep(0.3)

    # Optionally start dashboard
    if not args.no_dashboard:
        dashboard_log = LOGDIR / 'dashboard.log'
        start_process([PY, '-m', 'Sevidor.server_dashboard'], str(dashboard_log))
        time.sleep(0.3)

    # Wait for gRPC to be ready before starting GUI
    print('Waiting for gRPC to become ready...')
    ready = wait_grpc_ready(timeout=args.wait_timeout)
    print('gRPC ready:' , ready)

    # Start GUI only if allowed and gRPC ready
    if not args.no_gui:
        if ready:
            gui_log = LOGDIR / 'gui.log'
            start_process([PY, 'Cliente/gui.py', '--host', '0.0.0.0', '--port', '5000'], str(gui_log))
        else:
            print('gRPC not ready; skipping GUI start (use --no-gui to suppress this behavior).')

    print('All start commands issued. Check logs in:', LOGDIR)


if __name__ == '__main__':
    main()
