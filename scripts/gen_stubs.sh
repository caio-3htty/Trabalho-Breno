# filepath: /workspaces/Trabalho-Breno/scripts/gen_stubs.sh
#!/usr/bin/env bash
set -e
python -m grpc_tools.protoc \
  --proto_path=protos \
  --python_out=. \
  --grpc_python_out=. \
  protos/calc.proto
