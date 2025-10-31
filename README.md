# Calculadora gRPC (Python)

Projeto convertido para Python.

Como usar:
1. Gerar stubs:
   bash scripts/gen_stubs.sh

2. Instalar dependências:
   pip install -r requirements.txt

3. Rodar servidor:
   bash scripts/run_server.sh

4. Rodar cliente:
   python client/client.py --server localhost:50051

5. Rodar testes:
   pytest -q

Observações:
- Lógica matemática pura em server/calculator.py (testada por pytest).
- service_impl.py apenas converte entre gRPC e a lógica, retornando erros via campo `error`.
- Gere os stubs (calc_pb2.py e calc_pb2_grpc.py) na raiz do projeto usando gen_stubs.sh.
