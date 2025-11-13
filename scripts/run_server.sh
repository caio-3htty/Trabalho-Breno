# filepath: /workspaces/Trabalho-Breno/scripts/run_server.sh
#!/usr/bin/env bash
set -e
# pip install -r requirements.txt
export PYTHONPATH=.
python -m Sevidor.Servidor
