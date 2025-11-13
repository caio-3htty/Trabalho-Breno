#!/usr/bin/env python3
"""
Gerar stubs Python a partir dos protos (substitui gen_stubs.sh)

Uso: python scripts/gen_stubs.py
"""
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os_env = dict()

def main():
    print('Gerando stubs gRPC a partir de protos...')
    # Usar o módulo grpc_tools.protoc via subprocess para preservar comportamento
    cmd = [sys.executable, '-m', 'grpc_tools.protoc',
           '--proto_path=protos',
           '--python_out=.',
           '--grpc_python_out=.',
           'protos/calc.proto']
    res = subprocess.run(cmd, cwd=str(ROOT))
    if res.returncode != 0:
        print('Erro ao gerar stubs (exit', res.returncode, ')')
        sys.exit(res.returncode)
    print('Stubs gerados com sucesso.')

if __name__ == '__main__':
    main()
