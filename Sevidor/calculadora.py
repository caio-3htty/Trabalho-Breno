"""
Módulo de lógica matemática (pura) do pacote `Sevidor`.

Todas as funções "reais" são nomeadas em português. Mantemos aliases
em inglês para compatibilidade com código legado.
"""

def soma(x: float, y: float) -> float:
    """Retorna x + y."""
    return x + y

def subtrai(x: float, y: float) -> float:
    """Retorna x - y."""
    return x - y

def multiplica(x: float, y: float) -> float:
    """Retorna x * y."""
    return x * y

def divide(x: float, y: float) -> float:
    """
    Retorna x / y.

    :raises ValueError: se y == 0
    """
    if y == 0:
        raise ValueError("Divisão por zero não permitida.")
    return x / y

# Aliases em inglês (compatibilidade retroativa). Prefira usar os nomes em português.
def add(x: float, y: float) -> float:  # pragma: no cover - delega para soma
    return soma(x, y)

def sub(x: float, y: float) -> float:  # pragma: no cover - delega para subtrai
    return subtrai(x, y)

def mul(x: float, y: float) -> float:  # pragma: no cover - delega para multiplica
    return multiplica(x, y)

def div(x: float, y: float) -> float:  # pragma: no cover - delega para divide
    return divide(x, y)
