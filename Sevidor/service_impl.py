"""
Implementação dos métodos RPC: adapta chamadas gRPC para a lógica em
`Sevidor.calculadora`.

Observação: os nomes dos métodos RPC (Add/Subtract/...) vêm do proto e
devem permanecer para o gRPC funcionar; o restante do código foi
traduzido para português.
"""

import logging

from Calculadora import calc_pb2
from Calculadora import calc_pb2_grpc

from .calculadora import soma, subtrai, multiplica, divide

# Importar função de log do dashboard
try:
    from .server_dashboard import log_operation
except ImportError:
    def log_operation(*args, **kwargs):
        pass  # Fallback se dashboard não estiver disponível

class ServicoCalculadoraImpl(calc_pb2_grpc.CalculatorServicer):
    """
    Servicer que delega operações ao módulo `Sevidor.calculadora`.
    Em caso de exceção retorna Result com o campo `error` preenchido.
    """

    def _get_client_ip(self, context):
        """Extrai IP do cliente do contexto gRPC."""
        try:
            peer = context.peer()
            # Formato: "ipv4:127.0.0.1:port"
            # Formato: "ipv4:127.0.0.1:port" ou "ipv6:[::1]:port"
            if peer:
                if 'ipv4:' in peer:
                    parts = peer.split(':')
                    return parts[1] if len(parts) > 1 else "Desconhecido"
                elif 'ipv6:' in peer:
                    # IPv6 case: "ipv6:[::1]:port"
                    parts = peer.split(']:')
                    if len(parts) > 0:
                        ip = parts[0].replace('ipv6:[', '')
                        return ip if ip else "IPv6"
                    return "IPv6"
            return "Desconhecido"
        except:
            return "Desconhecido"

    def Add(self, request, context):
        client_ip = self._get_client_ip(context)
        try:
            valor = soma(request.x, request.y)
            op_str = f"{request.x} + {request.y}"
            result_str = f"Resultado: {valor}"
            log_operation(op_str, result_str, 'success', client_ip)
            return calc_pb2.Result(value=valor, error="")
        except Exception as e:
            logging.exception("Erro em Add")
            op_str = f"{request.x} + {request.y}"
            result_str = f"Erro: {str(e)}"
            log_operation(op_str, result_str, 'error', client_ip)
            return calc_pb2.Result(value=0.0, error=str(e))

    def Subtract(self, request, context):
        client_ip = self._get_client_ip(context)
        try:
            valor = subtrai(request.x, request.y)
            op_str = f"{request.x} − {request.y}"
            result_str = f"Resultado: {valor}"
            log_operation(op_str, result_str, 'success', client_ip)
            return calc_pb2.Result(value=valor, error="")
        except Exception as e:
            logging.exception("Erro em Subtract")
            op_str = f"{request.x} − {request.y}"
            result_str = f"Erro: {str(e)}"
            log_operation(op_str, result_str, 'error', client_ip)
            return calc_pb2.Result(value=0.0, error=str(e))

    def Multiply(self, request, context):
        client_ip = self._get_client_ip(context)
        try:
            valor = multiplica(request.x, request.y)
            op_str = f"{request.x} × {request.y}"
            result_str = f"Resultado: {valor}"
            log_operation(op_str, result_str, 'success', client_ip)
            return calc_pb2.Result(value=valor, error="")
        except Exception as e:
            logging.exception("Erro em Multiply")
            op_str = f"{request.x} × {request.y}"
            result_str = f"Erro: {str(e)}"
            log_operation(op_str, result_str, 'error', client_ip)
            return calc_pb2.Result(value=0.0, error=str(e))

    def Divide(self, request, context):
        client_ip = self._get_client_ip(context)
        try:
            valor = divide(request.x, request.y)
            op_str = f"{request.x} ÷ {request.y}"
            result_str = f"Resultado: {valor}"
            log_operation(op_str, result_str, 'success', client_ip)
            return calc_pb2.Result(value=valor, error="")
        except Exception as e:
            logging.exception("Erro em Divide")
            op_str = f"{request.x} ÷ {request.y}"
            result_str = f"Erro: {str(e)}"
            log_operation(op_str, result_str, 'error', client_ip)
            return calc_pb2.Result(value=0.0, error=str(e))
