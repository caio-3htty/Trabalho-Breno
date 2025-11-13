# Calculadora gRPC (Python)

Projeto com interface gráfica web (calculadora visual tipo máquina de calcular), servidor gRPC e dashboard de monitoramento em tempo real.

## Características

**Calculadora Visual** — Interface tipo máquina de calcular real com teclado numérico  
**Servidor gRPC** — Funcional com 4 operações matemáticas (Add, Subtract, Multiply, Divide)  
**Dashboard em Tempo Real** — Visualiza todas as operações sendo realizadas no servidor  
**Suporte a Teclado** — Use +, -, *, /, Enter, Backspace, Escape  
**Histórico de Operações** — Veja o que foi calculado no servidor  
**Tratamento de Erros** — Divisão por zero, validação, etc.  

## Início Rápido

### Opção 1: Executar Tudo de Uma Vez (Recomendado)

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar tudo
bash scripts/run_all.sh
```

Depois abra em dois navegadores:
- **Calculadora**: http://localhost:5000
- **Dashboard**: http://localhost:6100

### Opção 2: Executar Separadamente

**Terminal 1 — Servidor gRPC:**
```bash
export PYTHONPATH=.
python -m Sevidor.Servidor
```

**Terminal 2 — Dashboard (opcional):**
```bash
export PYTHONPATH=.
python -m Sevidor.server_dashboard
```

**Terminal 3 — Calculadora GUI:**
```bash
export PYTHONPATH=.
python Cliente/gui.py --host 0.0.0.0 --port 5000
```

## Como Usar a Calculadora

1. **Abra** http://localhost:5000
2. **Clique nos números** (0-9) ou **use o teclado**
3. **Escolha a operação**: +, −, ×, ÷
4. **Pressione =** para calcular (servidor calcula, resultado aparece)
5. **Abra o Dashboard** em http://localhost:6100 para ver o servidor operando em tempo real

### Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| 0-9 | Digitar número |
| . | Decimal |
| + | Adição |
| - | Subtração |
| * | Multiplicação |
| / | Divisão |
| Enter ou = | Calcular |
| Backspace | Apagar último dígito |
| Escape | Limpar tudo |
| +/- | Alterar sinal |

## Arquitetura

```
Navegador (Cliente)
    │
    ├─────── HTTP (JSON) ─────────┐
    │                              │
    ▼                              ▼
┌──────────────┐          ┌──────────────────┐
│ Calculadora  │          │  Dashboard       │
│  GUI         │          │  (Monitoração)   │
│ :5000        │          │  :6100           │

**Obter o código (via Git)**

Se você preferir puxar o projeto no seu computador, use os comandos abaixo.

- Clonar (HTTPS):

```bash
git clone https://github.com/caio-3htty/Trabalho-Breno.git
cd Trabalho-Breno
```

- Alternativamente, clonar via SSH:

```bash
git clone git@github.com:caio-3htty/Trabalho-Breno.git
cd Trabalho-Breno
```

- Trocar para a branch de desenvolvimento (ex.: `converte-para-python`):

```bash
git fetch origin
git checkout converte-para-python
```

- Atualizar o branch local com as últimas alterações remotas:

```bash
git pull origin converte-para-python
```

Esses comandos facilitam puxar/atualizar o código quando estiver em outra máquina.
└──────┬───────┘          └──────┬───────────┘
       │                         │
       └─────── gRPC ────────────┘
                  │
                  ▼
           ┌────────────────┐
           │ Servidor gRPC  │
           │ :50052         │
           ├────────────────┤
           │ service_impl   │
           │ calculadora.py │
           └────────────────┘
```

## Estrutura de Arquivos

```
Trabalho-Breno/
├── Cliente/
│   ├── gui.py                 # Interface web (calculadora visual)
│   ├── cliente.py             # Cliente CLI (alternativo)
│   └── cliente_menu.py        # Funções auxiliares
├── Sevidor/
│   ├── calculadora.py         # Lógica pura de cálculo
│   ├── service_impl.py        # Adaptador gRPC
│   ├── Servidor.py            # Servidor gRPC
│   └── server_dashboard.py    # Dashboard de monitoração
├── protos/
│   └── calc.proto             # Definição gRPC
├── scripts/
│   ├── gen_stubs.sh           # Gera stubs gRPC
│   ├── run_server.sh          # Roda servidor
│   ├── run_gui.sh             # Roda GUI
│   ├── run_dashboard.sh       # Roda dashboard
│   └── run_all.sh             # Roda tudo junto
├── tests/
│   └── test_calculator.py     # Testes unitários
└── README.md
```

## Rodar Testes

```bash
export PYTHONPATH=.
pytest -q tests/test_calculator.py
```

## Observações

- A lógica de cálculo está isolada em `Sevidor/calculadora.py` e é testada
- O servidor registra TODAS as operações no dashboard em tempo real
- Suporte a números decimais e negativos
- Tratamento automático de divisão por zero
- Interface responsiva funciona em mobile também

## Troubleshooting

**Porta 5000 já em uso?**
```bash
python Cliente/gui.py --port 5001
```

**Não consegue conectar ao servidor?**
- Certifique-se que `PYTHONPATH=.` está setado
- Servidor rodando em `localhost:50051`

**Módulo não encontrado?**
```bash
pip install -r requirements.txt
bash scripts/gen_stubs.sh
```

