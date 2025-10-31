# filepath: /workspaces/Trabalho-Breno/client/client.py
"""
Cliente gRPC que apresenta menu e chama o servidor.
Uso: python client/client.py --server localhost:50051
"""
import argparse
import logging

import grpc

import calc_pb2
import calc_pb2_grpc

from . import cli_menu
from common.helpers import pretty_result, format_server_address

def run_client(server_address: str):
    """
    Conecta ao servidor e executa loop do menu.
    :param server_address: endereco do servidor (ex.: localhost:50051)
    """
    logging.basicConfig(level=logging.INFO)
    endereco = server_address if ':' in server_address else format_server_address(server_address, "50051")
    with grpc.insecure_channel(endereco) as canal:
        stub = calc_pb2_grpc.CalculatorStub(canal)
        while True:
            escolha = cli_menu.show_menu()
            if escolha.lower() in ('q', 's', 'quit', 'exit'):
                print("Saindo.")
                break
            if escolha not in ('1','2','3','4'):
                print("Opção inválida.")
                continue
            x, y = cli_menu.read_operands()
            req = calc_pb2.Operands(x=x, y=y)
            try:
                if escolha == '1':
                    res = stub.Add(req)
                elif escolha == '2':
                    res = stub.Subtract(req)
                elif escolha == '3':
                    res = stub.Multiply(req)
                elif escolha == '4':
                    res = stub.Divide(req)
                print(pretty_result(res))
            except grpc.RpcError as e:
                print(f"Erro de comunicação com servidor: {e}")
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default="localhost:50051", help="endereço do servidor")
    args = parser.parse_args()
    run_client(args.server)
