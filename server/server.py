# filepath: /workspaces/Trabalho-Breno/server/server.py
"""
Servidor gRPC: inicia o servidor e registra o servicer.
Uso: python -m server.server
"""
import logging
import signal
import sys
from concurrent import futures

import grpc

import calc_pb2_grpc
from .service_impl import CalculatorServicerImpl

def serve(host: str = '[::]', port: int = 50051):
    """
    Inicia o servidor gRPC na interface/porta informada.
    """
    logging.basicConfig(level=logging.INFO)
    servidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calc_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicerImpl(), servidor)
    endereco = f"{host}:{port}"
    servidor.add_insecure_port(endereco)
    logging.info("Iniciando servidor gRPC na porta %s", endereco)
    servidor.start()

    def _shutdown(signum, frame):
        logging.info("Encerrando servidor gRPC...")
        servidor.stop(0)
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    servidor.wait_for_termination()

if __name__ == "__main__":
    serve()
