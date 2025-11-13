"""
Dashboard do Servidor - Visualiza operações em tempo real.
Mostra histórico de cálculos e status do servidor gRPC.

Usa um arquivo JSON para compartilhar operações com o service_impl.py

Uso: python -m Sevidor.server_dashboard
"""
import logging
import json
import os
import tempfile
import urllib.parse
from flask import Flask, render_template_string, jsonify, request
from datetime import datetime
from threading import Lock
from pathlib import Path

app = Flask(__name__)

# Arquivo para armazenar operações (compartilhado com service_impl)
OPERATIONS_FILE = Path(__file__).parent.parent / ".operations_log.json"

operations_lock = Lock()

def load_operations():
    """Carrega operações do arquivo."""
    if not OPERATIONS_FILE.exists():
        return []
    try:
        with open(OPERATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_operations(ops):
    """Salva operações no arquivo."""
    try:
        # Escrita atômica: escreve em arquivo temporário e substitui
        dirpath = OPERATIONS_FILE.parent
        with tempfile.NamedTemporaryFile('w', delete=False, dir=dirpath, encoding='utf-8') as tmp:
            json.dump(ops, tmp, ensure_ascii=False, indent=2)
            tmp_path = tmp.name
        os.replace(tmp_path, OPERATIONS_FILE)
    except Exception as e:
        logging.error(f"Erro ao salvar operações: {e}")


def _normalize_client_ip(raw_client):
    """Normaliza a string de client retirada do peer gRPC.

    Exemplos de entrada observada:
    - "ipv6:%5B::1%5D:42030"
    - "ipv4:127.0.0.1:52344"
    Retorna uma forma mais legível, como "::1:42030" ou "127.0.0.1:52344".
    """
    if not raw_client:
        return 'Desconhecido'
    try:
        # Decodifica percent-encoding (ex.: %5B -> [ )
        decoded = urllib.parse.unquote(raw_client)
        # Remove prefix ipv6: ou ipv4:
        if decoded.startswith('ipv6:'):
            decoded = decoded[len('ipv6:'):]
        elif decoded.startswith('ipv4:'):
            decoded = decoded[len('ipv4:'):]
        # Remove surrounding brackets em IPv6 se presentes
        decoded = decoded.replace('[', '').replace(']', '')
        return decoded
    except Exception:
        return raw_client

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard do Servidor Calculadora</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        h1 {
            font-size: 36px;
            margin-bottom: 10px;
            color: #00ff88;
            text-shadow: 0 0 10px #00ff88;
        }
        .status-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #2d2d44 0%, #1a1a2e 100%);
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        .stat-label {
            font-size: 12px;
            color: #999;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #00ff88;
        }
        .stat-value.error {
            color: #ff6b6b;
        }
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        @media (max-width: 1000px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
        }
        .panel {
            background: linear-gradient(135deg, #2d2d44 0%, #1a1a2e 100%);
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 20px;
        }
        .panel-title {
            color: #00ff88;
            margin-bottom: 15px;
            font-size: 18px;
            text-shadow: 0 0 10px #00ff88;
        }
        .history-container {
            max-height: 400px;
            overflow-y: auto;
        }
        .operation-item {
            background: #1a1a2e;
            border-left: 4px solid #667eea;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 5px;
            animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        .operation-item.error {
            border-left-color: #ff6b6b;
        }
        .operation-item.success {
            border-left-color: #00ff88;
        }
        .op-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }
        .op-time {
            font-size: 11px;
            color: #667eea;
        }
        .op-client {
            font-size: 11px;
            color: #ffaa00;
            font-weight: bold;
        }
        .op-calc {
            font-family: 'Courier New', monospace;
            font-size: 16px;
            color: #00ff88;
            margin-bottom: 5px;
        }
        .op-calc.error {
            color: #ff6b6b;
        }
        .op-result {
            font-size: 14px;
            color: #99ff99;
        }
        .empty-state {
            text-align: center;
            color: #666;
            padding: 40px;
        }
        .refresh-info {
            text-align: center;
            font-size: 12px;
            color: #666;
            margin-top: 10px;
        }
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #1a1a2e;
        }
        ::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00ff88;
        }
        .clients-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .client-tag {
            background: #667eea;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
        }
        .status-online {
            color: #00ff88;
        }
        .status-offline {
            color: #ff6b6b;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Dashboard do Servidor</h1>
            <p>Calculadora gRPC - Monitoramento em Tempo Real</p>
        </header>

        <!-- Navegação por abas -->
        <nav style="margin-bottom:20px; text-align:center;">
            <button class="tab-btn" data-tab="dashboard">Dashboard</button>
            <button class="tab-btn" data-tab="calculator">Calculadora</button>
            <button class="tab-btn" data-tab="history">Histórico</button>
            <button class="tab-btn" data-tab="clients">Clientes</button>
        </nav>

        <div id="tab-dashboard" class="tab-content">
            <div class="status-bar">
            <div class="stat-card">
                <div class="stat-label">Status</div>
                <div class="stat-value" id="status">Online</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total de Operações</div>
                <div class="stat-value" id="totalOps">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Sucessos</div>
                <div class="stat-value" id="successOps">0</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Erros</div>
                <div class="stat-value error" id="errorOps">0</div>
            </div>
            </div>
        </div>

        <div id="tab-calculator" class="tab-content" style="display:none;">
            <div class="panel">
                <div class="panel-title">Calculadora (integrada)</div>
                <iframe id="calculatorFrame" src="http://localhost:5000" style="width:100%; height:600px; border:0; border-radius:10px;"></iframe>
            </div>
        </div>

        <div id="tab-history" class="tab-content" style="display:none;">
            <div class="panel">
                <div class="panel-title">Histórico de Operações (Últimas 100)</div>
                <div class="history-container">
                    <div id="history" class="empty-state">Aguardando operações...</div>
                </div>
                <div class="refresh-info">Atualização em tempo real (a cada 1 segundo)</div>
            </div>
        </div>

        <div id="tab-clients" class="tab-content" style="display:none;">
            <div class="panel">
                <div class="panel-title">Clientes Conectados</div>
                <div class="clients-list" id="clientsList">
                    <div class="empty-state">Aguardando clientes...</div>
                </div>
            </div>
        </div>

        <div class="content-grid" id="legacy-grid" style="display:none;">
            <div class="panel">
                <div class="panel-title">Clientes Conectados</div>
                <div class="clients-list" id="clientsList_legacy">
                    <div class="empty-state">Aguardando clientes...</div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-title">Taxa de Operações</div>
                <div id="opRate" style="font-size: 24px; color: #00ff88; text-align: center; padding: 30px;">
                    0 ops/min
                </div>
            </div>
        </div>

        
    </div>

    <script>
        // Estado inicial e taxa
        let lastCount = 0;
        let lastTime = Date.now();

        // Dados iniciais embutidos pelo servidor (render_template_string)
        try {
            window.INITIAL_OPS = {{ operations_json | safe }} || [];
        } catch (e) {
            window.INITIAL_OPS = [];
        }

        async function refreshHistory() {
            try {
                const response = await fetch('/api/operations');
                const data = await response.json();
                
                const historyDiv = document.getElementById('history');
                const totalOps = document.getElementById('totalOps');
                const successOps = document.getElementById('successOps');
                const errorOps = document.getElementById('errorOps');
                const clientsList = document.getElementById('clientsList');
                const opRate = document.getElementById('opRate');
                
                totalOps.textContent = data.total || 0;
                successOps.textContent = data.success || 0;
                errorOps.textContent = data.errors || 0;
                
                // Calcular taxa de operações
                const now = Date.now();
                const timeDiff = (now - lastTime) / 60000; // em minutos
                const countDiff = (data.total || 0) - lastCount;
                const rate = timeDiff > 0 ? (countDiff / timeDiff).toFixed(1) : 0;
                opRate.textContent = rate + ' ops/min';
                lastCount = data.total || 0;
                lastTime = now;
                
                // Lista de clientes únicos
                const clients = new Set();
                (data.operations || []).forEach(op => {
                    if (op.client) clients.add(op.client);
                });
                
                if (clients.size === 0) {
                    clientsList.innerHTML = '<div class="empty-state">Nenhum cliente conectado</div>';
                } else {
                    clientsList.innerHTML = Array.from(clients).map(c => 
                        `<div class="client-tag">${c}</div>`
                    ).join('');
                }
                
                if ((data.operations || []).length === 0) {
                    historyDiv.innerHTML = '<div class="empty-state">Aguardando operações...</div>';
                    return;
                }
                
                        // Se fetch falhar, usar operações iniciais embutidas no HTML
                        const initialOps = window.INITIAL_OPS || [];

                        const opsToRender = (data && data.operations && data.operations.length) ? data.operations : initialOps;

                        historyDiv.innerHTML = (opsToRender || []).map(op => `
                    <div class="operation-item ${op.status}">
                        <div class="op-header">
                            <span class="op-time">${op.timestamp}</span>
                            <span class="op-client">${op.client || 'Desconhecido'}</span>
                        </div>
                        <div class="op-calc ${op.status === 'error' ? 'error' : ''}">${op.operation}</div>
                        <div class="op-result">${op.result}</div>
                    </div>
                `).reverse().join('');
            } catch (error) {
                console.error('Erro ao atualizar histórico:', error);
            }
        }

        // Renderizar inicialmente usando dados passados pelo servidor
        try {
            const initial = window.INITIAL_OPS || [];
            if (initial.length > 0) {
                const historyDiv = document.getElementById('history');
                const opsToRender = initial;
                historyDiv.innerHTML = (opsToRender || []).map(op => `
                    <div class="operation-item ${op.status}">
                        <div class="op-header">
                            <span class="op-time">${op.timestamp}</span>
                            <span class="op-client">${op.client || 'Desconhecido'}</span>
                        </div>
                        <div class="op-calc ${op.status === 'error' ? 'error' : ''}">${op.operation}</div>
                        <div class="op-result">${op.result}</div>
                    </div>
                `).reverse().join('');
            }
        } catch (e) {}

        refreshHistory();
        setInterval(refreshHistory, 1000);

        // --- Abas (tabs) ---
        function showTab(tabName) {
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(t => t.style.display = 'none');
            const el = document.getElementById('tab-' + tabName);
            if (el) el.style.display = 'block';
        }

        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = btn.getAttribute('data-tab');
                showTab(tab);
            });
        });

        // Exibir aba dashboard por padrão
        showTab('dashboard');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Carrega operações atuais e passa para o template para renderização inicial
    ops = load_operations()
    import json
    ops_json = json.dumps(ops[-100:], ensure_ascii=False)
    return render_template_string(HTML_TEMPLATE, operations_json=ops_json)

@app.route('/api/operations')
def get_operations():
    with operations_lock:
        ops = load_operations()
        success_count = sum(1 for op in ops if op.get('status') == 'success')
        error_count = sum(1 for op in ops if op.get('status') == 'error')
        return jsonify({
            'operations': ops[-100:],  # Últimas 100 operações
            'total': len(ops),
            'success': success_count,
            'errors': error_count
        })

def log_operation(operation_str, result_str, status='success', client_ip='Desconhecido'):
    """Registra uma operação no histórico."""
    with operations_lock:
        ops = load_operations()
        normalized = _normalize_client_ip(client_ip)
        ops.append({
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'operation': operation_str,
            'result': result_str,
            'status': status,
            'client': normalized
        })
        save_operations(ops)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Dashboard do servidor iniciando em http://localhost:6100")
    app.run(host='0.0.0.0', port=6100, debug=False)
