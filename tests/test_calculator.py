"""
Testes unitários da lógica pura em `Sevidor.calculadora` (funções em português).
"""

import pytest
from Sevidor import calculadora

def test_soma():
    assert calculadora.soma(2, 3) == 5

def test_subtrai():
    assert calculadora.subtrai(5, 2) == 3

def test_multiplica():
    assert calculadora.multiplica(4, 3) == 12

def test_divide():
    assert calculadora.divide(6, 3) == 2

def test_divisao_por_zero():
    with pytest.raises(ValueError):
        calculadora.divide(1, 0)
        calculadora.div(1,0)
