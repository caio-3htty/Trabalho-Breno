#!/usr/bin/env bash
# Script para testar o sistema completo

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "                   TESTE DO SISTEMA COMPLETO"
echo "════════════════════════════════════════════════════════════════"
echo ""

export PYTHONPATH=.

echo "✓ Verificando se os serviços estão rodando..."
echo ""

# Verificar Calculadora
if curl -s http://localhost:5000/ > /dev/null 2>&1; then
    echo "Calculadora está ONLINE (porta 5000)"
else
    echo "Calculadora OFFLINE (porta 5000)"
fi

# Verificar Dashboard
if curl -s http://localhost:6100/ > /dev/null 2>&1; then
    echo "Dashboard está ONLINE (porta 6100)"
else
    echo "Dashboard OFFLINE (porta 6100)"
fi

# Verificar Servidor gRPC
if timeout 1 bash -c "echo > /dev/tcp/localhost/50052" 2>/dev/null; then
    echo "Servidor gRPC está ONLINE (porta 50052)"
else
    echo "Servidor gRPC OFFLINE (porta 50052)"
fi

echo ""
echo "────────────────────────────────────────────────────────────────"
echo ""

# Contar operações registradas
if [ -f .operations_log.json ]; then
    COUNT=$(grep -o '"operation"' .operations_log.json | wc -l)
    echo "Operações registradas: $COUNT"
else
    echo "Nenhuma operação registrada ainda"
fi

echo ""
echo "────────────────────────────────────────────────────────────────"
echo ""

echo "ACESSAR:"
echo "   Calculadora:  http://localhost:5000"
echo "   Dashboard:    http://localhost:6100"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
