#!/usr/bin/env bash
# Script para rodar servidor, dashboard e GUI simultaneamente
# Uso: bash scripts/run_all.sh

set -e
export PYTHONPATH=.

echo "======================================"
echo "  Calculadora gRPC - Sistema Completo"
echo "======================================"
echo ""
echo "Iniciando todos os serviços..."
echo ""

# Gerar stubs se não existirem
if [ ! -f calc_pb2.py ]; then
    echo "📦 Gerando stubs gRPC..."
    bash scripts/gen_stubs.sh
fi

# Iniciar servidor gRPC em background
echo "Iniciando Servidor gRPC (porta 50052)..."
python -m Sevidor.Servidor &
SERVER_PID=$!
sleep 2

# Iniciar dashboard em background
echo "Iniciando Dashboard (porta 6100)..."
python -m Sevidor.server_dashboard &
DASHBOARD_PID=$!
sleep 2

# Iniciar GUI em background
echo "Iniciando Calculadora GUI (porta 5000)..."
python Cliente/gui.py --host 0.0.0.0 --port 5000 &
GUI_PID=$!
sleep 2

echo ""
echo "======================================"
echo "  Todos os serviços iniciados!"
echo "======================================"
echo ""
echo "Acesse:"
echo "  • Calculadora: http://localhost:5000"
echo "  • Dashboard:   http://localhost:6100"
echo ""
echo "Pressione Ctrl+C para parar todos os serviços..."
echo ""

# Trap para matar todos os processos ao sair
trap "kill $SERVER_PID $DASHBOARD_PID $GUI_PID 2>/dev/null; echo ''; echo 'Serviços parados.'; exit 0" SIGINT SIGTERM

# Aguardar indefinidamente
wait
