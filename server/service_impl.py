# filepath: /workspaces/Trabalho-Breno/server/service_impl.py
"""
Implementação dos métodos RPC: converte entre gRPC <-> lógica.
A lógica matemática fica em server.calculator para facilitar testes.
"""
import logging

import calc_pb2
import calc_pb2_grpc

from .calculator import add, sub, mul, div

class CalculatorServicerImpl(calc_pb2_grpc.CalculatorServicer):
    """
    Servicer que delega operações ao módulo server.calculator.
    Em caso de exceção retorna Result com campo error preenchido.
    """

    def Add(self, request, context):
        try:
            valor = add(request.x, request.y)
            return calc_pb2.Result(value=valor, error="")
        except Exception as e:
            logging.exception("Erro em Add")
            return calc_pb2.Result(value=0.0, error=str(e))

    def Subtract(self, request, context):
        try:
            valor = sub(request.x, request.y)
            return calc_pb2.Result(value=valor, error="")
        except Exception as e:
            logging.exception("Erro em Subtract")
            return calc_pb2.Result(value=0.0, error=str(e))

    def Multiply(self, request, context):
        try:
            valor = mul(request.x, request.y)
            return calc_pb2.Result(value=valor, error="")
        except Exception as e:
            logging.exception("Erro em Multiply")
            return calc_pb2.Result(value=0.0, error=str(e))

    def Divide(self, request, context):
        try:
            valor = div(request.x, request.y)
            return calc_pb2.Result(value=valor, error="")
        except Exception as e:
            logging.exception("Erro em Divide")
            return calc_pb2.Result(value=0.0, error=str(e))
