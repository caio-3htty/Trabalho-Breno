"""
GUI web da Calculadora gRPC usando Flask.
Calculadora visual tipo máquina de calcular real.

Uso: python Cliente/gui.py [--host 0.0.0.0] [--port 5000] [--server localhost:50051]
"""
import argparse
import logging
from flask import Flask, render_template_string, request, jsonify
import grpc

from Calculadora import calc_pb2
from Calculadora import calc_pb2_grpc

DEFAULT_SERVER = "localhost:50052"

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora gRPC</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .calculator {
            background: #1a1a2e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 400px;
            overflow: hidden;
        }
        .display-area {
            background: linear-gradient(135deg, #2d2d44 0%, #1a1a2e 100%);
            padding: 20px;
            border-bottom: 3px solid #667eea;
        }
        .server-info {
            font-size: 12px;
            color: #999;
            margin-bottom: 10px;
            text-align: right;
        }
        .display {
            background: #0f0f1e;
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 15px;
            font-size: 48px;
            color: #00ff88;
            text-align: right;
            word-wrap: break-word;
            word-break: break-all;
            min-height: 70px;
            display: flex;
            align-items: flex-end;
            justify-content: flex-end;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            text-shadow: 0 0 10px #00ff88;
        }
        .history {
            font-size: 12px;
            color: #667eea;
            margin-top: 10px;
            max-height: 40px;
            overflow-y: auto;
            min-height: 20px;
        }
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            padding: 20px;
            background: #1a1a2e;
        }
        button {
            padding: 20px;
            font-size: 24px;
            font-weight: bold;
            border: 2px solid #667eea;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            color: white;
            background: #2d2d44;
            text-transform: uppercase;
        }
        button:hover {
            background: #667eea;
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: scale(0.98);
        }
        button.number {
            color: #00ff88;
        }
        button.operator {
            color: #ff6b6b;
            border-color: #ff6b6b;
        }
        button.operator:hover {
            background: #ff6b6b;
        }
        button.equals {
            grid-column: span 2;
            color: #00ff88;
            border-color: #00ff88;
            background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
            color: #1a1a2e;
        }
        button.equals:hover {
            background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
            transform: scale(1.05);
        }
        button.clear {
            grid-column: span 2;
            color: #ffaa00;
            border-color: #ffaa00;
        }
        button.clear:hover {
            background: #ffaa00;
            color: #1a1a2e;
        }
        button.backspace {
            color: #ff6b6b;
            border-color: #ff6b6b;
        }
        button.backspace:hover {
            background: #ff6b6b;
        }
        .loading {
            display: none;
            text-align: center;
            color: #00ff88;
            padding: 10px;
            font-size: 12px;
        }
        .loading.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <div class="display-area">
            <div class="server-info">
                Servidor: <span id="serverStatus">Verificando...</span>
            </div>
            <div class="display" id="display">0</div>
            <div class="history" id="history"></div>
            <div class="loading" id="loading">Enviando...</div>
        </div>
        <div class="buttons">
            <button class="clear" onclick="clearDisplay()">C</button>
            <button class="backspace" onclick="backspace()">⌫</button>
            <button class="operator" onclick="setOperation('Divide')">÷</button>
            <button class="operator" onclick="setOperation('Multiply')">×</button>
            
            <button class="number" onclick="appendNumber('7')">7</button>
            <button class="number" onclick="appendNumber('8')">8</button>
            <button class="number" onclick="appendNumber('9')">9</button>
            <button class="operator" onclick="setOperation('Subtract')">−</button>
            
            <button class="number" onclick="appendNumber('4')">4</button>
            <button class="number" onclick="appendNumber('5')">5</button>
            <button class="number" onclick="appendNumber('6')">6</button>
            <button class="operator" onclick="setOperation('Add')">+</button>
            
            <button class="number" onclick="appendNumber('1')">1</button>
            <button class="number" onclick="appendNumber('2')">2</button>
            <button class="number" onclick="appendNumber('3')">3</button>
            <button class="operator" onclick="appendNumber('.')">.</button>
            
            <button class="number" onclick="appendNumber('0')" style="grid-column: span 2;">0</button>
            <button class="operator" onclick="toggleSign()">+/−</button>
            <button class="equals" onclick="calculate()">=</button>
        </div>
    </div>

    <script>
        let display = document.getElementById('display');
        let history = document.getElementById('history');
        let loading = document.getElementById('loading');
        let serverStatus = document.getElementById('serverStatus');
        
        let currentNumber = '0';
        let previousNumber = '';
        let operation = null;
        let shouldResetDisplay = false;

        function updateDisplay() {
            display.textContent = currentNumber;
        }

        function appendNumber(num) {
            if (shouldResetDisplay) {
                currentNumber = num;
                shouldResetDisplay = false;
            } else {
                if (num === '.' && currentNumber.includes('.')) return;
                if (currentNumber === '0' && num !== '.') {
                    currentNumber = num;
                } else if (num === '.' && currentNumber === '0') {
                    currentNumber = '0.';
                } else {
                    currentNumber += num;
                }
            }
            updateDisplay();
        }

        function setOperation(op) {
            if (currentNumber === '') return;
            if (previousNumber !== '') {
                calculate();
            } else {
                previousNumber = currentNumber;
                operation = op;
                shouldResetDisplay = true;
            }
        }

        function backspace() {
            if (currentNumber.length > 1) {
                currentNumber = currentNumber.slice(0, -1);
            } else {
                currentNumber = '0';
            }
            updateDisplay();
        }

        function clearDisplay() {
            currentNumber = '0';
            previousNumber = '';
            operation = null;
            shouldResetDisplay = false;
            history.textContent = '';
            updateDisplay();
        }

        function toggleSign() {
            if (currentNumber !== '0') {
                currentNumber = currentNumber.startsWith('-') ? 
                    currentNumber.slice(1) : '-' + currentNumber;
            }
            updateDisplay();
        }

        async function calculate() {
            if (!operation || previousNumber === '' || currentNumber === '') return;

            const x = parseFloat(previousNumber);
            const y = parseFloat(currentNumber);
            
            if (isNaN(x) || isNaN(y)) return;

            loading.classList.add('show');
            history.textContent = `${previousNumber} ${getOpSymbol(operation)} ${currentNumber} = ...`;

            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        x: x,
                        y: y,
                        operation: operation,
                        server: 'localhost:50052'
                    })
                });
                const data = await response.json();
                
                loading.classList.remove('show');

                if (data.error) {
                    currentNumber = 'Erro: ' + data.error;
                    history.textContent = 'Erro: ' + data.error;
                } else {
                    const result = data.result;
                    currentNumber = String(result);
                    history.textContent = `${previousNumber} ${getOpSymbol(operation)} ${y} = ${result}`;
                }
            } catch (error) {
                loading.classList.remove('show');
                currentNumber = 'Erro de conexão';
                history.textContent = 'Erro ao conectar ao servidor';
            }

            previousNumber = '';
            operation = null;
            shouldResetDisplay = true;
            updateDisplay();
        }

        function getOpSymbol(op) {
            const symbols = {
                'Add': '+',
                'Subtract': '−',
                'Multiply': '×',
                'Divide': '÷'
            };
            return symbols[op] || op;
        }

        // Suporte ao teclado
        document.addEventListener('keydown', (e) => {
            if (e.key >= '0' && e.key <= '9') appendNumber(e.key);
            if (e.key === '.') appendNumber('.');
            if (e.key === '+') setOperation('Add');
            if (e.key === '-') setOperation('Subtract');
            if (e.key === '*') setOperation('Multiply');
            if (e.key === '/') { e.preventDefault(); setOperation('Divide'); }
            if (e.key === 'Enter' || e.key === '=') { e.preventDefault(); calculate(); }
            if (e.key === 'Backspace') { e.preventDefault(); backspace(); }
            if (e.key === 'Escape') clearDisplay();
        });

        // Verificar status do servidor
        async function checkServer() {
            try {
                const response = await fetch('/api/server-status');
                const data = await response.json();
                serverStatus.textContent = data.status;
            } catch {
                serverStatus.textContent = 'Offline';
            }
        }
        checkServer();
        setInterval(checkServer, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    server = data.get('server', DEFAULT_SERVER)
    x = float(data.get('x', 0))
    y = float(data.get('y', 0))
    operation = data.get('operation', 'Add')

    try:
        with grpc.insecure_channel(server) as channel:
            stub = calc_pb2_grpc.CalculatorStub(channel)
            req = calc_pb2.Operands(x=x, y=y)

            if operation == "Add":
                res = stub.Add(req)
            elif operation == "Subtract":
                res = stub.Subtract(req)
            elif operation == "Multiply":
                res = stub.Multiply(req)
            elif operation == "Divide":
                res = stub.Divide(req)
            else:
                return jsonify({'error': 'Operação desconhecida'}), 400

            if res.error:
                return jsonify({'error': res.error}), 400
            return jsonify({'result': res.value})
    except grpc.RpcError as e:
        return jsonify({'error': f'Erro gRPC: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/server-status')
def server_status():
    server = DEFAULT_SERVER
    try:
        # Verifica conectividade do canal sem realizar uma chamada RPC
        with grpc.insecure_channel(server) as channel:
            try:
                grpc.channel_ready_future(channel).result(timeout=1)
                return jsonify({'status': 'Online'})
            except Exception:
                return jsonify({'status': 'Offline'})
    except:
        return jsonify({'status': 'Offline'})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0", help="Host para o servidor web")
    parser.add_argument("--port", type=int, default=5000, help="Porta do servidor web")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="Endereço do servidor gRPC")
    args = parser.parse_args()
    
    DEFAULT_SERVER = args.server
    
    logging.basicConfig(level=logging.INFO)
    app.run(host=args.host, port=args.port, debug=True)
