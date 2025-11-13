"""Interação com o usuário (entrada/saída) — separado da lógica e das chamadas gRPC.

Fornece funções para exibir menu, ler operandos e validar entradas do usuário
para o cliente CLI da calculadora.
"""
from typing import Tuple, Optional

def show_menu() -> str:
    """Mostra o menu e retorna a escolha do usuário como string."""
    print("Escolha a operação:")
    print("1) Somar")
    print("2) Subtrair")
    print("3) Multiplicar")
    print("4) Dividir")
    print("q) Sair")
    return input("Opção: ").strip()

def parse_float(s: str) -> Optional[float]:
    """Tenta converter string para float. Retorna None se inválido."""
    try:
        return float(s)
    except ValueError:
        return None

def read_operands() -> Tuple[float, float]:
    """Lê operandos do usuário, repetindo até entradas válidas."""
    while True:
        sx = input("x: ").strip()
        x = parse_float(sx)
        if x is None:
            print("Entrada inválida para x. Tente novamente.")
            continue
        sy = input("y: ").strip()
        y = parse_float(sy)
        if y is None:
            print("Entrada inválida para y. Tente novamente.")
            continue
        return x, y
