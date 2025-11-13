"""Funções utilitárias reutilizáveis.

Contém helpers simples usados tanto pelo cliente quanto pelo servidor,
por exemplo para formatar endereços e apresentar resultados de RPCs.
"""
from typing import Tuple
from Calculadora import calc_pb2

def format_server_address(host: str, port: str) -> str:
    """Formata host e porta em um endereço 'host:port'."""
    return f"{host}:{port}"

def pretty_result(res: calc_pb2.Result) -> str:
    """Converte um Result do proto em string amigável."""
    if res.error:
        return f"Erro: {res.error}"
    return f"Resultado: {res.value}"
