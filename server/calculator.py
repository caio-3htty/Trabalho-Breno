# filepath: /workspaces/Trabalho-Breno/server/calculator.py
"""
server.calculator
Lógica matemática pura e testável (sem efeitos colaterais).
"""

def add(x: float, y: float) -> float:
    """Soma x + y."""
    return x + y

def sub(x: float, y: float) -> float:
    """Subtração x - y."""
    return x - y

def mul(x: float, y: float) -> float:
    """Multiplicação x * y."""
    return x * y

def div(x: float, y: float) -> float:
    """
    Divisão x / y.

    :raises ValueError: se y == 0
    """
    if y == 0:
        raise ValueError("Divisão por zero não permitida.")
    return x / y
