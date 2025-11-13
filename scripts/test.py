#!/usr/bin/env python3
"""
Check services (dashboard, GUI, gRPC) and run unit tests (replaces test.sh)

Usage: python scripts/test.py
"""
import sys
import os
import time
import subprocess
from urllib.request import urlopen

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)

def check_http(url, timeout=1.0):
    try:
        with urlopen(url, timeout=timeout) as r:
            return r.status == 200
    except Exception:
        return False

def check_grpc(host='localhost:50052', timeout=1.0):
    try:
        import grpc
        ch = grpc.insecure_channel(host)
        grpc.channel_ready_future(ch).result(timeout=timeout)
        return True
    except Exception:
        return False

def run_pytest():
    try:
        res = subprocess.run([sys.executable, '-m', 'pytest', '-q', 'tests/test_calculator.py'], check=False)
        return res.returncode == 0
    except Exception:
        return False

def main():
    print('Checking services...')
    dashboard_ok = check_http('http://127.0.0.1:6100/')
    gui_ok = check_http('http://127.0.0.1:5000/')
    grpc_ok = check_grpc('localhost:50052')

    print(f"Dashboard (http://127.0.0.1:6100): {'ONLINE' if dashboard_ok else 'OFFLINE'}")
    print(f"GUI (http://127.0.0.1:5000): {'ONLINE' if gui_ok else 'OFFLINE'}")
    print(f"gRPC (localhost:50052): {'ONLINE' if grpc_ok else 'OFFLINE'}")

    print('\nRunning unit tests (tests/test_calculator.py) ...')
    tests_ok = run_pytest()
    print('Unit tests:', 'PASSED' if tests_ok else 'FAILED')

    if not (dashboard_ok and gui_ok and grpc_ok and tests_ok):
        print('\nOne or more checks failed. See logs in /logs or run services with scripts/start_all.py')
        sys.exit(1)
    print('\nAll checks passed.')

if __name__ == '__main__':
    main()
